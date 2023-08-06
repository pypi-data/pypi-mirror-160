# -*- bash -*-
mydir="$( dirname "${BASH_SOURCE[0]}" )"
python_root="$( which python )"
python_bin_root="${python_root%/*}"
python_bin_root="${python_bin_root%/*}"
data_file_pre="$(find ${python_bin_root} -name DB)"
data_file_pre="${data_file_pre%/*}"


export CONTUR_DATA_PATH="${data_file_pre%/*}" 
export CONTUR_USER_DIR="$HOME/contur_users"


# ------------------
# Add the local rivet area to the rivet data and analysis paths.
export RIVET_DATA_PATH=$(echo $CONTUR_DATA_PATH/data/Rivet:$CONTUR_DATA_PATH/data/Theory:$RIVET_DATA_PATH | awk -v RS=':' '!a[$1]++ { if (NR > 1) printf RS; printf $1 }')
export RIVET_ANALYSIS_PATH=$(echo $CONTUR_DATA_PATH/data/Rivet:$RIVET_ANALYSIS_PATH | awk -v RS=':' '!a[$1]++ { if (NR > 1) printf RS; printf $1 }')


# This file won't exist until make has been run
# TODO: we need a better way to do this
# replace this by internal python functions
ALIST=$CONTUR_USER_DIR/analysis-list
test -f $ALIST && source $ALIST

echo "Have defined CONTUR_DATA_PATH, where is the place contur data files put, including Makefile"
echo "Have defined CONTUR_USER_DIR=~/contur_users by default, users can feel free to change, it is the place to store generated files"
echo "Have added the local rivet area to the RIVET_DATA_PATH and RIVET_ANALYSIS_PATH"
