import pygame
import random
from color_palette import *
from config import WIDTH, HEIGHT, CELL



class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Snake:
    def __init__(self, color=(0, 255, 0)):
        self.body = [Point(10, 10), Point(10, 11), Point(10, 12)]
        self.dx = 1
        self.dy = 0
        self.color = color
        self.shield_active = False    # щит от одного столкновения
        self.speed_boost = False
        self.slow_motion = False
        self.effect_end_time = 0      # когда заканчивается текущий эффект скорости

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def draw(self, screen):
        head = self.body[0]
        head_color = tuple(min(255, c + 60) for c in self.color)
        pygame.draw.rect(screen, head_color,
                         (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, self.color,
                             (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_wall_collision(self):
        head = self.body[0]
        return head.x < 0 or head.x >= WIDTH // CELL or \
               head.y < 0 or head.y >= HEIGHT // CELL

    def check_self_collision(self):
        head = self.body[0]
        return any(head.x == s.x and head.y == s.y for s in self.body[1:])

    def grow(self):
        tail = self.body[-1]
        self.body.append(Point(tail.x, tail.y))

    def shrink(self, amount=2):
        for _ in range(amount):
            if len(self.body) > 1:
                self.body.pop()
        return len(self.body) <= 1

    def set_direction(self, dx, dy):
        if dx == -self.dx and dy == -self.dy:
            return
        self.dx, self.dy = dx, dy

    def update_effects(self, base_fps):
        now = pygame.time.get_ticks()
        if now >= self.effect_end_time:
            self.speed_boost = False
            self.slow_motion = False
        if self.speed_boost:
            return base_fps + 5
        if self.slow_motion:
            return max(2, base_fps - 3)
        return base_fps



class Food:
    def __init__(self):
        self.pos = Point(5, 5)
        self.weight = 1
        self.timer = 0

    def _free_pos(self, snake, obstacles):
        cols = WIDTH // CELL
        rows = HEIGHT // CELL
        attempts = 0
        while attempts < 500:
            x = random.randint(0, cols - 1)
            y = random.randint(0, rows - 1)
            blocked = any(s.x == x and s.y == y for s in snake.body)
            blocked = blocked or any(o.x == x and o.y == y for o in obstacles)
            if not blocked:
                return x, y
            attempts += 1
        return 1, 1  # запасной вариант

    def generate(self, snake, obstacles):
        x, y = self._free_pos(snake, obstacles)
        self.pos = Point(x, y)
        self.weight = random.randint(1, 3)
        self.timer = random.randint(50, 150)

    def draw(self, screen):
        colors = {1: colorGREEN, 2: colorBLUE, 3: colorGOLD}
        color = colors.get(self.weight, colorGREEN)
        pygame.draw.rect(screen, color,
                         (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def update(self, snake, obstacles):
        self.timer -= 1
        return self.timer <= 0


class PoisonFood:
    def __init__(self):
        self.pos = None
        self.timer = 0
        self.active = False

    def spawn(self, snake, obstacles):
        cols = WIDTH // CELL
        rows = HEIGHT // CELL
        for _ in range(500):
            x = random.randint(0, cols - 1)
            y = random.randint(0, rows - 1)
            blocked = any(s.x == x and s.y == y for s in snake.body)
            blocked = blocked or any(o.x == x and o.y == y for o in obstacles)
            if not blocked:
                self.pos = Point(x, y)
                self.timer = random.randint(60, 120)
                self.active = True
                return

    def draw(self, screen):
        if self.active and self.pos:
            pygame.draw.rect(screen, colorDARK_RED,
                             (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))
            cx = self.pos.x * CELL + CELL // 2
            cy = self.pos.y * CELL + CELL // 2
            pygame.draw.line(screen, colorWHITE,
                             (cx - 6, cy - 6), (cx + 6, cy + 6), 2)
            pygame.draw.line(screen, colorWHITE,
                             (cx + 6, cy - 6), (cx - 6, cy + 6), 2)

    def update(self):
        if self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.active = False




POWERUP_SPEED  = "speed"
POWERUP_SLOW   = "slow"
POWERUP_SHIELD = "shield"

POWERUP_COLORS = {
    POWERUP_SPEED:  colorORANGE,
    POWERUP_SLOW:   colorCYAN,
    POWERUP_SHIELD: colorPURPLE,
}

POWERUP_LABELS = {
    POWERUP_SPEED:  "⚡",
    POWERUP_SLOW:   "❄",
    POWERUP_SHIELD: "🛡",
}


class PowerUp:
    FIELD_LIFE_MS = 8000   # 8 секунд на поле
    EFFECT_MS     = 5000   # 5 секунд эффект

    def __init__(self):
        self.pos = None
        self.kind = None
        self.active = False
        self.spawn_time = 0

    def spawn(self, snake, obstacles):
        cols = WIDTH // CELL
        rows = HEIGHT // CELL
        for _ in range(500):
            x = random.randint(0, cols - 1)
            y = random.randint(0, rows - 1)
            blocked = any(s.x == x and s.y == y for s in snake.body)
            blocked = blocked or any(o.x == x and o.y == y for o in obstacles)
            if not blocked:
                self.pos = Point(x, y)
                self.kind = random.choice([POWERUP_SPEED, POWERUP_SLOW, POWERUP_SHIELD])
                self.spawn_time = pygame.time.get_ticks()
                self.active = True
                return

    def draw(self, screen, font_small):
        if not self.active or not self.pos:
            return
        color = POWERUP_COLORS[self.kind]
        pygame.draw.rect(screen, color,
                         (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))
        label = font_small.render(self.kind[0].upper(), True, colorBLACK)
        screen.blit(label, (self.pos.x * CELL + 4, self.pos.y * CELL + 4))

    def update(self):
        if self.active:
            if pygame.time.get_ticks() - self.spawn_time > self.FIELD_LIFE_MS:
                self.active = False

    def collect(self, snake, base_fps):
        now = pygame.time.get_ticks()
        if self.kind == POWERUP_SPEED:
            snake.speed_boost = True
            snake.slow_motion = False
            snake.effect_end_time = now + self.EFFECT_MS
        elif self.kind == POWERUP_SLOW:
            snake.slow_motion = True
            snake.speed_boost = False
            snake.effect_end_time = now + self.EFFECT_MS
        elif self.kind == POWERUP_SHIELD:
            snake.shield_active = True
        self.active = False




class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.rect(screen, colorDARK_GRAY,
                         (self.x * CELL, self.y * CELL, CELL, CELL))
        pygame.draw.rect(screen, colorGRAY,
                         (self.x * CELL, self.y * CELL, CELL, CELL), 2)


def generate_obstacles(snake, count=5):
    cols = WIDTH // CELL
    rows = HEIGHT // CELL
    obstacles = []
    attempts = 0
    # запрещённая зона вокруг головы (3x3)
    hx, hy = snake.body[0].x, snake.body[0].y
    forbidden = {(hx + dx, hy + dy) for dx in range(-2, 3) for dy in range(-2, 3)}
    forbidden |= {(s.x, s.y) for s in snake.body}

    while len(obstacles) < count and attempts < 1000:
        x = random.randint(0, cols - 1)
        y = random.randint(0, rows - 1)
        if (x, y) not in forbidden and not any(o.x == x and o.y == y for o in obstacles):
            obstacles.append(Obstacle(x, y))
        attempts += 1
    return obstacles
