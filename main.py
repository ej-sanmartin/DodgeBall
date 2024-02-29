import math
import pygame
import random

###### Constants ######

HORIZONTAL_SCREEN_SIZE = 800
VERTICAL_SCREEN_SIZE = 600
PLAYER_SIZE = 50
VERTICAL_MIDPOINT = (VERTICAL_SCREEN_SIZE / 2)

###### Helper methods ######

def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolate on the scale given by a to b, using t as the point on that scale.
    
    Args:
              a: starting point
              b: ending point
              t: point in time. 1 is 100% and will output whatever b is. Can output more than b
    
    Returns:
          value along the specified range around and within a and b
    """
    return (1 - t) * a + t * b


def handle_draw_score() -> None:
    if is_alive:
          score_text = font.render(str(math.floor(score)), True, (255, 255, 255))
          pygame.draw.rect(screen, (255, 255, 255), player)
          screen.blit(score_text, (400, 30))
    else:
          score_text = font.render("Game Over", True, (255, 255, 255))
          screen.blit(score_text, (350, 30))


def handle_player_movement() -> None:
    # Move the player
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        player.x -= 5
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        player.x += 5
    if pygame.key.get_pressed()[pygame.K_UP]:
        player.y -= 5
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        player.y += 5
  
    # Keep the player inside the screen
    player.x = max(0, player.x)
    player.x = min(HORIZONTAL_SCREEN_SIZE - PLAYER_SIZE, player.x)
    player.y = max(0, player.y)
    player.y = min(VERTICAL_SCREEN_SIZE - PLAYER_SIZE, player.y)
  
    # Keep the player from crossing the line
    if player.y <= VERTICAL_MIDPOINT:
        player.y = VERTICAL_MIDPOINT + 1


def create_obstacle() -> tuple:
    """Generate new obstacle object along with its randomly generated speed.
    
    Args:
          None
    
    Returns:
          A tuple, (obstacle object, obstacle speed)
    """
    obstacle = pygame.Rect(random.randrange(HORIZONTAL_SCREEN_SIZE), 0, 50, 50)
    speed = random.randrange(2, 10)
    return (obstacle, speed)
    

###### Core Pygame loop and state ######

# Initialize Pygame
pygame.init()

# Set the screen size
screen = pygame.display.set_mode((HORIZONTAL_SCREEN_SIZE, VERTICAL_SCREEN_SIZE))

# Set up font settings
font = pygame.font.SysFont("arial", 20)

# Set the title of the game
pygame.display.set_caption("Duckie's Game")

# Create a clock object
clock = pygame.time.Clock()

# Create a player object
player = pygame.Rect(400, 500, PLAYER_SIZE, PLAYER_SIZE)

# Is the player still alive?
is_alive = True

# Create a list of obstacles
obstacles = []

# Create a score variable
score = 0

# Game loop
while True:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Only runs while player is alive and the game is still going
    if is_alive:
      handle_player_movement()

      # Check for collisions
      for obstacle, _ in obstacles:
          if obstacle.colliderect(player):
              is_alive = False

    # Generate new obstacles
    spawn_probability = lerp(0.02, 0.06, (min(score, 10) / 10))
    if random.random() < spawn_probability:
        obstacles.append(create_obstacle());

    # Move the obstacles
    for obstacle, speed in obstacles:
        obstacle.y += speed

    # Increment the score
    score += .01

    # Draw the screen
    screen.fill((0, 0, 0))

    handle_draw_score()

    for obstacle, _ in obstacles:
        pygame.draw.rect(screen, (255, 0, 0), obstacle)
    
    # Horizontal line in the middle
    pygame.draw.line(screen, (255, 255, 255), (0, 300), (HORIZONTAL_SCREEN_SIZE, 300), 1)

    pygame.display.update()

    # Update the clock
    clock.tick(60)
