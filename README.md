🐺 Wolf Adventure: Roguelike
Wolf Adventure é um jogo de exploração e combate no estilo Roguelike, desenvolvido inteiramente em Python utilizando a biblioteca Pygame Zero. O projeto foca em movimentação precisa baseada em grade, animações fluidas e uma mecânica de combate estratégica.

🎮 Sobre o Jogo
Neste desafio, você controla um lobo guerreiro que deve limpar masmorras infestadas de inimigos. A cada nível superado, os perigos aumentam, exigindo precisão no tempo de ataque e movimentação para sobreviver.

🛠 Mecânicas Principais
Movimentação por Grade (Grid-Based): Sistema de movimento suave entre células, respeitando as colisões do cenário.

Combate com Machado: O herói possui uma área de ataque (hitbox) ampliada que atinge tanto a sua posição atual quanto a célula à frente.

Progressão de Dificuldade: A cada fase, o número de inimigos aumenta e o mapa é renovado.

Sistema de Cura: Ao limpar um nível, o herói recupera +1 ponto de vida como recompensa.

Inteligência Artificial: Inimigos possuem comportamento de perseguição e movimentação autônoma pelo mapa.

🕹 Controles
Movimentação: Teclas W, A, S, D ou Setas do teclado.

Ataque: Barra de Espaço.

Menu: Navegação por mouse com botões interativos.

🚀 Requisitos Técnicos Atendidos
Este projeto foi desenvolvido seguindo diretrizes rígidas de programação:

Código Limpo: Nomes de variáveis e funções em inglês, seguindo o padrão PEP8.

Sem Dependências Externas: Construído apenas com pgzero, math e random.

Animação de Sprites: Personagens possuem ciclos de animação contínuos (idle/walk), garantindo vivacidade ao ambiente.

Gestão de Estados: Sistema robusto para alternar entre Menu, Instruções, Jogo e Game Over.

Como Rodar
Certifique-se de ter o Python instalado.

Instale o Pygame Zero: pip install pgzero.

Execute o jogo: pgzrun main.py.
