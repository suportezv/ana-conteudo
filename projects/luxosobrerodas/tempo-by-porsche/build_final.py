"""Montagem final: entrevista Tempo by Porsche (~178s, 1080x1920).

Blocos de áudio = voz isolada (ElevenLabs) com sub-trims; visual alterna
A-cam 4K sincronizada e b-roll com speed ramps; grade única; legendas por último.
"""
import json, subprocess, os

BASE = '/tmp/claude-0/-home-user-ana-conteudo/d3f9a2e0-ccad-5a5c-9543-94e17805d096/scratchpad/uol2'
os.chdir(BASE)
os.makedirs('final', exist_ok=True)
run = lambda a: subprocess.run(a, check=True)

GRADE = "eq=contrast=1.05:saturation=1.12"
NORM = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,{GRADE},format=yuv420p"
ACAM = 'brutos/entrevista_4399.MOV'

spine = dict((n, (a, b)) for n, a, b in json.load(open('spine.json')))

# ---- plano de áudio: (bloco, sub-ranges dentro do arquivo isolado) ----
AUDIO = [
    ('s01_hook',     [(0, 5.82)]),
    ('_interlude',   None),                      # 4.0s de ambiente
    ('s02_apres',    [(0, 5.18)]),
    ('s03_artecarro',[(0, 9.82)]),
    ('s04_15anos',   [(0, 8.60)]),
    ('s05_origem',   [(0, 14.90)]),
    ('s06_euvou',    [(5.70, 16.30), (17.40, 19.66)]),
    ('s07_cafe',     [(0, 13.42)]),
    ('s08_proposta', [(0, 13.00)]),
    ('s09_pessoas',  [(0, 9.31)]),
    ('s10_carroRS',  [(0, 10.30), (13.90, 35.90)]),
    ('s11_conexao',  [(2.95, 18.36)]),
    ('s12_eventos',  [(0, 10.50)]),
    ('s14_endereco', [(0, 11.52)]),
    ('s15_fecho',    [(0, 5.20)]),
    ('s16_fecho2',   [(0, 4.74)]),
]
INTERLUDE_D = 4.0

# ---- timeline de saída: calcula início de cada bloco ----
starts, t = {}, 0.0
for name, subs in AUDIO:
    starts[name] = round(t, 2)
    if subs is None:
        t += INTERLUDE_D
    else:
        t += sum(b - a for a, b in subs)
TOTAL = round(t, 2)
print('TOTAL previsto:', TOTAL)

# ---- áudio: monta cadeia ----
ins, fc, labels = [], [], []
idx = 0
for name, subs in AUDIO:
    if subs is None:
        ins += ['-ss', '5', '-t', str(INTERLUDE_D), '-i', 'proxies/b4392.mp4']
        fc.append(f"[{idx}:a]volume=0.5,afade=t=in:st=0:d=0.3,afade=t=out:st={INTERLUDE_D-0.4}:d=0.4[a{idx}]")
        labels.append(f"[a{idx}]"); idx += 1
        continue
    for a, b in subs:
        ins += ['-i', f'audio/seg/{name}_iso.mp3']
        d = b - a
        fc.append(f"[{idx}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.03,afade=t=out:st={round(d-0.04,2)}:d=0.04[a{idx}]")
        labels.append(f"[a{idx}]"); idx += 1
fc.append(''.join(labels) + f"concat=n={len(labels)}:v=0:a=1[voz]")
run(['ffmpeg', '-y', '-v', 'error'] + ins + ['-filter_complex', ';'.join(fc),
     '-map', '[voz]', '-ac', '2', '-ar', '48000', '-c:a', 'pcm_s16le', 'final/voz.wav'])
