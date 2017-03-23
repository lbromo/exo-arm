#!/bin/bash
if [ -z "$1" ]
then
    CORES=1
else
    CORES=$1
fi

echo "$CORES"

for i in {1..$CORES}
do
    screen -dmS "parest_$j_$i" \
           bash -c         \
           "
           source venv/bin/activate;
           export LD_LIBRARY_PATH=/afs/ies.auc.dk/group/17gr1035/no_backup/pagmo/build/lib;
           export PYTHONPATH=/afs/ies.auc.dk/group/17gr1035/no_backup/pagmo/build/usr/lib/python2.7/dist-packages;
           cd software/model/muscles/parameter_estimation
           python parest.py parest_$j_$i.pickle;
           exec bash
           "
done
