#!/bin/bash

simname=LHC6.8TeV_v1_Q1R5_0_sey1.35_1.20e11ppb_multi5
ffmpeg -i images_${simname}/Pass%05d.png -c:v libx264 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2,setpts=1.*PTS" -profile:v high -level:v 4.0 -pix_fmt yuv420p -crf 22  -codec:a aac movie_${simname}.mp4
