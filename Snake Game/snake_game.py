from tkinter import *
import random

# Constants for the game's settings
GAME_WIDTH = 1000
GAME_HEIGHT = 1000
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#0000FF"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class SnakeGame:
    """Class representing the snake in the game."""

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        self._direction = 'right'

        for i in range(0, BODY_PARTS):
            self.coordinates.append([(BODY_PARTS - i - 1) * SPACE_SIZE, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake_segment")
            self.squares.append(square)

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, new_direction):
        if new_direction in ['left', 'right', 'up', 'down']:
            if (new_direction == 'left' and self._direction != 'right') or \
                    (new_direction == 'right' and self._direction != 'left') or \
                    (new_direction == 'up' and self._direction != 'down') or \
                    (new_direction == 'down' and self._direction != 'up'):
                self._direction = new_direction


class GameFood:
    """Class representing the food in the game."""

    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food_piece")


class Game:
    def __init__(self):
        self.score = 0
        self.snake = SnakeGame()
        self.food = GameFood()

    def move_snake(self):
        x, y = self.snake.coordinates[0]

        if self.snake.direction == "up":
            y -= SPACE_SIZE
        elif self.snake.direction == "down":
            y += SPACE_SIZE
        elif self.snake.direction == "left":
            x -= SPACE_SIZE
        elif self.snake.direction == "right":
            x += SPACE_SIZE

        self.snake.coordinates.insert(0, (x, y))
        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
        self.snake.squares.insert(0, square)

        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.score += 1
            label.config(text="Score:{}".format(self.score))
            canvas.delete("food_piece")
            self.food = GameFood()
        else:
            canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]
            del self.snake.coordinates[-1]

        if self.collision_detected():
            self.display_game_over()
        else:
            window.after(SPEED, self.move_snake)

    def collision_detected(self):
        x, y = self.snake.coordinates[0]
        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True
        for segment in self.snake.coordinates[1:]:
            if x == segment[0] and y == segment[1]:
                return True
        return False

    def display_game_over(self):
        canvas.delete(ALL)
        canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                           font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover_text")

    def change_direction(self, new_direction):
        self.snake.direction = new_direction


window = Tk()
window.title("Snake Game")
window.resizable(False, False)

label = Label(window, text="Score:0", font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

game = Game()


def key_bindings(event):
    directions = {
        'Up': 'up',
        'Down': 'down',
        'Left': 'left',
        'Right': 'right'
    }
    game.change_direction(directions.get(event.keysym))


window.bind('<Up>', key_bindings)
window.bind('<Down>', key_bindings)
window.bind('<Left>', key_bindings)
window.bind('<Right>', key_bindings)

game.move_snake()

window.mainloop()
