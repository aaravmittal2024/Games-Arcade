import pygame
import sys
from math import *
import random

# Initialize pygame
pygame.init()

# Screen dimensions and properties
width = 660
height = 360
outerHeight = 400
margin = 30
display = pygame.display.set_mode((width, outerHeight))
pygame.display.set_caption("8 Ball Pool")
clock = pygame.time.Clock()

# Define colors
background = (51, 51, 51)
white = (236, 240, 241)
gray = (123, 125, 125)
black = (23, 32, 42)
yellow = (244, 208, 63)
blue = (52, 152, 219)
red = (203, 67, 53)
purple = (136, 78, 160)
orange = (230, 126, 34)
green = (40, 180, 99)
brown = (100, 30, 22)
stickColor = (249, 231, 159)
colors = [yellow, blue, red, purple, orange, green, brown, black, yellow, blue, red, purple, orange, green, brown]

# Ball properties
balls, noBalls, radius, friction = [], 15, 10, 0.005


class Ball:
    """Represents a Ball on the pool table."""
    def __init__(self, x, y, speed, color, angle, ballNum):
        self.x = x + radius
        self.y = y + radius
        self.color = color
        self.angle = angle
        self.speed = speed
        self.ballNum = ballNum
        self.font = pygame.font.SysFont("Agency FB", 10)

    def draw(self, x, y):
        """Draws the ball on the screen."""
        pygame.draw.ellipse(display, self.color, (x - radius, y - radius, radius*2, radius*2))
        if self.color == black or self.ballNum == "cue":
            ballNo = self.font.render(str(self.ballNum), True, white)
            display.blit(ballNo, (x - 5, y - 5))
        else:
            ballNo = self.font.render(str(self.ballNum), True, black)
            if self.ballNum > 9:
                display.blit(ballNo, (x - 6, y - 5))
            else:
                display.blit(ballNo, (x - 5, y - 5))

    def move(self):
        """Moves the ball based on its speed and angle."""
        self.speed = max(self.speed - friction, 0)
        self.x += self.speed * cos(radians(self.angle))
        self.y += self.speed * sin(radians(self.angle))

        # Collision with Borders
        x_bound_right = width - radius - margin
        x_bound_left = radius + margin
        y_bound_bottom = height - radius - margin
        y_bound_top = radius + margin

        if self.x <= x_bound_left or self.x >= x_bound_right:
            self.angle = 180 - self.angle
            self.x = min(max(self.x, x_bound_left), x_bound_right)

        if self.y <= y_bound_top or self.y >= y_bound_bottom:
            self.angle = 360 - self.angle
            self.y = min(max(self.y, y_bound_top), y_bound_bottom)


class Pockets:
    """Represents pockets on the pool table."""
    def __init__(self, x, y, color):
        self.r = margin/2
        self.x = x + self.r + 10
        self.y = y + self.r + 10
        self.color = color

    def draw(self):
        """Draws the pocket on the screen."""
        pygame.draw.ellipse(display, self.color, (self.x - self.r, self.y - self.r, self.r*2, self.r*2))

    def checkPut(self):
        """Checks if any ball has entered the pocket."""
        global balls
        to_remove = []
        for ball in balls:
            dx = self.x - ball.x
            dy = self.y - ball.y
            squared_dist = dx**2 + dy**2
            if squared_dist < (self.r + radius)**2:
                if ball.ballNum == 8:
                    gameOver()
                else:
                    to_remove.append(ball)
        for ball in to_remove:
            balls.remove(ball)

class CueStick:
    """Represents the cue stick used to hit balls."""
    def __init__(self, x, y, length, color):
        self.x = x
        self.y = y
        self.length = length
        self.color = color
        self.tangent = 0

    def applyForce(self, cueBall, force):
        """Applies a force to the cue ball."""
        cueBall.angle = self.tangent
        cueBall.speed = force

    def draw(self, cuex, cuey):
        """Draws the cue stick on the screen."""
        self.x, self.y = pygame.mouse.get_pos()
        self.tangent = (degrees(atan2((cuey - self.y), (cuex - self.x))))
        pygame.draw.line(display, white, (cuex + self.length*cos(radians(self.tangent)), cuey + self.length*sin(radians(self.tangent))), (cuex, cuey), 1)
        pygame.draw.line(display, self.color, (self.x, self.y), (cuex, cuey), 3)

def collision(ball1, ball2):
    """Checks if two balls have collided."""
    dist = ((ball1.x - ball2.x)**2 + (ball1.y - ball2.y)**2)**0.5
    if dist <= radius*2: return True
    else: return False

def checkCueCollision(cueBall):
    """Checks if the cue ball has collided with any other ball."""
    for ball in balls:
        if collision(cueBall, ball):
            # Collision logic
            dx = ball.x - cueBall.x
            dy = ball.y - cueBall.y
            
            if dx == 0:
                angleIncline = 180
            else:
                tangent = degrees(atan(dy / dx)) + 90
                angle = tangent + 90
                
                # Update speeds based on collision physics
                u1, u2 = ball.speed, cueBall.speed
                ball.speed = ((u1 * cos(radians(ball.angle)))**2 + (u2 * sin(radians(cueBall.angle)))**2)**0.5
                cueBall.speed = ((u2 * cos(radians(cueBall.angle)))**2 + (u1 * sin(radians(ball.angle)))**2)**0.5

                # Update angles based on the tangent at the point of collision
                ball.angle = 2 * tangent - ball.angle
                cueBall.angle = 2 * tangent - cueBall.angle

                # Update positions
                ball.x += ball.speed * sin(radians(angle))
                ball.y -= ball.speed * cos(radians(angle))
                cueBall.x -= cueBall.speed * sin(radians(angle))
                cueBall.y += cueBall.speed * cos(radians(angle))

