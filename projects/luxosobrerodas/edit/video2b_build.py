"""Vídeo 2.1 'Missão: entrar num carro de gaiola' — freeze, contador, cutaway de pista."""
import subprocess, os

BASE = '/tmp/claude-0/-home-user-ana-conteudo/d3f9a2e0-ccad-5a5c-9543-94e17805d096/scratchpad/luxo'
DINA = '/tmp/claude-0/-home-user-ana-conteudo/d3f9a2e0-ccad-5a5c-9543-94e17805d096/scratchpad/dinamico'
os.chdir(BASE)
os.makedirs('parts2b', exist_ok=True)

def run(args):
    subprocess.run(args, check=True)

NORM = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p"
def seg(out, src, ss, dur, extra=None):
    vf = (extra + "," if extra else "") + NORM
    run(["ffmpeg","-y","-v","error","-ss",str(ss),"-i",src,"-t",str(dur),
         "-vf",vf,"-r","30","-c:v","libx264","-crf","19","-preset","fast","-an",f"parts2b/{out}.mp4"])
    print("ok",out)

Z = "zoompan=z=min(1.08\\,1+0.08*in/(60*{d})):x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):d=1:s=1080x1920:fps=60"

# cortes
seg("c1","proxies/uol05.mp4",1.70,5.10,Z.format(d=5.10))
seg("c2","proxies/uol05.mp4",7.50,2.90)
seg("c3","proxies/uol05.mp4",15.40,3.70,Z.format(d=3.70))
seg("c4","proxies/uol05.mp4",20.00,3.20)
# freeze BW: frame de 23.15 congelado 1.30s com push-in
run(["ffmpeg","-y","-v","error","-ss","23.15","-i","proxies/uol05.mp4","-frames:v","1","parts2b/freeze.png"])
run(["ffmpeg","-y","-v","error","-loop","1","-t","1.30","-i","parts2b/freeze.png",
     "-vf","hue=s=0,zoompan=z=min(1.12\\,1+0.12*in/39):x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):d=1:s=1080x1920:fps=30,"+NORM,
     "-r","30","-c:v","libx264","-crf","19","-preset","fast","-an","parts2b/f1.mp4"])
print("ok f1")
seg("c5","proxies/uol05.mp4",25.70,5.30,Z.format(d=5.30))
# cutaway pista (Interlagos 5977) com flash branco na entrada
run(["ffmpeg","-y","-v","error","-ss","13.30","-i",f"{DINA}/proxies/IMG_5977.mp4","-t","2.00",
     "-vf",NORM+",fade=t=in:st=0:d=0.10:color=white",
     "-r","30","-c:v","libx264","-crf","19","-preset","fast","-an","parts2b/p1.mp4"])
print("ok p1")
seg("c6","proxies/uol05.mp4",38.90,7.30)
seg("c7","proxies/uol05.mp4",48.10,6.70,Z.format(d=6.70))
# end card: último frame congelado 2.0s
run(["ffmpeg","-y","-v","error","-ss","54.70","-i","proxies/uol05.mp4","-frames:v","1","parts2b/last.png"])
run(["ffmpeg","-y","-v","error","-loop","1","-t","2.00","-i","parts2b/last.png",
     "-vf","hue=s=0.35,"+NORM,"-r","30","-c:v","libx264","-crf","19","-preset","fast","-an","parts2b/f2.mp4"])
print("ok f2")

order = ["c1","c2","c3","c4","f1","c5","p1","c6","c7","f2"]
open("parts2b/list.txt","w").write("\n".join(f"file '{n}.mp4'" for n in order)+"\n")
run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i","parts2b/list.txt","-c","copy","parts2b/timeline.mp4"])
d = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0","parts2b/timeline.mp4"],capture_output=True,text=True).stdout.strip()
print("timeline:",d)
t=0
for n in order:
    dd=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"parts2b/{n}.mp4"],capture_output=True,text=True).stdout.strip())
    print(f"{n}: start={t:.2f} dur={dd:.2f}")
    t+=dd

# legendas
def ts(x):
    h=int(x//3600); m=int(x%3600//60); s=x%60
    return f"{h}:{m:02d}:{s:05.2f}"
FR = [
 (0.28,1.76,"Léo, não dá pra levantar?"),
 (2.22,3.26,"Tem almofada aí."),
 (3.22,5.10,"Almofada, ó a humilhação."),
 (5.30,7.90,"Meu Deus do céu,\\Nolha isso aqui, olha isso aqui."),
 (8.12,8.86,"Vai, vai, vai, mais uma."),
 (8.88,9.90,"Muita almofada, Léo."),
 (10.30,11.60,"A situação."),
 (11.90,12.95,"Não, tá bom já."),
 (13.32,14.90,"Cadê o ar condicionado?"),
 (16.36,18.20,"Dá outra acelerada aí, Tony."),
 (24.30,25.90,"Não, como é que tira ele aqui?"),
 (28.34,28.60,"Tá mal?"),
 (28.60,30.80,"Não, nada de mal,\\Neu faço academia, meu filho."),
 (31.00,33.30,"Ai, [bip], é duro."),
 (34.04,35.80,"Não dá certo."),
 (36.46,37.50,"Ah, assim é muito mais fácil."),
]
lines=["[Script Info]","ScriptType: v4.00+","PlayResX: 1080","PlayResY: 1920","WrapStyle: 2","",
"[V4+ Styles]",
"Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
"Style: Legenda,Liberation Sans,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,3.5,2.5,2,60,60,240,1",
"","[Events]",
"Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
for a,b,t_ in FR:
    lines.append(f"Dialogue: 0,{ts(a)},{ts(b)},Legenda,,0,0,0,,{t_}")
open("legendas2b.ass","w").write("\n".join(lines)+"\n")
print("ass ok; carai bip em 32.44-32.68")
