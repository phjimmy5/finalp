import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BIRD_WIDTH = 68
BIRD_HEIGHT = 60
PIPE_WIDTH = 52
PIPE_HEIGHT = 320
PIPE_GAP = 175
GRAVITY = 0.25
JUMP = -6.5
PIPE_SPEED = -3
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load bird image
bird_img = pygame.image.load("bird.png")  # Ensure you have a bird image file called bird.png
bird_img = pygame.transform.scale(bird_img, (BIRD_WIDTH, BIRD_HEIGHT))

# Pipe Class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.top = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - self.height - PIPE_GAP)

    def move(self):
        self.x += PIPE_SPEED
        self.top.x = self.x
        self.bottom.x = self.x

    def draw(self):
        pygame.draw.rect(screen, (0, 255, 0), self.top)
        pygame.draw.rect(screen, (0, 255, 0), self.bottom)

    def off_screen(self):
        return self.x + PIPE_WIDTH < 0

# Bird Class
class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.rect = pygame.Rect(self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT)

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y

    def jump(self):
        self.velocity = JUMP

    def draw(self):
        screen.blit(bird_img, (self.x, self.y))

    def is_colliding(self, pipes):
        if self.y < 0 or self.y > SCREEN_HEIGHT - BIRD_HEIGHT:
            return True
        for pipe in pipes:
            if self.rect.colliderect(pipe.top) or self.rect.colliderect(pipe.bottom):
                return True
        return False

# Display start message
def display_start_message():
    font = pygame.font.SysFont(None, 48)
    start_text = font.render("Press SPACE to Start", True, BLACK)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - start_text.get_height() // 2))
    pygame.display.update()

# Main game loop
def game():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = []
    score = 0
    running = True
    frame_count = 0
    game_started = False  # New flag to track if game has started

    # Intro screen
    while not game_started:
        screen.fill(WHITE)
        bird.draw()  # Show bird but do not update it
        display_start_message()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Start game on spacebar
                    game_started = True
        
        clock.tick(FPS)

    # Actual game loop
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        # Bird update
        bird.update()
        bird.draw()

        # Pipe creation and update
        if frame_count % 90 == 0:
            pipes.append(Pipe())

        for pipe in pipes:
            pipe.move()
            pipe.draw()

        pipes = [pipe for pipe in pipes if not pipe.off_screen()]

        # Collision check
        if bird.is_colliding(pipes):
            running = False

        # Display score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Increment score for passing pipes
        if pipes and bird.x > pipes[0].x + PIPE_WIDTH:
            pipes.pop(0)
            score += 1

        pygame.display.update()
        clock.tick(FPS)
        frame_count += 1

    pygame.quit()

# Run the game
if __name__ == "__main__":
    game()
