#!/usr/bin python

import argparse
import os
import shutil
import warnings

import contur

beams = contur.data.static_db.get_beams()

# compare whether files are equal


def filesEqual(origFile, newFile):
    f1 = open(origFile, "r")
    f2 = open(newFile, "r")

    lines1 = f1.readlines()
    lines2 = f2.readlines()
    f1.close()
    f2.close()

    # files can't be equal if number of lines differs
    if len(lines1) != len(lines2):
        return False

    for i in range(len(lines1)):
        if lines1[i] != lines2[i]:
            return False
    return True

# create symlink to file


def createSymlink(origDir, newDir, fileName):
    origFilePath = os.path.join(os.path.abspath(origDir), fileName)
    newFilePath = os.path.join(newDir, fileName)
    os.symlink(origFilePath, newFilePath)
    return

# check if at least one of the given terms appears in the given string


def appears(s, terms=[]):
    for term in terms:
        if term in s:
            return True
    return False


# get all files of a certain file type from a given list
def fileTypeInList(fileTypes, fileList, exclude=[], include=[]):
    filesOfInterest = []
    for f in fileList:
        # skip file if names contains terms that are excluded or does not contain terms that have to be included
        if appears(f, exclude) or (len(include) > 0 and not appears(f, include)):
            continue

        # check if file is of one of the given file types
        for fileType in fileTypes:
            if f.endswith(fileType):
                filesOfInterest.append(f)
                break
    return filesOfInterest

# get seed number from file name


def getSeed(fileName):
    return fileName.split("-")[1]

# remove a single yoda file from given list


def removeYoda(logFile, lineNumber, yodaFiles):
    with open(logFile, "r") as f:
        content = f.readlines()
        currentLine = 0
        for line in content:
            if currentLine > lineNumber:  # we're beyond the position we need to consider
                break
            if "hepmc" in line:  # this might the line of interest
                hepmcFile = line.split("'")[1]
            currentLine += 1
    yodaFile = ".".join(hepmcFile.split(".")[:-1])+".yoda"
    yodaFileFullPath = "/".join(logFile.split("/")[:-1])+"/"+yodaFile
    # yoda file was only available compressed
    if not os.path.isfile(yodaFileFullPath):
        yodaFile += ".gz"
        yodaFileFullPath += ".gz"

    if os.path.isfile(yodaFileFullPath):  # remove file if existing
        # have to use only file name as full path is not stored in list
        yodaFiles.remove(yodaFile)
        print("Skipping broken yoda file", yodaFileFullPath)
    else:  # print message so we can make sure nothing bad went wrong
        warnings.warn("Cannot skip broken yoda file %s" %
                      yodaFileFullPath, UserWarning)
    return

# remove broken yoda files as given in logfile from list of yodafiles


def removeBrokenYodas(logFile, yodaFiles):
    with open(logFile, "r") as f:
        content = f.readlines()
        lineNumber = 0
        for line in content:
            if "NaN" in line:
                removeYoda(logFile, lineNumber, yodaFiles)
            lineNumber += 1

# return the beam energy from a given file name


def getEnergy(fileName):
    return fileName.split("/")[1]

# get position in list for energy


def getEnergyPosition(energy):
    if energy == "7TeV":
        return 0
    elif energy == "8TeV":
        return 1
    elif energy == "13TeV":
        return 2
    return 3


def merge_main(argv):
    parser = argparse.ArgumentParser(
        description="Merge different grids into one using symlinks.")
    parser.add_argument("outDir", help="Output directory.")
    parser.add_argument("mergeDirs", nargs="+",
                        help="Directories to be merged.")
    args = parser. parse_args(argv)

    if len(args.mergeDirs) < 2:
        print("Cannot merge single directory! Abort.")
        exit()

    if os.path.isdir(args.outDir):
        print("Output directory exists. Deleting it.")
        shutil.rmtree(args.outDir)

    # recursively make directories
    os.makedirs(args.outDir)

    # store written parameters
    with open(os.path.join(args.outDir, "Summary.txt"), "w") as f:
        f.write("Merged grids: "+", ".join(args.mergeDirs))

    paramFiles = [[] for i in range(len(beams)+1)]
    for sourceDir in args.mergeDirs:
        print("Processing", sourceDir)
        for root, dirs, files in sorted(os.walk(sourceDir)):
            currParam = os.path.join(root, "params.dat")
            # skip if there is no param file in directory
            if not os.path.isfile(currParam):
                continue

            yodaFiles = fileTypeInList(
                [".yoda", ".yoda.gz"], files, include=["LHC"])
            outDir = os.path.join(args.outDir, getEnergy(root))

            if len(yodaFiles) > 0:  # we're in a directory that contains yoda files
                # remove broken yoda files
                # TODO: this is just a guess at the defult log file name.
                logFile = os.path.join(root, "contur_analysis.log")
                removeBrokenYodas(logFile, yodaFiles)
                if not len(yodaFiles) > 0:  # skip if all yoda files are broken
                    print("Only broken yoda files in %s. Skipping." % root)
                    continue

                # find matching param file
                currDir = "-1"
                matched = False
                energy = getEnergy(currParam)
                try:
                    beamPos = beams.index(energy)
                except:
                    print("Unknown beam energy")
                    beamPos = len(beams)
                currParamFiles = paramFiles[beamPos]
                for paramFile in currParamFiles:
                    if not getEnergy(paramFile) == energy:
                        continue
                    currDir = os.path.dirname(paramFile)
                    matched = filesEqual(currParam, paramFile)
                    if matched:
                        break

                availableSeeds = []
                if not matched:  # create dir
                    currDir = os.path.join(outDir, "%04d" % (
                        int(currDir.split("/")[-1])+1))
                    os.makedirs(currDir)
                    # get symlink to params file
                    createSymlink(root, currDir, "params.dat")
                    currParamFiles.append(os.path.join(currDir, "params.dat"))
                else:  # find all already taken seeds
                    currDirYFiles = fileTypeInList(
                        [".yoda", ".yoda.gz"], os.listdir(currDir))
                    for y in currDirYFiles:
                        availableSeeds.append(getSeed(y))

                # create symlinks to missing yoda files
                for y in yodaFiles:
                    seed = getSeed(y)
                    if not seed in availableSeeds:
                        createSymlink(root, currDir, y)
    print("Found %d grid points" % sum([len(x) for x in paramFiles]))
