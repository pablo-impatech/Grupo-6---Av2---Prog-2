import os
import random
import pygame
import time
import matplotlib.pyplot as plt
import agents as agent

# Inicialização do Pygame
pygame.init()

size_of_w = pygame.display.get_desktop_sizes()
tela_x = size_of_w[0][0]
tela_y = size_of_w[0][1]

TREE_ALIVE_IMG = pygame.image.load(os.path.join("images", "Tree_Small.png"))
TREE_BURNING_IMG = pygame.image.load(os.path.join("images", "Fire_Small.png"))
WATER_IMG = pygame.image.load(os.path.join("images", "pixil-frame-0 (2).png"))
START_IMG = pygame.image.load(os.path.join("images", "shadedDark42.png"))
TREE_BURNED_IMG = pygame.image.load(os.path.join("images", "pixil-frame-0 (4).png"))
BUTTOM_UP_IMG = pygame.image.load(os.path.join("images", "shadedDark03.png"))
BUTTOM_LEFT_IMG = pygame.image.load(os.path.join("images", "shadedDark05.png"))
BUTTOM_DOWN_IMG = pygame.image.load(os.path.join("images", "shadedDark10.png"))
BUTTOM_RIGHT_IMG = pygame.image.load(os.path.join("images", "shadedDark06.png"))
BUTTOM_X_IMG = pygame.image.load(os.path.join("images", "shadedDark35.png"))
BUTTOM_PAUSE_IMG = pygame.image.load(os.path.join("images", "shadedDark44.png"))
FIREMAN_IMG = pygame.image.load(os.path.join("images", "pixil-frame-0 (5).png"))
FIREMAN_BURNING2_IMG = pygame.image.load(
    os.path.join("images", "pixil-frame-0 (8).png")
)
FIREMAN_BURNING1_IMG = pygame.image.load(
    os.path.join("images", "pixil-frame-0 (9).png")
)

cell_size = tela_x // 50
TREE_ALIVE_IMG = pygame.transform.scale(TREE_ALIVE_IMG, (cell_size, cell_size))
TREE_BURNING_IMG = pygame.transform.scale(TREE_BURNING_IMG, (cell_size, cell_size))
WATER_IMG = pygame.transform.scale(WATER_IMG, (cell_size, cell_size))
TREE_BURNED_IMG = pygame.transform.scale(TREE_BURNED_IMG, (cell_size, cell_size))
BUTTOM_UP_IMG = pygame.transform.scale(
    BUTTOM_UP_IMG, (1.5 * cell_size, 1.5 * cell_size)
)
BUTTOM_LEFT_IMG = pygame.transform.scale(
    BUTTOM_LEFT_IMG, (1.5 * cell_size, 1.5 * cell_size)
)
BUTTOM_DOWN_IMG = pygame.transform.scale(
    BUTTOM_DOWN_IMG, (1.5 * cell_size, 1.5 * cell_size)
)
BUTTOM_RIGHT_IMG = pygame.transform.scale(
    BUTTOM_RIGHT_IMG, (1.5 * cell_size, 1.5 * cell_size)
)
BUTTOM_X_IMG = pygame.transform.scale(BUTTOM_X_IMG, (1.5 * cell_size, 1.5 * cell_size))
FIREMAN_IMG = pygame.transform.scale(FIREMAN_IMG, (1.5 * cell_size, 1.5 * cell_size))
FIREMAN_BURNING1_IMG = pygame.transform.scale(
    FIREMAN_BURNING1_IMG, (1.5 * cell_size, 1.5 * cell_size)
)
FIREMAN_BURNING2_IMG = pygame.transform.scale(
    FIREMAN_BURNING2_IMG, (1.5 * cell_size, 1.5 * cell_size)
)


