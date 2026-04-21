import pygame
from color_palette import *
import random

pygame.init()

WIDTH = 600
HEIGHT = 600
CELL = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

font = pygame.font.SysFont("Arial", 24)

def draw_grid():  # рисует сетку поля
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)

class Point:
    def __init__(self, x, y):  # хранит координаты клетки
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.body = [Point(10, 10), Point(10, 11), Point(10, 12)]  # тело змейки
        self.dx = 1
        self.dy = 0  # направление движения

    def move(self):  # движение змейки
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def draw(self):  # отрисовка змейки
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))

        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_wall_collision(self):  # проверка столкновения со стенами
        head = self.body[0]
        if head.x < 0 or head.x >= WIDTH // CELL or head.y < 0 or head.y >= HEIGHT // CELL:
            return True
        return False

    def check_self_collision(self):  # проверка столкновения с собой
        head = self.body[0]
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False

    def grow(self):  # увеличение змейки
        tail = self.body[-1]  
        self.body.append(Point(tail.x, tail.y))  


class Food:
    def __init__(self):
        self.pos = Point(5, 5)

    def draw(self):  # отрисовка еды
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self, snake):  # генерация еды вне змейки
        while True:
            x = random.randint(0, WIDTH // CELL - 1)
            y = random.randint(0, HEIGHT // CELL - 1)

            overlap = False
            for segment in snake.body:
                if segment.x == x and segment.y == y:
                    overlap = True
                    break

            if not overlap:
                self.pos = Point(x, y)
                break


FPS = 5
clock = pygame.time.Clock()

snake = Snake()
food = Food()

score = 0
level = 1

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:  # управление змейкой
            if event.key == pygame.K_RIGHT:
                snake.dx, snake.dy = 1, 0
            elif event.key == pygame.K_LEFT:
                snake.dx, snake.dy = -1, 0
            elif event.key == pygame.K_DOWN:
                snake.dx, snake.dy = 0, 1
            elif event.key == pygame.K_UP:
                snake.dx, snake.dy = 0, -1

    snake.move()

    head = snake.body[0]
    if head.x == food.pos.x and head.y == food.pos.y:  # съели еду
        snake.grow()
        food.generate_random_pos(snake)
        score += 1

        if score % 3 == 0:
            level += 1
            FPS += 2  # ускорение игры

    if snake.check_wall_collision() or snake.check_self_collision():  # конец игры
        print("GAME OVER")
        running = False

    screen.fill(colorBLACK)
    draw_grid()

    snake.draw()
    food.draw()

    text = font.render(f"Score: {score}  Level: {level}", True, colorWHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()