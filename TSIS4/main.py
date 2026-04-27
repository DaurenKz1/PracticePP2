import pygame
import json
import random
import sys
import os

from config import WIDTH, HEIGHT, CELL, BASE_FPS
from color_palette import *
from game import (Snake, Food, PoisonFood, PowerUp,
                  generate_obstacles, POWERUP_SPEED, POWERUP_SLOW, POWERUP_SHIELD)
from db import init_db, get_or_create_player, save_session, get_personal_best, get_leaderboard

# ─────────────────────────────────────────────
#  Инициализация
# ─────────────────────────────────────────────

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

font_big   = pygame.font.SysFont("Arial", 36, bold=True)
font_med   = pygame.font.SysFont("Arial", 26)
font_small = pygame.font.SysFont("Arial", 18)

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")


def start_music(settings):
    if settings.get("sound"):
        path = os.path.join(os.path.dirname(__file__), "assets", "background.wav")
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1) 
        except Exception:
            pass

def stop_music():
    pygame.mixer.music.stop()


def load_settings():
    try:
        with open(SETTINGS_FILE) as f:
            return json.load(f)
    except Exception:
        return {"snake_color": [0, 255, 0], "grid": True, "sound": False}

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)



def draw_grid():
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, (30, 30, 30),
                             (j * CELL, i * CELL, CELL, CELL), 1)

def draw_button(text, rect, hover=False):
    color = (80, 80, 80) if hover else (50, 50, 50)
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, colorGRAY, rect, 2, border_radius=8)
    label = font_med.render(text, True, colorWHITE)
    lx = rect[0] + (rect[2] - label.get_width()) // 2
    ly = rect[1] + (rect[3] - label.get_height()) // 2
    screen.blit(label, (lx, ly))

def get_mouse_hover(rect):
    mx, my = pygame.mouse.get_pos()
    return pygame.Rect(rect).collidepoint(mx, my)



