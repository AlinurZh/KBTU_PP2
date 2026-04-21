import pygame
import random
import sys

pygame.init()

# ============================================================
# CONSTANTS
# ============================================================

WIDTH = 400
HEIGHT = 600

# --- Road geometry ---
# Road boundaries
ROAD_LEFT = 80
ROAD_RIGHT = 320
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT  # 240 pixels

# Number of lanes
NUM_LANES = 4
LANE_WIDTH = ROAD_WIDTH // NUM_LANES  # 240 / 4 = 60 pixels per lane

# Center X of each lane (calculated automatically so all lanes are equal)
# Lane 0 center: 80 + 30 = 110
# Lane 1 center: 80 + 90 = 170
# Lane 2 center: 80 + 150 = 230
# Lane 3 center: 80 + 210 = 290
LANES = [ROAD_LEFT + LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(NUM_LANES)]

# Divider line X positions (between lanes, NOT on lane centers)
# Line 0: between lane 0 and 1 → x = 80 + 60 = 140
# Line 1: between lane 1 and 2 → x = 80 + 120 = 200
# Line 2: between lane 2 and 3 → x = 80 + 180 = 260
DIVIDER_LINES = [ROAD_LEFT + LANE_WIDTH * (i + 1) for i in range(NUM_LANES - 1)]

# Colors
WHITE      = (255, 255, 255)
BLACK      = (0, 0, 0)
RED        = (255, 0, 0)
GREEN      = (0, 200, 0)
BLUE       = (0, 0, 255)
YELLOW     = (255, 215, 0)
GRAY       = (100, 100, 100)
DARK_GRAY  = (50, 50, 50)
LIGHT_GRAY = (170, 170, 170)
ORANGE     = (255, 140, 0)
ROAD_COLOR = (40, 40, 40)
GRASS_COLOR = (34, 139, 34)
LINE_COLOR = (200, 200, 200)

# Player settings
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_SPEED = 5
PLAYER_START_X = LANES[1] - PLAYER_WIDTH // 2  # start in lane 1 (second lane)
PLAYER_START_Y = HEIGHT - 100

# Enemy settings
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 60
INITIAL_ENEMY_SPEED = 3
ENEMY_SPEED_INCREMENT = 0.5
MAX_ENEMIES = 4
ENEMY_SPAWN_RATE = 60

# Coin settings (EXTRA TASK)
COIN_RADIUS = 12
COIN_SPEED = 3
COIN_SPAWN_RATE = 90
COIN_SCORE = 10

# Road line animation
LINE_SPEED = 4

# Scoring
SCORE_INCREMENT = 1
LEVEL_THRESHOLD = 500

# ============================================================
# PLAYER CLASS
# ============================================================
class Player:
    """
    The player's car, controlled with arrow keys.
    Moves left and right, constrained to the road.
    """

    def __init__(self):
        """Initialize the player car at lane 1, near the bottom."""
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.speed = PLAYER_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, keys):
        """
        Move left/right based on input.
        Car stays within road boundaries.
        """
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed

        # Clamp to road boundaries
        if self.x < ROAD_LEFT:
            self.x = ROAD_LEFT
        if self.x + self.width > ROAD_RIGHT:
            self.x = ROAD_RIGHT - self.width

        # Update collision rect
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, surface):
        """Draw the player car (blue) with simple details."""
        # Body
        pygame.draw.rect(surface, BLUE,
                         (self.x, self.y, self.width, self.height),
                         border_radius=5)
        # Windshield
        pygame.draw.rect(surface, (0, 0, 150),
                         (self.x + 5, self.y + 8, self.width - 10, 15),
                         border_radius=3)
        # Rear window
        pygame.draw.rect(surface, (0, 0, 150),
                         (self.x + 5, self.y + self.height - 20,
                          self.width - 10, 12),
                         border_radius=3)
        # Headlights
        pygame.draw.rect(surface, YELLOW,
                         (self.x + 3, self.y, 8, 5), border_radius=2)
        pygame.draw.rect(surface, YELLOW,
                         (self.x + self.width - 11, self.y, 8, 5),
                         border_radius=2)


