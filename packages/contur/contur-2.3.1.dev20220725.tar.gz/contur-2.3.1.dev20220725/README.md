# Contur

Contur is a procedure and toolkit designed to probe theories Beyond the
Standard Model using measurements at particle colliders. The original procedure
is defined in a
[white paper](https://inspirehep.net/literature/1470949)
, which should be used as a reference for the method, with an updated manual [here](https://inspirehep.net/literature/1845411).

Results are available [here](https://hepcedar.gitlab.io/contur-webpage/index.html). This README
concentrates on how to get Contur running yourself.

We also have a support mailing list where volunteer developers will do their best to answer your questions: contur-support@cern.ch

## In-code documentation

The in-code documentation, processed via Sphinx in the [doc](doc) directory, is available [here](https://hepcedar.gitlab.io/contur/).

## Directory structure

### [`contur`](contur/README.md)

The main source code and template run area.

### [`data`](data/README.md)

Common area for all data files (models, rivet, measurements etc)

### [`tests`](tests)

To run contur's code tests, do `make check` from the top directory, or to use other pytest options, `cd` into `tests` and run `$ pytest`.

## Setting up and running Contur

Contur and Rivet are generator-independent, and so as long as you have an event generator producing
HepMC files, you can run those events through Rivet and then run Contur on the resulting yoda file. However, Contur
also provides tools to scan over model parameters generating events, which of course requires an event generator to 
be installed. These instructions will guide you through first of all setting up the minimal Contur installation, to run on an existing yoda file, and then take you through running Rivet on an existing file of HepMC events, some ways of generating those 
HepMC files with a BSM model, and finally running a parameter scan using a BSM model and an event generator, then running Contur on that to get a senstitvity heatmap.

### Running Contur on an existing Yoda file

You will need a working installation of [Rivet](https://rivet.hepforge.org/) and [Yoda](https://yoda.hepforge.org/).
You can find installation instructions on their web pages, [Rivet](https://rivet.hepforge.org) and 
[Yoda](https://yoda.hepforge.org), or obtain them from their gitlab repositories in the [Cedar group](https://gitlab.com/hepcedar). 

You need to make sure your environment is set up appropriately for the required version Rivet etc. If these are in $INSTALLDIR, for example:

        $ source $INSTALLDIR/rivetenv.sh
        $ source $INSTALLDIR/yodaenv.sh

This needs be done every time you start a shell, so you might want to add it to your .bashrc file or similar.

You will need a Python 3 development environment.

To generate your own events and parameter scans (later steps), you will need to install at least one event generator, such as
[Herwig](https://herwig.hepforge.org/), Madgraph or Pythia. The examples below use Herwig.

#### Install contur into your python virtual environment (user only install)

        $ pip install contur

#### Or check out the repository (developers only)

There are contur releases listed [here](/hepcedar/contur/-/releases) and we are looking to
package contur better for distribution (see [Open Projects](/hepcedar/contur/-/wikis/Open-and-ongoing-projects) if you'd like to help)
but at present we still recommend the user checks out the repository from git and then moves to the latest release tag from there, as follows:

- Check out code from repository. (Assume you start in $HOME.)

        $ git clone https://gitlab.com/hepcedar/contur.git

- This will get you the default version, which is currently the `main` branch. Go into the contur directory
  that will have been created. (If you want to be able to push changes, you should set yourself up for ssh access to gitlab.)

        $ cd contur/

- For getting started, we recommended you use the latest stable release version given [here](/hepcedar/contur/-/releases). The syntax to do this is:

        $ git checkout <tag name>

- Now in your contur directory, go to ``dist`` and install from the wheel

        $ cd dist
        $ pip install contur-2.3.x-py3-none-any.whl

  In this step, you use ``pip install`` to install contur, and extra data_files including ``analyses.sql`` will be installed in ``<sys.prefix>/contur``

### Set up the contur environment

- Set some environment variables so that you can execute the contur from anywhere. You will need to find the path of your virtual Python environment and:

        $ source your_virtual_python_path/bin/conturenv.sh

  Since this is also done every time you start a shell, we suggest adding it to the script where you source `rivetenv.sh` and `yodaenv.sh`

- Set up your own user path:   After sourcing this bash script, you will find that the environment variables ``$CONTUR_DATA_PATH`` and ``$CONTUR_USER_DIR`` have been set. By default ``$CONTUR_USER_DIR`` will be set to ``~/contur_users``, but you can change it to your prefered location. Note that this will be the place in which all the generated files needed by contur are installed in thr next step.

- Now run `make`, which is under your ``$CONTUR_DATA_PATH``:

        $ cd $CONTUR_DATA_PATH
        $ make

  You need only do this once. It will build any modified rivet analyses, build the database of static analysis information, containing some analysis steering files for the generators under ``$CONTUR_USER_DIR`` (e.g. `*.ana` for Herwig) and create a script to define some environment variables which can be used to run rivet on a HepMC file. 

-  After doing above steps, you should

        $ source $CONTUR_USER_DIR/analysis-list 

   to update those environment variables.

**You are now ready to run contur on an existing yoda file!**

        $ contur myrivetresults.yoda

- Run 'contur --help' to see more options. 

- There are sample yoda files to try this on in the test area, under `test/sources/myscan00`. Running `make check` also runs contur on these.

- This will output an ANALYSIS folder and a log file, and print some other information to the screen.

- You can then generate a 'contur-plots' directory containing histograms and an index.html
  file to view them all: whilst in the directory containing this yoda file, run:

        $ contur-mkhtml 

### Making your own yoda file 

If you have produced a HepMC event file from somewhere and want to run Contur on that, you need to run Rivet on your events.

        $ rivet -a $ANALYSIS-LIST myfile.hepmc

where $ANALYSIS-LIST is a comma-separated list of the analyses you want to run. Contur defines some convenient environment
variables with the list of relevant analyses for 7, 8 and 13 TeV LHC running, $CONTUR_RA7TeV, $CONTU_RA8TeV and $CONTUR_RA13TeV.
Rivet will produce a .yoda file which you can then use as in the previous steps. For other rivet command line options, see

        $ rivet --help

as usual.

### Running on a BSM model

To do this you of course need a working event generator. Contur current provides some tools to work with Herwig, Pythia and Madgraph, and there is some documentation for each of these on the wiki. This example with take you through using Herwig, though it will flag up where things would change for other generators.

Create a run area seperate from the repository where you installed Contur. This run area is where you will run everything from now on.

        $ mkdir run-area
        $ cd run-area
        $ cp -r  $CONTUR_ROOT/data/share RunInfo

#### Choose a model

You should copy a UFO model directory from somewhere. Many of those previously used in contur are in '$CONTUR_ROOT/Models', for example DMsimp_s_spin1 is a widely used simplified Dark Matter model, with some Contur results [here](https://hepcedar.gitlab.io/contur-webpage/results/DMsimp_s_spin1/index.html).

        $ cd RunInfo
        $ cp -r $CONTUR_ROOT/data/Models/DM/DMsimp_s_spin1 .

- A template `param_file.dat` will be provided for each model. This is generator-independent and lists the parameters and scan ranges. Here's the link to the one for our example model: [`data/Models/DM/DMsimp_s_spin1/param_file.dat`](data/Models/DM/DMsimp_s_spin1/param_file.dat). There are four main ways to define a scan range:

        $ # 1 linear scale:
        $ [[x]]
        $ mode = LIN
        $ start = 0.1
        $ stop = 2.5
        $ number = 40

        $ # 2 logarithmic scale
        $ [[y]]
        $ mode = LOG 
        $ start = 1.0
        $ stop = 200.
        $ number = 10

        $ # 3 define a constant
        $ [[z]] 
        $ mode = CONST 
        $ value = 2112

        $ # 4 relative to other parameters
        $ [[function]]
        $ mode = REL 
        $ form = 15 * {x}
        
        $ # 5 impose a condition parameters should satisfy
        $ [[condition1]]
        $ mode = CONDITION
        $ form = {y} > 50

        $ # 6 Pickled object containing the parameter points
        $ [[dataframe]]
        $ mode = DATAFRAME
        $ name = my_parameters.pickle

        $ # use a single SLHA as the starting point for a scan. Must then provide parameter names to step over 
        $ # (see below).
        $ [[slha_file]]
        $ mode = SINGLE
        $ name = SLHA_file.dat

        $ # using a single SLHA file as the starting point for a scan, specify SLHA parameters to modify/step over.
        $ # This example picks out the mass of particle 1000022.
        $ [[M1000022]]
        $ block = MASS
        $ mode = LIN
        $ start = 10
        $ stop = 220
        $ number = 14

        $ # use a single SLHA as the starting point for a scan, scale all values in the block specified below 
        $ # by a factor which can be stepped over
        $ [[slha_file]]
        $ mode = SCALED
        $ name = SLHA_file.dat

        $ # specify SLHA block to scale, and the factors to scale by.
        $ [[MASS]] 	   
        $ mode = LIN
        $ start = 10
        $ stop = 0.5
        $ number = 1.5

        $ # link to directory containing a colleaction of SLHA files to run over.
        $ [[dir]]
        $ mode = DIR
        $ name = "/abs/path/to/directory"


- Template Herwig `herwig.in` files are provided in the many of the model directories (obviously these are generator-dependent, 
   and we'll provide examples for other generators when we can). The  `herwig.in` file specifies parameters in curly brackets, e.g. 
   `.{name}` for future use with the batch system. 

- Build the UFO model using Herwig's 'ufo2herwig' command.

        $ ufo2herwig DMsimp_s_spin1
        $ make

#### Herwig and Rivet combined run on a Single single set of Rivet Analyses

This section is specific to a single run of Herwig with one of these models, a recommended first step.

- Copy the template `herwig.in` file from inside the model to the top level of your run area.

        $ cd run-area
        $ cp RunInfo/DMsimp_s_spin1/herwig.in .
        $ cp RunInfo/DMsimp_s_spin1/param_file.dat .

- Build the full herwig input file

        $ contur-batch --single 

  This will create a directory called `myscan00/13TeV/0000` which will contain a `herwig.in` file with the full instructions
  for a run, and with BSM model variables substituted from `param_file.dat`. There will be some other files which would be used
  if we were generating a scan, but which you can ignore for now.

- Build the Herwig run card (herwig.run).

        $ cd myscan00/13TeV/0000
        $ Herwig read herwig.in -I ../../../RunInfo -L ../../../RunInfo

- Run the Herwig run card, specifying the number of events to generate. This
  can take a while so, as a first test, running around 200 events is fine.

        $ Herwig run herwig.run  -N 200

- This will produce the file herwig.yoda containing the results of the Herwig run. You can run on this as described above (running on a single Yoda file).

Note that if you are running a generator independently of Rivet, you can use a pipe for this, so the (sometimes large) file never has to be resident on disk. For example:

        $ mkfifo fifo.hepmc
        $ run-pythia -n 200000 -e 8000 -c Top:all=on -o fifo.hepmc &
        $ rivet fifo.hepmc -a $RA8TeV

If you have a version of Herwig built without the rivet interface, you will also need to run via this pipe. The appropriate `herwig.in` file can be built using the `-P` option for `contur-batch`.

#### Running a batch job to Generate Heatmaps

In your run-area, run a test scan over the parameter space defined in 'param_file.dat' without submitting it
to a batch farm.  (The `-s` flag ensures no jobs will be submitted.)

         $ contur-batch -n 1000 --seed 101 -s

  or if you have a version of Herwig without the rivet interface installed,use the pipe option:

         $ contur-batch -n 1000 --seed 101 -s -P

This will produce a directory called 'myscan00' (or some higher integer if myscan00 already existed) containing one directory for each selection beam energy (just 13TeV pp by default), containing however many runpoint directories are indicated by the ranges in your param_file.dat. Have a look at the shell scripts (`runpoint_xxxx.sh`) which have been generated and the `herwig.in` files to check all is as you expected. You can manually submit some of the `runpoint_xxxx.sh` files as a test, or run Herwig local as above using the generated `herwig.in` files.

- Now you are ready to run batch jobs. Remove the myscan00 directory tree you just created, and run the
  batch submit command again, now without the `-s` flag and specifying the queue
  on your batch farm. For example:

         $ contur-batch -n 1000 --seed 101 -Q medium

  or
  
         $ contur-batch -n 1000 --seed 101 -P -Q medium


  (Note that we assume `qsub` is available on your system here and has a queue called `medium`.
  Slurm and condor batch systems are also supported, and of course you can change the queue name.
  If you have a different submission system you'll need to
  look into `$CONTUR_ROOT/contur/scan/batch_submit.py` and work out how to change the appropriate submission
  commands.)

- A successful run will produce a directory called 'myscan00' as before. You need to wait for the farm
  to finish the jobs before continuing. On PBS, you can check the progress using the 'qstat' command.

- When the batch job is complete there should, in every run point directory, be
  files `herwig-runpoint_xxx.yoda`.

- Analyse results with contur. Resulting .map file will be output to the
  ANALYSIS folder.

        $ contur -g myscan00/

  For various options see

        $ contur --help

- Plot a heatmap.

        $ cd ANALYSIS/
        $ contur-plot --help
        $ contur-plot contur.map mXd mY1  -T "My First Heatmap"

#### Running Contur with Madgraph

Instead of Herwig, Contur can also be used in combination with other Monte Carlo generators that provide hepmc files. For Madgraph, it is recommended to use version 2.7.2 or later and the latest Rivet release (>3.1.2). When running

        $ $MG_DIR/bin/mg5_aMC <Madgraph script>

where `$MG_DIR` is the directory containg the Madgraph installation, Madgraph will produce an LHE file containing MC events in e.g. mgevents/Events/Run01. Include `shower=Pythia8` in your Madgraph script to have Pythia shower the events in the LHE file and give a hepmc file as output. This one can be read in with Rivet, giving the yoda file. As Madgraph provides a large number of event weights, it is recommended to use the `--skip-weights` option with Rivet to reduce the number of processed weights with different names.

        $ rivet --skip-weights -a $ANALYSIS-LIST <hepmc file>

For the same reason, when running Contur on the yoda file, use the `--wn "Weight_MERGING=0.000"` option

        $ contur --wn "Weight_MERGING=0.000" <yoda file>

When using `contur-batch`, set the generator name to Madgraph using `-m`:

        $ contur-batch -m madgraph -p <param file> -t <Madgraph script>

Within the param file, make sure the model parameters are set similar to the the way it's done for Herwig, e.g.

        set gPXd        {gPXd}
        set tanbeta     {tanbeta}

By default, Madgraph runs on multiple cores. On a batch system, the jobs are however usually assigned a single core. To configure Madgraph correctly for single core mode and thus use the computational ressources most efficiently, include

        set run_mode 0
        set nb_core 1
        set low_mem_multicore_nlo_generation

in your Madgraph script. Example Madgraph scripts containing the important functionality can be found at data/Models/DM/DM_vector_mediator_UFO/mg-example.sh and data/Models/DM/Pseudoscalar_2HDM/mg-example.sh.

As Madgraph might generate a large quantity of output while running, it is recommended to run the Contur clean-up functionality

        $ contur-gridtool <grid directory>

directly after all jobs have finished.

There is an ongoing project to improve interoperability with Madgraph, see [Open Projects](/hepcedar/contur/-/wikis/Open-and-ongoing-projects).

#### Running machine-learning assisted parameter scanning (the CONTUR ORACLE)

The CONTUR ORACLE is the name given to the machine-learning-assisted parameter scanning functionality described in [https://arxiv.org/abs/2202.05882](https://arxiv.org/abs/2202.05882).
The basic idea is that a Random-Forest classifier is used on sampled points to predict the exclusion status of nearby points, thereby reducing the total number of points needed when studying large (multi-dimensional) grids.
Additional Python libraries which are needed are: `sklearn` and `click`.

The setup of a scan if very similar to that described above in `Running a Batch Job to Generate Heatmap`.
Once the UFO file has been copied and compiled, one should initialise the ORACLE using

        contur-oracle init

Which will create a dummy `oracle.config.yaml` file and the appropriate directories for each iteration.
First, choose the parameters of the model which you wish to scan using the ORACLE.
Those should be specified in `oracle.config.yaml`  `params` section with a `range` vector specifying the extremal values of the parameter, as well as a `resolution` parameter which dictates the minimum separation between points.
For example:

        params:
          gVq1:
            range:
            - 0.09
            - 0.99
            resolution: 0.1
          gVq2:
            range:
            - 0.09
            - 0.99
            resolution: 0.1
          gVq3:
            range:
            - 0.09
            - 0.99
            resolution: 0.1
          mXd:
            range:
            - 10.0
            - 5010.0
            resolution: 250
          mY1:
            range:
            - 10.0
            - 10010.0
            resolution: 500

One should also specify the number of points to sample in the initial and subsequent iterations, and the stopping conditions (in precision, recall and entropy) after which the ORACLE is deemed to have converged. For example:

          initial_points: 500
          iteration_points: 300
          precision_goal: 0.90
          recall_goal: 0.90
          entropy_goal: 0.2


In the `param _file.dat`, the parameters which are listed in the `oracle.config.yaml` should be listed in `DATAFRAME` mode and with the dummy `DATAFRAME_LOCATION` being used as the `name` parameter. For example:
          
          [Parameters]
          [[mXd]]
          mode = DATAFRAME
          name = DATAFRAME_LOCATION
          [[mY1]]
          mode = DATAFRAME
          name = DATAFRAME_LOCATION
          [[gVq1]]
          mode = DATAFRAME
          name = DATAFRAME_LOCATION
          [[gVq2]]
          mode = DATAFRAME
          name = DATAFRAME_LOCATION
          [[gVq3]]
          mode = DATAFRAME
          name = DATAFRAME_LOCATION
          [[gVl]]
          mode = CONST
          value = 0.0
          [[gVXd]]
          mode = CONST
          value = 1.0
          [[gAXd]]
          mode = CONST
          value = 0.0
          [[gAq]]
          mode = CONST
          value = 0.0

For expert users, other hyper-parameters such as the test/train split, the number of trees, and the CL of the contours, can be modified in `contur/oracle/hyperparams.py`.

Once the config file is set up, the ORACLE can be set running using:
         
         contur-oracle start

This will randomly pick a subset of size `initial_points` of the grid, and prepare a CONTUR run for those points.
The user will be prompted as to what to do next with a printout on the screen:



          1. Contur batch to generate the events:
          contur-batch -p /path/to/your/param_files/param_file_1.dat -o contur_batch_output_1 -Q medium --seed 101 -n 30000 -b 13TeV
          
          2. Contur to analyse the points
          contur -g contur_batch_output_1 -o contur_analysis_1
          
          3. Contur export to extract the corresponding CSV wiThis th the results
          contur-export -i contur_analysis_1/contur.map -o output_cls/run-output-1.csv
          
          4. Contur oracle to process the results, train the classifier, and determine if more points need to be generated
          contur-oracle start
 
In 1., the user is prompted to submit the jobs to the HPC farm. The user should manually edit the queue name, beams, etc to match their specifications. This part has to be done by the user for security reasons.
The user should then wait until their jobs from 1. have finished (usually a few hours depending on the number of points and the number of nodes on your batch farm), and then can merge them with the command listed in 2.
Once the merge is completed (usually 10 min to an hour or so), the results are exported to a CSV in 3. (a few seconds).

Finally, one can start the next iteration of the ORACLE with 4. : `contur-oracle start`, which will take the points from this iteration and previous ones, separate the sampled points into test/train datasets.
The points in the training dataset are used to train the Random Forest classifier. This classifier is then applied to the testing dataset, and the classifier predictions are compared to the true exclusion status of these points, to obtain the performance metrics of recall, precision and entropy.
These are printed to screen, eg.

          contur-oracle 2021-12-15 16:30:35: it 1: Recall: [0.89/0.95], Precision: [0.75/0.95], Entropy: [0.37/0.20], total points: 342, testing: 114

If the metrics do not yet meet the stopping conditions specified in the configuration file, the next iteration is prepared, sampling the points with the worst entropy values.
The user is then prompted to repeat steps 1.-4. until the performance metrics are met.

All the prompts and performance metrics are printed to screen are also logged in `oracle.log` for future reference.
The classifiers for each iteration are stored in the `classifiers` directory. These are pickle files which can be used as follows to extract predictions:


        import pickle
        classifierFeatures = ["gVq1","gVq2","gVq3","mXd", "mY1"] # as specified in your config file
        file_1 =  open(f"classifiers/classifier-1.pkl", "rb")
        rf_1 = pickle.load(file_1)
        
        grid = ... # array of array of values for the features (ie an arbitrary number of sets of parameter values can be predicted at once)
        pred =  rf.predict(grid) 
        entropy =  entr(rf.predict_proba(grid)).sum(axis=1) / np.log(3)

 `pred` will return a list of 0, 1 or 2, for each row of the `grid`, where 0 is not excluded, 1 is excluded at 68% CL and 2 is excluded at 68-95% CL.
 The entropy can be calculated as shown.


#### Other functionality

`contur-gridtool` provides some utilities for compressing or merging grids, recovering failed grid points, and locating the files corresponding to a particular parameter point.

### Docker 

Note that Dockerfiles containing a working setup (with or without Herwig) are available in the [docker subdirectory](docker).
Instructions for how best to use Contur from these are still in preparation, but you can now get the latest by doing
`docker pull hepstore/contur`. The Rivet/Yoda docker setup is quite mature and the guidance
[here](https://gitlab.com/hepcedar/rivet/-/blob/release-3-1-x/doc/tutorials/docker.md)
might help.

