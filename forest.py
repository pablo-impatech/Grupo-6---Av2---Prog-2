import agents as agent
import random


class Forest:
    def __init__(self, matriz):
        self.matriz = matriz
        self.n = len(matriz)
        self.m = len(matriz[0])
        self.vent = agent.vento()
        self.surge_trees = True

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
        fire = True
        for i in range(self.n):
            for j in range(self.m):
                if isinstance(self.matriz[i][j], agent.Tree):
                    if (
                        self.matriz[i][j].condition == "burning"
                        or self.matriz[i][j].condition == "burned"
                    ):
                        fire = False

                    self.matriz[i][j].update_condition(self)

                if self.surge_trees:
                    rand = random.randint(1, 100)
                    if rand == 4:
                        if self.matriz[i][j] == "v":
                            self.matriz[i][j] = agent.Tree([i, j])
        if fire:
            self.incendio()  # Caso não tenha fogo, causa um incêndio aleatório