# ============================================================
# ENEMY CLASS
# ============================================================
class Enemy:
    """
    An enemy car that spawns at the top in a random lane
    and moves downward toward the player.
    """

    def __init__(self, speed):
        """
        Initialize enemy in a random lane at the top.

        Args:
            speed: downward movement speed (pixels per frame)
        """
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        # Pick a random lane and center the enemy in it
        lane_center = random.choice(LANES)
        self.x = lane_center - self.width // 2
        self.y = -self.height  # start above screen
        self.speed = speed
        # Random color for variety
        self.color = random.choice([RED, ORANGE, GREEN, (200, 0, 200), (0, 200, 200)])
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        """Move enemy downward each frame."""
        self.y += self.speed
        self.rect.y = self.y

    def is_off_screen(self):
        """Check if enemy has passed the bottom of the screen."""
        return self.y > HEIGHT

    def draw(self, surface):
        """Draw the enemy car with simple details."""
        # Body
        pygame.draw.rect(surface, self.color,
                         (self.x, self.y, self.width, self.height),
                         border_radius=5)
        # Windshield
        pygame.draw.rect(surface, DARK_GRAY,
                         (self.x + 5, self.y + self.height - 20,
                          self.width - 10, 12),
                         border_radius=3)
        # Rear lights
        pygame.draw.rect(surface, RED,
                         (self.x + 3, self.y + self.height - 5, 8, 4),
                         border_radius=2)
        pygame.draw.rect(surface, RED,
                         (self.x + self.width - 11, self.y + self.height - 5,
                          8, 4), border_radius=2)


# ============================================================
# COIN CLASS (EXTRA TASK)
# ============================================================
class Coin:
    """
    EXTRA TASK: A collectible coin that spawns in the center of a random lane.
    Coin never spawns on top of an existing enemy car.
    """

    def __init__(self, enemies):
        """
        Initialize coin in a random lane that is NOT occupied by an enemy
        near the top of the screen.

        Args:
            enemies: list of current Enemy objects to avoid overlap
        """
        self.radius = COIN_RADIUS
        self.y = -self.radius * 2  # start above screen
        self.speed = COIN_SPEED
        self.pulse_timer = 0

        # Pick a lane that doesn't have an enemy near the spawn area
        self.x = self._find_free_lane(enemies)

        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                self.radius * 2, self.radius * 2)

    def _find_free_lane(self, enemies):
        """
        Find a lane center where no enemy is currently near the top.
        If all lanes are blocked, pick a random one anyway.

        Args:
            enemies: list of current Enemy objects

        Returns:
            x coordinate (center of a free lane)
        """
        # Collect all available lanes
        available_lanes = []

        for lane_center in LANES:
            lane_is_free = True

            # Check every enemy to see if it occupies this lane near the top
            for enemy in enemies:
                # Calculate enemy's center x
                enemy_center_x = enemy.x + enemy.width // 2

                # Check if enemy is in the same lane
                same_lane = abs(enemy_center_x - lane_center) < LANE_WIDTH // 2

                # Check if enemy is near the spawn zone (top of screen)
                # We check from above screen (-ENEMY_HEIGHT) to some distance below
                near_top = enemy.y < 150

                if same_lane and near_top:
                    lane_is_free = False
                    break

            if lane_is_free:
                available_lanes.append(lane_center)

        # If there are free lanes, pick one randomly
        if available_lanes:
            return random.choice(available_lanes)
        else:
            # All lanes blocked — pick random lane as fallback
            return random.choice(LANES)

    def move(self):
        """Move coin downward and update animation timer."""
        self.y += self.speed
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius
        self.pulse_timer += 1

    def is_off_screen(self):
        """Check if coin has passed the bottom of the screen."""
        return self.y > HEIGHT + self.radius

    def draw(self, surface):
        """Draw coin as a pulsing yellow circle with '$' symbol."""
        pulse = abs((self.pulse_timer % 20) - 10) / 10.0
        current_radius = int(self.radius - pulse * 2)

        pygame.draw.circle(surface, (218, 165, 32),
                           (self.x, self.y), current_radius + 2)
        pygame.draw.circle(surface, YELLOW,
                           (self.x, self.y), current_radius)
        font_coin = pygame.font.SysFont("Arial", 14, bold=True)
        text = font_coin.render("$", True, (150, 100, 0))
        text_rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, text_rect)


