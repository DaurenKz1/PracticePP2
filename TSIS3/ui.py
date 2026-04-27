import pygame
from pygame.locals import *
from racer import SCREEN_WIDTH, SCREEN_HEIGHT, draw_rounded_rect

BG        = (15,  15,  25)
ACCENT    = (255, 200,  40)
BTN_NORM  = (40,  45,  70)
BTN_HOV   = (70,  80, 130)
BTN_BORD  = (80,  90, 140)
WHITE     = (255, 255, 255)
GRAY      = (160, 160, 160)
BLACK     = (0,   0,   0)
GREEN     = (60,  200,  80)
RED_C     = (220,  50,  50)
BLUE_C    = (60,  120, 220)
GOLD      = (255, 215,   0)
SILVER    = (192, 192, 192)
BRONZE    = (205, 127,  50)


def _fnt(size, bold=False):
    return pygame.font.SysFont("Verdana", size, bold=bold)



class Button:
    def __init__(self, text, rect, font_size=20):
        self.text  = text
        self.rect  = pygame.Rect(rect)
        self.fnt   = _fnt(font_size, bold=True)
        self.hov   = False

    def draw(self, surf):
        col = BTN_HOV if self.hov else BTN_NORM
        draw_rounded_rect(surf, col,    self.rect, 8)
        pygame.draw.rect (surf, BTN_BORD, self.rect, 2, border_radius=8)
        lbl = self.fnt.render(self.text, True, WHITE)
        surf.blit(lbl, lbl.get_rect(center=self.rect.center))

    def update(self, pos):
        self.hov = self.rect.collidepoint(pos)

    def clicked(self, event):
        return (event.type == MOUSEBUTTONDOWN and event.button == 1
                and self.rect.collidepoint(event.pos))



def draw_title(surf, text, cy, size=52):
    fnt = _fnt(size, bold=True)
    shadow = fnt.render(text, True, (0, 0, 0))
    lbl    = fnt.render(text, True, ACCENT)
    cx     = SCREEN_WIDTH // 2
    surf.blit(shadow, shadow.get_rect(center=(cx + 2, cy + 2)))
    surf.blit(lbl,    lbl.get_rect(center=(cx, cy)))


def draw_bg(surf):
    surf.fill(BG)
    # subtle grid
    for i in range(0, SCREEN_WIDTH, 40):
        pygame.draw.line(surf, (25, 28, 45), (i, 0), (i, SCREEN_HEIGHT))
    for j in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.line(surf, (25, 28, 45), (0, j), (SCREEN_WIDTH, j))



