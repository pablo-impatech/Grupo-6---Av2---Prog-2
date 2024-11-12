
import pygame
import time
import agents as agent
from forest import Forest 
import images_but as im

pygame.init()

def draw_forest(screen, forest):

    for i in range(forest.n):
        for j in range(forest.m):
            cell = forest.matriz[i][j]
            if isinstance(cell, agent.Tree):
                if cell.condition == "alive":
                    screen.blit(im.TREE_ALIVE_IMG, (j * im.cell_size, i * im.cell_size))
                elif cell.condition == "burning":
                    screen.blit(im.TREE_BURNING_IMG, (j * im.cell_size, i * im.cell_size))
                elif cell.condition == "burned":
                    screen.blit(im.TREE_BURNED_IMG, (j * im.cell_size, i * im.cell_size))
            elif isinstance(cell, agent.Barrier):
                screen.blit(im.WATER_IMG, (j * im.cell_size, i * im.cell_size))
            if cell == "v":
                pygame.draw.rect(
                    screen,
                    (95, 107, 47),
                    (j * im.cell_size, i * im.cell_size, im.cell_size, im.cell_size),
                )
            if cell == "black":
                pygame.draw.rect(
                    screen,
                    (105, 107, 47),
                    (j * im.cell_size, i * im.cell_size, im.cell_size, im.cell_size),
                )

def draw_bombeiros(screen, lista_bombeiros):
        for bombeiro in lista_bombeiros:
            if bombeiro.status == "alive":
                screen.blit(
                    im.FIREMAN_IMG, (bombeiro.y * im.cell_size, bombeiro.x * im.cell_size)
                )
            if bombeiro.status == "burning":
                screen.blit(
                    im.FIREMAN_BURNING2_IMG,
                    (bombeiro.y * im.cell_size, bombeiro.x * im.cell_size),
                )
            if bombeiro.status == "burning2":
                screen.blit(
                    im.FIREMAN_BURNING1_IMG,
                    (bombeiro.y * im.cell_size, bombeiro.x * im.cell_size),
                )

def init_screen():
        screen = pygame.display.set_mode((im.tela_x, im.tela_y))
        #Podemos arrumar um jeito mais eficiente de determinar a matriz
        matriz = [
            [agent.Tree((i, j)) for j in range(im.tela_x // im.cell_size)]
            for i in range((im.tela_y // im.cell_size))
        ]


        for i in range((im.tela_x//im.cell_size)//4):
            for j in range(im.tela_y // im.cell_size):
                matriz[j][i] = "black"


        return matriz, screen

def main():


    matriz, screen = init_screen()
    forest = Forest(matriz)  # Inicializando a Floresta
    forest.vent = agent.vento()

    running = True
    start = False  # Controle para verificar se o incêndio deve iniciar
    start2 = False
    loading = False
    bombeiros = [agent.bombeiro(matriz) for _ in range(10)]
    bombeiros_andar = False
    forest.surge_trees = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if im.start_but.is_button_clicked(event.pos) and im.start_but.visible:
                    if start2:
                        loading = True

                    print("Botão clicado!")
                    im.start_but.visible = False  # Esconde o botão após o clique
                    start = True  # Inicia o incêndio após o clique
                    im.pause_but.visible = True
                    bombeiros_andar = True
                    loading = True

                if im.up_but.is_button_clicked(event.pos):
                    print("up clicado")
                    forest.vent = agent.vento("N")

                if im.down_but.is_button_clicked(event.pos):
                    print("down clicado")
                    forest.vent = agent.vento("S")

                if im.right_but.is_button_clicked(event.pos):
                    print("right clicado")
                    forest.vent = agent.vento("L")

                if im.left_but.is_button_clicked(event.pos):
                    print("left clicado")
                    forest.vent = agent.vento("O")

                if im.x_but.is_button_clicked(event.pos):
                    print("x clicado")
                    forest.vent = agent.vento()

                if im.pause_but.is_button_clicked(event.pos):
                    print("pause clicado")
                    im.start_but.visible = True
                    im.pause_but.visible = False
                    start2 = True
                    loading = False

        screen.fill((85, 107, 47))
        draw_forest(screen, forest)
        bombeiros_vivos = []
        for bomb in bombeiros:
            if bomb.status != "dead":
                bombeiros_vivos.append(bomb)
        draw_bombeiros(screen,bombeiros_vivos)

        # Desenhar o botão apenas se ele estiver visível
        if im.start_but.visible:
            screen.blit(im.START_IMG, (im.start_but.x, im.start_but.y))

        if im.up_but.visible:
            screen.blit(im.BUTTOM_UP_IMG, (im.up_but.x, im.up_but.y))
            screen.blit(im.BUTTOM_DOWN_IMG, (im.down_but.x, im.down_but.y))
            screen.blit(im.BUTTOM_LEFT_IMG, (im.left_but.x, im.left_but.y))
            screen.blit(im.BUTTOM_RIGHT_IMG, (im.right_but.x, im.right_but.y))
            screen.blit(im.BUTTOM_X_IMG, (im.x_but.x, im.x_but.y))

        if im.pause_but.visible:
            screen.blit(im.BUTTOM_PAUSE_IMG, (im.pause_but.x, im.pause_but.y))

        pygame.display.flip()  # Atualiza a tela

        if start:
            forest.incendio()  # Inicia o incêndio
            start = False
    
        if loading:
            a = forest.update_forest()
            if a:
                forest.incendio()
            forest.update_forest()
            if bombeiros_andar:
                for bombeirx in bombeiros_vivos:
                    bombeirx.andar()
                    # bombeirx.probability_atualization()
                    # leia sobre na função
                    bombeirx.atualizar_bombeiro()

        time.sleep(0.01)

    pygame.quit()


if __name__ == "__main__":
    main()
