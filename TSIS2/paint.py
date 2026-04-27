import pygame
import math
import datetime
import sys
from tools import (
    draw_right_triangle,
    draw_equilateral_triangle,
    draw_rhombus,
    flood_fill,
    norm_rect,
    preview_shape
)

def main():
    pygame.init()

    SCREEN_W = 900
    SCREEN_H = 600
    TOOLBAR_H = 80

    BLACK      = (0,   0,   0)
    WHITE      = (255, 255, 255)
    GRAY       = (128, 128, 128)
    LIGHT_GRAY = (200, 200, 200)

    PALETTE_COLORS = [
        (0,   0,   0),    # чёрный
        (255, 255, 255),  # белый
        (255, 0,   0),    # красный
        (0,   255, 0),    # зелёный
        (0,   0,   255),  # синий
        (255, 255, 0),    # жёлтый
        (0,   255, 255),  # голубой
        (255, 0,   255),  # пурпурный
        (255, 165, 0),    # оранжевый
        (128, 0,   128),  # фиолетовый
        (128, 128, 128),  # серый
    ]

    BRUSH_SIZES = [2, 5, 10]
    brush_index = 1
    brush_size  = BRUSH_SIZES[brush_index]

    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()

    canvas = pygame.Surface((SCREEN_W, SCREEN_H - TOOLBAR_H))
    canvas.fill(WHITE)

    undo_stack = []
    redo_stack = []

    mode      = 'draw'       # текущий режим
    color     = BLACK        # текущий цвет
    start_pos = None         # начальная точка фигуры
    current   = None         # текущая позиция мыши
    drawing   = False        # флаг рисования

    typing   = False
    text     = ""
    text_pos = (0, 0)
    font     = pygame.font.SysFont(None, 28)

    selected_color_idx = 0

    btn_font = pygame.font.Font(None, 18)

    # Кнопки режимов
    mode_buttons = [
        ("Pencil", 'draw'),
        ("Line",    'line'),
        ("Rect",  'rect'),
        ("Square",  'square'),
        ("Circle",     'circle'),
        ("R_tr", 'right_triangle'),
        ("Eq_tr",'equilateral_triangle'),
        ("Rhomb",     'rhombus'),
        ("Eraser",   'eraser'),
        ("Bucket",  'bucket'),
        ("Text",    'text'),
    ]

    # Кнопки размера кисти
    size_buttons = [("S", 0), ("M", 1), ("L", 2)]

    def draw_toolbar():
        pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, SCREEN_W, TOOLBAR_H))

        for i, (label, _) in enumerate(mode_buttons):
            x = 5 + i * 77
            rect = pygame.Rect(x, 5, 72, 25)
            btn_color = (100, 180, 100) if mode == mode_buttons[i][1] else GRAY
            pygame.draw.rect(screen, btn_color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            txt = btn_font.render(label, True, BLACK)
            screen.blit(txt, txt.get_rect(center=rect.center))

        for j, (label, idx) in enumerate(size_buttons):
            x = 5 + j * 45
            rect = pygame.Rect(x, 36, 40, 22)
            btn_color = (100, 180, 100) if brush_index == idx else GRAY
            pygame.draw.rect(screen, btn_color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            txt = btn_font.render(label, True, BLACK)
            screen.blit(txt, txt.get_rect(center=rect.center))

        for i, c in enumerate(PALETTE_COLORS):
            r = pygame.Rect(145 + i * 35, 36, 30, 22)
            pygame.draw.rect(screen, c, r)
            pygame.draw.rect(screen, BLACK, r, 1)
            if i == selected_color_idx:
                pygame.draw.rect(screen, WHITE, r, 3)

        pygame.draw.rect(screen, color, (535, 36, 30, 22))
        pygame.draw.rect(screen, BLACK, (535, 36, 30, 22), 2)


    running = True

    while running:

        mx, my = pygame.mouse.get_pos()
        cy = my - TOOLBAR_H  

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                # Ctrl S сохранение
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename  = f"canvas_{timestamp}.png"
                    pygame.image.save(canvas, filename)

                # Ctrl Z отмена
                elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if undo_stack:
                        redo_stack.append(canvas.copy())
                        canvas.blit(undo_stack.pop(), (0, 0))

                # Ctrl Y повтор
                elif event.key == pygame.K_y and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if redo_stack:
                        undo_stack.append(canvas.copy())
                        canvas.blit(redo_stack.pop(), (0, 0))

                elif not typing:

                    if event.key == pygame.K_1:
                        brush_index = 0
                        brush_size  = BRUSH_SIZES[brush_index]
                    elif event.key == pygame.K_2:
                        brush_index = 1
                        brush_size  = BRUSH_SIZES[brush_index]
                    elif event.key == pygame.K_3:
                        brush_index = 2
                        brush_size  = BRUSH_SIZES[brush_index]

                    elif event.key == pygame.K_r:
                        color = (255, 0, 0)
                    elif event.key == pygame.K_g:
                        color = (0, 255, 0)
                    elif event.key == pygame.K_b:
                        color = (0, 0, 255)

                    elif event.key == pygame.K_f:
                        mode = 'draw'
                    elif event.key == pygame.K_e:
                        mode = 'eraser'
                    elif event.key == pygame.K_c:
                        mode = 'circle'
                    elif event.key == pygame.K_t:
                        mode = 'rect'
                    elif event.key == pygame.K_q:
                        mode = 'right_triangle'
                    elif event.key == pygame.K_w:
                        mode = 'equilateral_triangle'
                    elif event.key == pygame.K_d:
                        mode = 'rhombus'

                if typing:
                    if event.key == pygame.K_RETURN:
                        img = font.render(text, True, color)
                        canvas.blit(img, text_pos)
                        typing = False
                        text   = ""
                    elif event.key == pygame.K_ESCAPE:
                        typing = False
                        text   = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:

                x, y = event.pos

                if y < TOOLBAR_H:

                    for i, (_, m) in enumerate(mode_buttons):
                        btn_rect = pygame.Rect(5 + i * 77, 5, 72, 25)
                        if btn_rect.collidepoint(x, y):
                            mode = m

                    for j, (_, idx) in enumerate(size_buttons):
                        btn_rect = pygame.Rect(5 + j * 45, 36, 40, 22)
                        if btn_rect.collidepoint(x, y):
                            brush_index = idx
                            brush_size  = BRUSH_SIZES[brush_index]

                    for i, c in enumerate(PALETTE_COLORS):
                        r = pygame.Rect(145 + i * 35, 36, 30, 22)
                        if r.collidepoint(x, y):
                            color = c
                            selected_color_idx = i

                else:
                    undo_stack.append(canvas.copy())
                    redo_stack.clear()

                    if mode == 'bucket':
                        target = canvas.get_at((x, cy))[:3]
                        flood_fill(canvas, (x, cy), target, color)
                        continue

                    if mode == 'text':
                        typing   = True
                        text     = ""
                        text_pos = (x, cy)
                        continue

                    drawing   = True
                    start_pos = (x, cy)
                    current   = start_pos

            elif event.type == pygame.MOUSEMOTION:

                if drawing:
                    current = (mx, cy)

                    if mode == 'draw':
                        pygame.draw.line(canvas, color, start_pos, current, brush_size)
                        start_pos = current

                    elif mode == 'eraser':
                        pygame.draw.line(canvas, WHITE, start_pos, current, brush_size)
                        start_pos = current

            elif event.type == pygame.MOUSEBUTTONUP:

                if drawing and start_pos and current:

                    if mode == 'line':
                        pygame.draw.line(canvas, color, start_pos, current, brush_size)

                    elif mode == 'rect':
                        pygame.draw.rect(canvas, color, norm_rect(*start_pos, *current), brush_size)

                    elif mode == 'square':
                        x1, y1 = start_pos
                        x2, y2 = current
                        side = max(abs(x2 - x1), abs(y2 - y1))
                        sx = x1 if x2 >= x1 else x1 - side
                        sy = y1 if y2 >= y1 else y1 - side
                        pygame.draw.rect(canvas, color, (sx, sy, side, side), brush_size)

                    elif mode == 'circle':
                        r = int(((current[0] - start_pos[0])**2 + (current[1] - start_pos[1])**2) ** 0.5)
                        pygame.draw.circle(canvas, color, start_pos, r, brush_size)

                    elif mode == 'right_triangle':
                        draw_right_triangle(canvas, color, start_pos, current, brush_size)

                    elif mode == 'equilateral_triangle':
                        draw_equilateral_triangle(canvas, color, start_pos, current, brush_size)

                    elif mode == 'rhombus':
                        draw_rhombus(canvas, color, start_pos, current, brush_size)

                drawing   = False
                start_pos = None
                current   = None

        screen.fill(GRAY)
        screen.blit(canvas, (0, TOOLBAR_H))

        if drawing and start_pos and current:
            temp = screen.copy()
            preview_shape(temp, mode, start_pos, current, brush_size, TOOLBAR_H)
            screen.blit(temp, (0, 0))

        draw_toolbar()

        if typing:
            img = font.render(text, True, color)
            screen.blit(img, (text_pos[0], text_pos[1] + TOOLBAR_H))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()