class Forest:
    def __init__(self, matriz):
        self.matriz = matriz
        self.n = len(matriz)
        self.m = len(matriz[0])
        self.vent = agent.vento()

    def incendio(self):
        for i in range(5):
            k = random.randint(0, self.n - 1)
            l = random.randint(0, self.m - 1)
            if (
                isinstance(self.matriz[k][l], agent.Tree)
                and self.matriz[k][l].condition == "alive"
            ):
                self.matriz[k][l].attempt_to_burn(self.matriz, self.vent)
                break

    def update_forest(self):
        for row in self.matriz:
            for cell in row:
                if isinstance(cell, agent.Tree):
                    cell.update_condition(self)

    def extinguish_tree_at(self, x, y):
        col, row = x // cell_size, y // cell_size
        if 0 <= row < self.n and 0 <= col < self.m:
            cell = self.matriz[row][col]
            if isinstance(cell, agent.Tree):
                cell.extinguish_fire()

    def surge_trees(self):
        for i in range(self.n):
            for j in range(self.m):
                if self.matriz[i][j] == "v":
                    a = random.randint(1, 100)
                    if a == 1:
                        self.matriz[i][j] = agent.Tree((i, j))

    def tree_f_pos(self, coord):
        self.matriz[coord[0]][coord[1]] == agent.Tree((coord[0], coord[1]))


def draw_forest(screen, forest):

    for i in range(forest.n):
        for j in range(forest.m):
            cell = forest.matriz[i][j]
            if isinstance(cell, agent.Tree):
                if cell.condition == "alive":
                    screen.blit(TREE_ALIVE_IMG, (j * cell_size, i * cell_size))
                elif cell.condition == "burning":
                    screen.blit(TREE_BURNING_IMG, (j * cell_size, i * cell_size))
                elif cell.condition == "burned":
                    screen.blit(TREE_BURNED_IMG, (j * cell_size, i * cell_size))
            elif isinstance(cell, agent.Barrier):
                screen.blit(WATER_IMG, (j * cell_size, i * cell_size))
            if cell == "v":
                pygame.draw.rect(
                    screen,
                    (95, 107, 47),
                    (j * cell_size, i * cell_size, cell_size, cell_size),
                )
            if cell == "black":
                pygame.draw.rect(
                    screen,
                    (105, 107, 47),
                    (j * cell_size, i * cell_size, cell_size, cell_size),
                )


