# Windows
# keycode_up = 87  # w
# keycode_left = 65  # a
# keycode_down = 83  # s
# keycode_right = 68  # d

# Linux
keycode_up = 25  # w
keycode_left = 38  # a
keycode_down = 39  # s
keycode_right = 40  # d


class SnakeController:

    def __init__(self, model, view):
        self.sm = model
        sv = view
        sv.window.bind("<Key>", self.key_pressed)

    def key_pressed(self, event):
        keycode = event.keycode
        if keycode == keycode_up:
            self.sm.change_direction(0)
        if keycode == keycode_left:
            self.sm.change_direction(1)
        if keycode == keycode_down:
            self.sm.change_direction(2)
        if keycode == keycode_right:
            self.sm.change_direction(3)
