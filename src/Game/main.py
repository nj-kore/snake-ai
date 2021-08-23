from controller import SnakeController
from model import SnakeModel
from view import SnakeView

sm = SnakeModel()
sv = SnakeView(sm)
sc = SnakeController(sm, sv)

sm.reset()
sm.start_game()
sv.start_rendering()