# ============================================================
# ROAD CLASS
# ============================================================
class Road:
    """
    Draws the road background: grass, asphalt, edge lines,
    and animated dashed lane dividers.
    Divider lines are placed exactly between lanes.
    """

    def __init__(self):
        """Initialize road line animation offset."""
        self.line_offset = 0

    def update(self):
        """Animate dashed lines moving downward."""
        self.line_offset += LINE_SPEED
        if self.line_offset >= 40:
            self.line_offset = 0

    def draw(self, surface):
        """Draw complete road: grass, asphalt, edge lines, lane dividers."""
        # Grass background
        surface.fill(GRASS_COLOR)

        # Road asphalt
        pygame.draw.rect(surface, ROAD_COLOR,
                         (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))

        # Solid white edge lines (left and right borders of road)
        pygame.draw.line(surface, WHITE,
                         (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 3)
        pygame.draw.line(surface, WHITE,
                         (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 3)

        # Dashed lane divider lines — placed exactly between lanes
        dash_length = 20
        gap_length = 20
        total = dash_length + gap_length

        for line_x in DIVIDER_LINES:
            y = -total + self.line_offset
            while y < HEIGHT:
                start_y = max(0, y)
                end_y = min(HEIGHT, y + dash_length)
                if end_y > start_y:
                    pygame.draw.line(surface, LINE_COLOR,
                                     (line_x, start_y), (line_x, end_y), 2)
                y += total


# ============================================================
# HUD
# ============================================================
def draw_hud(surface, score, level, coins_collected):
    """
    Draw score (top left), level (top center), coins (top right).
    EXTRA TASK: coin counter with icon in top right corner.
    """
    font = pygame.font.SysFont("Arial", 22, bold=True)

    # Score — top left
    score_text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (10, 10))

    # Level — top center
    level_text = font.render(f"Level: {level}", True, YELLOW)
    level_rect = level_text.get_rect(center=(WIDTH // 2, 22))
    surface.blit(level_text, level_rect)

    # Coins — top right with icon
    coin_text = font.render(f"Coins: {coins_collected}", True, YELLOW)
    coin_rect = coin_text.get_rect(topright=(WIDTH - 10, 10))
    surface.blit(coin_text, coin_rect)

    # Small coin icon next to counter
    icon_x = coin_rect.left - 20
    icon_y = 20
    pygame.draw.circle(surface, YELLOW, (icon_x, icon_y), 8)
    pygame.draw.circle(surface, (218, 165, 32), (icon_x, icon_y), 8, 2)
    tiny_font = pygame.font.SysFont("Arial", 10, bold=True)
    dollar = tiny_font.render("$", True, (150, 100, 0))
    dollar_rect = dollar.get_rect(center=(icon_x, icon_y))
    surface.blit(dollar, dollar_rect)


def draw_game_over(surface, score, level, coins_collected):
    """Draw Game Over overlay with final stats and restart hint."""
    # Dark overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    surface.blit(overlay, (0, 0))

    font_large = pygame.font.SysFont("Arial", 55, bold=True)
    font_medium = pygame.font.SysFont("Arial", 26)
    font_small = pygame.font.SysFont("Arial", 20)

    # Title
    title = font_large.render("GAME OVER", True, RED)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
    surface.blit(title, title_rect)

    # Score
    text = font_medium.render(f"Score: {score}", True, WHITE)
    surface.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))

    # Level
    text = font_medium.render(f"Level: {level}", True, YELLOW)
    surface.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 15)))

    # Coins
    text = font_medium.render(f"Coins: {coins_collected}", True, YELLOW)
    surface.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))

    # Restart hint
    hint = font_small.render("Press ENTER to restart", True, LIGHT_GRAY)
    surface.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100)))