class MainMenu:
    def __init__(self):
        cx = SCREEN_WIDTH // 2
        self.btns = {
            "play":        Button("Play",        (cx-90, 240, 180, 44)),
            "leaderboard": Button("Leaderboard", (cx-90, 300, 180, 44)),
            "settings":    Button("Settings",    (cx-90, 360, 180, 44)),
            "quit":        Button("Quit",        (cx-90, 420, 180, 44)),
        }
        self.fnt_sub = _fnt(14)

    def run(self, surf, clock) -> str:
        while True:
            pos = pygame.mouse.get_pos()
            for b in self.btns.values():
                b.update(pos)

            for event in pygame.event.get():
                if event.type == QUIT:
                    return "quit"
                for key, btn in self.btns.items():
                    if btn.clicked(event):
                        return key

            draw_bg(surf)
            draw_title(surf, "RACER", 120)
            sub = self.fnt_sub.render("Dodge traffic · Collect power-ups · Beat the track",
                                      True, GRAY)
            surf.blit(sub, sub.get_rect(center=(SCREEN_WIDTH//2, 170)))
            for b in self.btns.values():
                b.draw(surf)

            pygame.display.flip()
            clock.tick(60)



class NameEntry:
    MAX_LEN = 14

    def __init__(self):
        self.fnt_title = _fnt(30, bold=True)
        self.fnt_input = _fnt(26, bold=True)
        self.fnt_hint  = _fnt(14)
        self.name      = ""

    def run(self, surf, clock) -> str:
        box = pygame.Rect(SCREEN_WIDTH//2 - 110, 270, 220, 44)
        ok  = Button("Start Race", (SCREEN_WIDTH//2 - 80, 340, 160, 44))

        while True:
            pos = pygame.mouse.get_pos()
            ok.update(pos)

            for event in pygame.event.get():
                if event.type == QUIT:
                    return "Player"
                if event.type == KEYDOWN:
                    if event.key == K_RETURN and self.name.strip():
                        return self.name.strip()
                    elif event.key == K_BACKSPACE:
                        self.name = self.name[:-1]
                    elif len(self.name) < self.MAX_LEN and event.unicode.isprintable():
                        self.name += event.unicode
                if ok.clicked(event) and self.name.strip():
                    return self.name.strip()

            draw_bg(surf)
            draw_title(surf, "ENTER YOUR NAME", 150, size=32)

            # input box
            draw_rounded_rect(surf, BTN_NORM, box, 8)
            pygame.draw.rect(surf, ACCENT, box, 2, border_radius=8)
            txt = self.fnt_input.render(self.name + "|", True, WHITE)
            surf.blit(txt, txt.get_rect(center=box.center))

            ok.draw(surf)
            hint = self.fnt_hint.render("Press Enter or click Start", True, GRAY)
            surf.blit(hint, hint.get_rect(center=(SCREEN_WIDTH//2, 400)))

            pygame.display.flip()
            clock.tick(60)



class SettingsScreen:
    """Returns updated settings dict."""

    def __init__(self, settings: dict):
        self.s = dict(settings)   # local copy
        cx     = SCREEN_WIDTH // 2
        self.btn_sound = Button(self._sound_label(),  (cx-90, 220, 180, 40))
        self.btn_diff  = Button(self._diff_label(),   (cx-90, 280, 180, 40))
        self.btn_car   = Button(self._car_label(),    (cx-90, 340, 180, 40))
        self.btn_back  = Button("Back",             (cx-90, 430, 180, 40))
        self.fnt_lbl   = _fnt(14)

    def _sound_label(self):  return f"Sound: {'ON' if self.s['sound'] else 'OFF'}"
    def _diff_label(self):   return f"Difficulty: {self.s['difficulty'].capitalize()}"
    def _car_label(self):    return f"Car color: {self.s['car_color'].capitalize()}"

    def _refresh(self):
        self.btn_sound.text = self._sound_label()
        self.btn_diff.text  = self._diff_label()
        self.btn_car.text   = self._car_label()

    def run(self, surf, clock) -> dict:
        btns = [self.btn_sound, self.btn_diff, self.btn_car, self.btn_back]
        while True:
            pos = pygame.mouse.get_pos()
            for b in btns:
                b.update(pos)

            for event in pygame.event.get():
                if event.type == QUIT:
                    return self.s
                if self.btn_sound.clicked(event):
                    self.s["sound"] = not self.s["sound"]
                elif self.btn_diff.clicked(event):
                    order = ["easy", "normal", "hard"]
                    idx   = order.index(self.s["difficulty"])
                    self.s["difficulty"] = order[(idx + 1) % 3]
                elif self.btn_car.clicked(event):
                    order = ["red", "blue", "green"]
                    idx   = order.index(self.s["car_color"])
                    self.s["car_color"] = order[(idx + 1) % 3]
                elif self.btn_back.clicked(event):
                    return self.s
                self._refresh()

            draw_bg(surf)
            draw_title(surf, "SETTINGS", 120, size=38)
            self._hint(surf, "SOUND",      220)
            self._hint(surf, "DIFFICULTY", 280)
            self._hint(surf, "CAR COLOR",  340)
            for b in btns:
                b.draw(surf)

            pygame.display.flip()
            clock.tick(60)

    def _hint(self, surf, text, y):
        lbl = self.fnt_lbl.render(text, True, GRAY)
        surf.blit(lbl, (SCREEN_WIDTH//2 - 88, y - 16))



class GameOverScreen:
    def __init__(self):
        cx = SCREEN_WIDTH // 2
        self.btn_retry = Button("Retry",     (cx-90, 400, 180, 44))
        self.btn_menu  = Button("Main Menu", (cx-90, 460, 180, 44))
        self.fnt_big   = _fnt(40, bold=True)
        self.fnt_med   = _fnt(20, bold=True)
        self.fnt_sm    = _fnt(16)

    def run(self, surf, clock, score, distance, coins) -> str:
        while True:
            pos = pygame.mouse.get_pos()
            self.btn_retry.update(pos)
            self.btn_menu.update(pos)

            for event in pygame.event.get():
                if event.type == QUIT:
                    return "quit"
                if self.btn_retry.clicked(event):
                    return "retry"
                if self.btn_menu.clicked(event):
                    return "menu"

            draw_bg(surf)

            # red flash band
            pygame.draw.rect(surf, (80, 0, 0), (0, 160, SCREEN_WIDTH, 90))
            lbl = self.fnt_big.render("GAME OVER", True, RED_C)
            surf.blit(lbl, lbl.get_rect(center=(SCREEN_WIDTH//2, 200)))

            # stats
            stats = [
                ("Score",    str(score)),
                ("Distance", f"{distance} m"),
                ("Coins",    str(coins)),
            ]
            for i, (k, v) in enumerate(stats):
                ky = self.fnt_med.render(k + ":", True, GRAY)
                vl = self.fnt_med.render(v,       True, WHITE)
                y  = 290 + i * 34
                surf.blit(ky, (80,  y))
                surf.blit(vl, (250, y))

            self.btn_retry.draw(surf)
            self.btn_menu.draw(surf)

            pygame.display.flip()
            clock.tick(60)



class LeaderboardScreen:
    def __init__(self):
        self.btn_back = Button("Back", (SCREEN_WIDTH//2 - 60, 550, 120, 36))
        self.fnt_hd   = _fnt(15, bold=True)
        self.fnt_row  = _fnt(14)
        self.medals   = [GOLD, SILVER, BRONZE]

    def run(self, surf, clock, entries: list) -> None:
        while True:
            pos = pygame.mouse.get_pos()
            self.btn_back.update(pos)

            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if self.btn_back.clicked(event):
                    return

            draw_bg(surf)
            draw_title(surf, "LEADERBOARD", 70, size=34)

            # header
            cols = (30, 130, 230, 310, 370)
            headers = ("#", "Name", "Score", "Dist", "Coins")
            for hdr, x in zip(headers, cols):
                lbl = self.fnt_hd.render(hdr, True, ACCENT)
                surf.blit(lbl, (x, 110))
            pygame.draw.line(surf, ACCENT, (20, 128), (SCREEN_WIDTH-20, 128), 1)

            # rows
            for i, e in enumerate(entries[:10]):
                y   = 135 + i * 38
                col = self.medals[i] if i < 3 else WHITE

                # alternating row bg
                if i % 2 == 0:
                    pygame.draw.rect(surf, (25, 28, 45),
                                     (20, y-2, SCREEN_WIDTH-40, 34),
                                     border_radius=4)

                vals = [
                    str(i+1),
                    e.get("name", "?")[:12],
                    str(e.get("score", 0)),
                    f"{e.get('distance', 0)}m",
                    str(e.get("coins", 0)),
                ]
                for val, x in zip(vals, cols):
                    lbl = self.fnt_row.render(val, True, col)
                    surf.blit(lbl, (x, y + 8))

            if not entries:
                msg = self.fnt_hd.render("No entries yet — play first!", True, GRAY)
                surf.blit(msg, msg.get_rect(center=(SCREEN_WIDTH//2, 280)))

            self.btn_back.draw(surf)
            pygame.display.flip()
            clock.tick(60)