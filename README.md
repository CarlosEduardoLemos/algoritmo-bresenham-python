# Peca cotada com OpenGL e Bresenham

Este projeto desenha uma peca tecnica cotada em uma janela OpenGL, usando Python. A figura foi montada a partir das medidas da imagem de referencia, considerando o ponto vermelho como a origem `(0, 0)`.

O programa exibe:

- o contorno da peca;
- o preenchimento interno em cor clara;
- as linhas de cota e extensao;
- os textos com as medidas;
- o ponto de origem em vermelho.

## Requisitos

Para executar o codigo, e necessario ter Python instalado e instalar as bibliotecas do OpenGL:

```bash
pip install PyOpenGL PyOpenGL_accelerate
```

## Como executar

No terminal, dentro da pasta do projeto, execute:

```bash
python bresenham_figura.py
```

Ao rodar o arquivo, sera aberta uma janela chamada **Peca cotada com Bresenham**, mostrando a peca desenhada com suas respectivas cotas.

## Como o codigo funciona

O arquivo `bresenham_figura.py` usa a biblioteca `PyOpenGL` para abrir uma janela grafica e desenhar a figura. As coordenadas principais da peca ficam na lista `PIECE_POINTS`, que representa os vertices do contorno com base nas medidas da imagem original.

A funcao `to_screen()` converte as coordenadas da peca para coordenadas da tela, aplicando escala e deslocamento. Isso permite trabalhar com as medidas da imagem e depois posicionar tudo corretamente na janela.

As linhas sao desenhadas com o algoritmo de **Bresenham**, implementado na funcao `bresenham()`. Esse algoritmo calcula quais pixels devem ser marcados para formar uma linha entre dois pontos, evitando depender diretamente de comandos prontos de linha do OpenGL.

O preenchimento da peca e feito em `draw_piece_fill()`, usando uma varredura horizontal: para cada linha da tela, o codigo encontra as intersecoes com o poligono e preenche os intervalos internos.

As funcoes `horizontal_dimension()`, `vertical_dimension()`, `draw_arrow()` e `draw_dimension_text()` desenham as cotas, setas e textos das medidas. Por fim, a funcao `display()` organiza a ordem do desenho: preenchimento, linhas auxiliares, cotas, contorno e ponto de origem.

## Arquivos

- `bresenham_figura.py`: codigo principal do desenho.
- `imagens/Resultado Solicitado.jpg`: imagem usada como referencia.
- `imagens/Resultado do Código.png`: exemplo do resultado gerado.
