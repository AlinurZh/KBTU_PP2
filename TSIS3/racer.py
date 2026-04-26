import pygame
pygame.init()

import random
import sys
from pygame.locals import *
from persistence import load_settings, save_score

FPS = 60
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)
RED = (220, 40, 40)
GREEN = (40, 180, 40)
BLUE = (40, 80, 220)
GRAY = (120, 120, 120)
ORANGE = (255, 140, 0)
PURPLE = (150, 60, 200)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

font_big = pygame.font.SysFont("Verdana", 45)
font = pygame.font.SysFont("Verdana", 25)
font_small = pygame.font.SysFont("Verdana", 18)


def draw_text(text, x, y, size="small", color=BLACK):
    if size == "big":
        img = font_big.render(text, True, color)
    elif size == "medium":
        img = font.render(text, True, color)
    else:
        img = font_small.render(text, True, color)

    screen.blit(img, (x, y))


class Player(pygame.sprite.Sprite):
    def __init__(self, settings):
        super().__init__()

        if settings["car_color"] == "black":
            image_path = "images/Player_Black.png"
        elif settings["car_color"] == "green":
            image_path = "images/Player_Green.png"
        else:
            image_path = "images/Player_Blue.png"

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (50, 90))

        self.rect = self.image.get_rect()
        self.rect.center = (200, 520)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-6, 0)

        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(6, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

        self.image = pygame.image.load("images/Enemy.png")
        self.image = pygame.transform.scale(self.image, (50, 90))
        self.rect = self.image.get_rect()
        self.speed = speed

        self.safe_spawn()

    def safe_spawn(self):
        self.rect.center = (
            random.randint(40, SCREEN_WIDTH - 40),
            random.randint(-600, -80)
        )

    def move(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > SCREEN_HEIGHT:
            self.safe_spawn()


class Coin(pygame.sprite.Sprite):
    def __init__(self, image_path, value, speed):
        super().__init__()

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()

        self.value = value
        self.speed = speed

        self.rect.center = (
            random.randint(40, SCREEN_WIDTH - 40),
            random.randint(-500, -50)
        )

    def move(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (
                random.randint(40, SCREEN_WIDTH - 40),
                random.randint(-500, -50)
            )


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, kind, speed):
        super().__init__()

        self.kind = kind
        self.speed = speed

        if kind == "oil":
            self.image = pygame.Surface((60, 30))
            self.image.fill(BLACK)
        elif kind == "barrier":
            self.image = pygame.Surface((70, 25))
            self.image.fill(ORANGE)
        else:
            self.image = pygame.Surface((50, 35))
            self.image.fill(GRAY)

        self.rect = self.image.get_rect()
        self.rect.center = (
            random.randint(50, SCREEN_WIDTH - 50),
            random.randint(-700, -100)
        )

    def move(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (
                random.randint(50, SCREEN_WIDTH - 50),
                random.randint(-700, -100)
            )


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, kind, speed):
        super().__init__()

        self.kind = kind
        self.speed = speed

        self.image = pygame.Surface((35, 35))

        if kind == "nitro":
            self.image.fill(BLUE)
        elif kind == "shield":
            self.image.fill(PURPLE)
        else:
            self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.spawn_time = pygame.time.get_ticks()

        self.rect.center = (
            random.randint(40, SCREEN_WIDTH - 40),
            random.randint(-800, -200)
        )

    def move(self):
        self.rect.move_ip(0, self.speed)

        now = pygame.time.get_ticks()

        if self.rect.top > SCREEN_HEIGHT or now - self.spawn_time > 7000:
            self.rect.center = (
                random.randint(40, SCREEN_WIDTH - 40),
                random.randint(-800, -200)
            )
            self.spawn_time = pygame.time.get_ticks()


def game_loop(player_name):
    settings = load_settings()

    background = pygame.image.load("images/AnimatedStreet.png")

    if settings["difficulty"] == "easy":
        base_speed = 4
        enemy_count = 1
    elif settings["difficulty"] == "hard":
        base_speed = 6
        enemy_count = 3
    else:
        base_speed = 5
        enemy_count = 2

    speed = base_speed
    score = 0
    coins = 0
    distance = 0
    finish_distance = 1500

    active_power = None
    power_end_time = 0
    shield = False

    player = Player(settings)

    enemies = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    all_sprites.add(player)

    for i in range(enemy_count):
        enemy = Enemy(speed)
        enemies.add(enemy)
        all_sprites.add(enemy)

    coin1 = Coin("images/Power1.png", 1, speed)
    coin2 = Coin("images/Power2.png", 2, speed)

    coins_group.add(coin1, coin2)
    all_sprites.add(coin1, coin2)

    for i in range(2):
        obs = Obstacle(random.choice(["oil", "barrier", "pothole"]), speed)
        obstacles.add(obs)
        all_sprites.add(obs)

    for kind in ["nitro", "shield", "repair"]:
        power = PowerUp(kind, speed)
        powerups.add(power)
        all_sprites.add(power)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        distance += speed * 0.05
        score = coins * 10 + int(distance)

        if distance > 500 and len(enemies) < enemy_count + 1:
            enemy = Enemy(speed)
            enemies.add(enemy)
            all_sprites.add(enemy)

        if distance > 900 and len(obstacles) < 4:
            obs = Obstacle(random.choice(["oil", "barrier", "pothole"]), speed)
            obstacles.add(obs)
            all_sprites.add(obs)

        now = pygame.time.get_ticks()

        if active_power == "nitro" and now > power_end_time:
            active_power = None
            speed = base_speed + distance / 600

        screen.blit(background, (0, 0))

        for entity in all_sprites:
            entity.move()
            screen.blit(entity.image, entity.rect)

        coin_hit = pygame.sprite.spritecollideany(player, coins_group)

        if coin_hit:
            coins += coin_hit.value
            coin_hit.rect.center = (
                random.randint(40, SCREEN_WIDTH - 40),
                random.randint(-500, -50)
            )

        power_hit = pygame.sprite.spritecollideany(player, powerups)

        if power_hit and active_power is None:
            if power_hit.kind == "nitro":
                active_power = "nitro"
                power_end_time = pygame.time.get_ticks() + 4000
                speed += 3

            elif power_hit.kind == "shield":
                active_power = "shield"
                shield = True

            elif power_hit.kind == "repair":
                score += 50

                for obs in obstacles:
                    obs.rect.center = (
                        random.randint(50, SCREEN_WIDTH - 50),
                        random.randint(-700, -100)
                    )
                    break

            power_hit.rect.center = (
                random.randint(40, SCREEN_WIDTH - 40),
                random.randint(-900, -200)
            )
            power_hit.spawn_time = pygame.time.get_ticks()

        obstacle_hit = pygame.sprite.spritecollideany(player, obstacles)

        if obstacle_hit:
            if obstacle_hit.kind == "oil":
                player.rect.x += random.choice([-40, 40])
                obstacle_hit.rect.center = (
                    random.randint(50, SCREEN_WIDTH - 50),
                    random.randint(-700, -100)
                )

            elif obstacle_hit.kind == "barrier":
                if shield:
                    shield = False
                    active_power = None
                    obstacle_hit.rect.center = (
                        random.randint(50, SCREEN_WIDTH - 50),
                        random.randint(-700, -100)
                    )
                else:
                    if settings["sound"]:
                        try:
                            pygame.mixer.Sound("sounds/crash.wav").play()
                        except:
                            pass

                    from ui import game_over_screen
                    game_over_screen(player_name, score, distance, coins)
                    return

            elif obstacle_hit.kind == "pothole":
                speed = max(3, speed - 1)
                obstacle_hit.rect.center = (
                    random.randint(50, SCREEN_WIDTH - 50),
                    random.randint(-700, -100)
                )

        enemy_hit = pygame.sprite.spritecollideany(player, enemies)

        if enemy_hit:
            if shield:
                shield = False
                active_power = None
                enemy_hit.safe_spawn()
            else:
                if settings["sound"]:
                    try:
                        pygame.mixer.Sound("sounds/crash.wav").play()
                    except:
                        pass

                from ui import game_over_screen
                game_over_screen(player_name, score, distance, coins)
                return

        remaining = max(0, finish_distance - int(distance))

        draw_text(f"Score: {score}", 10, 10)
        draw_text(f"Coins: {coins}", 10, 35)
        draw_text(f"Distance: {int(distance)}m", 10, 60)
        draw_text(f"Remaining: {remaining}m", 10, 85)

        if active_power == "nitro":
            left = max(0, int((power_end_time - pygame.time.get_ticks()) / 1000))
            draw_text(f"Power: Nitro {left}s", 10, 110, color=BLUE)
        elif active_power == "shield":
            draw_text("Power: Shield", 10, 110, color=PURPLE)
        else:
            draw_text("Power: None", 10, 110)

        if distance >= finish_distance:
            save_score(player_name, score + 500, distance)
            screen.fill(GREEN)
            draw_text("You finished!", 55, 230, "big", WHITE)
            pygame.display.update()
            pygame.time.delay(2000)
            return

        pygame.display.update()
        clock.tick(FPS)