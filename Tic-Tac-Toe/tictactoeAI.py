import tkinter as tk
from tkinter import simpledialog, messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title('Tic Tac Toe: Human vs AI')

        # Variables
        self.board = [' '] * 9
        self.human = ''
        self.ai = ''
        self.current_player = ''

        # UI Setup
        self.buttons = [tk.Button(root, text=' ', font='Arial 20', width=5, height=2, command=lambda i=i: self.make_move(i)) for i in range(9)]
        for idx, button in enumerate(self.buttons):
            row = idx // 3
            col = idx % 3
            button.grid(row=row, column=col)

        # Ask player choice
        self.human = simpledialog.askstring('Choice', 'Do you want to be X or O?').upper()
        if self.human == 'X':
            self.ai = 'O'
            self.current_player = 'X'
        else:
            self.ai = 'X'
            self.current_player = self.ai
            self.ai_play()

    def make_move(self, idx):
        if self.board[idx] == ' ' and self.current_player == self.human:
            self.board[idx] = self.human
            self.buttons[idx].config(text=self.human)
            if self.check_win(self.human):
                messagebox.showinfo("Result", "Human Wins!")
                self.reset_game()
            elif ' ' not in self.board:
                messagebox.showinfo("Result", "It's a Draw!")
                self.reset_game()
            else:
                self.current_player = self.ai
                self.ai_play()

    def ai_play(self):
        best_score = float('-inf')
        best_move = -1
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = self.ai
                score = self.minimax(False)
                self.board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i

        self.board[best_move] = self.ai
        self.buttons[best_move].config(text=self.ai)
        if self.check_win(self.ai):
            messagebox.showinfo("Result", "AI Wins!")
            self.reset_game()
        elif ' ' not in self.board:
            messagebox.showinfo("Result", "It's a Draw!")
            self.reset_game()
        else:
            self.current_player = self.human

    def minimax(self, is_ai):
        if self.check_win(self.human):
            return -1
        if self.check_win(self.ai):
            return 1
        if ' ' not in self.board:
            return 0

        if is_ai:
            best_score = float('-inf')
            for i in range(9):
                if self.board[i] == ' ':
                    self.board[i] = self.ai
                    score = self.minimax(False)
                    self.board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if self.board[i] == ' ':
                    self.board[i] = self.human
                    score = self.minimax(True)
                    self.board[i] = ' '
                    best_score = min(score, best_score)
            return best_score

    def check_win(self, player):
        win_configurations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for config in win_configurations:
            if self.board[config[0]] == self.board[config[1]] == self.board[config[2]] == player:
                return True
        return False

    def reset_game(self):
        self.board = [' '] * 9
        for button in self.buttons:
            button.config(text=' ')
        self.current_player = self.human if self.ai == 'O' else self.ai
        if self.current_player == self.ai:
            self.ai_play()

if __name__ == '__main__':
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
