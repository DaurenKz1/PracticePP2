import pygame
import math

WHITE      = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)


def norm_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))


def draw_right_triangle(surface, color, start, end, w):
    x1, y1 = start
    x2, y2 = end
    pygame.draw.polygon(surface, color, [(x1, y1), (x2, y2), (x1, y2)], w)


def draw_equilateral_triangle(surface, color, start, end, w):
    x1, y1 = start
    x2, y2 = end

    dx = x2 - x1
    dy = y2 - y1

    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2

    side = math.hypot(dx, dy)
    if side == 0:
        return

    h  = (math.sqrt(3) / 2) * side  
    ux = -dy / side
    uy =  dx / side

    apex = (mx + ux * h, my + uy * h) 

    pygame.draw.polygon(surface, color, [(x1, y1), (x2, y2), apex], w)


def draw_rhombus(surface, color, start, end, w):
    
    x1, y1 = start
    x2, y2 = end

    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2

    points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
    pygame.draw.polygon(surface, color, points, w)


def flood_fill(surface, pos, target, replacement):

    if target == replacement:
        return

    w, h  = surface.get_size()
    stack = [pos]

    while stack:
        x, y = stack.pop()

        if x < 0 or y < 0 or x >= w or y >= h:
            continue

        if surface.get_at((x, y))[:3] != target:
            continue

        surface.set_at((x, y), replacement)

        stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])


def preview_shape(surface, mode, start, end, size, toolbar_h):
      
    if not start or not end:
        return

    s = (start[0], start[1] + toolbar_h)
    e = (end[0],   end[1]   + toolbar_h)

    x1, y1 = s
    x2, y2 = e

    if mode == 'line':
        pygame.draw.line(surface, LIGHT_GRAY, s, e, size)

    elif mode == 'rect':
        pygame.draw.rect(surface, LIGHT_GRAY, norm_rect(x1, y1, x2, y2), size)

    elif mode == 'square':
        side = max(abs(x2 - x1), abs(y2 - y1))
        sx   = x1 if x2 >= x1 else x1 - side
        sy   = y1 if y2 >= y1 else y1 - side
        pygame.draw.rect(surface, LIGHT_GRAY, (sx, sy, side, side), size)

    elif mode == 'circle':
        r = int(((x2 - x1)**2 + (y2 - y1)**2) ** 0.5)
        pygame.draw.circle(surface, LIGHT_GRAY, s, r, size)

    elif mode == 'right_triangle':
        pygame.draw.polygon(surface, LIGHT_GRAY, [(x1, y1), (x2, y2), (x1, y2)], size)

    elif mode == 'equilateral_triangle':
        draw_equilateral_triangle(surface, LIGHT_GRAY, s, e, size)

    elif mode == 'rhombus':
        draw_rhombus(surface, LIGHT_GRAY, s, e, size)