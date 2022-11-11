#!/bin/bash

for ecloud in no mb mq all
do
    for optimization in 0 1 2 3 4 5 6
    do 
        for num_particles in 2 4 6 8 10 12 14 16 18 20 22 24 26 28 30
        do
            python time_injection.py --num_particles ${num_particles}000 --optimization $optimization --ecloud $ecloud
        done
        for num_particles in 6912 6913 13824 13825 20738 20739 27648 27649
        do
            python time_injection.py --num_particles $num_particles --optimization $optimization --ecloud $ecloud
        done
    done
done
