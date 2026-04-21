import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    radius = 10
    mode = 'draw'   # текущий режим: рисование / ластик / фигуры
    color = (0, 0, 255)  # текущий цвет (по умолчанию синий)

    points = []  # список точек для свободного рисования
    start_pos = None  # начальная точка для фигур

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                start_pos = event.pos  # запоминаем начальную точку

            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    if mode == 'draw':
                        points.append(event.pos)  # добавляем точки для линии
                    elif mode == 'eraser':
                        pygame.draw.circle(screen, (0, 0, 0), event.pos, radius)  # стираем

            if event.type == pygame.MOUSEBUTTONUP:
                end_pos = event.pos  # конечная точка

                if mode == 'rect' and start_pos:
                    rect = pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                    pygame.draw.rect(screen, color, rect, 2)  # рисуем прямоугольник

                elif mode == 'circle' and start_pos:
                    radius_circle = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2) ** 0.5)
                    pygame.draw.circle(screen, color, start_pos, radius_circle, 2)  # рисуем круг

                start_pos = None

        # рисование линий между точками
        for i in range(len(points) - 1):
            pygame.draw.line(screen, color, points[i], points[i+1], radius)

        pygame.display.flip()
        clock.tick(60)

main()