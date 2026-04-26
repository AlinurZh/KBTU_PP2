import pygame
import sys
from pygame.locals import *

from persistence import load_settings, save_settings, load_leaderboard, save_score
from racer import game_loop, screen, clock, FPS

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (40, 80, 220)
RED = (220, 40, 40)
GRAY = (120, 120, 120)

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


def button(text, x, y, w, h):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    rect = pygame.Rect(x, y, w, h)

    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, GRAY, rect)

        if click[0]:
            pygame.time.delay(200)
            return True
    else:
        pygame.draw.rect(screen, WHITE, rect)

    pygame.draw.rect(screen, BLACK, rect, 2)

    text_img = font_small.render(text, True, BLACK)
    screen.blit(text_img, (x + 15, y + 10))

    return False


def enter_name_screen():
    name = ""

    while True:
        screen.fill(WHITE)

        draw_text("Enter your name:", 55, 180, "medium")
        draw_text(name, 100, 240, "medium", BLUE)
        draw_text("Press ENTER to start", 85, 320)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_RETURN and name != "":
                    return name
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 12:
                        name += event.unicode

        pygame.display.update()
        clock.tick(FPS)


def main_menu():
    while True:
        screen.fill(BLUE)

        draw_text("RACER", 115, 100, "big", WHITE)

        if button("Play", 125, 220, 150, 45):
            player_name = enter_name_screen()
            game_loop(player_name)

        if button("Leaderboard", 125, 280, 150, 45):
            leaderboard_screen()

        if button("Settings", 125, 340, 150, 45):
            settings_screen()

        if button("Quit", 125, 400, 150, 45):
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)


def leaderboard_screen():
    while True:
        screen.fill(WHITE)

        draw_text("Leaderboard", 70, 40, "medium", BLACK)

        leaderboard = load_leaderboard()

        y = 100

        if len(leaderboard) == 0:
            draw_text("No scores yet", 130, 180)
        else:
            for i, item in enumerate(leaderboard):
                text = f"{i + 1}. {item['name']} | Score: {item['score']} | {item['distance']}m"
                draw_text(text, 20, y)
                y += 35

        if button("Back", 125, 520, 150, 45):
            return

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)


def settings_screen():
    settings = load_settings()

    colors = ["blue", "black", "green"]
    difficulties = ["easy", "normal", "hard"]

    while True:
        screen.fill(WHITE)

        draw_text("Settings", 120, 50, "medium")

        draw_text(f"Sound: {settings['sound']}", 90, 130)
        draw_text(f"Car color: {settings['car_color']}", 90, 190)
        draw_text(f"Difficulty: {settings['difficulty']}", 90, 250)

        if button("Toggle Sound", 105, 330, 190, 40):
            settings["sound"] = not settings["sound"]
            save_settings(settings)

        if button("Change Color", 105, 380, 190, 40):
            index = colors.index(settings["car_color"])
            settings["car_color"] = colors[(index + 1) % len(colors)]
            save_settings(settings)

        if button("Change Difficulty", 105, 430, 190, 40):
            index = difficulties.index(settings["difficulty"])
            settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]
            save_settings(settings)

        if button("Back", 125, 520, 150, 45):
            return

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)


def game_over_screen(name, score, distance, coins):
    save_score(name, score, distance)

    while True:
        screen.fill(RED)

        draw_text("Game Over", 60, 120, "big", WHITE)
        draw_text(f"Score: {score}", 120, 220, "medium", WHITE)
        draw_text(f"Distance: {int(distance)}m", 100, 260, "medium", WHITE)
        draw_text(f"Coins: {coins}", 130, 300, "medium", WHITE)

        if button("Retry", 125, 390, 150, 45):
            game_loop(name)

        if button("Main Menu", 125, 450, 150, 45):
            return

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)