def main():

    size_of_w = pygame.display.get_desktop_sizes()
    tela_x = size_of_w[0][0]
    tela_y = size_of_w[0][1]

    def init_screen():
        screen = pygame.display.set_mode((tela_x, tela_y))
        matriz = [
            [agent.Tree((i, j)) for j in range(tela_x // cell_size)]
            for i in range((tela_y // cell_size))
        ]

        for i in range((tela_x) // int(0.002 * tela_x * cell_size)):
            for j in range(tela_y // cell_size):
                matriz[j][i] = "black"

        matriz[15][38] = agent.Barrier((23, 78))

        return matriz, screen

    matriz, screen = init_screen()

    def draw_bombeiros(lista_bombeiros):
        for bombeiro in lista_bombeiros:
            if bombeiro.status == "alive":
                screen.blit(
                    FIREMAN_IMG, (bombeiro.y * cell_size, bombeiro.x * cell_size)
                )
            if bombeiro.status == "burning":
                screen.blit(
                    FIREMAN_BURNING2_IMG,
                    (bombeiro.y * cell_size, bombeiro.x * cell_size),
                )
            if bombeiro.status == "burning2":
                screen.blit(
                    FIREMAN_BURNING1_IMG,
                    (bombeiro.y * cell_size, bombeiro.x * cell_size),
                )

    forest = Forest(matriz)  # Inicializando a Floresta
    forest.vent = agent.vento()
    alive_burning_burned = (
        []
    )  # Carregará número de árvores vivas, queimando e queimadas para gerar o gráfico
    running = True

    # Criando os botões
    button_width, button_height = START_IMG.get_width(), START_IMG.get_height()
    button_x, button_y = tela_x // 2, tela_y // 2
    start_but = agent.buttom(button_x, button_y, button_width, button_height)

    button_x, button_y = tela_x // 10, 0.42 * tela_y
    button_width, button_height = BUTTOM_UP_IMG.get_width(), BUTTOM_UP_IMG.get_height()
    up_but = agent.buttom(button_x, button_y, button_width, button_height)

    button_y = 0.525 * tela_y
    down_but = agent.buttom(button_x, button_y, button_width, button_height)
    button_x = 0.07 * tela_x
    button_y = 0.475 * tela_y
    left_but = agent.buttom(button_x, button_y, button_width, button_height)
    button_x = 0.13 * tela_x
    right_but = agent.buttom(button_x, button_y, button_width, button_height)
    button_x = 0.1 * tela_x
    x_but = agent.buttom(button_x, button_y, button_width, button_height)
    button_x, button_y = 0.003 * tela_x * cell_size, 0.03 * tela_y * cell_size
    button_width, button_height = (
        BUTTOM_PAUSE_IMG.get_width(),
        BUTTOM_PAUSE_IMG.get_height(),
    )
    pause_but = agent.buttom(button_x, button_y, button_width, button_height)

    start = False  # Controle para verificar se o incêndio deve iniciar
    aux = False
    start2 = False
    loading = True
    pause_but.visible = False
    bombeiros = [agent.bombeiro(matriz) for _ in range(5)]
    bombeiros_andar = False

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_but.is_button_clicked(event.pos) and start_but.visible:
                    if start2:
                        loading = True

                    print("Botão clicado!")
                    start_but.visible = False  # Esconde o botão após o clique
                    start = True  # Inicia o incêndio após o clique
                    pause_but.visible = True
                    bombeiros_andar = True

                if up_but.is_button_clicked(event.pos):
                    print("up clicado")
                    forest.vent = agent.vento("N")

                if down_but.is_button_clicked(event.pos):
                    print("down clicado")
                    forest.vent = agent.vento("S")

                if right_but.is_button_clicked(event.pos):
                    print("right clicado")
                    forest.vent = agent.vento("L")

                if left_but.is_button_clicked(event.pos):
                    print("left clicado")
                    forest.vent = agent.vento("O")

                if x_but.is_button_clicked(event.pos):
                    print("x clicado")
                    forest.vent = agent.vento()

                if pause_but.is_button_clicked(event.pos):
                    print("pause clicado")
                    start_but.visible = True
                    pause_but.visible = False
                    start2 = True
                    loading = False
        draw_bombeiros(bombeiros)
        screen.fill((85, 107, 47))
        draw_forest(screen, forest)
        bombeiros_vivos = []
        for bomb in bombeiros:
            print(bomb.life)
            if bomb.status != "dead":
                bombeiros_vivos.append(bomb)

        draw_bombeiros(bombeiros_vivos)

        # Desenhar o botão apenas se ele estiver visível
        if start_but.visible:
            screen.blit(START_IMG, (start_but.x, start_but.y))

        if up_but.visible:
            screen.blit(BUTTOM_UP_IMG, (up_but.x, up_but.y))
            screen.blit(BUTTOM_DOWN_IMG, (down_but.x, down_but.y))
            screen.blit(BUTTOM_LEFT_IMG, (left_but.x, left_but.y))
            screen.blit(BUTTOM_RIGHT_IMG, (right_but.x, right_but.y))
            screen.blit(BUTTOM_X_IMG, (x_but.x, x_but.y))

        if pause_but.visible:
            screen.blit(BUTTOM_PAUSE_IMG, (pause_but.x, pause_but.y))

        pygame.display.flip()  # Atualiza a tela

        if start:
            forest.incendio()  # Inicia o incêndio
            start = False
            aux = True

        burned = 0
        burning = 0
        alive = 0
        incendio = False
        if aux:
            incendio = True
        for row in matriz:
            for cell in row:
                if cell == "v":
                    burned += 1
                if isinstance(cell, agent.Tree):
                    if cell.condition == "alive":
                        alive += 1

                    if cell.condition == "burning":
                        burning += 1
                    if cell.next_condition == "burning":
                        incendio = False
        if incendio:
            forest.incendio()  # caso o incêndio acabe inicia um novo

        alive_burning_burned.append((alive, burning, burned))
        if loading:
            forest.update_forest()
            forest.surge_trees()
            if bombeiros_andar:
                for bombeirx in bombeiros_vivos:
                    bombeirx.andar()
                    # bombeirx.probability_atualization()
                    # leia sobre na função
                    bombeirx.atualizar_bombeiro()

        time.sleep(0.01)

    pygame.quit()

    def graph():
        first_values = [item[0] for item in alive_burning_burned]
        second_values = [item[1] for item in alive_burning_burned]
        third_values = [item[2] for item in alive_burning_burned]
        x = list(range(len(alive_burning_burned)))
        plt.plot(x, first_values, label="Árvores vivas")
        plt.plot(x, second_values, label="Árvores queimando")
        plt.plot(x, third_values, label="Árvores queimadas")

        plt.title("")
        plt.xlabel("Índice")
        plt.ylabel("Valor")
        plt.legend()

        plt.show()


if __name__ == "__main__":
    main()
