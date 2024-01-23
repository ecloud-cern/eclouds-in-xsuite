#!/bin/bash

# export EOS_MGM_URL=root://eosuser.cern.ch

echo $KRB5CCNAME
klist -f


pwd
which python


echo $1
echo $2

cp /afs/cern.ch/work/k/kparasch/public/SimCampaigns/LHC_Triplet_Pinches/pinch.py .
cp /afs/cern.ch/work/k/kparasch/public/SimCampaigns/LHC_Triplet_Pinches/eclouds_LHCIT_v1.json .
cp /afs/cern.ch/work/k/kparasch/public/SimCampaigns/LHC_Triplet_Pinches/ecloud_xsuite_filemanager.py .
cp /afs/cern.ch/work/k/kparasch/public/SimCampaigns/LHC_Triplet_Pinches/replaceline.py .

python pinch.py --ecloud $1 --sey $2
ls -lrtah
ls simulations/* -lrtah

SEY=$2
IFS='.'
ec=($1)
index=${ec[3]}
ecloud_type=${ec[1]}
ecloud_type=${ecloud_type^^}
unset IFS

pinch_name=LHC6.8TeV_v1_${ecloud_type}_${index}_sey${SEY}_1.20e11ppb

xrdcp simulations/${pinch_name}/${pinch_name}.h5 root://eosproject.cern.ch//eos/project/e/ecloud-simulations/kparasch/LHC_Triplets/Pinches/run3_bet30cm_160urad_1.2e11ppb_2.0um/SEY${SEY}/${pinch_name}.h5
