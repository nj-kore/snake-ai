import Game

class Environment:
    def __init__(self):
        self.game_model = Game.model.SnakeModel()
        self.game_view = Game.view.SnakeView(self.game_model)
        self.game_controller = Game.controller.SnakeController(self.game_model, self.game_view)

    def step(self, action):
        pass



