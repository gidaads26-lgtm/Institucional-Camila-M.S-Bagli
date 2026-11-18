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
CIDADE = ["Ribas do Rio Pardo/MS", "Presencial e online"]
SELO = "Agende pelo WhatsApp"

S = 2  # superamostragem para bordas suaves


def texto_espacado(d, xy, texto, fonte, cor, espaco):
    x, y = xy
    for ch in texto:
        d.text((x, y), ch, font=fonte, fill=cor)
        x += d.textlength(ch, font=fonte) + espaco
    return x


def largura_espacada(d, texto, fonte, espaco):
    return sum(d.textlength(ch, font=fonte) + espaco for ch in texto) - espaco


def fonte_que_cabe(caminho, texto, tam, largura_max, d):
    while tam > 10:
        f = ImageFont.truetype(str(caminho), tam)
        if d.textlength(texto, font=f) <= largura_max:
            return f
        tam -= 1
    return ImageFont.truetype(str(caminho), tam)


def og():
    """Fundo ameixa, retrato no centro (a miniatura quadrada do WhatsApp corta o meio)."""
    W, H = 1200 * S, 630 * S
    im = Image.new("RGB", (W, H), AMEIXA)
    d = ImageDraw.Draw(im)

    # retrato redondo com anel laranja
    diam = 420 * S
    cx, cy = 600 * S, 300 * S
    anel = 9 * S
    folga = 9 * S
    d.ellipse([cx - diam // 2 - folga - anel, cy - diam // 2 - folga - anel, cx + diam // 2 + folga + anel, cy + diam // 2 + folga + anel], fill=LARANJA)
    d.ellipse([cx - diam // 2 - folga, cy - diam // 2 - folga, cx + diam // 2 + folga, cy + diam // 2 + folga], fill=AMEIXA)
    foto = Image.open(AQUI / "fotos" / "hero.jpg").convert("RGB")
    foto = ImageOps.fit(foto, (diam, diam), Image.LANCZOS, centering=(0.5, 0.42))
    mascara = Image.new("L", (diam, diam), 0)
    ImageDraw.Draw(mascara).ellipse([0, 0, diam - 1, diam - 1], fill=255)
    im.paste(foto, (cx - diam // 2, cy - diam // 2), mascara)

    esquerda_max = (cx - diam // 2 - folga - anel) - 64 * S - 30 * S
    x = 64 * S

    # esquerda: rotulo, nome e tecnicas
    rot = ImageFont.truetype(str(SANS_B), 17 * S)
    d.ellipse([x, 170 * S, x + 9 * S, 179 * S], fill=LARANJA)
    texto_espacado(d, (x + 22 * S, 163 * S), "TERAPEUTA INTEGRATIVA", rot, LARANJA, 3.2 * S)
    nome = fonte_que_cabe(SERIF, NOME_2, 60 * S, esquerda_max, d)
    d.text((x, 205 * S), NOME_1, font=nome, fill=DAMASCO)
    d.text((x, 275 * S), NOME_2, font=nome, fill=DAMASCO)
    sans = ImageFont.truetype(str(SANS), 23 * S)
    y = 375 * S
    for linha in FRASE:
        d.text((x, y), linha, font=sans, fill=(217, 195, 184))
        y += 34 * S

    # direita: cidade e selo do WhatsApp
    xr = 1140 * S
    direita_min = cx + diam // 2 + folga + anel + 30 * S
    larg = xr - direita_min
    cid = ImageFont.truetype(str(SANS), 23 * S)
    y = 205 * S
    for i, linha in enumerate(CIDADE):
        w = d.textlength(linha, font=cid)
        d.text((xr - w, y), linha, font=cid, fill=DAMASCO if i == 0 else (217, 195, 184))
        y += 34 * S
    selo = fonte_que_cabe(SANS_B, SELO, 23 * S, larg - 48 * S, d)
    w = d.textlength(SELO, font=selo)
    px, py = 24 * S, 20 * S
    topo = 300 * S
    caixa = [xr - w - 2 * px, topo, xr, topo + 28 * S + 2 * py]
    r = 12 * S
    d.rounded_rectangle(caixa, radius=r, fill=LARANJA)
    # canto inferior direito bem arredondado, a assinatura do site
    d.rectangle([caixa[2] - 40 * S, caixa[3] - 40 * S, caixa[2], caixa[3]], fill=AMEIXA)
    d.pieslice([caixa[2] - 80 * S, caixa[3] - 80 * S, caixa[2], caixa[3]], 0, 90, fill=LARANJA)
    d.rectangle([caixa[2] - 40 * S, caixa[3] - 40 * S, caixa[2] - 0, caixa[3] - 40 * S + 1], fill=LARANJA)
    d.text((caixa[0] + px, caixa[1] + py + 1 * S), SELO, font=selo, fill=AMEIXA)

    im = im.resize((1200, 630), Image.LANCZOS)
    im.save(RAIZ / "og-image.jpg", "JPEG", quality=85, optimize=True, progressive=True)


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
