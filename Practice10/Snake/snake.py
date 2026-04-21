import pygame
import random
import sys

pygame.init()

WIDTH = 600
HEIGHT = 600
CELL = 30
GRID_WIDTH = WIDTH // CELL    # 20 cells
GRID_HEIGHT = HEIGHT // CELL  # 20 cells

# --- Colors (from color_palette.py) ---
colorBLACK  = (0, 0, 0)
colorWHITE  = (255, 255, 255)
colorRED    = (255, 0, 0)
colorGREEN  = (0, 255, 0)
colorYELLOW = (255, 255, 0)
colorGRAY   = (128, 128, 128)
colorBLUE   = (0, 100, 255)
colorDARKGRAY = (60, 60, 60)
colorORANGE = (255, 165, 0)

# --- Game settings ---
INITIAL_FPS = 5           # Starting speed
SPEED_INCREMENT = 1       # Speed increase per level
FOODS_PER_LEVEL = 3       # Foods needed to advance one level
SCORE_PER_FOOD = 10       # Points per food eaten

def generate_walls(level):
    """
    Generate a list of wall positions (Point objects) for each level.
    Level 1: no internal walls, only borders checked separately.
    Level 2+: progressively more complex wall patterns.

    Returns:
        list of Point objects representing wall cell positions.
    """
    walls = []

    if level >= 2:
        # Level 2: two horizontal bars in the middle area
        for x in range(5, 9):
            walls.append(Point(x, 10))          # left bar
            walls.append(Point(x + 7, 10))      # right bar

    if level >= 3:
        # Level 3: add two vertical bars
        for y in range(5, 9):
            walls.append(Point(10, y))           # upper bar
            walls.append(Point(10, y + 7))       # lower bar

    if level >= 4:
        # Level 4: add corner blocks (small L-shapes)
        for i in range(3):
            walls.append(Point(3, 3 + i))        # top-left vertical
            walls.append(Point(3 + i, 3))        # top-left horizontal
            walls.append(Point(16, 3 + i))       # top-right vertical
            walls.append(Point(16 - i, 3))       # top-right horizontal
            walls.append(Point(3, 16 - i))       # bottom-left vertical
            walls.append(Point(3 + i, 16))       # bottom-left horizontal
            walls.append(Point(16, 16 - i))      # bottom-right vertical
            walls.append(Point(16 - i, 16))      # bottom-right horizontal

    if level >= 5:
        # Level 5: add a cross in the center
        for i in range(-2, 3):
            walls.append(Point(10 + i, 10))      # horizontal part
            walls.append(Point(10, 10 + i))      # vertical part

    if level >= 6:
        # Level 6+: add diagonal lines
        for i in range(4):
            walls.append(Point(2 + i, 6 + i))    # left diagonal
            walls.append(Point(17 - i, 6 + i))   # right diagonal

    return walls


