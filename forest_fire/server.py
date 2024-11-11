import mesa

from .model import ForestFire

SPRITES = {
    "Fine": "forest_fire/resources/fine_tree.png",
    "On Fire": "forest_fire/resources/fire.png",
    "Burned Out": "forest_fire/resources/burned_tree.png"
}
COLORS = {"Fine": "#00AA00", "On Fire": "#880000", "Burned Out": "#000000"}
GRID_WIDTH = 25
GRID_HEIGHT = 25

def forest_fire_portrayal(tree):
    if tree is None:
        return
    portrayal = {}

    (x, y) = tree.pos
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Layer"] = 0
    portrayal["Shape"] = SPRITES[tree.condition]
    return portrayal


canvas_element = mesa.visualization.CanvasGrid(
    forest_fire_portrayal, GRID_WIDTH, GRID_HEIGHT, 500, 500
)
tree_chart = mesa.visualization.ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)
pie_chart = mesa.visualization.PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

model_params = {
    "height": GRID_HEIGHT,
    "width": GRID_WIDTH,
    "density": mesa.visualization.Slider("Tree density", 0.65, 0.01, 1.0, 0.01),
    "fire": mesa.visualization.Slider("Fire probability", 0.01, 0.01, 1.0, 0.01, "Only works to multiple flames"),
    "multiple_flames": mesa.visualization.Checkbox("Multiple flames", False),
}
server = mesa.visualization.ModularServer(
    ForestFire, [canvas_element, tree_chart, pie_chart], "Forest Fire", model_params
)