def checkCollision():
    """Checks if any two balls on the table have collided."""
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            if collision(balls[i], balls[j]):
                # Collision logic
                ball1, ball2 = balls[i], balls[j]

                dx = ball1.x - ball2.x
                dy = ball1.y - ball2.y

                if dx == 0:
                    angleIncline = 180
                else:
                    tangent = degrees(atan(dy / dx)) + 90
                    angle = tangent + 90

                    # Update speeds based on collision physics
                    u1, u2 = ball1.speed, ball2.speed
                    ball1.speed = ((u1 * cos(radians(ball1.angle)))**2 + (u2 * sin(radians(ball2.angle)))**2)**0.5
                    ball2.speed = ((u2 * cos(radians(ball2.angle)))**2 + (u1 * sin(radians(ball1.angle)))**2)**0.5

                    # Update angles based on the tangent at the point of collision
                    ball1.angle = 2 * tangent - ball1.angle
                    ball2.angle = 2 * tangent - ball2.angle

                    # Update positions
                    ball1.x += ball1.speed * sin(radians(angle))
                    ball1.y -= ball1.speed * cos(radians(angle))
                    ball2.x -= ball2.speed * sin(radians(angle))
                    ball2.y += ball2.speed * cos(radians(angle))

def border():
    """Draws the borders of the pool table."""
    pygame.draw.rect(display, gray, (0, 0, width, 30))
    pygame.draw.rect(display, gray, (0, 0, 30, height))
    pygame.draw.rect(display, gray, (width - 30, 0, width, height))
    pygame.draw.rect(display, gray, (0, height - 30, width, height))

def score():
    """Displays the score on the screen."""
    font = pygame.font.SysFont("Agency FB", 30)

    pygame.draw.rect(display, (51, 51, 51), (0, height, width, outerHeight))
    for i in range(len(balls)):
        balls[i].draw((i + 1)*2*(radius + 1), height + radius + 10)

    text = font.render("Remaining Balls: " + str(len(balls)), True, stickColor)
    display.blit(text, (width/2 + 50, height + radius/2))

def reset():
    """Resets the pool table to its initial state."""
    global balls, noBalls
    noBalls = 15
    balls = []

    s = 70
    rows = 5
    positions = [(row, col) for row in range(rows) for col in range(-row, row + 1, 2)]

    for i, (row, col) in enumerate(positions):
        x = s + col * radius
        y = height / 2 - row * 1.5 * radius
        ball = Ball(x, y, 0, colors[i], 0, i + 1)
        balls.append(ball)


def gameOver():
    """Displays the game over screen."""
    font = pygame.font.SysFont("Agency FB", 75)
    if len(balls) == 0: text = font.render("You Won!", True, (133, 193, 233))
    else: text = font.render("You Lost! Black in Hole!", True, (241, 148, 138))
    text_position = (50, height / 2)
    display.blit(text, text_position)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    close()
                    running = False
                elif event.key == pygame.K_r:
                    poolTable()
                    running = False
        pygame.display.update()
        clock.tick()


def close():
    """Closes the game window."""
    pygame.quit()
    sys.exit()

def poolTable():
    """Main game loop function."""
    reset()

    pockets = [
        Pockets(x - 2*radius if x == width/2 else x, y, black)
        for x, y in [
            (0, 0),
            (width/2, 0),
            (width - margin - 5, 0),
            (0, height - margin - 5),
            (width/2, height - margin - 5),
            (width - margin - 5, height - margin - 5)
        ]
    ]

    cueBall = Ball(width/2, height/2, 0, white, 0, "cue")
    cueStick = CueStick(0, 0, 100, stickColor)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    poolTable()

            if event.type == pygame.MOUSEBUTTONDOWN:
                start_pos = (cueBall.x, cueBall.y)
                end_pos = pygame.mouse.get_pos()
                force = min(((start_pos[0] - end_pos[0])**2 + (start_pos[1] - end_pos[1])**2)**0.5 / 10.0, 10)
                cueStick.applyForce(cueBall, force)

        display.fill(background)
        cueBall.draw(cueBall.x, cueBall.y)
        cueBall.move()

        if cueBall.speed <= 0:
            cueStick.draw(cueBall.x, cueBall.y)

        for ball in balls:
            ball.draw(ball.x, ball.y)
            ball.move()

        checkCollision()
        checkCueCollision(cueBall)
        border()

        for pocket in pockets:
            pocket.draw()
            pocket.checkPut()

        if len(balls) == 1 and balls[0].ballNum == 8:
            gameOver()

        score()

        pygame.display.update()
        clock.tick(60)


poolTable()
