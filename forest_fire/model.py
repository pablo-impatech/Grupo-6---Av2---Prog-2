import mesa

from .agent import TreeCell
from random import randint

class ForestFire(mesa.Model):
    """
    Simple Forest Fire model.
    """

    def __init__(self, width=100, height=100, density=0.65, multiple_flames=False, fire=0.01):
        """
        Create a new forest fire model.

        Args:
            width, height: The size of the grid to model.
            density: What fraction of grid cells have a tree in them.
            multiple_flames: Set more than one tree on fire.
            fire: What fraction of trees starts on fire (to multiple_flames=True).
        """
        super().__init__()
        # Set up model objects
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.SingleGrid(width, height, torus=False)

        self.datacollector = mesa.DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
            }
        )
        
        # Set one tree in a random cell on fire with Prob = 1
        fire_pos = (None, None)
        if not multiple_flames:
            fire_pos = (randint(0, self.grid.width - 1), randint(0, self.grid.height - 1))
            fire_tree = TreeCell((fire_pos[0], fire_pos[1]), self)
            fire_tree.condition = "On Fire"
            self.grid.place_agent(fire_tree, (fire_pos[0], fire_pos[1]))
            self.schedule.add(fire_tree)

        # Place a tree in each cell with Prob = density
        for contents, (x, y) in self.grid.coord_iter():
            if self.random.random() < density and (x, y) != fire_pos:
                # Create a tree
                new_tree = TreeCell((x, y), self)
                # Set a tree on fire with Prob = fire
                if self.random.random() < fire and multiple_flames:
                    new_tree.condition = "On Fire"
                self.grid.place_agent(new_tree, (x, y))
                self.schedule.add(new_tree)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Halt if no more fire
        if self.count_type(self, "On Fire") == 0:
            self.running = False

    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count
