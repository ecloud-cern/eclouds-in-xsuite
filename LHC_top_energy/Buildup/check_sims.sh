#!/bin/bash

grep --include=logfile.txt -rnw simulations_SEY1.45 -e 401/402 | wc -l
# for d in simulations_SEY1.20/LHC*
# do
#     vari=`ls -ltrah $d/MP* | wc -l`
#     if [[ $vari != 20 ]]
#     then
#         echo "$vari" $d
#     fi
# done
