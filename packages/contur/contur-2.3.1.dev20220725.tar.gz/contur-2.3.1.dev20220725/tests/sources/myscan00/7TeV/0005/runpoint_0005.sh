#! /bin/bash
#$ -j y # Merge the error and output streams into a single file
#$ -o /unix/atlas3/jmb/Work/Regression_Test/myscan01/7TeV/0005/contur_batch.log # Output file path
source /unix/cedar/software/cos7/defaults/setupEnv.sh;
source /home/jmb/gitstuff/contur-rel/setupContur.sh
cd /unix/atlas3/jmb/Work/Regression_Test/myscan01/7TeV/0005
Herwig read herwig.in -I /unix/atlas3/jmb/Work/Regression_Test/RunInfo -L /unix/atlas3/jmb/Work/Regression_Test/RunInfo;
Herwig run herwig.run --seed=101  --tag=runpoint_0005  --numevents=30000 ;
