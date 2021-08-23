import tkinter as tk


class SnakeView:
    def __init__(self, model):
        self.sm = model
        self.window = tk.Tk()

        self.stats_frame = tk.Frame(master=self.window, width=100, height=200)
        self.stats_frame.grid(row=0, column=0)
        self.iter_text_var = tk.StringVar()
        self.length_text_var = tk.StringVar()
        self.iter_label = tk.Label(master=self.stats_frame, textvariable=self.iter_text_var)
        self.length_label = tk.Label(master=self.stats_frame, textvariable=self.length_text_var)
        self.iter_label.place(anchor='nw')
        self.length_label.place(anchor='nw', rely=0.1)

        self.game_frame = tk.Frame(master=self.window, width=100, height=100, bg='green')
        self.game_frame.grid(row=0, column=1)

        self.tile_frames = [[tk.Frame() for w in range(self.sm.grid_width + 2)] for h in range(self.sm.grid_height + 2)]
        self.init_tile_frames()
        self.sm.game_loop_observable.subscribe(self.draw_game)
        self.draw_border()

    def init_tile_frames(self):
        for i in range(self.sm.grid_width + 2):
            for j in range(self.sm.grid_height + 2):
                frame = tk.Frame(
                    master=self.game_frame,
                    relief=tk.RAISED,
                    borderwidth=1,
                    background='black',
                    width=50,
                    height=50
                )
                frame.grid(row=self.sm.grid_width - j - 1 + 2, column=i)
                self.tile_frames[i][j] = frame

    def draw_game(self):
        self.iter_text_var.set("Itr: " + str(self.sm.game_loop_itr))
        self.length_text_var.set("Length: " + str(self.sm.snake_length))
        if self.sm.game_status == 0:
            self.draw_board()
            self.draw_fruit()
            self.draw_player()

    def start_rendering(self):
        self.draw_game()
        self.window.mainloop()

    # sets all board pieces to black
    def draw_board(self):
        for i in range(1, self.sm.grid_width + 1):
            for j in range(1, self.sm.grid_height + 1):
                self.tile_frames[i][j].config(bg='black')

    def draw_border(self):
        for i in [0, self.sm.grid_width + 1]:
            for j in range(self.sm.grid_height + 2):
                self.tile_frames[i][j].config(bg='red')

        for i in range(self.sm.grid_width + 2):
            for j in [0, self.sm.grid_height + 1]:
                self.tile_frames[i][j].config(bg='red')

    def draw_player(self):
        # draw body (excluding head)
        for body_piece in self.sm.player_body:
            self.tile_frames[body_piece[0] + 1][body_piece[1] + 1].config(bg='green')

        # draw head
        self.tile_frames[self.sm.player_head[0] + 1][self.sm.player_head[1] + 1].config(bg='green')

    def draw_fruit(self):
        self.tile_frames[self.sm.fruit[0] + 1][self.sm.fruit[1] + 1].config(bg='purple')