def screen_username():
    username = ""
    active = True
    while active:
        screen.fill(colorBLACK)
        title = font_big.render("SNAKE", True, colorGREEN)
        screen.blit(title, ((WIDTH - title.get_width()) // 2, 120))

        prompt = font_med.render("Enter your username:", True, colorWHITE)
        screen.blit(prompt, ((WIDTH - prompt.get_width()) // 2, 220))

        # поле ввода
        input_rect = pygame.Rect(WIDTH // 2 - 150, 265, 300, 44)
        pygame.draw.rect(screen, (30, 30, 30), input_rect, border_radius=6)
        pygame.draw.rect(screen, colorGREEN, input_rect, 2, border_radius=6)
        inp_surf = font_med.render(username + "|", True, colorGREEN)
        screen.blit(inp_surf, (input_rect.x + 10, input_rect.y + 8))

        btn = (WIDTH // 2 - 80, 340, 160, 48)
        draw_button("START", btn, get_mouse_hover(btn))

        hint = font_small.render("Press Enter or click START", True, colorGRAY)
        screen.blit(hint, ((WIDTH - hint.get_width()) // 2, 410))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username.strip():
                    return username.strip()
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif len(username) < 20 and event.unicode.isprintable():
                    username += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(btn).collidepoint(event.pos) and username.strip():
                    return username.strip()



def screen_main_menu():
    while True:
        screen.fill(colorBLACK)
        title = font_big.render("SNAKE", True, colorGREEN)
        screen.blit(title, ((WIDTH - title.get_width()) // 2, 100))

        buttons = [
            ("PLAY",        (WIDTH // 2 - 100, 200, 200, 50)),
            ("LEADERBOARD", (WIDTH // 2 - 100, 270, 200, 50)),
            ("SETTINGS",    (WIDTH // 2 - 100, 340, 200, 50)),
            ("QUIT",        (WIDTH // 2 - 100, 410, 200, 50)),
        ]
        for label, rect in buttons:
            draw_button(label, rect, get_mouse_hover(rect))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for label, rect in buttons:
                    if pygame.Rect(rect).collidepoint(event.pos):
                        return label


def screen_leaderboard():
    rows = get_leaderboard(10)
    while True:
        screen.fill(colorBLACK)
        title = font_big.render("LEADERBOARD", True, colorGOLD)
        screen.blit(title, ((WIDTH - title.get_width()) // 2, 20))

        headers = ["#", "Player", "Score", "Lvl", "Date"]
        col_x = [20, 60, 260, 340, 400]
        for i, h in enumerate(headers):
            s = font_small.render(h, True, colorGRAY)
            screen.blit(s, (col_x[i], 75))

        pygame.draw.line(screen, colorGRAY, (15, 95), (WIDTH - 15, 95), 1)

        for idx, row in enumerate(rows):
            rank, uname, score, level, date = row
            color = colorGOLD if idx == 0 else colorWHITE
            data = [str(rank), str(uname), str(score), str(level), str(date)]
            for i, val in enumerate(data):
                s = font_small.render(val, True, color)
                screen.blit(s, (col_x[i], 105 + idx * 28))

        btn = (WIDTH // 2 - 80, HEIGHT - 70, 160, 45)
        draw_button("BACK", btn, get_mouse_hover(btn))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(btn).collidepoint(event.pos):
                    return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return



COLOR_OPTIONS = [
    ("Green",  (0, 220, 0)),
    ("Yellow", (255, 220, 0)),
    ("Cyan",   (0, 220, 220)),
    ("Orange", (255, 140, 0)),
    ("White",  (220, 220, 220)),
]

def screen_settings(settings):
    selected_color_idx = 0
    for i, (name, rgb) in enumerate(COLOR_OPTIONS):
        if list(rgb) == settings["snake_color"]:
            selected_color_idx = i
            break

    while True:
        screen.fill(colorBLACK)
        title = font_big.render("SETTINGS", True, colorWHITE)
        screen.blit(title, ((WIDTH - title.get_width()) // 2, 30))

        grid_btn = (WIDTH // 2 - 130, 120, 260, 48)
        grid_label = f"Grid: {'ON' if settings['grid'] else 'OFF'}"
        draw_button(grid_label, grid_btn, get_mouse_hover(grid_btn))

        sound_btn = (WIDTH // 2 - 130, 190, 260, 48)
        sound_label = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
        draw_button(sound_label, sound_btn, get_mouse_hover(sound_btn))

        color_title = font_med.render("Snake Color:", True, colorWHITE)
        screen.blit(color_title, (WIDTH // 2 - 130, 265))

        for i, (name, rgb) in enumerate(COLOR_OPTIONS):
            cx = 70 + i * 100
            cy = 310
            pygame.draw.rect(screen, rgb, (cx, cy, 50, 50), border_radius=6)
            if i == selected_color_idx:
                pygame.draw.rect(screen, colorWHITE, (cx, cy, 50, 50), 3, border_radius=6)
            label = font_small.render(name, True, colorGRAY)
            screen.blit(label, (cx, cy + 54))

        preview_color = COLOR_OPTIONS[selected_color_idx][1]
        pygame.draw.rect(screen, preview_color, (WIDTH // 2 - 25, 390, 50, 50), border_radius=6)
        prev_label = font_small.render("Preview", True, colorGRAY)
        screen.blit(prev_label, (WIDTH // 2 - prev_label.get_width() // 2, 448))

        save_btn = (WIDTH // 2 - 100, HEIGHT - 70, 200, 48)
        draw_button("SAVE & BACK", save_btn, get_mouse_hover(save_btn))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(grid_btn).collidepoint(event.pos):
                    settings["grid"] = not settings["grid"]
                elif pygame.Rect(sound_btn).collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]
                    if settings["sound"]:
                        start_music(settings)  
                    else:
                        stop_music()           
                elif pygame.Rect(save_btn).collidepoint(event.pos):
                    settings["snake_color"] = list(COLOR_OPTIONS[selected_color_idx][1])
                    save_settings(settings)
                    return settings
                else:
                    for i, (name, rgb) in enumerate(COLOR_OPTIONS):
                        cx = 70 + i * 100
                        cy = 310
                        if pygame.Rect(cx, cy, 50, 50).collidepoint(event.pos):
                            selected_color_idx = i
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                settings["snake_color"] = list(COLOR_OPTIONS[selected_color_idx][1])
                save_settings(settings)
                return settings


def screen_game_over(score, level, personal_best):
    while True:
        screen.fill(colorBLACK)
        title = font_big.render("GAME OVER", True, colorRED)
        screen.blit(title, ((WIDTH - title.get_width()) // 2, 100))

        lines = [
            (f"Score:    {score}",        colorWHITE),
            (f"Level:    {level}",         colorWHITE),
            (f"Best:     {personal_best}", colorGOLD),
        ]
        for i, (text, color) in enumerate(lines):
            surf = font_med.render(text, True, color)
            screen.blit(surf, ((WIDTH - surf.get_width()) // 2, 200 + i * 44))

        retry_btn = (WIDTH // 2 - 110, 380, 200, 50)
        menu_btn  = (WIDTH // 2 - 110, 448, 200, 50)
        draw_button("RETRY",     retry_btn, get_mouse_hover(retry_btn))
        draw_button("MAIN MENU", menu_btn,  get_mouse_hover(menu_btn))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(retry_btn).collidepoint(event.pos):
                    return "RETRY"
                if pygame.Rect(menu_btn).collidepoint(event.pos):
                    return "MENU"



def run_game(player_id, personal_best, settings):
    start_music(settings)  
    snake_color = tuple(settings["snake_color"])
    snake = Snake(color=snake_color)
    food  = Food()
    obstacles = []
    food.generate(snake, obstacles)

    poison = PoisonFood()
    powerup = PowerUp()

    score = 0
    level = 1
    fps   = BASE_FPS

    poison_spawn_counter = 0
    powerup_spawn_counter = 0

    running = True
    while running:
        fps = snake.update_effects(BASE_FPS + (level - 1) * 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake.set_direction(1, 0)
                elif event.key == pygame.K_LEFT:
                    snake.set_direction(-1, 0)
                elif event.key == pygame.K_DOWN:
                    snake.set_direction(0, 1)
                elif event.key == pygame.K_UP:
                    snake.set_direction(0, -1)

        snake.move()
        head = snake.body[0]

        if head.x == food.pos.x and head.y == food.pos.y:
            snake.grow()
            score += food.weight
            food.generate(snake, obstacles)
            new_level = 1 + score // 3
            if new_level > level:
                level = new_level
                if level >= 3:
                    extra = generate_obstacles(snake, count=level)
                    obstacles.extend(extra)

        if food.update(snake, obstacles):
            food.generate(snake, obstacles)

        poison_spawn_counter += 1
        if not poison.active and poison_spawn_counter > 60:
            poison_spawn_counter = 0
            if random.random() < 0.3:
                poison.spawn(snake, obstacles)
        poison.update()
        if poison.active and head.x == poison.pos.x and head.y == poison.pos.y:
            dead = snake.shrink(2)
            poison.active = False
            if dead:
                running = False

        powerup_spawn_counter += 1
        if not powerup.active and powerup_spawn_counter > 80:
            powerup_spawn_counter = 0
            if random.random() < 0.25:
                powerup.spawn(snake, obstacles)
        powerup.update()
        if powerup.active and head.x == powerup.pos.x and head.y == powerup.pos.y:
            powerup.collect(snake, fps)

        wall_hit = snake.check_wall_collision()
        self_hit = snake.check_self_collision()
        obs_hit  = any(head.x == o.x and head.y == o.y for o in obstacles)

        if wall_hit or self_hit or obs_hit:
            if snake.shield_active:
                snake.shield_active = False
                snake.body[0].x -= snake.dx
                snake.body[0].y -= snake.dy
            else:
                running = False

        screen.fill(colorBLACK)
        if settings.get("grid"):
            draw_grid()

        for obs in obstacles:
            obs.draw(screen)

        food.draw(screen)
        poison.draw(screen)
        powerup.draw(screen, font_small)
        snake.draw(screen)

        hud = font_small.render(
            f"Score: {score}  Level: {level}  Best: {personal_best}",
            True, colorWHITE
        )
        screen.blit(hud, (8, 8))

        if snake.shield_active:
            sh = font_small.render("🛡SHIELD", True, colorPURPLE)
            screen.blit(sh, (8, 28))
        if snake.speed_boost:
            sb = font_small.render("⚡SPEED", True, colorORANGE)
            screen.blit(sb, (8, 46))
        if snake.slow_motion:
            sl = font_small.render("❄SLOW", True, colorCYAN)
            screen.blit(sl, (8, 46))

        pygame.display.flip()
        clock.tick(fps)

    stop_music()  
    return score, level




def main():
    init_db()
    settings = load_settings()

    username  = screen_username()
    player_id = get_or_create_player(username)
    best      = get_personal_best(player_id)

    while True:
        choice = screen_main_menu()

        if choice == "PLAY":
            score, level = run_game(player_id, best, settings)
            save_session(player_id, score, level)
            best = max(best, score)
            result = screen_game_over(score, level, best)
            if result == "RETRY":
                score, level = run_game(player_id, best, settings)
                save_session(player_id, score, level)
                best = max(best, score)
                screen_game_over(score, level, best)

        elif choice == "LEADERBOARD":
            screen_leaderboard()

        elif choice == "SETTINGS":
            settings = screen_settings(settings)

        elif choice == "QUIT":
            break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()