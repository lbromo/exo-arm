#!/bin/bash
if [ -z "$1" ]
then
    RUNS=1
else
    RUNS=$1
fi

i=0

while [ $i -lt $RUNS ]
do
    if [ "$(ps -ef | grep -v grep | grep parest.py | wc -l)" -lt  "36" ]
    then
        screen -XdmS "parest_$i" \
               bash -c         \
               "
               source venv/bin/activate; \\
               export LD_LIBRARY_PATH=/afs/ies.auc.dk/group/17gr1035/no_backup/usr/local/lib; \\
               export PYTHONPATH=/afs/ies.auc.dk/group/17gr1035/no_backup/usr/lib/python2.7/dist-packages; \\
               cd software/model/muscles/parameter_estimation; \\
               nice -n 10 python parest.py parest_$i.pickle; \\
               exec bash; \\
               ^C;
               "
    i=$[$i+1]
    else
        sleep 300
    fi
done
