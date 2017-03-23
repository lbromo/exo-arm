#!/bin/bash
for j in {1..4}
do
    for i in {1..16}
    do
        screen -dmS "parest_$j_$i" \
               bash -c         \
               "
               source venv/bin/activate;
               export LD_LIBRARY_PATH=/afs/ies.auc.dk/group/17gr1035/Private/pagmo/build/lib;
               export PYTHONPATH=/afs/ies.auc.dk/group/17gr1035/Private/pagmo/build/usr/lib/python2.7/dist-packages;
               cd software/model/muscles/parameter_estimation
               python parest.py parest_$j_$i.pickle;
               exec bash
               "
    done
    sleep 3600
done
