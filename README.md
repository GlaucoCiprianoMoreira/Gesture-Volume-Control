# Volume Gesture Control

## Visão Geral:
  * Este é um projeto de Visão Computacional que permite controlar o volume principal do sistema operacional (Windows) utilizando apenas gestos com as mãos, capturados em tempo real através da sua webcam.

---

## Objetivo principal do projeto:
  * **Estudo**: aprender a usar bibliotecas de visão computacional como `OpenCV` e `Mediapipe`
  * **Explicação:** O sistema utiliza inteligência artificial para rastrear os pontos de articulação da sua mão. Ao calcular a distância entre a ponta do seu dedo polegar e a ponta do dedo indicador, o programa ajusta dinamicamente o volume do computador. 
  * **Por que é útil:** Oferece uma interface *touchless* (sem toque). É extremamente útil para momentos em que você não pode tocar no teclado ou mouse (como quando está cozinhando ou com as mãos sujas), atua como uma ferramenta de acessibilidade e demonstra uma aplicação prática e interativa de IA para o dia a dia.

---

## Project Concepts:
  * **Visão Computacional e Rastreamento:** Utiliza a biblioteca **OpenCV** para a manipulação da câmera corporativa e a moderna API de *Tasks Vision* do **MediaPipe** para o rastreamento dos marcos (landmarks) da mão.
  * **Controle de Áudio:** A biblioteca **Pycaw** atua como a ponte de comunicação direta com a interface de áudio do Windows.
  * **Matemática Aplicada (A Mecânica):** O algoritmo localiza 21 pontos (nós) na sua mão. A lógica principal aplica o cálculo da hipotenusa (distância euclidiana) entre as coordenadas `(x, y)` do Nó 4 (Polegar) e do Nó 8 (Indicador). 
  * **Interpolação:** A variação do comprimento em pixels (geralmente entre 50 e 300) é mapeada para a faixa de decibéis do sistema operacional usando a função `interp` da biblioteca `numpy`.

---

## How to play:
  * O projeto foi desenvolvido e testado utilizando Python 3.11
  * Importante: A nova API do MediaPipe exige o arquivo de modelo pré-treinado (hand_landmarker.task). Certifique-se de que ele esteja na mesma pasta dos scripts
  * Abra o seu terminal e clone o repositório: `git clone https://github.com/GlaucoCiprianoMoreira/Gesture-Volume-Control.git`
  * Já com o projeto aberto no VS Code, instale todas as dependências necessárias executando: `pip install opencv-python mediapipe numpy pycaw comtypes`
  * Dê "play" no jogo/ferramenta executando o script principal: `python VolumeHandControl.py`
