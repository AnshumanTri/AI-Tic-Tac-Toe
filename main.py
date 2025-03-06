import tkinter as tk
from tkinter import messagebox
import random

# Constants
PLAYER_X = "X"
PLAYER_O = "O"
EMPTY = " "

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#1F1F1F")  # Dark mode background
        self.root.title("Tic-Tac-Toe 🎮")

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.scores = {PLAYER_X: 0, PLAYER_O: 0}
        
        self.create_widgets()
        self.reset_game()

    def create_widgets(self):
        """Create UI elements: board, status, scoreboard, and restart button."""
        self.status_label = tk.Label(self.root, text="Player X's Turn", font=("Arial", 18, "bold"), bg="#1F1F1F", fg="white")
        self.status_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.score_label = tk.Label(self.root, text="X: 0  |  O: 0", font=("Arial", 14, "bold"), bg="#1F1F1F", fg="lightgray")
        self.score_label.grid(row=1, column=0, columnspan=3)

        # Game board buttons
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text=EMPTY, font=('Arial', 40, 'bold'), width=5, height=2,
                                               bg="#2E2E2E", fg="white", relief="flat", bd=3, activebackground="#575757",
                                               command=lambda row=i, col=j: self.button_click(row, col))
                self.buttons[i][j].grid(row=i + 2, column=j, padx=5, pady=5)

        # Restart button
        self.restart_button = tk.Button(self.root, text="Restart 🔄", font=("Arial", 14, "bold"), bg="#E74C3C", fg="white",
                                        command=self.reset_game, padx=10, pady=5, relief="flat", bd=2, activebackground="#C0392B")
        self.restart_button.grid(row=5, column=0, columnspan=3, pady=10)

    def reset_game(self):
        """Resets the board and updates UI."""
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]
        self.current_player = PLAYER_X
        self.game_over = False
        self.update_buttons()
        self.status_label.config(text="Player X's Turn", fg="lightgreen")

    def update_buttons(self):
        """Updates button text and enables/disables them."""
        for i in range(3):
            for j in range(3):
                btn = self.buttons[i][j]
                btn.config(text=self.board[i][j], state=tk.NORMAL if self.board[i][j] == EMPTY else tk.DISABLED,
                           bg="#2E2E2E")

    def is_winner(self, player):
        """Checks if a player has won."""
        for i in range(3):
            if all([cell == player for cell in self.board[i]]) or \
               all([self.board[j][i] == player for j in range(3)]):
                return True
        if all([self.board[i][i] == player for i in range(3)]) or \
           all([self.board[i][2 - i] == player for i in range(3)]):
            return True
        return False

    def is_full(self):
        """Checks if the board is full."""
        return all(cell != EMPTY for row in self.board for cell in row)

    def make_move(self, row, col, player):
        """Places a move on the board."""
        if self.board[row][col] == EMPTY:
            self.board[row][col] = player
            return True
        return False

    def ai_move(self):
        """AI selects a random available move."""
        move = random.choice(self.get_available_moves())
        self.make_move(move[0], move[1], PLAYER_O)

    def get_available_moves(self):
        """Returns a list of available moves."""
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == EMPTY]

    def play_game(self):
        """Handles AI moves and checks game state."""
        if self.current_player == PLAYER_O and not self.game_over:
            self.ai_move()
            self.update_buttons()

            if self.is_winner(PLAYER_O):
                self.scores[PLAYER_O] += 1
                self.score_label.config(text=f"X: {self.scores[PLAYER_X]}  |  O: {self.scores[PLAYER_O]}")
                messagebox.showinfo("Game Over", "O wins! 🎉")
                self.game_over = True
                return
            if self.is_full():
                messagebox.showinfo("Game Over", "It's a tie! 🤝")
                self.game_over = True
                return

            self.current_player = PLAYER_X
            self.status_label.config(text="Player X's Turn", fg="lightgreen")

    def button_click(self, row, col):
        """Handles user clicks and switches turns."""
        if self.game_over:
            return

        if self.make_move(row, col, PLAYER_X):
            self.update_buttons()

            if self.is_winner(PLAYER_X):
                self.scores[PLAYER_X] += 1
                self.score_label.config(text=f"X: {self.scores[PLAYER_X]}  |  O: {self.scores[PLAYER_O]}")
                messagebox.showinfo("Game Over", "X wins! 🎉")
                self.game_over = True
                return
            if self.is_full():
                messagebox.showinfo("Game Over", "It's a tie! 🤝")
                self.game_over = True
                return

            self.current_player = PLAYER_O
            self.status_label.config(text="AI's Turn", fg="orange")
            self.root.after(500, self.play_game)  # Delay for AI response

# Run the game
root = tk.Tk()
game = TicTacToe(root)
root.mainloop()
