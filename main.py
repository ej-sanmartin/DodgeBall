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
          screen.fill((0, 0, 0))
          score_text = font.render(str(math.floor(score)), True, (255, 255, 255))
          pygame.draw.rect(screen, (255, 255, 255), player)
          screen.blit(score_text, (400, 30))
    else:
          screen.fill(get_end_screen_colour())
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


def get_end_screen_colour() -> tuple:
    """Gets the game over screen color.

      Args:
            None
      Returns:
            RGB value of the screen when the game is over
    """
    # Accesses global var, prevents creating new local variable
    global end_screen_colour
    if end_screen_colour is None:
      end_screen_colour = generate_rgb()
    return end_screen_colour


def create_obstacle() -> tuple:
    """Generate new obstacle object along with its randomly generated speed.
    
    Args:
          None
    
    Returns:
          A tuple, (obstacle object, obstacle speed, obstacle's colour)
    """
    obstacle = pygame.Rect(random.randrange(HORIZONTAL_SCREEN_SIZE), 0, 50, 50)
    speed = random.randrange(2, 10)
    color = generate_rgb()
    return (obstacle, speed, color)


def generate_rgb() -> tuple:
    """Generate a random RGB value
    
    Args:
          None
    Returns:
          A tuple that represents an RGB value, (R, G, B)
    """
    r = random.randrange(255)
    g = random.randrange(255)
    b = random.randrange(255)
    
    return (r, g, b)
    

###### Core Pygame loop and state ######

def main() -> None:
  global screen, font, clock, player, is_alive, obstacles, score, end_screen_colour

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
  
  # Colour of background when the game is over. Prevents epileptic siezuring.
  end_screen_colour = None
  
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
        for obstacle, _, _ in obstacles:
            if obstacle.colliderect(player):
                is_alive = False
  
      # Generate new obstacles
      spawn_probability = lerp(0.02, 0.06, (min(score, 10) / 10))
      if random.random() < spawn_probability:
          obstacles.append(create_obstacle());
  
      # Move the obstacles
      for obstacle, speed, _ in obstacles:
          obstacle.y += speed
  
      # Increment the score
      score += .01
  
      handle_draw_score()

      for obstacle, _, color in obstacles:
          pygame.draw.rect(screen, color, obstacle)
      
      # Horizontal line in the middle
      pygame.draw.line(screen, (255, 255, 255), (0, 300), (HORIZONTAL_SCREEN_SIZE, 300), 1)

      pygame.display.update()
  
      # Update the clock
      clock.tick(60)


if __name__ == '__main__':
    main()
