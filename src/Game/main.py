from controller import SnakeController
from model import SnakeModel
from view import SnakeView

sm = SnakeModel()
sv = SnakeView(sm)
sc = SnakeController(sm, sv)

sm.start_new_game()
sv.start_rendering()