# ============================================================
# DEBUG: print lane layout to verify correctness
# ============================================================
print(f"Road: {ROAD_LEFT} to {ROAD_RIGHT}, width={ROAD_WIDTH}")
print(f"Lane width: {LANE_WIDTH}")
print(f"Lane centers: {LANES}")
print(f"Divider lines: {DIVIDER_LINES}")


# ============================================================
# GAME INITIALIZATION
# ============================================================
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")
clock = pygame.time.Clock()
FPS = 60

# Game state
player = Player()
road = Road()
enemies = []
coins = []
score = 0
level = 1
coins_collected = 0
game_over = False
enemy_spawn_timer = 0
coin_spawn_timer = 0
enemy_speed = INITIAL_ENEMY_SPEED


def reset_game():
    """Reset all game state for a fresh start."""
    global player, enemies, coins, score, level
    global coins_collected, game_over, enemy_speed
    global enemy_spawn_timer, coin_spawn_timer

    player = Player()
    enemies = []
    coins = []
    score = 0
    level = 1
    coins_collected = 0
    game_over = False
    enemy_speed = INITIAL_ENEMY_SPEED
    enemy_spawn_timer = 0
    coin_spawn_timer = 0


# ============================================================
# MAIN GAME LOOP
# ============================================================
running = True
while running:

    # --- EVENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_RETURN:
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False

    # --- LOGIC ---
    if not game_over:
        keys = pygame.key.get_pressed()
        player.move(keys)
        road.update()

        # Score increases each frame
        score += SCORE_INCREMENT

        # Level progression
        new_level = score // LEVEL_THRESHOLD + 1
        if new_level > level:
            level = new_level
            enemy_speed = INITIAL_ENEMY_SPEED + (level - 1) * ENEMY_SPEED_INCREMENT
            print(f"Level Up! Level: {level}, Speed: {enemy_speed}")

        # Spawn enemies
        enemy_spawn_timer += 1
        current_spawn_rate = max(20, ENEMY_SPAWN_RATE - level * 5)
        if enemy_spawn_timer >= current_spawn_rate and len(enemies) < MAX_ENEMIES:
            enemies.append(Enemy(enemy_speed))
            enemy_spawn_timer = 0

        # EXTRA TASK: Spawn coins
        coin_spawn_timer += 1
        if coin_spawn_timer >= COIN_SPAWN_RATE:
            coins.append(Coin(enemies))
            coin_spawn_timer = 0

        # Move enemies
        for enemy in enemies:
            enemy.move()

        # Move coins
        for coin in coins:
            coin.move()

        # Check player vs enemy collision
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                game_over = True
                break

        # EXTRA TASK: Check player vs coin collision
        for coin in coins[:]:
            if player.rect.colliderect(coin.rect):
                coins_collected += 1
                score += COIN_SCORE
                coins.remove(coin)

        # Remove off-screen objects
        enemies = [e for e in enemies if not e.is_off_screen()]
        coins = [c for c in coins if not c.is_off_screen()]

    # --- DRAWING ---
    road.draw(screen)

    for coin in coins:
        coin.draw(screen)

    for enemy in enemies:
        enemy.draw(screen)

    player.draw(screen)

    draw_hud(screen, score, level, coins_collected)

    if game_over:
        draw_game_over(screen, score, level, coins_collected)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()