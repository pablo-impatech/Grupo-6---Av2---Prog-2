import random


class Agent:
    # Todo agente carregará neighbors e update_condition
    def neighbors(self, matriz):
        lista = []
        directions = [
            (0, 1),
            (1, 0),
            (-1, 0),
            (0, -1),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            if (
                0 <= nx < len(matriz)
                and 0 <= ny < len(matriz[0])
                and isinstance(matriz[nx][ny], Tree)
            ):
                lista.append(matriz[nx][ny])

        return lista

    def update_condition(self):
        raise NotImplementedError

    # O ideal ao criar um agente deve ser conter tudo que ele faz em update_condition
    # Assim facilitaria atualizar o agente a cada iteração


class bombeiro(Agent):
    def __init__(self, matriz):
        self.step = 0  # Definindo o numero de atualizações para o bombeiro andar
        self.matriz = matriz  # Matriz da floresta
        self.life = 1  # O bombeiro terá vida igual a 1 e perderá conforme as árvores ao seu redor pegam fogo
        self.status = "alive"

        # Posição aleatória em que o bombeiro nascerá
        while True:
            self.x, self.y = random.randint(0, len(matriz) - 1), random.randint(
                0, len(matriz[0]) - 1
            )
            if isinstance(matriz[self.x][self.y], Tree):
                break

    def update_condition(self):
        self.andar()  # O bomebiro anda
        # Verificando árvores que estão queimando
        for neigh in self.neighbors(self.matriz):
            if isinstance(neigh, Tree):
                if neigh.condition == "burning":
                    self.life -= 0.01

        if 0.5 <= self.life <= 0.8:
            self.status = "burning"

        elif 0 < self.life < 0.5:
            self.status = "burning2"

        elif self.life <= 0:
            self.status = "dead"

    def andar(self):
        # A função andar, por enquanto apenas leva o bombeiro para um vizinho aleatório
        self.step += 1
        if self.step == 5:
            direction = [
                (0, 1),
                (0, -1),
                (1, 0),
                (-1, 0),
                (1, 1),
                (-1, 1),
                (1, -1),
                (-1, -1),
            ]
            random.shuffle(direction)
            directions_possi = []
            for dx, dy in direction:
                nx, ny = self.x + dx, self.y + dy
                if (
                    0 <= nx < len(self.matriz)
                    and 0 <= ny < len(self.matriz[0])
                    and (
                        isinstance(self.matriz[nx][ny], Tree)
                        or self.matriz[nx][ny] == "v"
                    )
                ):
                    self.x, self.y = nx, ny  # Move o bombeiro para a nova posição
                    directions_possi.append((nx, ny))

            if directions_possi:
                a = random.choice(directions_possi)
                self.x, self.y = a[0], a[1]

            self.step = 0


class buttom:
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.visible = True

    def is_button_clicked(self, pos):
        if self.visible:
            return (
                self.x <= pos[0] <= self.x + self.width
                and self.y <= pos[1] <= self.y + self.height
            )
        else:
            return None


class Tree(Agent):
    def __init__(self, coord):
        self.condition = "alive"
        self.density = random.randint(50, 80)
        self.next_condition = None
        self.x = coord[0]
        self.y = coord[1]
        self.count = 0
        self.step = 0

    def attempt_to_burn(self, matriz, vent):
        for neighbor in self.neighbors(matriz):
            if neighbor.condition == "alive" and neighbor.next_condition != "burning":
                probability = 100 - neighbor.density
                if self.condition == "burned":  # A intensidade do fogo é menor
                    probability -= 10
                if vent.directions:
                    if neighbor in vent.neighbors_vento(self, matriz):
                        probability = min(80, probability + 30)
                        probability = 100  # Probabilidade determinada assim para melhorar a visualização do vento
                    else:
                        probability = max(40, probability - 20)
                        probability = 0
                if (
                    random.random() < probability / 100
                ):  # queima o vizinho com probabilidade (1 - densidade da árvore)
                    neighbor.next_condition = "burning"

    def update_condition(self, forest):
        matriz = forest.matriz
        vent = forest.vent
        if self.next_condition == "burned":
            self.next_condition = "step"
            self.condition = "burned"
            # self.attempt_to_burn(matriz, vent)

        elif self.next_condition == "step":
            self.step += 1
            # self.attempt_to_burn(matriz, vent)
            if self.step == 3:
                self.next_condition = "final"

        elif self.next_condition == "final":
            matriz[self.x][self.y] = "v"

        if self.next_condition == "burning":  # Se o próximo estágio é queimando
            self.attempt_to_burn(
                matriz, vent
            )  # queima os vizinhos com influência do vento
            self.count += 1
            self.condition = self.next_condition
            if self.count == 2:
                self.next_condition = "burned"

    def __repr__(self):  # para visualizar a matriz
        if self.condition == "alive":
            return "1"
        if self.condition == "burning":
            return "b"
        if self.condition == "burned":
            return "0"


class Barrier:  # representará barreiras como água ou muro, algo assim
    def __init__(self, coord):
        self.x = coord[0]
        self.y = coord[1]

    def __repr__(self):
        return "a"


class Houses:
    def __init__(self, coord):
        self.x = coord[0]
        self.y = coord[0]

    def __repr__(self):
        return "h"


class vento:
    def __init__(self, direction=None):
        lista_directions = ["N", "S", "L", "O", "NO", "NE", "SE", "SO"]
        self.directions = []
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

    def neighbors_vento(self, tree, matriz):
        lista = []
        if self.directions:
            for dx, dy in self.directions:
                nx, ny = tree.x + dx, tree.y + dy
                if (
                    0 <= nx < len(matriz)
                    and 0 <= ny < len(matriz[0])
                    and isinstance(matriz[nx][ny], Tree)
                ):
                    lista.append(matriz[nx][ny])

        return lista
