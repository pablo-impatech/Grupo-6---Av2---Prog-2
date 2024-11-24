import pygame
from pygame_widgets.button import Button

# Inicializa o Pygame
pygame.init()

# Configurações da tela
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Botão Chuva!")
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)


# Função chamada ao clicar no botão
def chuva_action():
    print("Chuva!")


# Botão com o texto "Chuva!"
chuva_button = Button(
    screen,
    100,
    100,
    200,
    50,  # Posição e tamanho (x, y, largura, altura)
    text="Chuva!",  # Texto no botão
    fontSize=30,  # Tamanho da fonte
    margin=5,  # Margem ao redor do texto
    inactiveColour=GREY,  # Cor do botão quando inativo
    hoverColour=BLACK,  # Cor do botão quando o mouse está sobre ele
    pressedColour=BLACK,  # Cor do botão quando clicado
    textColour=WHITE,  # Cor do texto
    radius=10,  # Bordas arredondadas
    onClick=chuva_action,  # Ação ao clicar no botão
)

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Atualiza o botão
        chuva_button.listen(event)

    # Desenha a interface
    screen.fill(WHITE)
    chuva_button.draw()

    pygame.display.update()
    clock.tick(30)

pygame.quit()
