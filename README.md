# 🐺 Wolf Adventure: Roguelike

**Wolf Adventure** é um jogo de exploração e combate desenvolvido inteiramente em **Python** utilizando a biblioteca **Pygame Zero**. O projeto foca em movimentação precisa baseada em grade, animações fluidas e mecânicas estratégicas.



## 🎮 Sobre o Jogo
Controle um lobo guerreiro em masmorras perigosas. A cada nível superado, a dificuldade aumenta, exigindo precisão e estratégia para sobreviver.

## 🛠 Mecânicas Principais
* **Movimentação por Grade:** Sistema suave entre células com detecção de colisão.
* **Combate com Machado:** Hitbox ampliada que atinge a célula atual e a célula à frente.
* **Progressão:** Aumento gradual de inimigos e renovação de mapas.
* **Sistema de Cura:** O herói recupera **+1 HP** ao limpar cada nível.
* **IA de Inimigos:** Comportamento de perseguição e patrulha autônoma.



## 🕹 Controles
* **Movimentação:** `W`, `A`, `S`, `D` ou `Setas`.
* **Ataque:** `Espaço`.
* **Menu:** Navegação por `Mouse`.

## 🚀 Requisitos Técnicos Atendidos
* **Código Limpo:** Nomenclatura em inglês seguindo o padrão **PEP8**.
* **Dependências:** Uso exclusivo de `pgzero`, `math` e `random`.
* **Animação de Sprites:** Ciclos contínuos (Idle/Walk) para todos os personagens.
* **Gestão de Estados:** Sistema para Menu, Instruções, Jogo e Game Over.

## 💻 Como Rodar
1. Certifique-se de ter o **Python** instalado.
2. Instale o Pygame Zero: 
   ```bash
   pip install pgzero
   pgzrun main.py
