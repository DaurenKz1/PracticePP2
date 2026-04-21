import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    radius = 10
    mode = 'draw'  # текущий режим
    color = (0, 0, 255)  # текущий цвет

    points = []  # точки для свободного рисования
    start_pos = None  # начальная точка фигур

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                # смена цвета
                if event.key == pygame.K_r:
                    color = (255, 0, 0)
                elif event.key == pygame.K_g:
                    color = (0, 255, 0)
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)

                # смена режима
                elif event.key == pygame.K_f:
                    mode = 'draw'
                elif event.key == pygame.K_e:
                    mode = 'eraser'
                elif event.key == pygame.K_c:
                    mode = 'circle'
                elif event.key == pygame.K_t:
                    mode = 'rect'
                elif event.key == pygame.K_s:
                    mode = 'square'
                elif event.key == pygame.K_q:
                    mode = 'right_triangle'
                elif event.key == pygame.K_w:
                    mode = 'equilateral_triangle'
                elif event.key == pygame.K_d:
                    mode = 'rhombus'

            if event.type == pygame.MOUSEBUTTONDOWN:
                start_pos = event.pos  # запоминаем начало

            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    if mode == 'draw':
                        points.append(event.pos)  # рисование линии
                    elif mode == 'eraser':
                        pygame.draw.circle(screen, (0, 0, 0), event.pos, radius)  # стирание

            if event.type == pygame.MOUSEBUTTONUP:
                end_pos = event.pos  # конечная точка

                if mode == 'rect' and start_pos:
                    rect = pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                    pygame.draw.rect(screen, color, rect, 2)  # прямоугольник

                elif mode == 'square' and start_pos:
                    side = min(abs(end_pos[0]-start_pos[0]), abs(end_pos[1]-start_pos[1]))
                    rect = pygame.Rect(start_pos, (side, side))
                    pygame.draw.rect(screen, color, rect, 2)  # квадрат

                elif mode == 'circle' and start_pos:
                    radius_circle = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2) ** 0.5)
                    pygame.draw.circle(screen, color, start_pos, radius_circle, 2)  # круг

                elif mode == 'right_triangle' and start_pos:
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    # прямоугольный треугольник
                    pygame.draw.polygon(screen, color, [(x1, y1), (x2, y2), (x1, y2)], 2)

                elif mode == 'equilateral_triangle' and start_pos:
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    side = abs(x2 - x1)
                    height = int(side * math.sqrt(3) / 2)  # формула высоты
                    pygame.draw.polygon(screen, color,
                        [(x1, y1), (x1 + side, y1), (x1 + side // 2, y1 - height)])  # равносторонний

                elif mode == 'rhombus' and start_pos:
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    # ромб через центр
                    pygame.draw.polygon(screen, color,
                        [(cx, y1), (x2, cy), (cx, y2), (x1, cy)], 2)

                start_pos = None

        # соединяем точки линиями
        for i in range(len(points) - 1):
            pygame.draw.line(screen, color, points[i], points[i+1], radius)

        pygame.display.flip()
        clock.tick(60)

main()