class Point:
    """Simple class to store (x, y) grid coordinates."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        """Allow comparison of two Point objects by their coordinates."""
        if other is None:
            return False
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"


class Snake:
    """Represents the snake: a list of body segments moving on the grid."""

    def __init__(self):
        """Initialize snake with 3 segments, moving right."""
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1       # horizontal direction: 1=right, -1=left, 0=none
        self.dy = 0       # vertical direction: 1=down, -1=up, 0=none
        self.should_grow = False  # flag: grow on next move?

    def move(self):
        """
        Move the snake one cell in the current direction.
        If should_grow is True, the tail is kept (snake gets longer).
        """
        # Calculate new head position
        new_head = Point(self.body[0].x + self.dx, self.body[0].y + self.dy)

        # Insert new head at the front
        self.body.insert(0, new_head)

        # Remove tail unless growing
        if self.should_grow:
            self.should_grow = False  # reset flag after growing
        else:
            self.body.pop()          # remove last segment

    def draw(self, surface):
        """Draw the snake: red head, yellow body."""
        # Draw head
        head = self.body[0]
        pygame.draw.rect(surface, colorRED,
                         (head.x * CELL, head.y * CELL, CELL, CELL))
        # Small highlight on head for visibility
        pygame.draw.rect(surface, (255, 100, 100),
                         (head.x * CELL + 4, head.y * CELL + 4, CELL - 8, CELL - 8))

        # Draw body segments
        for segment in self.body[1:]:
            pygame.draw.rect(surface, colorYELLOW,
                             (segment.x * CELL, segment.y * CELL, CELL, CELL))
            # Thin border between segments
            pygame.draw.rect(surface, (200, 200, 0),
                             (segment.x * CELL, segment.y * CELL, CELL, CELL), 1)

    def check_food_collision(self, food):
        """
        Check if the snake's head is on the food.
        Returns True if food was eaten.
        """
        head = self.body[0]
        if head == food.pos:
            self.should_grow = True  # snake will grow on next move
            return True
        return False

    def check_wall_collision(self, walls):
        """
        REQUIREMENT 1: Check if snake's head has hit a border or an internal wall.

        Border collision: head goes outside the grid (x<0, x>=GRID_WIDTH, etc.)
        Wall collision: head lands on any wall cell from the walls list.

        Returns True if collision detected (game over).
        """
        head = self.body[0]

        # --- Check border collision (snake leaving the playing area) ---
        if head.x < 0 or head.x >= GRID_WIDTH:
            return True
        if head.y < 0 or head.y >= GRID_HEIGHT:
            return True

        # --- Check internal wall collision ---
        for wall in walls:
            if head == wall:
                return True

        return False

    def check_self_collision(self):
        """
        Check if the snake's head overlaps with any body segment.
        Returns True if snake has bitten itself.
        """
        head = self.body[0]
        for segment in self.body[1:]:
            if head == segment:
                return True
        return False

    def occupies(self, point):
        """Check if a given point is occupied by any part of the snake."""
        for segment in self.body:
            if segment == point:
                return True
        return False


class Food:
    """Represents a food item that the snake can eat."""

    def __init__(self):
        """Initialize food at a default position."""
        self.pos = Point(5, 5)

    def draw(self, surface):
        """Draw the food as a green square on the screen."""
        pygame.draw.rect(surface, colorGREEN,
                         (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))
        # Inner highlight
        pygame.draw.rect(surface, (100, 255, 100),
                         (self.pos.x * CELL + 4, self.pos.y * CELL + 4,
                          CELL - 8, CELL - 8))

    def generate_random_pos(self, snake, walls):
        """
        REQUIREMENT 2: Generate a random position for food so that
        it does NOT fall on a wall or on the snake.

        Uses a while loop to keep generating until a valid position is found.

        Args:
            snake: Snake object (to check body positions)
            walls: list of Point objects (wall positions to avoid)
        """
        while True:
            # Generate random coordinates within the grid
            new_x = random.randint(0, GRID_WIDTH - 1)
            new_y = random.randint(0, GRID_HEIGHT - 1)
            new_pos = Point(new_x, new_y)

            # Check 1: is the position on the snake?
            if snake.occupies(new_pos):
                continue  # try again

            # Check 2: is the position on a wall?
            on_wall = False
            for wall in walls:
                if new_pos == wall:
                    on_wall = True
                    break
            if on_wall:
                continue  # try again

            # Position is valid — place food here
            self.pos = new_pos
            return


def draw_grid(surface):
    """Draw a simple grid with thin gray lines."""
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            pygame.draw.rect(surface, colorDARKGRAY,
                             (i * CELL, j * CELL, CELL, CELL), 1)


def draw_walls(surface, walls):
    """
    Draw all wall cells as dark gray blocks with a subtle 3D effect.
    """
    for wall in walls:
        rect = pygame.Rect(wall.x * CELL, wall.y * CELL, CELL, CELL)
        # Main wall color
        pygame.draw.rect(surface, colorGRAY, rect)
        # Light edge on top and left (3D highlight)
        pygame.draw.line(surface, (180, 180, 180), rect.topleft, rect.topright, 1)
        pygame.draw.line(surface, (180, 180, 180), rect.topleft, rect.bottomleft, 1)
        # Dark edge on bottom and right (3D shadow)
        pygame.draw.line(surface, (40, 40, 40), rect.bottomleft, rect.bottomright, 1)
        pygame.draw.line(surface, (40, 40, 40), rect.topright, rect.bottomright, 1)


def draw_ui(surface, score, level, fps, foods_eaten):
    """
    REQUIREMENT 5: Draw score counter, level counter, speed, and food progress.
    Displayed as a semi-transparent bar at the top of the screen.
    """
    # Semi-transparent header background
    header = pygame.Surface((WIDTH, 32), pygame.SRCALPHA)
    header.fill((0, 0, 0, 150))
    surface.blit(header, (0, 0))

    font = pygame.font.SysFont("Arial", 20, bold=True)

    # Score — left side
    score_text = font.render(f"Score: {score}", True, colorWHITE)
    surface.blit(score_text, (10, 5))

    # Level — center
    level_text = font.render(f"Level: {level}", True, colorYELLOW)
    level_rect = level_text.get_rect(center=(WIDTH // 2, 16))
    surface.blit(level_text, level_rect)

    # Food progress and speed — right side
    info_text = font.render(
        f"Food: {foods_eaten}/{FOODS_PER_LEVEL}  Speed: {fps}",
        True, colorWHITE
    )
    info_rect = info_text.get_rect(topright=(WIDTH - 10, 5))
    surface.blit(info_text, info_rect)


def draw_game_over(surface, score, level):
    """
    Draw the Game Over overlay with final score and restart instructions.
    """
    # Dark overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))

    font_large = pygame.font.SysFont("Arial", 60, bold=True)
    font_medium = pygame.font.SysFont("Arial", 28)
    font_small = pygame.font.SysFont("Arial", 22)

    # "Game Over" text
    text1 = font_large.render("Game Over", True, colorRED)
    rect1 = text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
    surface.blit(text1, rect1)

    # Final score
    text2 = font_medium.render(f"Score: {score}    Level: {level}", True, colorWHITE)
    rect2 = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    surface.blit(text2, rect2)

    # Restart hint
    text3 = font_small.render("Press ENTER to restart", True, colorGRAY)
    rect3 = text3.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 45))
    surface.blit(text3, rect3)


def draw_level_up(surface, level):
    """
    Show a brief 'Level Up!' announcement overlay.
    """
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    surface.blit(overlay, (0, 0))

    font = pygame.font.SysFont("Arial", 50, bold=True)
    text = font.render(f"Level {level}!", True, colorYELLOW)
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    surface.blit(text, rect)


# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# --- Game state variables ---
snake = Snake()
food = Food()
score = 0
level = 1
foods_eaten_this_level = 0
FPS = INITIAL_FPS
game_over = False
level_up_timer = 0       # frames remaining to show "Level Up!" message

# Generate walls for current level
walls = generate_walls(level)

# Generate first food position (not on snake, not on walls)
food.generate_random_pos(snake, walls)


def reset_game():
    """Reset all game state to start a fresh game."""
    global snake, food, score, level, foods_eaten_this_level
    global FPS, game_over, walls, level_up_timer

    snake = Snake()
    food = Food()
    score = 0
    level = 1
    foods_eaten_this_level = 0
    FPS = INITIAL_FPS
    game_over = False
    level_up_timer = 0
    walls = generate_walls(level)
    food.generate_random_pos(snake, walls)


def advance_level():
    """
    REQUIREMENT 3 & 4: Advance to next level.
    - Reset food counter
    - Increase speed
    - Generate new wall layout
    - Respawn food in valid location
    - Show level-up message
    """
    global level, foods_eaten_this_level, FPS, walls, level_up_timer

    level += 1
    foods_eaten_this_level = 0

    # REQUIREMENT 4: Increase speed
    FPS += SPEED_INCREMENT

    # Generate new walls for the new level
    walls = generate_walls(level)

    # Check if snake is inside a new wall — if so, game continues
    # but food must be respawned in a valid spot
    food.generate_random_pos(snake, walls)

    level_up_timer = 10

    print(f"Level Up! Level: {level}, Speed: {FPS}")


running = True
while running:

    # --- EVENT HANDLING ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_over:
                # Restart game on Enter
                if event.key == pygame.K_RETURN:
                    reset_game()
            else:
                # Direction controls with 180-degree turn prevention
                if event.key == pygame.K_RIGHT and snake.dx != -1:
                    snake.dx = 1
                    snake.dy = 0
                elif event.key == pygame.K_LEFT and snake.dx != 1:
                    snake.dx = -1
                    snake.dy = 0
                elif event.key == pygame.K_DOWN and snake.dy != -1:
                    snake.dx = 0
                    snake.dy = 1
                elif event.key == pygame.K_UP and snake.dy != 1:
                    snake.dx = 0
                    snake.dy = -1

    # --- GAME LOGIC (only when game is active) ---
    if not game_over:

        # Move the snake
        snake.move()

        # REQUIREMENT 1: Check border and wall collision
        if snake.check_wall_collision(walls):
            game_over = True
            print(f"Game Over! Hit a wall. Score: {score}, Level: {level}")

        # Check self collision
        elif snake.check_self_collision():
            game_over = True
            print(f"Game Over! Hit yourself. Score: {score}, Level: {level}")

        # Check food collision
        elif snake.check_food_collision(food):
            # REQUIREMENT 5: Update score
            score += SCORE_PER_FOOD
            foods_eaten_this_level += 1
            print(f"Food eaten! Score: {score}, "
                  f"Food this level: {foods_eaten_this_level}/{FOODS_PER_LEVEL}")

            # REQUIREMENT 3: Check if level should advance
            if foods_eaten_this_level >= FOODS_PER_LEVEL:
                advance_level()
            else:
                # REQUIREMENT 2: Respawn food not on wall or snake
                food.generate_random_pos(snake, walls)

        # Decrease level-up message timer
        if level_up_timer > 0:
            level_up_timer -= 1

    # --- DRAWING ---
    # Clear screen
    screen.fill(colorBLACK)

    # Draw grid
    draw_grid(screen)

    # Draw walls for current level
    draw_walls(screen, walls)

    # Draw food
    food.draw(screen)

    # Draw snake
    snake.draw(screen)

    # REQUIREMENT 5: Draw score and level counters
    draw_ui(screen, score, level, FPS, foods_eaten_this_level)

    # Show "Level Up!" announcement
    if level_up_timer > 0 and not game_over:
        draw_level_up(screen, level)

    # Show Game Over screen
    if game_over:
        draw_game_over(screen, score, level)

    # Update display
    pygame.display.flip()

    # Control game speed (REQUIREMENT 4: speed increases with level)
    clock.tick(FPS)

pygame.quit()
sys.exit()