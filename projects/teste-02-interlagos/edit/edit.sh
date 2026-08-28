#!/usr/bin/env bash
# Montagem do edit dinâmico de Interlagos: 19 segmentos na grade de 129 BPM.
set -euo pipefail
DIR="/tmp/claude-0/-home-user-ana-conteudo/d3f9a2e0-ccad-5a5c-9543-94e17805d096/scratchpad/dinamico"
cd "$DIR"; mkdir -p parts
P=proxies

# seg <out> <src> <ss> <dur_out> <filtro extra de vídeo>
seg() {
  local out=$1 src=$2 ss=$3 dur=$4 vf=$5
  ffmpeg -y -v error -ss "$ss" -i "$P/$src.mp4" -t "$dur" \
    -vf "$vf,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p" \
    -r 30 -c:v libx264 -crf 18 -preset fast -an "parts/$out.mp4"
  echo "ok $out"
}

ZIN='zoompan=z=min(1.10\,1+0.10*in/(60*D)):x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):d=1:s=1080x1920:fps=60'
ZOUT='zoompan=z=max(1.0001\,1.15-0.15*in/(60*D)):x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):d=1:s=1080x1920:fps=60'
PUNCH='zoompan=z=1.22:x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):d=1:s=1080x1920:fps=60'

# BUILD
seg s01 IMG_5966 37.15 5.90 "${ZIN//D/5.90}"
seg s02 IMG_5963 32.00 2.30 "${ZOUT//D/2.30}"
seg s03 IMG_5962 1.20 0.93 "${PUNCH}"
seg s04 IMG_5972 4.50 0.93 "${ZIN//D/0.93}"
seg s05 IMG_5966 13.50 0.93 "${ZOUT//D/0.93}"
seg s06 IMG_5978 6.30 1.06 "${ZIN//D/1.06}"
# DROP: passada com speed ramp (0.5x por 1.4s, depois 2x) + flash branco
ffmpeg -y -v error -ss 12.95 -i "$P/IMG_5977.mp4" -t 0.75 -vf "setpts=2*PTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fade=t=in:st=0:d=0.12:color=white,format=yuv420p" -r 30 -c:v libx264 -crf 18 -preset fast -an parts/s07a.mp4
ffmpeg -y -v error -ss 13.70 -i "$P/IMG_5977.mp4" -t 2.70 -vf "setpts=PTS/2,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p" -r 30 -c:v libx264 -crf 18 -preset fast -an parts/s07b.mp4
echo ok s07
seg s08 IMG_5964 30.20 0.93 "${PUNCH}"
seg s09 IMG_5967 0.80 0.93 "${ZOUT//D/0.93}"
seg s10 IMG_5967 8.00 0.93 "${ZIN//D/0.93}"
seg s11 IMG_5972 0.30 0.93 "${ZOUT//D/0.93}"
seg s12 IMG_5965 19.50 1.86 "${ZIN//D/1.86}"
ffmpeg -y -v error -ss 0.50 -i "$P/IMG_5973.mp4" -t 2.98 -vf "setpts=PTS/1.6,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p" -r 30 -c:v libx264 -crf 18 -preset fast -an parts/s13.mp4
echo ok s13
seg s14 IMG_5980 21.60 2.32 "${ZIN//D/2.32}"
seg s15 IMG_5976 0.80 0.93 "${PUNCH}"
seg s16 IMG_5979 0.30 0.93 "${ZIN//D/0.93}"
seg s17 IMG_5981 99.50 1.86 "${ZIN//D/1.86}"
seg s18 IMG_5964 74.50 1.86 "${ZOUT//D/1.86}"
# OUTRO em slow leve
ffmpeg -y -v error -ss 8.00 -i "$P/IMG_5963.mp4" -t 2.81 -vf "setpts=PTS/0.85,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p" -r 30 -c:v libx264 -crf 18 -preset fast -an parts/s19.mp4
echo ok s19

# concat
ls parts/s01.mp4 parts/s02.mp4 parts/s03.mp4 parts/s04.mp4 parts/s05.mp4 parts/s06.mp4 \
   parts/s07a.mp4 parts/s07b.mp4 parts/s08.mp4 parts/s09.mp4 parts/s10.mp4 parts/s11.mp4 \
   parts/s12.mp4 parts/s13.mp4 parts/s14.mp4 parts/s15.mp4 parts/s16.mp4 parts/s17.mp4 \
   parts/s18.mp4 parts/s19.mp4 | sed "s/^/file '/;s/$/'/" > parts/list.txt
ffmpeg -y -v error -f concat -safe 0 -i parts/list.txt -c copy parts/timeline.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 parts/timeline.mp4
echo "== TIMELINE OK =="