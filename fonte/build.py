#!/usr/bin/env python3
"""
Gera o index.html autocontido do site da Camila M. S. Bagli.

Como usar:
    python3 build.py

Para atualizar dados, edite o bloco DADOS abaixo e rode de novo.
Para trocar fotos, substitua os arquivos em fotos/ (hero.jpg, sobre.jpg,
consultorio.jpg) e rode de novo. Para regerar a imagem de compartilhamento
e os ícones, rode gerar_imagens.py.
"""
import base64
import datetime
import io
import json
import pathlib
import urllib.parse

from PIL import Image

# ------------------------------------------------------------------
# DADOS DA PROFISSIONAL (edite aqui)
# ------------------------------------------------------------------
DADOS = {
    "NOME": "Camila M. S. Bagli",
    "PRIMEIRO_NOME": "Camila",
    "PROFISSAO": "Fisioterapeuta e Terapeuta Integrativa",
    # Texto curto que aparece embaixo do nome no cabeçalho
    "AREA_CABECALHO": "Terapeuta Integrativa",
    # Só números, com DDI e DDD
    "WHATSAPP": "5567996913697",
    "INSTAGRAM_URL": "https://www.instagram.com/camilamirandabagli/",
    "CIDADE_UF": "Ribas do Rio Pardo/MS",
    "LOCAL_NOME": "Saúde & Cia",
    "ENDERECO_RUA": "R. Júlio Lorenzoni, 122, Sala 03",
    "ENDERECO_BAIRRO": "Santos Dummont",
    "ENDERECO_CEP": "79180-000",
    # Número do CREFITO. Vazio: a linha não aparece no site. Preenchido: aparece no rodapé.
    "CREFITO": "",
}

# Endereço onde o site está publicado (sem barra no final).
# Ao trocar pelo domínio definitivo, rode build.py de novo e suba os arquivos.
DOMINIO = "https://insticamilabagli.vercel.app"

# Depoimentos: o Código de Ética do COFFITO (Res. 424/2013, art. 10, V)
# veda o uso de mensagens de pacientes na divulgação. Por isso o site
# não tem seção de depoimentos.

MSG_AGENDAR = "Olá, {nome}! Vim pelo site e gostaria de agendar uma consulta de avaliação."
MSG_DUVIDA = "Olá, {nome}! Vim pelo site e tenho uma dúvida antes de agendar."

# ------------------------------------------------------------------
AQUI = pathlib.Path(__file__).resolve().parent
SAIDA = AQUI.parent / "index.html"


def foto_base64(nome, largura_max=1000, qualidade=80):
    im = Image.open(AQUI / "fotos" / nome).convert("RGB")
    if im.width > largura_max:
        im = im.resize((largura_max, round(im.height * largura_max / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=qualidade, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def wa(msg):
    return "https://wa.me/" + DADOS["WHATSAPP"] + "?text=" + urllib.parse.quote(msg.format(nome=DADOS["PRIMEIRO_NOME"]))


def main():
    d = dict(DADOS)
    d["DOMINIO"] = DOMINIO
    d["TITULO"] = f'{d["NOME"]} | {d["PROFISSAO"]}'
    d["DESCRICAO"] = (
        f'{d["NOME"]}, fisioterapeuta e terapeuta integrativa em {d["CIDADE_UF"]} e online: '
        "hipnose clínica, Constelação Sistêmica e Barras de Access."
    )
    # A linha do CREFITO só aparece no rodapé quando o número estiver preenchido.
    d["CREFITO_TEXTO"] = f'<br>CREFITO-13: {d["CREFITO"]}' if d["CREFITO"] else ""
    d["ANO"] = str(datetime.date.today().year)
    d["WA_AGENDAR"] = wa(MSG_AGENDAR)
    d["WA_DUVIDA"] = wa(MSG_DUVIDA)
    endereco_completo = f'{d["ENDERECO_RUA"]}, {d["ENDERECO_BAIRRO"]}, {d["CIDADE_UF"].replace("/", " - ")}, {d["ENDERECO_CEP"]}'
    d["MAPS_URL"] = "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(f'{d["LOCAL_NOME"]}, {endereco_completo}')

    cidade, uf = d["CIDADE_UF"].split("/")
    jsonld = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": d["NOME"],
        "description": d["DESCRICAO"],
        "url": DOMINIO + "/",
        "image": DOMINIO + "/og-image.jpg?v=2",
        "telephone": "+" + d["WHATSAPP"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": f'{d["ENDERECO_RUA"]}, {d["ENDERECO_BAIRRO"]}',
            "addressLocality": cidade,
            "addressRegion": uf,
            "postalCode": d["ENDERECO_CEP"],
            "addressCountry": "BR",
        },
        "areaServed": [cidade + "/" + uf, "Atendimento online"],
        "sameAs": [d["INSTAGRAM_URL"]],
        "founder": {"@type": "Person", "name": d["NOME"], "jobTitle": d["PROFISSAO"]},
    }
    d["JSONLD"] = json.dumps(jsonld, ensure_ascii=False)

    d["FOTO_HERO"] = foto_base64("hero.jpg", 900, 82)
    d["FOTO_SOBRE"] = foto_base64("sobre.jpg", 800, 80)
    d["FOTO_LOCAL"] = foto_base64("consultorio.jpg", 900, 80)

    html = (AQUI / "template.html").read_text(encoding="utf-8")
    for chave, valor in d.items():
        html = html.replace("{{" + chave + "}}", valor)
    sobrou = [p for p in html.split("{{")[1:]]
    if sobrou:
        raise SystemExit("Marcadores sem valor: " + ", ".join(p.split("}}")[0] for p in sobrou))
    SAIDA.write_text(html, encoding="utf-8")
    print(f"index.html gerado ({SAIDA.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
