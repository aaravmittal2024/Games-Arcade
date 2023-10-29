import pygame, sys, random

# CONSTANTS
WIDTH, HEIGHT = 900, 500
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FPS = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.init()
background = pygame.Surface((WIDTH, HEIGHT))
background.fill(BLACK)
pygame.draw.aaline(background, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))



class Paddle:
    """ Represents the paddle object in the Pong game. """
    
    def __init__(self, x, y):   
        """ Initialize the paddle with a specific position. """
        self.rect = pygame.Rect(x, y, 20, 120)

    def move(self, speed, direction):
        """ Move the paddle up or down by a given speed. """
        if direction == 'up':
            self.rect.y = max(0, self.rect.y - speed)
        elif direction == 'down':
            self.rect.y = min(HEIGHT - self.rect.height, self.rect.y + speed)

    def draw(self):
        """ Draw the paddle on the screen. """
        pygame.draw.rect(screen, WHITE, self.rect)

    def restart(self):
        """ Reset the paddle to its default vertical position. """
        self.rect.centery = HEIGHT // 2

class Ball:
    """ Represents the ball object in the Pong game. """
    
    def __init__(self):
        """ Initialize the ball at the center of the screen with a random direction. """
        self.rect = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
        self.dx = 15 if random.randint(0, 1) == 0 else -15
        self.dy = random.choice([-5, 5])

    def move(self):
        """ Move the ball by its speed in the x and y direction. """
        self.rect.x += self.dx
        self.rect.y += self.dy

    def wall_collision(self):
        """ Reverse y direction if the ball hits top or bottom of the screen. """
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy = -self.dy

    def paddle_collision(self):
        """ Reverse x direction if the ball hits a paddle. """
        self.dx = -self.dx

    def draw(self):
        """ Draw the ball on the screen. """
        pygame.draw.ellipse(screen, WHITE, self.rect)
        pygame.draw.aaline(screen, WHITE, (self.rect.left, self.rect.centery), (self.rect.right, self.rect.centery))

    def restart(self):
        """ Reset the ball to the center of the screen with a random y direction and reversed x direction. """
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.dy = random.choice([-5, 5])
        self.dx *= -1

class Score:
    """ Represents the score for a player. """
    
    def __init__(self, x, y):
        """ Initialize score at a given position on the screen. """
        self.score = 0
        self.font = pygame.font.SysFont("monospace", 80, bold=True)
        self.x = x
        self.y = y

    def display(self):
        """ Display the current score on the screen. """
        score_display = self.font.render(str(self.score), 0, WHITE)
        screen.blit(score_display, (self.x - score_display.get_width() // 2, self.y))

    def increase(self):
        """ Increase the score by one point. """
        self.score += 1

    def reset(self):
        """ Reset the score to zero. """
        self.score = 0

def main():
    """ Main game loop function. """
    paddle_speed = 10
    paddle1 = Paddle(15, HEIGHT // 2 - 60)
    paddle2 = Paddle(WIDTH - 35, HEIGHT // 2 - 60)
    ball = Ball()
    score1 = Score(WIDTH // 4, 15)
    score2 = Score(3 * WIDTH // 4, 15)

    playing = False

    while True:
        keys = pygame.key.get_pressed()
        
        # Check if game is being played to save computation when game is paused
        if playing:
            if keys[pygame.K_w]:
                paddle1.move(paddle_speed, 'up')
            if keys[pygame.K_s]:
                paddle1.move(paddle_speed, 'down')
            if keys[pygame.K_UP]:
                paddle2.move(paddle_speed, 'up')
            if keys[pygame.K_DOWN]:
                paddle2.move(paddle_speed, 'down')

            ball.move()
            ball.wall_collision()

            if ball.rect.colliderect(paddle1.rect) or ball.rect.colliderect(paddle2.rect):
                ball.paddle_collision()

            if ball.rect.left <= 0:
                score2.increase()
                ball.restart()

            if ball.rect.right >= WIDTH:
                score1.increase()
                ball.restart()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Handle 'P' and 'R' key events in the event loop
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    playing = not playing  # Toggle play/pause
                if event.key == pygame.K_r:
                    playing = False
                    score1.reset()
                    score2.reset()
                    ball.restart()
                    paddle1.restart()
                    paddle2.restart()

        # Draw the background with static elements
        screen.blit(background, (0, 0))

        if playing:
            ball.draw()
            paddle1.draw()
            paddle2.draw()

        score1.display()
        score2.display()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
