#!/usr/bin/env bash
# Finalização: overlays de motion, legendas por último, mix de áudio sincronizado, -14 LUFS.
set -euo pipefail
DIR="/tmp/claude-0/-home-user-ana-conteudo/d3f9a2e0-ccad-5a5c-9543-94e17805d096/scratchpad/dinamico"
cd "$DIR"

ffmpeg -y -v error \
  -i parts/timeline.mp4 \
  -loop 1 -t 33.57 -i motion/cabelo.png \
  -loop 1 -t 33.57 -i motion/titulo_interlagos.png \
  -loop 1 -t 33.57 -i motion/dia_pista.png \
  -ss 37.15 -t 5.90 -i proxies/IMG_5966.mp4 \
  -i audio/trilha_full.wav \
  -ss 12.95 -t 3.30 -i proxies/IMG_5977.mp4 \
  -ss 21.60 -t 2.33 -i proxies/IMG_5980.mp4 \
  -i audio/sfx_impact.mp3 \
  -i audio/sfx_whoosh.mp3 \
  -i audio/sfx_riser.mp3 \
  -filter_complex "\
[1:v]format=rgba,fade=t=in:st=3.97:d=0.10:alpha=1,fade=t=out:st=5.70:d=0.20:alpha=1[cab];\
[2:v]format=rgba,fade=t=in:st=5.90:d=0.12:alpha=1,fade=t=out:st=7.90:d=0.30:alpha=1[tit];\
[3:v]format=rgba,fade=t=in:st=30.90:d=0.25:alpha=1[dia];\
[0:v][cab]overlay=0:0:enable='between(t,3.97,5.90)'[v1];\
[v1][tit]overlay=0:0:enable='between(t,5.90,8.20)'[v2];\
[v2][dia]overlay=0:0:enable='between(t,30.90,33.57)'[v3];\
[v3]fade=t=out:st=33.10:d=0.47,subtitles=legendas.ass[vout];\
[5:a]volume='if(lt(t,5.85),0.32,1.0)':eval=frame[trilha];\
[4:a]volume=1.9,highpass=f=90[fala];\
[6:a]volume=0.55,afade=t=in:st=0:d=0.15,adelay=12067|12067[motor1];\
[7:a]volume=0.38,afade=t=in:st=0:d=0.15,adelay=22900|22900[motor2];\
[8:a]volume=1.0,adelay=5900|5900[imp1];\
[8:a]volume=1.1,adelay=12067|12067[imp2];\
[9:a]volume=0.9,adelay=8200|8200[wh1];\
[9:a]volume=0.9,adelay=15400|15400[wh2];\
[9:a]volume=0.8,adelay=22900|22900[wh3];\
[10:a]volume=0.9,adelay=10050|10050[ris];\
[trilha][fala][motor1][motor2][imp1][imp2][wh1][wh2][wh3][ris]amix=inputs=10:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st=32.80:d=0.77[aout]" \
  -map "[vout]" -map "[aout]" -t 33.57 \
  -c:v libx264 -crf 21 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart \
  interlagos_dinamico_v1.mp4

ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 interlagos_dinamico_v1.mp4
echo "== RENDER OK =="