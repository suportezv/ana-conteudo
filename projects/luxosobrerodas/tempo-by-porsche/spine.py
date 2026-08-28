"""Espinha editorial da entrevista Tempo by Porsche: refina cortes por palavra e
extrai os segmentos de áudio ORIGINAL para isolamento de voz."""
import json, subprocess, os

BASE = '/tmp/claude-0/-home-user-ana-conteudo/d3f9a2e0-ccad-5a5c-9543-94e17805d096/scratchpad/uol2'
os.chdir(BASE)
os.makedirs('audio/seg', exist_ok=True)
d = json.load(open('edit/transcripts/entrevista_limpa.json'))
words = [w for w in d['words'] if w['type'] == 'word']

def bound(t_start, t_end, pad_in=0.18, pad_out=0.30):
    """Ajusta para fronteiras reais de palavra dentro da janela dada."""
    ws = [w for w in words if w['start'] >= t_start - 0.4 and w['end'] <= t_end + 0.4]
    if not ws:
        return round(t_start, 2), round(t_end, 2)
    return round(max(0, ws[0]['start'] - pad_in), 2), round(ws[-1]['end'] + pad_out, 2)

# blocos: (nome, início, fim aproximados; refinados por palavra)
BLOCKS = [
    ('s01_hook',      212.10, 217.60),
    ('s02_apres',      42.10, 46.60),
    ('s03_artecarro',  52.80, 62.50),
    ('s04_15anos',     80.10, 89.10),
    ('s05_origem',    125.00, 139.20),
    ('s06_euvou',     165.50, 184.50),
    ('s07_cafe',      186.60, 199.40),
    ('s08_proposta',  218.30, 233.50),
    ('s09_pessoas',   281.40, 289.60),
    ('s10_carroRS',   354.80, 390.40),
    ('s11_conexao',   480.80, 498.30),
    ('s12_eventos',   524.50, 534.20),
    ('s13_mural',     538.80, 552.40),
    ('s14_endereco',  667.90, 678.90),
    ('s15_fecho',     738.60, 744.60),
    ('s16_fecho2',    751.60, 756.00),
]
total = 0
plan = []
for name, a, b in BLOCKS:
    a2, b2 = bound(a, b)
    plan.append((name, a2, b2))
    total += b2 - a2
    print(f"{name}: {a2:7.2f}-{b2:7.2f}  ({b2-a2:5.2f}s)")
print('TOTAL fala:', round(total, 1), 's')
json.dump(plan, open('spine.json', 'w'))

# extrai áudio ORIGINAL (proxy tem o áudio da câmera intacto) por bloco para isolar
for name, a, b in plan:
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(a), '-i', 'proxies/entrevista_4399.mp4',
                    '-t', str(round(b - a, 2)), '-vn', '-c:a', 'libmp3lame', '-q:a', '2',
                    f'audio/seg/{name}.mp3'], check=True)
print('segmentos extraídos')
