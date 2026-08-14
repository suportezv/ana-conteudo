#!/usr/bin/env bash
# Vídeo 1 @luxosobrerodas: ASMR POV GT4 RS. Áudio contínuo de motor, punch-ins nos giros.
set -euo pipefail
DIR="/tmp/claude-0/-home-user-ana-conteudo/d3f9a2e0-ccad-5a5c-9543-94e17805d096/scratchpad/luxo"
MOTION="/tmp/claude-0/-home-user-ana-conteudo/d3f9a2e0-ccad-5a5c-9543-94e17805d096/scratchpad/dinamico/motion"
cd "$DIR"; mkdir -p parts1

# A: garagem, motor liga (uol02a 17.70-20.70), zoom in suave. 1074x1920 -> pad p/ 1080.
ffmpeg -y -v error -ss 17.70 -i proxies/uol02a.mp4 -t 3.0 \
  -vf "zoompan=z=min(1.08\,1+0.08*in/180):x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):d=1:s=1074x1920:fps=60,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p" \
  -r 30 -c:v libx264 -crf 19 -preset fast -an parts1/a.mp4

# B: POV contínuo (uol03 3.20-28.75) com punch-ins por frame @60fps
Z="if(lt(in,243),1.001,if(lt(in,611),1.15,if(lt(in,888),1.001,if(lt(in,971),1.18,if(lt(in,1098),1.001,if(lt(in,1296),1.15,1.001))))))"
ffmpeg -y -v error -ss 3.20 -i proxies/uol03.mp4 -t 25.55 \
  -vf "zoompan=z='$Z':x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):d=1:s=1080x1920:fps=60,format=yuv420p" \
  -r 30 -c:v libx264 -crf 19 -preset fast -an parts1/b.mp4

printf "file 'a.mp4'\nfile 'b.mp4'\n" > parts1/list.txt
ffmpeg -y -v error -f concat -safe 0 -i parts1/list.txt -c copy parts1/timeline.mp4

# Áudio: motor real contínuo + impacto sutil na virada garagem->POV
ffmpeg -y -v error \
  -i parts1/timeline.mp4 \
  -loop 1 -t 28.55 -i "$MOTION/pov_abre.png" \
  -loop 1 -t 28.55 -i "$MOTION/pov_fecha.png" \
  -ss 17.70 -t 3.0 -i proxies/uol02a.mp4 \
  -ss 3.20 -t 25.55 -i proxies/uol03.mp4 \
  -i "$SFX_IMPACT" \
  -filter_complex "\
[1:v]format=rgba,fade=t=in:st=0.30:d=0.25:alpha=1,fade=t=out:st=3.20:d=0.30:alpha=1[abre];\
[2:v]format=rgba,fade=t=in:st=26.30:d=0.30:alpha=1[fecha];\
[0:v][abre]overlay=0:0:enable='between(t,0.30,3.50)'[v1];\
[v1][fecha]overlay=0:0:enable='between(t,26.30,28.55)'[v2];\
[v2]fade=t=out:st=28.10:d=0.45[vout];\
[3:a]volume=1.0[ga];\
[4:a]volume=1.0[pa];\
[ga][pa]concat=n=2:v=0:a=1[eng];\
[5:a]volume=0.45,adelay=2900|2900[imp];\
[eng][imp]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st=27.80:d=0.75[aout]" \
  -map "[vout]" -map "[aout]" -t 28.55 \
  -c:v libx264 -crf 21 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart \
  luxo_v1_asmr_pov.mp4
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 luxo_v1_asmr_pov.mp4
echo "== V1 OK =="