"""Gera PNGs de motion/lettering 1080x1920 para o edit de Interlagos.

Uso: python3 motion.py  (gera todos em motion/)
Estilo: condensed caps branco com sombra dura, acento amarelo #FFE234,
barras diagonais estilo racing.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1920
FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
YELLOW = (255, 226, 52, 255)
WHITE = (255, 255, 255, 255)
BLACK = (10, 10, 10, 255)
SHADOW = (0, 0, 0, 220)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "motion")
os.makedirs(OUT, exist_ok=True)


def fit(draw, s, size, max_w):
    f = ImageFont.truetype(FONT, size)
    while draw.textbbox((0, 0), s, font=f)[2] > max_w and size > 20:
        size -= 4
        f = ImageFont.truetype(FONT, size)
    return f


def shadowed(d, xy, s, f, fill, off=(6, 8)):
    d.text((xy[0] + off[0], xy[1] + off[1]), s, font=f, fill=SHADOW)
    d.text(xy, s, font=f, fill=fill)


def condensed(img):
    """Aperta horizontalmente (fake condensed 80%)."""
    w, h = img.size
    return img.resize((int(w * 0.82), h), Image.LANCZOS)


def title_card(name, line_main, line_sub=None, accent_word=None):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # barras diagonais racing no canto superior esquerdo
    for i, c in enumerate([YELLOW, WHITE, YELLOW]):
        x0 = 60 + i * 54
        d.polygon([(x0, 320), (x0 + 30, 320), (x0 - 40, 470), (x0 - 70, 470)], fill=c)

    f_main = fit(d, line_main, 190, W - 120)
    # renderiza numa camada própria para condensar
    tw = d.textbbox((0, 0), line_main, font=f_main)
    layer = Image.new("RGBA", (tw[2] + 20, tw[3] + 30), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    shadowed(ld, (4, 4), line_main, f_main, WHITE)
    layer = condensed(layer)
    img.alpha_composite(layer, ((W - layer.width) // 2, 520))

    y = 520 + layer.height + 30
    if line_sub:
        f_sub = fit(d, line_sub, 64, W - 200)
        tw = d.textbbox((0, 0), line_sub, font=f_sub)
        # faixa amarela atrás do subtítulo
        pad = 18
        bw, bh = tw[2] + pad * 2, tw[3] + pad
        bar = Image.new("RGBA", (bw, bh + 14), (0, 0, 0, 0))
        bd = ImageDraw.Draw(bar)
        bd.polygon([(10, 0), (bw, 0), (bw - 10, bh), (0, bh)], fill=YELLOW)
        bd.text((pad, pad // 2 - 4), line_sub, font=f_sub, fill=BLACK)
        img.alpha_composite(bar, ((W - bw) // 2, y))
    img.save(os.path.join(OUT, name))
    print("ok", name)


def impact_phrase(name, text, y_center=1300, size=110):
    """Lettering de frase de impacto: branco condensado + palavra(s) em amarelo entre *asteriscos*."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    lines = text.split("\n")
    f = None
    for ln in lines:
        cand = fit(d, ln.replace("*", ""), size, W - 140)
        if f is None or cand.size < f.size:
            f = cand
    total_h = 0
    rendered = []
    for ln in lines:
        parts = ln.split("*")  # ímpares = amarelo
        widths = [d.textbbox((0, 0), p, font=f)[2] for p in parts]
        lw = sum(widths)
        lh = d.textbbox((0, 0), ln.replace("*", "") or "X", font=f)[3]
        layer = Image.new("RGBA", (lw + 24, lh + 34), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        x = 4
        for i, p in enumerate(parts):
            if not p:
                continue
            shadowed(ld, (x, 4), p, f, YELLOW if i % 2 else WHITE)
            x += widths[i]
        layer = condensed(layer)
        rendered.append(layer)
        total_h += layer.height + 6
    y = int(y_center - total_h / 2)
    for layer in rendered:
        img.alpha_composite(layer, ((W - layer.width) // 2, y))
        y += layer.height + 6
    img.save(os.path.join(OUT, name))
    print("ok", name)


if __name__ == "__main__":
    title_card("titulo_interlagos.png", "INTERLAGOS", "AUTÓDROMO • SÃO PAULO")
    impact_phrase("outro_eita.png", "DIA DE *PISTA*", y_center=960, size=150)
