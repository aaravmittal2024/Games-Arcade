import pygame
import sys
import time
import random

pygame.init()

width = 700
height = 500

display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("Space Invaders")

ship_width = 40
ship_height = 30

background = (0, 0, 0)
white = (244, 246, 247)
yellow = (241, 196, 15)
orange = (186, 74, 0)
blue = (0, 0, 255)
dark_gray = (23, 32, 42)
alien_colors = [(255, 0, 0), (255, 128, 0)]
stars = [(random.randint(0, width), random.randint(0, height), random.randint(1, 3)) for _ in range(100)]

def draw_stars():
    """Draw stars for the space background."""
    for star in stars:
        pygame.draw.circle(display, white, (star[0], star[1]), star[2])

class SpaceShip:
    """Class to represent the player's spaceship."""
    def __init__(self, x, y, w, h, colour):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.colour = colour

    def draw(self):
        """Draw the spaceship on the display."""
        pygame.draw.rect(display, yellow, (self.x + self.w/2 - 8, self.y - 10, 16, 10))
        pygame.draw.rect(display, self.colour, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(display, dark_gray, (self.x + 5, self.y + 6, 10, self.h - 10))
        pygame.draw.rect(display, dark_gray, (self.x + self.w - 15, self.y + 6, 10, self.h - 10))

class Bullet:
    """Class to represent bullets fired by the spaceship."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.d = 10
        self.speed = -10

    def draw(self):
        """Draw the bullet on the display."""
        pygame.draw.ellipse(display, blue, (self.x, self.y, self.d, self.d))

    def move(self):
        """Move the bullet upwards."""
        self.y += self.speed

    def hit(self, x, y, d):
        """Check if the bullet hits an alien."""
        if x < self.x < x + d:
            if y + d > self.y > y:
                return True

class Alien:
    """Class to represent the alien enemies."""
    def __init__(self, x, y, d, color):
        self.x = x
        self.y = y
        self.d = d
        self.color = color
        self.x_dir = 1
        self.speed = 3

    def draw(self):
        """Draw the alien on the display."""
        pygame.draw.ellipse(display, self.color, (self.x, self.y, self.d, self.d))
        pygame.draw.ellipse(display, dark_gray, (self.x + 10, self.y + self.d/3, 8, 8), 2)
        pygame.draw.ellipse(display, dark_gray, (self.x + self.d - 20, self.y + self.d/3, 8, 8), 2)
        pygame.draw.rect(display, dark_gray, (self.x, self.y+self.d-20, 50, 7))

    def move(self):
        """Move the alien horizontally."""
        self.x += self.x_dir*self.speed

    def shift_down(self):
        """Shift the alien downwards."""
        self.y += self.d

def saved():
    """Display the winning message."""
    font = pygame.font.SysFont("Wide Latin", 22)
    font_large = pygame.font.SysFont("Wide Latin", 43)
    text2 = font_large.render("Congratulations!", True, white)
    text = font.render("You Prevented the Alien Invasion!", True, white)
    display.blit(text2, (60, height/2))
    display.blit(text, (45, height/2 + 100))
    pygame.display.update()
    time.sleep(3)

def GameOver():
    """Display the losing message."""
    font = pygame.font.SysFont("Chiller", 50)
    font_large = pygame.font.SysFont("Chiller", 100)
    text2 = font_large.render("Game Over!", True, white)
    text = font.render("You Could not Prevent the Alien Invasion!", True, white)
    display.blit(text2, (180, height/2-50))
    display.blit(text, (45, height/2 + 100))

def game():
    """Main game loop."""
    invasion = False
    ship = SpaceShip(width/2-ship_width/2, height-ship_height - 10, ship_width, ship_height, white)

    bullets = []
    x_move = 0

    aliens = []
    num_aliens_per_row = 8
    num_rows = 2
    d = 30
    space_between_rows = 20

    for row in range(num_rows):
        for i in range(num_aliens_per_row):
            color = alien_colors[row % len(alien_colors)]
            alien = Alien((i+1)*d + i*20, (row+1)*d + row*space_between_rows, d, color)
            aliens.append(alien)

    while not invasion:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_RIGHT:
                    x_move = 5

                if event.key == pygame.K_LEFT:
                    x_move = -5

                if event.key == pygame.K_SPACE:
                    bullet = Bullet(ship.x + ship_width/2 - 5, ship.y)
                    bullets.append(bullet)

            if event.type == pygame.KEYUP:
                x_move = 0

        display.fill(background)
        draw_stars()

        for bullet in bullets:
            bullet.draw()
            bullet.move()

        for alien in list(aliens):
            alien.draw()
            alien.move()
            for bullet in list(bullets):
                if bullet.hit(alien.x, alien.y, alien.d):
                    bullets.remove(bullet)
                    aliens.remove(alien)

        if len(aliens) == 0:
            saved()
            invasion = True

        for alien in aliens:
            if alien.x + d >= width:
                for each_alien in aliens:
                    each_alien.x_dir = -1
                    each_alien.shift_down()

            if alien.x <= 0:
                for each_alien in aliens:
                    each_alien.x_dir = 1
                    each_alien.shift_down()

        try:
            if aliens[0].y + d > height:
                GameOver()
                pygame.display.update()
                time.sleep(3)
                invasion = True
        except Exception as e:
            pass

        ship.x += x_move

        if ship.x < 0:
            ship.x -= x_move
        if ship.x + ship_width > width:
            ship.x -= x_move

        ship.draw()
        pygame.display.update()
        clock.tick(60)

game()