print('voz ok:', subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','final/voz.wav'],capture_output=True,text=True).stdout.strip())

# ---- vídeo: lista de segmentos (out_dur, fonte) ----
# tipos: ('acam', src_in)  |  ('broll', file, src_in, speed)
def acam_windows(name, subs):
    src0 = spine[name][0]
    return [(round(b - a, 2), ('acam', round(src0 + a, 2))) for a, b in subs]

V = []
V += [(2.0, ('broll', 'b4402', 8.0, 0.85)), (2.0, ('broll', 'b4403', 6.0, 0.8)), (1.82, ('broll', 'b4398', 30.0, 1.0))]
V += [(1.6, ('broll', 'b4387', 40.0, 2.0)), (1.2, ('broll', 'b4392', 8.0, 3.0)), (1.2, ('broll', 'b4394', 66.0, 2.0))]
V += acam_windows('s02_apres', [(0, 5.18)])
V += acam_windows('s03_artecarro', [(0, 9.82)])
V += [(4.0, ('broll', 'b4401', 28.0, 0.85)), (4.6, ('broll', 'b4408', 16.0, 0.9))]
V += acam_windows('s05_origem', [(0, 14.90)])
V += acam_windows('s06_euvou', [(5.70, 16.30), (17.40, 19.66)])
V += acam_windows('s07_cafe', [(0, 13.42)])
V += [(3.0, ('broll', 'b4404', 6.0, 2.0)), (4.0, ('broll', 'b4398', 34.0, 0.9)),
      (3.0, ('broll', 'b4406', 20.0, 2.0)), (3.0, ('broll', 'b4404', 14.0, 1.0))]
V += acam_windows('s09_pessoas', [(0, 9.31)])
# s10: A(0-10.3) visual: carro slow 2x cortes; B(13.9-35.9) visual: cam/carro/capacete/cam
V += [(5.0, ('broll', 'b4403', 4.0, 0.7)), (5.3, ('broll', 'b4403', 19.0, 0.75))]
V += acam_windows('s10_carroRS', [(13.90, 19.40)])
V += [(5.0, ('broll', 'b4403', 27.0, 0.8)), (4.0, ('broll', 'b4408', 40.0, 0.9))]
V += acam_windows('s10_carroRS', [(28.40, 35.90)])
# s11: cam (2.95-11.45) + abraço slow (visual p/ 11.45-15.45) + cam (15.45-18.36)
V += acam_windows('s11_conexao', [(2.95, 11.45)])
V += [(4.0, ('broll', 'b4398', 46.0, 0.6))]
V += acam_windows('s11_conexao', [(15.45, 18.36)])
V += [(2.5, ('broll', 'b4406', 8.0, 2.0)), (2.5, ('broll', 'b4402', 30.0, 1.0)),
      (2.5, ('broll', 'b4404', 2.0, 2.0)), (3.0, ('broll', 'b4405', 30.0, 0.9))]
V += [(3.0, ('broll', 'b6184', 12.0, 2.0)), (2.5, ('broll', 'bvideo706', 2.0, 1.2)),
      (3.0, ('broll', 'b4397', 1.5, 1.0)), (3.02, ('broll', 'b4398', 0.5, 0.9))]
V += acam_windows('s15_fecho', [(0, 5.20)])
V += acam_windows('s16_fecho2', [(0, 4.74)])

json.dump([d for d, _ in V], open('final/plan.json', 'w'))
vd = sum(d for d, _ in V)
print('vídeo total:', round(vd, 2), '(alvo', TOTAL, ')')

# gera partes
os.makedirs('final/parts', exist_ok=True)
plist = []
for i, (d, src) in enumerate(V):
    out = f'final/parts/v{i:03d}.mp4'
    plist.append(out)
    if os.path.exists(out):
        continue
    if src[0] == 'acam':
        run(['ffmpeg', '-y', '-v', 'error', '-ss', str(src[1]), '-i', ACAM, '-t', str(d),
             '-vf', NORM, '-r', '30', '-an', '-c:v', 'libx264', '-crf', '19', '-preset', 'fast', out])
    else:
        _, f, si, speed = src
        src_d = round(d * speed, 3)
        run(['ffmpeg', '-y', '-v', 'error', '-ss', str(si), '-t', str(src_d), '-i', f'proxies/{f}.mp4',
             '-vf', f"setpts=PTS/{speed},{NORM}", '-r', '30', '-an', '-t', str(d),
             '-c:v', 'libx264', '-crf', '19', '-preset', 'fast', out])
    print('ok', out, d, src)
open('final/list.txt', 'w').write('\n'.join(f"file 'parts/{os.path.basename(p)}'" for p in plist) + '\n')
run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', 'final/list.txt', '-c', 'copy', 'final/timeline.mp4'])
print('timeline:', subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','final/timeline.mp4'],capture_output=True,text=True).stdout.strip())

# ---- legendas: sentenças remapeadas ----
d = json.load(open('edit/transcripts/entrevista_limpa.json'))
words = [w for w in d['words'] if w['type'] == 'word']

def ts(x):
    h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f"{h}:{m:02d}:{s:05.2f}"

events = []
for name, subs in AUDIO:
    if subs is None:
        continue
    src0 = spine[name][0]
    out0 = starts[name]
    off = 0.0
    for a, b in subs:
        lo, hi = src0 + a, src0 + b
        ws = [w for w in words if w['start'] >= lo - 0.05 and w['end'] <= hi + 0.05]
        # agrupa por pontuação/tamanho
        cur, cstart = [], None
        for w in ws:
            if cstart is None:
                cstart = w['start']
            cur.append(w['text'])
            endp = w['text'].rstrip()[-1:] in '.?!'
            if endp or len(cur) >= 8:
                t0 = out0 + off + (cstart - lo)
                t1 = out0 + off + (w['end'] - lo) + 0.25
                events.append((t0, min(t1, out0 + off + (b - a)), ' '.join(cur)))
                cur, cstart = [], None
        if cur:
            t0 = out0 + off + (cstart - lo)
            t1 = out0 + off + (b - a)
            events.append((t0, t1, ' '.join(cur)))
        off += b - a

lines = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "WrapStyle: 2", "",
         "[V4+ Styles]",
         "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
         "Style: Legenda,Liberation Sans,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,3,2.2,2,55,55,215,1",
         "", "[Events]",
         "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
prev_end = 0.0
for a, b, txt in events:
    a = max(a, prev_end + 0.01)
    if b <= a:
        continue
    prev_end = b
    lines.append(f"Dialogue: 0,{ts(a)},{ts(b)},Legenda,,0,0,0,,{txt}")
open('final/legendas.ass', 'w').write('\n'.join(lines) + '\n')
print('legendas:', len(events))
json.dump(starts, open('final/starts.json', 'w'), indent=1)
