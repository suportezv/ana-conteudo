"""Vídeo 3 'Como comprar um carro de corrida em 30 segundos' (uol04 + contraste Interlagos)."""
import subprocess, os

BASE = '/tmp/claude-0/-home-user-ana-conteudo/d3f9a2e0-ccad-5a5c-9543-94e17805d096/scratchpad/luxo'
DINA = '/tmp/claude-0/-home-user-ana-conteudo/d3f9a2e0-ccad-5a5c-9543-94e17805d096/scratchpad/dinamico'
os.chdir(BASE)
os.makedirs('parts3', exist_ok=True)
run = lambda a: subprocess.run(a, check=True)
NORM = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p"
Z = "zoompan=z=min(1.10\\,1+0.10*in/(60*{d})):x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):d=1:s=1080x1920:fps=60"
P = "zoompan=z=1.20:x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):d=1:s=1080x1920:fps=60"

def seg(out, src, ss, dur, extra=None, flash=False):
    vf = (extra + "," if extra else "") + NORM + (",fade=t=in:st=0:d=0.08:color=white" if flash else "")
    run(["ffmpeg","-y","-v","error","-ss",str(ss),"-i",src,"-t",str(dur),
         "-vf",vf,"-r","30","-c:v","libx264","-crf","19","-preset","fast","-an",f"parts3/{out}.mp4"])
    print("ok",out)

seg("c1","proxies/uol04.mp4",0.30,2.20,Z.format(d=2.20))                    # walk-in + título
seg("c2","proxies/uol04.mp4",2.50,0.90,P,flash=True)                        # porta 73 punch
seg("c3","proxies/uol04.mp4",3.30,2.10)                                     # "Vai comprar um desse? Eu vou."
run(["ffmpeg","-y","-v","error","-ss","5.15","-i","proxies/uol04.mp4","-frames:v","1","parts3/fz1.png"])
run(["ffmpeg","-y","-v","error","-loop","1","-t","1.00","-i","parts3/fz1.png",
     "-vf","hue=s=0,zoompan=z=min(1.10\\,1+0.10*in/30):x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):d=1:s=1080x1920:fps=30,"+NORM,
     "-r","30","-c:v","libx264","-crf","19","-preset","fast","-an","parts3/f1.mp4"]); print("ok f1")
seg("c4","proxies/uol04.mp4",5.50,1.10,P,flash=True)                        # lateral punch
seg("c5","proxies/uol04.mp4",25.90,1.10,P,flash=True)                       # frente faróis punch
seg("c6","proxies/uol04.mp4",11.40,5.20)                                    # piadas da época
seg("c7",f"{DINA}/proxies/IMG_5972.mp4",4.50,1.50,None,flash=True)          # novinhos do box
seg("c8","proxies/uol04.mp4",19.00,2.50,Z.format(d=2.50))                   # risada close
seg("c9","proxies/uol04.mp4",27.15,4.05)                                    # eu vou correr com um desse
run(["ffmpeg","-y","-v","error","-ss","32.50","-i","proxies/uol04.mp4","-frames:v","1","parts3/fz2.png"])
run(["ffmpeg","-y","-v","error","-loop","1","-t","2.20","-i","parts3/fz2.png",
     "-vf","hue=s=0.35,"+NORM,"-r","30","-c:v","libx264","-crf","19","-preset","fast","-an","parts3/f2.mp4"]); print("ok f2")

order = ["c1","c2","c3","f1","c4","c5","c6","c7","c8","c9","f2"]
open("parts3/list.txt","w").write("\n".join(f"file '{n}.mp4'" for n in order)+"\n")
run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i","parts3/list.txt","-c","copy","parts3/timeline.mp4"])
t=0
for n in order:
    dd=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"parts3/{n}.mp4"],capture_output=True,text=True).stdout.strip())
    print(f"{n}: start={t:.2f} dur={dd:.2f}"); t+=dd
print("TOTAL", round(t,2))

def ts(x):
    h=int(x//3600); m=int(x%3600//60); s=x%60
    return f"{h}:{m:02d}:{s:05.2f}"
# mapeamento: c3 começa em 3.10 (src 3.30); c6 em 7.30 (src 11.40); c9 depois
# starts esperados: c1 0, c2 2.20, c3 3.10, f1 5.20, c4 6.20, c5 7.30, c6 8.40, c7 13.60, c8 15.10, c9 17.60, f2 21.65
FR = [
 (3.32, 4.18, "Vai comprar um desse?"),
 (4.38, 5.15, "Eu vou."),
 (8.70, 9.85, "Perfeito, é da minha época."),
 (10.18,10.64,"Como é que é?"),
 (10.88,11.74,"É da minha época."),
 (12.16,13.55,"Não, ele não é tão velho assim."),
 (17.83,19.00,"Eu vou correr com um desse."),
 (19.01,20.20,"O que que cês acham?"),
 (20.59,21.60,"Ó que belezinha."),
]
lines=["[Script Info]","ScriptType: v4.00+","PlayResX: 1080","PlayResY: 1920","WrapStyle: 2","",
"[V4+ Styles]",
"Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
"Style: Legenda,Liberation Sans,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,3.5,2.5,2,60,60,240,1",
"","[Events]",
"Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
for a,b,t_ in FR:
    lines.append(f"Dialogue: 0,{ts(a)},{ts(b)},Legenda,,0,0,0,,{t_}")
open("legendas3.ass","w").write("\n".join(lines)+"\n")
print("ass ok")
