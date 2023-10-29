import random
import tkinter as tk
import tkinter.ttk as ttk

SEGMENT = 100  # Size of each cell in the board grid
GRID_LINES = [(SEGMENT, 10, SEGMENT, 290) for SEGMENT in [100, 200]] + [(10, SEGMENT, 290, SEGMENT) for SEGMENT in [100, 200]]

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.grid()
        
        # Initialize game state
        self.board = {(i, j): ' ' for i in range(3) for j in range(3)}
        self.x_score = 0
        self.o_score = 0
        self.players = ['X', 'O']
        self.current_player = random.choice(self.players)
        
        # Draw the game UI components
        self.draw_header_frame()
        self.draw_body_frame()

    def draw_header_frame(self):
        self.header = tk.Frame(self, width=300, height=100)
        self.header.grid(row=0, column=0)
        self.header.grid_propagate(False)

        self.score_frame = tk.Frame(self.header, width=300, height=100)
        self.score_frame.grid(row=0, column=0)
        self.score_frame.grid_propagate(False)

        self.x_label = tk.Label(self.score_frame, text=f'X   {self.x_score}', fg='black', font=('Arial', 18))
        self.x_label.grid(row=0, column=0, padx=(10, 50), pady=5)

        self.o_label = tk.Label(self.score_frame, text=f'O   {self.o_score}', fg='black', font=('Arial', 18))
        self.o_label.grid(row=0, column=1, padx=(50, 10), pady=5)

        self.player_label = tk.Label(self.score_frame, text=f'Current Player : {self.current_player}', fg='black', font=('Arial', 12))
        self.player_label.grid(row=1, column=0, columnspan=2, pady=15)

    def draw_body_frame(self):
        self.body = tk.Frame(self, width=300, height=300)
        self.body.grid(row=1, column=0)
        self.body.grid_propagate(False)

        self.canvas = tk.Canvas(self.body, width=300, height=300, bg='gray')
        self.canvas.grid()

        for line in GRID_LINES:
            self.canvas.create_line(line, width=4, fill='black')

        self.canvas.bind('<Button-1>', self.draw_text)

    def is_win_move(self, row, col, mark):
        # Check row, column and diagonals
        return all(self.board[(row, i)] == mark for i in range(3)) or \
               all(self.board[(i, col)] == mark for i in range(3)) or \
               (row == col and all(self.board[(i, i)] == mark for i in range(3))) or \
               (row + col == 2 and all(self.board[(i, 2 - i)] == mark for i in range(3)))

    def get_text_pos(self, pos):
        x, y = pos
        row, col = y // SEGMENT, x // SEGMENT
        return (col * SEGMENT + SEGMENT // 2, row * SEGMENT + SEGMENT // 2), (row, col)

    def restart_game(self):
        self.top.destroy()
        self.canvas.delete('all')
        self.body.destroy()
        self.board = {(i, j): ' ' for i in range(3) for j in range(3)}
        self.draw_body_frame()
        self.current_player = random.choice(self.players)
        self.player_label['text'] = f'Current Player : {self.current_player}'

    def game_over_window(self, msg):
        self.top = tk.Toplevel(self)
        self.top.geometry('200x100+500+380')

        label = tk.Label(self.top, text=msg, fg='black', font=('Arial', 14))
        label.pack(pady=10)

        restart_button = ttk.Button(self.top, text="Restart", command=self.restart_game)
        restart_button.pack(pady=5)

    def draw_text(self, event):
        pos, (row, col) = self.get_text_pos((event.x, event.y))
        if self.board[(row, col)] == ' ':
            mark = self.current_player
            self.board[(row, col)] = mark
            self.canvas.create_text(pos, text=mark, font=('Arial', 32))
            
            if self.is_win_move(row, col, mark):
                if mark == 'X':
                    self.x_score += 1
                    self.x_label['text'] = f'X   {self.x_score}'
                else:
                    self.o_score += 1
                    self.o_label['text'] = f'O   {self.o_score}'
                self.game_over_window(f'Player {mark} Won!')
            elif ' ' not in self.board.values():
                self.game_over_window("It's a Tie!")
            else:
                self.current_player = 'X' if mark == 'O' else 'O'
                self.player_label['text'] = f'Current Player : {self.current_player}'

root = tk.Tk()
root.geometry('300x400+450+200')
root.title('Tic Tac Toe')
root.resizable(0, 0)
app = Application(master=root)
app.mainloop()
