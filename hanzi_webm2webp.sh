#!/usr/bin/env bash

fname="${1%webm}"

ffmpeg \
  -y \
  -i "${fname}.webm" \
  -vcodec libwebp \
  -vf "fps=25,scale=256:-1,negate,hue=h=180" \
  -loop 0 \
  -compression_level 6 \
  -q:v 50 \
  "${fname}.webp"
