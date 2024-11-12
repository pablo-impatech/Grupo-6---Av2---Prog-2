import random


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
        nx, ny = self[0] + dx, self[1] + dy
        if (
            0 <= nx < len(matriz)
            and 0 <= ny < len(matriz[0])
            and isinstance(matriz[nx][ny], Tree)
        ):
            lista.append(matriz[nx][ny])
    return lista


class bombeiro:
    def __init__(self, matriz):
        self.step = 0
        self.matriz = matriz
        self.life = 1
        self.status = "alive"
        while True:
            self.x, self.y = random.randint(0, len(matriz) - 1), random.randint(
                0, len(matriz[0]) - 1
            )
            if isinstance(matriz[self.x][self.y], Tree):
                break

    def andar(self):
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

    """def probability_atualization(self):
        for neigh in neighbors([self.x, self.y], self.matriz):
            if isinstance(neigh, Tree):
                neigh.density = 1"""
    """
    é preciso determinar como o bombeiro influenciará as árvores ao redor.
    -> as árvores ao seu redor aumentam de densidade, ou seja tem menos chance de pegar fogo
    -> a cada frame o bombeiro retorna uma condição da árvore,
    Se a segunda for escolhida é necessário que as árvores guardem um self.previous_condition
    
    """

    def atualizar_bombeiro(self):
        for neigh in neighbors((self.x, self.y), self.matriz):
            if neigh.condition == "burning":
                self.life -= 0.01

        if 0.5 <= self.life <= 0.8:
            self.status = "burning"

        elif 0 < self.life < 0.5:
            self.status = "burning2"

        elif self.life <= 0:
            self.status = "dead"


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


class Tree:
    def __init__(self, coord):
        self.condition = "alive"
        self.density = random.randint(50, 80)
        self.next_condition = None
        self.x = coord[0]
        self.y = coord[1]
        self.count = 0
        self.step = 0

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

    def attempt_to_burn(self, matriz, vent):

        if self.condition == "alive":
            self.next_condition = "burning"
            for neighbor in self.neighbors(matriz):
                if (
                    neighbor.condition == "alive"
                    and neighbor.next_condition != "burning"
                ):
                    probability = 100 - neighbor.density
                    if vent.directions:
                        if neighbor in vent.neighbors_vento(self, matriz):
                            probability = min(80, probability + 30)
                            probability = 100  # Probabilidade determinada assim para melhorar a visualização do vento
                        else:
                            probability = max(40, probability - 20)
                            probability = 0
                    if (
                        random.random() < probability / 100
                    ):  # queima o vizinho com probabilidade 1 - densidade da árvore
                        neighbor.next_condition = "tick"

    def burn_continuos(self, matriz, vent):
        for neighbor in self.neighbors(matriz):
            if neighbor.condition == "alive" and neighbor.next_condition != "burning":
                probability = min(100 - neighbor.density - 40, 10)
                if vent.directions:
                    if neighbor in vent.neighbors_vento(self, matriz):
                        probability = min(60, probability + 10)
                        probability = 100  # Probabilidade determinada assim para melhorar a visualização do vento
                    else:
                        probability = max(10, probability - 20)
                        probability = 0
                if (
                    random.random() < probability / 100
                ):  # queima o vizinho com probabilidade 1 - densidade da árvore
                    neighbor.next_condition = "tick"

    def update_condition(self, forest):
        matriz = forest.matriz
        vent = forest.vent
        if self.next_condition == "burned":
            self.next_condition = "step"
            self.condition = "burned"
            self.burn_continuos(matriz, vent)

        elif self.next_condition == "step":
            self.step += 1
            self.burn_continuos(matriz, vent)
            if self.step == 3:
                self.next_condition = "final"

        elif self.next_condition == "final":
            matriz[self.x][self.y] = "v"

        if self.next_condition == "burning":  # Se o próximo estágio é queimando
            self.attempt_to_burn(matriz, vent)  # queima os vizinhos
            self.count += 1
            self.condition = self.next_condition
            if self.count == 4:
                self.next_condition = "burned"

        if (
            self.next_condition == "tick"
        ):  # tick pode ser usado para melhorar a transição entre alive e burning
            self.next_condition = "burning"

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
