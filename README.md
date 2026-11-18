# Site de Camila M. S. Bagli

Site institucional de uma página: Fisioterapeuta e Terapeuta Integrativa, Ribas do Rio Pardo/MS e online.

## Arquivos

- `index.html`: o site pronto, com CSS, JavaScript e fotos embutidos. É o arquivo que vai para a hospedagem.
- `og-image.jpg`: imagem que aparece ao compartilhar o link (WhatsApp, Instagram, Facebook).
- `apple-touch-icon.png` e `favicon-32.png`: ícones do site.
- `fonte/`: tudo o que gera o site.
  - `template.html`: estrutura, textos e estilo.
  - `build.py`: dados da profissional (nome, WhatsApp, endereço, CREFITO, domínio) e geração do `index.html`.
  - `gerar_imagens.py`: gera a imagem de compartilhamento e os ícones.
  - `fotos/`: fotos usadas no site.

## Como atualizar

1. Dados (CREFITO, WhatsApp, endereço, domínio): edite o bloco `DADOS` e a constante `DOMINIO` no topo de `fonte/build.py`.
2. Fotos: troque `fonte/fotos/hero.jpg`, `sobre.jpg` ou `consultorio.jpg` mantendo o nome.
3. Rode:

```
cd fonte
python3 gerar_imagens.py
python3 build.py
```

4. Suba para a hospedagem os quatro arquivos da raiz: `index.html`, `og-image.jpg`, `apple-touch-icon.png` e `favicon-32.png`.

Quando trocar a imagem de compartilhamento, mude `?v=1` para `?v=2` no `template.html` para o WhatsApp buscar a versão nova.

Requisitos: Python 3 com Pillow (`pip install pillow`).
