#!/bin/bash

for SEY in 1.50
do
mkdir simulations_SEY${SEY}_tars
cd simulations_SEY${SEY}
for d in */ ; do
    tar -cvf ../simulations_SEY${SEY}_tars/${d%/}.tar $d
done
cd ..
done
