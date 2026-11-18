#!/usr/bin/env python3
"""
Gera a imagem de compartilhamento (og-image.jpg, 1200x630) e os ícones
(apple-touch-icon.png 180px e favicon-32.png) no estilo do site.

O rosto fica no centro porque a miniatura quadrada do WhatsApp corta o meio.

Fontes usadas: Young Serif (títulos) e Instrument Sans (apoio). Se não
encontrar os arquivos .ttf nos caminhos abaixo, ajuste FONTES.
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont, ImageOps

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent

GIZ = (255, 253, 251)
LARANJA = (245, 145, 23)
AMEIXA = (58, 30, 46)
DAMASCO = (253, 227, 196)
ARGILA = (201, 114, 122)
ROSA = (232, 185, 160)
COBRE = (154, 82, 7)
SUAVE = (106, 86, 94)

FONTES = pathlib.Path("/mnt/skills/examples/canvas-design/canvas-fonts")
SERIF = FONTES / "YoungSerif-Regular.ttf"
SANS = FONTES / "InstrumentSans-Regular.ttf"
SANS_B = FONTES / "InstrumentSans-Bold.ttf"

NOME_1, NOME_2 = "Camila", "M. S. Bagli"
FRASE = ["Hipnose clínica,", "Constelação Sistêmica", "e Barras de Access"]
CIDADE = ["Ribas do Rio Pardo/MS", "e online"]
SELO = "Agende pelo WhatsApp"

S = 2  # superamostragem para bordas suaves


def og():
    W, H = 1200 * S, 630 * S
    im = Image.new("RGB", (W, H), GIZ)
    d = ImageDraw.Draw(im)

    # mesa
    d.ellipse([300 * S, 470 * S, 900 * S, 700 * S], fill=DAMASCO)

    # retrato redondo no centro
    diam = 400 * S
    foto = Image.open(AQUI / "fotos" / "hero.jpg").convert("RGB")
    foto = ImageOps.fit(foto, (diam, diam), Image.LANCZOS, centering=(0.5, 0.45))
    mascara = Image.new("L", (diam, diam), 0)
    ImageDraw.Draw(mascara).ellipse([0, 0, diam - 1, diam - 1], fill=255)
    cx, cy = 600 * S, 290 * S
    d.ellipse([cx - diam // 2 - 12 * S, cy - diam // 2 - 12 * S, cx + diam // 2 + 12 * S, cy + diam // 2 + 12 * S], fill=GIZ)
    im.paste(foto, (cx - diam // 2, cy - diam // 2), mascara)


    serif = ImageFont.truetype(str(SERIF), 50 * S)
    sans = ImageFont.truetype(str(SANS), 25 * S)
    sans_b = ImageFont.truetype(str(SANS_B), 24 * S)

    # esquerda: nome e frase
    x = 60 * S
    d.text((x, 150 * S), NOME_1, font=serif, fill=AMEIXA)
    d.text((x, 210 * S), NOME_2, font=serif, fill=AMEIXA)
    y = 300 * S
    for linha in FRASE:
        d.text((x, y), linha, font=sans, fill=SUAVE)
        y += 36 * S

    # direita: cidade e selo
    xr = 1140 * S
    y = 190 * S
    for linha in CIDADE:
        w = d.textlength(linha, font=sans)
        d.text((xr - w, y), linha, font=sans, fill=SUAVE)
        y += 36 * S
    w = d.textlength(SELO, font=sans_b)
    px, py = 26 * S, 18 * S
    caixa = [xr - w - 2 * px, 300 * S, xr, 300 * S + 30 * S + 2 * py]
    r = 14 * S
    d.rounded_rectangle(caixa, radius=r, fill=LARANJA)
    d.rounded_rectangle([caixa[2] - 2 * r - 20 * S, caixa[3] - 2 * r - 20 * S, caixa[2], caixa[3]], radius=r + 16 * S, fill=LARANJA)
    d.text((caixa[0] + px, caixa[1] + py + 2 * S), SELO, font=sans_b, fill=AMEIXA)

    im = im.resize((1200, 630), Image.LANCZOS)
    im.save(RAIZ / "og-image.jpg", "JPEG", quality=86, optimize=True, progressive=True)


def icone(tam, nome):
    """Monograma C em laranja sobre ameixa."""
    T = tam * 4
    im = Image.new("RGB", (T, T), AMEIXA)
    d = ImageDraw.Draw(im)
    fonte = ImageFont.truetype(str(SERIF), int(T * 0.74))
    caixa = d.textbbox((0, 0), "C", font=fonte)
    w, h = caixa[2] - caixa[0], caixa[3] - caixa[1]
    d.text(((T - w) / 2 - caixa[0], (T - h) / 2 - caixa[1]), "C", font=fonte, fill=LARANJA)
    im = im.resize((tam, tam), Image.LANCZOS)
    im.save(RAIZ / nome, "PNG", optimize=True)


if __name__ == "__main__":
    og()
    icone(180, "apple-touch-icon.png")
    icone(32, "favicon-32.png")
    print("og-image.jpg, apple-touch-icon.png e favicon-32.png gerados")
