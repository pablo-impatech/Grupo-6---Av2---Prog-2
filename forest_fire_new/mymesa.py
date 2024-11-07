import random
import pygame
import time

# Inicialização do Pygame
pygame.init()

TREE_ALIVE_IMG = pygame.image.load("forest_fire_new\images\Tree_Small.png")
TREE_BURNING_IMG = pygame.image.load("forest_fire_new\images\Fire_Small.png")

cell_size = 20
TREE_ALIVE_IMG = pygame.transform.scale(TREE_ALIVE_IMG, (cell_size, cell_size))
TREE_BURNING_IMG = pygame.transform.scale(TREE_BURNING_IMG, (cell_size, cell_size))


class Tree():
    def __init__(self, coord):
        self.condition = "alive"
        self.density = random.randint(50, 80)
        self.next_condition = None
        self.x = coord[0]
        self.y = coord[1]

    def neighbors(self, matriz):
        lista = []
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < len(matriz) and 0 <= ny < len(matriz[0]) and isinstance(matriz[nx][ny], Tree):
                lista.append(matriz[nx][ny])
        return lista

    def attempt_to_burn(self, matriz,vent):
                
        if self.condition == "alive":
            self.next_condition = "burning"
            for neighbor in self.neighbors(matriz):
                if neighbor.condition == "alive" and neighbor.next_condition != "burning":
                    probability = 100 - neighbor.density
                    if neighbor in vent.neighbors_vento(self,matriz):
                        probability = max(95,probability+30)
                    else:
                        probability  = min(50,probability-20)
                    if random.random() < probability / 100: #queima o vizinho com probabilidade 1 - densidade da árvore
                            neighbor.next_condition = "tick"
                            """
                            é preciso pensar bem nesta parte, ao usar tick, evita o problema
                            de queimar tudo de uma vez, porém não fica tão fluido a ação do fogo
                                                        
                            """
                    
                        

    def update_condition(self,forest):
        matriz = forest.matriz
        vent = forest.vent
        if self.next_condition == "burned": #Se o próximo estágio é queimada esvazia seu lugar na matriz
            matriz[self.x][self.y] = "v"

        if self.next_condition == "burning": #Se o próximo estágio é queimando
            self.attempt_to_burn(matriz,vent) #queima os vizinhos
            self.condition = self.next_condition 
            self.next_condition = "burned"
        
        if self.next_condition == "tick": #tick pode ser usado para melhorar a transição entre alive e burning
            self.next_condition = "burning"
    

    def __repr__(self): #para visualizar a matriz
        if self.condition == "alive":
            return "1"
        if self.condition == "burning":
            return "b"
        if self.condition == "burned":
            return "0"

class Barrier: #representará barreiras como água ou muro, algo assim
    def __init__(self, coord):
        self.x = coord[0]
        self.y = coord[1]
    
    def __repr__(self):
        return "a"
class vento():
    def __init__(self,direction=None):
        lista_directions = ["N","S","L","O","NO","NE","SE","SO"]
        self.directions =[]
        if direction == 1:
            direction = random.choice(lista_directions)
        if direction == "L":
            self.directions = [(0, 1), (1, 1), (-1, 1)]
        elif direction == "O":
            self.directions = [(0, -1), (1, -1), (-1, -1)]
        elif direction == "S":
            self.directions = [(1, 0), (1, 1), (1, -1)]
        elif direction == "N":
            self.directions = [(-1, 0), (-1, 1), (-1, -1)]
        elif direction == "SE":
            self.directions = [(0, 1), (1, 0), (1, 1)]
        elif direction == "NE":
            self.directions = [(0, 1), (-1, 0), (-1, 1)]
        elif direction == "SO":
            self.directions = [(0, -1), (1, 0), (1, -1)]
        elif direction == "NO":
            self.directions = [(0, -1), (-1, 0), (-1, -1)]
    
    def neighbors_vento(self,tree,matriz):
        lista = []
        if self.directions:
            for dx,dy in self.directions:
                nx, ny = tree.x+dx, tree.y+dy
                if 0 <= nx < len(matriz) and 0 <= ny < len(matriz[0]) and isinstance(matriz[nx][ny], Tree):
                    lista.append(matriz[nx][ny])

        return lista    

class Forest:
    def __init__(self, matriz):
        self.matriz = matriz
        self.n = len(matriz)
        self.m = len(matriz[0])
        self.vent = vento()
    
    def incendio(self):
        while True:
            k = random.randint(0, self.n - 1)
            l = random.randint(0, self.m - 1)
            if isinstance(self.matriz[k][l], Tree) and self.matriz[k][l].condition == "alive":
                self.matriz[k][l].attempt_to_burn(self.matriz,self.vent)
                break

    def update_forest(self):
        for row in self.matriz:
            for cell in row:
                if isinstance(cell, Tree):
                    cell.update_condition(self)

    def extinguish_tree_at(self, x, y):
        col, row = x // cell_size, y // cell_size
        if 0 <= row < self.n and 0 <= col < self.m:
            cell = self.matriz[row][col]
            if isinstance(cell, Tree):
                cell.extinguish_fire()

    def surge_trees(self):
        for i in range(self.n):
            for j in range(self.m):
                if self.matriz[i][j] == "v":
                    a = random.randint(1,5)
                    if a == 1:
                        self.matriz[i][j] = Tree((i,j))

    def tree_f_pos(self,coord):
        self.matriz[coord[0]][coord[1]] == Tree((coord[0],coord[1]))

def draw_forest(screen, forest):
    for i in range(forest.n):
        for j in range(forest.m):
            cell = forest.matriz[i][j]
            if isinstance(cell, Tree):
                if cell.condition == "alive":
                    screen.blit(TREE_ALIVE_IMG, (j * cell_size, i * cell_size))
                elif cell.condition == "burning":
                    screen.blit(TREE_BURNING_IMG, (j * cell_size, i * cell_size))
            elif isinstance(cell, Barrier):
                pygame.draw.rect(screen, (173, 216, 230), (j * cell_size, i * cell_size, cell_size, cell_size))

    

def main():
    screen_width, screen_height = 400, 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Forest Fire Simulation")
    screen.fill((0, 0, 255))
    
    matriz = [[Tree((i, j)) for j in range(20)] for i in range(20)]
       
    matriz[4][4] = Barrier((4,4))
    matriz[4][5] = Barrier((4,5))
    matriz[5][5] = Barrier((5,5))
    
    forest = Forest(matriz)
    forest.incendio()
    forest.vent = vento(1) #A floresta agora estará sobre a ação de um vento com direção aleatória

    running = True
    while running:
        screen.fill((85, 107, 47))
        incendio = True
        for row in matriz:
            for cell in row:
                if isinstance(cell, Tree):
                    if cell.next_condition == "burning":
                        incendio = False
        if incendio:
            forest.incendio()
    

        draw_forest(screen, forest)
        pygame.display.flip()
        forest.surge_trees()


        forest.update_forest()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
                

        time.sleep(0.01)

    pygame.quit()

if __name__ == "__main__":
    main()
