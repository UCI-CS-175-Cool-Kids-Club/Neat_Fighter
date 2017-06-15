#!/bin/bash

for i in `find ../generations-winner/ -type f | tr "-" " " | sort -k 4n | tr " " "-"`; do
    fitness=`./StartClients.py $i '../generations-winner/linh-gen-23-winner' | grep "TARGET:" | awk '{print $8}'`
    echo $i : $fitness
done
