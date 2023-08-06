import os
import pickle

import numpy as np
from configobj import ConfigObj


def generate_zoom_params(args):
    """
    This function will investigate an n-dimensional .map file and rescale each
    parameter by checking for regions where there is little change. This
    function will investigate each point, and find the change is CLs values
    of all adjacent points. It will then find the average difference over all
    adjacent points. It will then consider a point inactive if the average
    CLs change is less than the threshold. For each parameter, this function
    will create a new range which excludes all inactive values at the maximum
    and minimum value for that parameter. If all points in the range of a
    parameter are considered inactive, it will return the original parameter
    range.

    :param replace: Boolean flag to replace new param file with old one

    :param map_fname: Name/path of map file

    :param param_old_fname: Name/path of original param file

    :param param_new_fname: Name/path of new generated param file

    :param thresh: Threshold to consider a point unchanging/unimportant
    """

    # Get parameters from args
    replace = args.replace
    map_fname = args.m_path
    param_old_fname = args.o_path
    param_new_fname = args.n_path
    thresh = float(args.thresh)
    change_param = args.param
    skipPoints = args.skipPoints
    nEventScalings = args.nEventScalings
    rebin = args.rebin

    if args.vals is None:
        important_vals = None
    else:
        important_vals = [float(i) for i in args.vals]

    # Open map file, load all points, and save store info for all variables
    # (parameters)
    map_file = open(map_fname, 'rb')
    points = pickle.load(map_file)
    depot = points.inbox
    num_points = len(depot)
    var_num = len(points.map_axis)
    var_names = points.map_axis.keys()

    # Get size of range for each variable
    var_sizes = []
    for var in points.map_axis:
        var_sizes.append(len(points.map_axis[var]))
    var_sizes = np.array(var_sizes)

    # Create dictionary of dictionaries, where the outer key is each variable,
    # and the inner key is each value that that key can takes in the .map
    # file. Initialize the value of each inner dictionary to 0.
    var_val_dic = {}
    for var in var_names:
        var_val_dic[var] = {}
        for val in points.map_axis[var]:
            var_val_dic[var][val] = 0

    # Create variable to locate adjacent points in n-dimensional space. For
    # instance, if there are 4 variables using a range of 2, 3, 4,
    # 5 respectively, we can find adjacent points by using offsets of +/- (1),
    # +/- (5*1=5), +/- (4*5*1=20), +/- (3*4*5*1=60). This is because the points
    # will be ordered in a way where the last variable will iterate through
    # values first, then the second to last variable, so on to the first
    # variable.

    var_mods = np.append(var_sizes[1:], 1)
    for i in reversed(range(1, len(var_mods))):
        var_mods[i - 1] *= var_mods[i]

    # Here I will iterate through each point in the n-dimensional grid and find
    # the average CLs change for each adjacent point. I will then look at
    # each variable value for each point and update var_val_dic to ensure
    # that the maximum CLs change is used for each (variable, value)
    # combination. This will ensure that a variable range is included even
    # if there is no CLs change in most regions, but a high CLs change
    # somewhere in an (n-1)-dimensional space, with that variable fixed.

    # Helper variable to store average CLs difference for each point
    point_diffs = np.zeros(num_points)

    # Iterate through all points
    for num in range(num_points):
        point_ind = depot[num].param_point
        point_val = depot[num].yoda_factory.likelihood.CLs
        adjacents = 0

        # Iterate through all adjacent points. This will check if a point is on
        # the edge and not move out of the n-dimensional space when counting
        # adjacent points
        for i in range(len(var_mods)):
            # Check if variable is at min range, add CLs change and increment
            # adjacent points if not
            if float(point_ind[var_names[i]]) > min(
                    points.map_axis[var_names[i]]):
                point_diffs[num] += (abs(point_val - depot[
                    num - var_mods[i]].yoda_factory.likelihood.CLs))
                adjacents += 1
                # Check if variable is at max range, add CLs change and
                # increment adjacent points if not
            if float(point_ind[var_names[i]]) < max(
                    points.map_axis[var_names[i]]):
                point_diffs[num] += (abs(point_val - depot[
                    num + var_mods[i]].yoda_factory.likelihood.CLs))
                adjacents += 1
        # Normalize CLs change by number of adjacent points
        point_diffs[num] /= adjacents
        # Automatically set Change value to 1.0 (maximum) if marked as important
        if is_important_val(point_val, important_vals):
            point_diffs[num] = 1.0
        # Iterate though each variable in this point. Look at the value for
        # each variable at this point, and update var_val_dic if the average
        # CLs change is greater than we have previously seen.
        for var in var_names:
            val = float(point_ind[var])
            var_val_dic[var][val] = max(var_val_dic[var][val], point_diffs[num])

    # This is the case where we want to exclude exact points as opposed to
    # making a new rectangular grid. This will not alter rectangular shape of
    # scan.
    config = ConfigObj(param_old_fname)
    if skipPoints:
        excl_points = np.where(point_diffs < thresh)[0]
        excl_strs = [str(i) for i in excl_points]
        config['SkippedPoints'] = {'points': " ".join(excl_strs)}

    # This is the case where we want to scale number of events generated based
    # on 'importance' of point. This will not alter rectangular shape of scan
    if nEventScalings:
        nEventScalings_strs = [str(i) for i in point_diffs]
        config['NEventScalings'] = {'points': " ".join(nEventScalings_strs)}

    if rebin:
        if skipPoints:
            excl_points = np.where(point_diffs < thresh)[0]
            excl_points = np.array([get_expanded_diffs(i, var_mods) for i in
                                    excl_points]).flatten()
            excl_strs = [str(i) for i in excl_points]
            config['SkippedPoints'] = {'points': " ".join(excl_strs)}
        if nEventScalings:
            nEventScalingss = np.empty(num_points * len(np.unique(var_mods)) ** 2)
            for i in range(num_points):
                for j in get_expanded_diffs(i, var_mods):
                    nEventScalingss[j] = point_diffs[i]
            nEventScalings_strs = [str(i) for i in nEventScalingss]
            config['NEventScalings'] = {'points': " ".join(nEventScalings_strs)}
        params = config['Parameters'].keys()
        for param in params:
            mode = config['Parameters'][param]['mode']
            if (mode == 'LIN') or (mode == 'LOG'):
                config['Parameters'][param]['number'] = int(
                    config['Parameters'][param]['number']) * 2

    if skipPoints or nEventScalings or rebin:
        config.filename = param_new_fname
        config.write()
        map_file.close()
        if replace:
            os.system('rm ' + param_old_fname)
            os.system('mv ' + param_new_fname + ' ' + param_old_fname)
        return

    # Here I am constructing the new ranges (limits) for each variable. First I
    # will iterate over each variable. Then I will check if the maximum CLs
    # change for each value of that variable is over the provided threshold.
    # I will then create a new range for each variable by excluding
    # the edge values that do not meet this threshold.
    new_var_lims = {}
    # Iterate over all variables
    for var in var_names:
        # Get all values for this variable
        param_vals = var_val_dic[var].items()
        # Find the indices where CLs change is above the threshold for each
        # value in the variable
        adequate_diffs = [k for k, v in param_vals if v >= thresh]
        # If all CLs changes are below the threshold, show warning and exit
        # function. If the CLs change is less than the threshold for all
        # values in one variable, it must be less than the threshold for all
        # points in all variables. Otherwise return a range that cuts off
        # edge values which do not meet the threshold.
        if len(adequate_diffs) == 0:
            print('Warning: Average CLs change is below threshold '
                  'for all values')
            exit(1)
            # new_var_lims[var] = np.array([min(param_vals),max(param_vals)])
        else:
            new_var_lims[var] = np.array(
                [min(adequate_diffs), max(adequate_diffs)])

    # Create list with variable names using format of a param_file.dat file
    param_var_names = []
    if change_param is None:
        for var in var_names:
            param_var_names.append('[[' + var + ']]')
    # Only change one parameter if input
    else:
        param_var_names = ['[[' + change_param + ']]']

    # Iterate through each line of param_file.dat and update ranges according
    # to new those generated. This will iterate through each line of the param
    # file, and copy these lines in the new param file. When this detects a
    # variable range, it will update that range according to the new values
    # if that variable is not constant.
    with open(param_old_fname, 'r') as old_fp:
        with open(param_new_fname, 'w') as new_fp:
            line = old_fp.readline()
            # Iterate through each line in the old param file
            while line:
                new_fp.write(line)  # Copy each line to new param file
                # Detect if this line is presenting a variable range from the
                # .map file
                match_var_ind = [i for i, x in enumerate(param_var_names) if
                                 x == line.strip()]
                if len(match_var_ind) > 0:
                    # If we are presented with a new variable, ensure that it
                    # is not constant
                    next_line = old_fp.readline()
                    new_fp.write(next_line)
                    if not 'CONST' in next_line:
                        # If this variable is not constant, update next to
                        # lines to show new ranges. Skip over the old lines
                        # and continue iterating over original param file.
                        change_var = var_names[match_var_ind[0]]
                        new_fp.write(
                            "start = {:.2f}\n".format(new_var_lims[change_var][0]))
                        new_fp.write(
                            "stop = {:.2f}\n".format(new_var_lims[change_var][1]))
                        line = old_fp.readline()
                        line = old_fp.readline()
                line = old_fp.readline()

    # If replace flag has been set, replace the old param file with the new one.
    # Otherwise, create a new and differently named param file.
    if replace:
        os.system('rm ' + param_old_fname)
        os.system('mv ' + param_new_fname + ' ' + param_old_fname)

    # Close all files
    map_file.close()
    old_fp.close()
    new_fp.close()


def is_important_val(point_val, important_vals):
    if important_vals is None:
        return False
    for important in important_vals:
        if (point_val > important - .01) and (point_val < important + .01):
            return True
    return False


def get_expanded_diffs(orig, mod_vals):
    # Get diffs
    mod_vals = np.unique(mod_vals)
    diffs = [0]
    level = 0
    for i in mod_vals:
        new_diffs = []
        for diff in diffs:
            new_diffs.append(diff)
            new_diffs.append(diff + (2 ** level) * i)
        diffs = new_diffs
        level += 1
    base = 0
    for i in mod_vals:
        base += 2 * (orig // i) * i
    return base + np.array(diffs)
