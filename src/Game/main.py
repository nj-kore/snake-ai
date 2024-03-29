from controller import SnakeController
from model import SnakeModel
from view import SnakeView

if __name__ == "__main__":
    sm = SnakeModel(8, 8)
    sv = SnakeView(sm)
    sc = SnakeController(sm, sv)

    sm.reset()
    sm.start_game()
    sv.start_rendering()
