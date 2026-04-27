import pygame
import random
import math
import os
from pygame.locals import *

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600
FPS           = 60

# Colors
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
RED    = (220,  40,  40)
BLUE   = ( 30, 100, 220)
GREEN  = ( 30, 180,  60)
YELLOW = (255, 210,   0)
ORANGE = (255, 140,   0)
GRAY   = (120, 120, 120)
DARK   = ( 30,  30,  30)
LIGHT_GRAY = (200, 200, 200)
ROAD_GRAY  = ( 60,  60,  60)
LANE_MARK  = (255, 255, 100)
NITRO_COL  = ( 50, 230, 255)
SHIELD_COL = ( 80, 130, 255)
REPAIR_COL = ( 60, 210,  80)
OIL_COL    = ( 20,  20,  80)
BUMP_COL   = (160, 100,  30)
NITRO_STRIP = (255, 200,  20)

# Road layout  (3 lanes)
LANE_CENTERS = [100, 200, 300]
ROAD_LEFT    = 40
ROAD_RIGHT   = 360

CAR_COLORS = {
    "red":   RED,
    "blue":  BLUE,
    "green": GREEN,
}

DIFFICULTY = {
    "easy":   {"base_speed": 4,  "enemies": 1, "obstacles": 1},
    "normal": {"base_speed": 5,  "enemies": 2, "obstacles": 2},
    "hard":   {"base_speed": 7,  "enemies": 3, "obstacles": 3},
}

POWERUP_TYPES   = ["nitro", "shield", "repair"]
POWERUP_TIMEOUT = 7_000   


def draw_rounded_rect(surf, color, rect, radius=8):
    pygame.draw.rect(surf, color, rect, border_radius=radius)


ASSETS_DIR = "assets"

def load_image(filename, size=None):
    """Load image from assets/ folder first, then current dir. Returns None on failure."""
    candidates = [
        os.path.join(ASSETS_DIR, filename),
        filename,
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                if size:
                    img = pygame.transform.scale(img, size)
                return img
            except Exception:
                pass
    return None


def safe_spawn_x(player_rect, margin=60):
    """Return a random x that isn't directly above the player."""
    for _ in range(20):
        x = random.randint(ROAD_LEFT + 20, ROAD_RIGHT - 20)
        if abs(x - player_rect.centerx) > margin:
            return x
    return random.choice([c for c in LANE_CENTERS
                          if abs(c - player_rect.centerx) > margin] or LANE_CENTERS)



class Road:
    """Scrolling road with lane markers. Uses AnimatedStreet.png if present."""
    def __init__(self):
        self.scroll_y  = 0
        self.segment_h = 60
        bg = load_image("AnimatedStreet.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bg = bg  

    def update(self, speed):
        self.scroll_y = (self.scroll_y + speed) % (self.segment_h * 2)

    def draw(self, surf):
        if self.bg:
            y_off = int(self.scroll_y) % SCREEN_HEIGHT
            surf.blit(self.bg, (0, y_off - SCREEN_HEIGHT))
            surf.blit(self.bg, (0, y_off))
            return

        pygame.draw.rect(surf, ROAD_GRAY,
                         (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, SCREEN_HEIGHT))
        pygame.draw.rect(surf, (200, 40, 40), (ROAD_LEFT - 10, 0, 10, SCREEN_HEIGHT))
        pygame.draw.rect(surf, (200, 40, 40), (ROAD_RIGHT,     0, 10, SCREEN_HEIGHT))
        for lx in [150, 250]:
            y = -self.segment_h + self.scroll_y
            while y < SCREEN_HEIGHT:
                pygame.draw.rect(surf, LANE_MARK, (lx - 2, int(y), 4, 30))
                y += self.segment_h * 2



class Player(pygame.sprite.Sprite):
    def __init__(self, color="red"):
        super().__init__()
        self.color_name  = color
        self.color       = CAR_COLORS.get(color, RED)
        self.image       = self._load_or_draw(color)
        self.rect        = self.image.get_rect(center=(200, 520))
        self.speed           = 5
        self.shield          = False
        self.shield_cooldown = 0
        self.nitro           = False
        self.nitro_timer     = 0

    @staticmethod
    def _load_or_draw(color_name):
        for fname in (f"Player_{color_name}.png", "Player.png"):
            img = load_image(fname, (40, 60))
            if img is not None:
                return img
        return Player._make_image(CAR_COLORS.get(color_name, RED))

    @staticmethod
    def _make_image(color):
        img = pygame.Surface((40, 60), pygame.SRCALPHA)
        draw_rounded_rect(img, color,           (5,  5, 30, 50), 6)
        draw_rounded_rect(img, (180, 230, 255), (9, 10, 22, 14), 3)
        for wx, wy in [(2, 10), (28, 10), (2, 38), (28, 38)]:
            pygame.draw.rect(img, DARK, (wx, wy, 10, 12), border_radius=3)
        return img

    def set_color(self, color_name):
        self.color_name = color_name
        self.color      = CAR_COLORS.get(color_name, RED)
        cx = self.rect.centerx
        cy = self.rect.centery
        self.image = self._load_or_draw(color_name)
        self.rect  = self.image.get_rect(center=(cx, cy))

    def move(self):
        keys = pygame.key.get_pressed()
        spd  = 7 if self.nitro else self.speed

        if keys[K_LEFT]  and self.rect.left  > ROAD_LEFT:
            self.rect.move_ip(-spd, 0)
        if keys[K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.move_ip( spd, 0)
        if keys[K_UP]    and self.rect.top   > SCREEN_HEIGHT // 2:
            self.rect.move_ip(0, -spd)
        if keys[K_DOWN]  and self.rect.bottom < SCREEN_HEIGHT - 10:
            self.rect.move_ip(0,  spd)

    def activate_nitro(self, duration_ms=4000):
        self.nitro       = True
        self.nitro_timer = pygame.time.get_ticks() + duration_ms

    def activate_shield(self):
        self.shield          = True
        self.shield_cooldown = 0  
    def shield_absorb(self):
        self.shield          = False
        self.shield_cooldown = pygame.time.get_ticks() + 1500  # 1.5 s grace

    def shield_on_cooldown(self):
        return pygame.time.get_ticks() < self.shield_cooldown

    def update(self):
        if self.nitro and pygame.time.get_ticks() > self.nitro_timer:
            self.nitro = False

    def draw_overlay(self, surf):
        if self.shield:
            cx, cy = self.rect.center
            pygame.draw.circle(surf, (*SHIELD_COL, 140),
                               (cx, cy), 36, 3)
        if self.nitro:
            remaining = max(0, self.nitro_timer - pygame.time.get_ticks())
            for i in range(5):
                fy = self.rect.bottom + i * 7 + random.randint(-2, 2)
                fx = self.rect.centerx + random.randint(-6, 6)
                r  = max(2, 8 - i * 1.5)
                alpha_surf = pygame.Surface((int(r*2), int(r*2)), pygame.SRCALPHA)
                a = int(200 - i * 35)
                pygame.draw.circle(alpha_surf, (*NITRO_COL, a),
                                   (int(r), int(r)), int(r))
                surf.blit(alpha_surf, (int(fx - r), int(fy - r)))



class Enemy(pygame.sprite.Sprite):
    COLORS = [(180, 60, 60), (60, 60, 180), (60, 160, 60),
              (160, 120, 40), (120, 40, 120)]

    _cached_img  = None   # set once after first successful load
    _load_done   = False  # flag so we only attempt once

    def __init__(self, player_rect=None):
        super().__init__()
        self.image = self._get_image()
        self.rect  = self.image.get_rect()
        self._respawn(player_rect)

    @classmethod
    def _get_image(cls):
        if not cls._load_done:
            cls._cached_img = load_image("Enemy.png", (40, 60))
            cls._load_done  = True
        if cls._cached_img is not None:
            return cls._cached_img.copy()
        return cls._make_image(random.choice(cls.COLORS))

    @staticmethod
    def _make_image(color):
        img = pygame.Surface((40, 60), pygame.SRCALPHA)
        draw_rounded_rect(img, color,           (5,  5, 30, 50), 6)
        draw_rounded_rect(img, (180, 230, 255), (9, 10, 22, 14), 3)
        for wx, wy in [(2, 10), (28, 10), (2, 38), (28, 38)]:
            pygame.draw.rect(img, DARK, (wx, wy, 10, 12), border_radius=3)
        return img

    def _respawn(self, player_rect=None):
        if player_rect:
            x = safe_spawn_x(player_rect)
        else:
            x = random.choice(LANE_CENTERS)
        self.rect.center = (x, -random.randint(10, 200))

    def move(self, speed, player_rect=None):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT + 20:
            self._respawn(player_rect)



class Coin(pygame.sprite.Sprite):
    _base_img  = None   
    _img_tried = False

    def __init__(self, player_rect=None):
        super().__init__()
        self.value = random.choices([1, 2, 3], weights=[5, 3, 2])[0]
        sz         = 16 + self.value * 6
        self.image = self._get_image(sz)
        self.rect  = self.image.get_rect()
        self._spawn(player_rect)

    @classmethod
    def _get_image(cls, sz):
        if not cls._img_tried:
            cls._base_img  = load_image("coin.png")
            cls._img_tried = True

        if cls._base_img is not None:
            return pygame.transform.scale(cls._base_img, (sz, sz))

        img = pygame.Surface((sz, sz), pygame.SRCALPHA)
        col = [YELLOW, ORANGE, (220, 180, 255)][min(sz // 6 - 3, 2)]
        pygame.draw.circle(img, col,          (sz//2, sz//2), sz//2)
        pygame.draw.circle(img, (255,255,255),(sz//2, sz//2), sz//2, 2)
        return img

    def _spawn(self, player_rect=None):
        if player_rect:
            x = safe_spawn_x(player_rect)
        else:
            x = random.choice(LANE_CENTERS)
        self.rect.center = (x, -random.randint(10, 300))

    def move(self, speed, player_rect=None):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT + 10:
            self._spawn(player_rect)



class PowerUp(pygame.sprite.Sprite):
    INFO = {
        "nitro":  {"color": NITRO_COL,   "label": "N", "desc": "NITRO"},
        "shield": {"color": SHIELD_COL,  "label": "S", "desc": "SHIELD"},
        "repair": {"color": REPAIR_COL,  "label": "R", "desc": "REPAIR"},
    }

    def __init__(self, kind, player_rect=None):
        super().__init__()
        self.kind    = kind
        self.born    = pygame.time.get_ticks()
        info         = self.INFO[kind]
        self.image   = self._make_img(info["color"], info["label"])
        self.rect    = self.image.get_rect()
        x = safe_spawn_x(player_rect) if player_rect else random.choice(LANE_CENTERS)
        self.rect.center = (x, -20)

    @staticmethod
    def _make_img(color, label):
        img = pygame.Surface((36, 36), pygame.SRCALPHA)
        pygame.draw.rect(img, color, (0, 0, 36, 36), border_radius=8)
        pygame.draw.rect(img, WHITE,  (0, 0, 36, 36), 2, border_radius=8)
        fnt = pygame.font.SysFont("Verdana", 18, bold=True)
        lbl = fnt.render(label, True, WHITE)
        img.blit(lbl, lbl.get_rect(center=(18, 18)))
        return img

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.kill()
        if pygame.time.get_ticks() - self.born > POWERUP_TIMEOUT:
            self.kill()



class Obstacle(pygame.sprite.Sprite):
    """Oil spill, pothole, speed bump."""

    def __init__(self, kind="oil", player_rect=None):
        super().__init__()
        self.kind  = kind
        self.image = self._make_img(kind)
        self.rect  = self.image.get_rect()
        x = safe_spawn_x(player_rect) if player_rect else random.choice(LANE_CENTERS)
        self.rect.center = (x, -20)
        self.slow_zone = (kind == "oil")

    @staticmethod
    def _make_img(kind):
        if kind == "oil":
            img = pygame.Surface((50, 30), pygame.SRCALPHA)
            pygame.draw.ellipse(img, (*OIL_COL, 200), (0, 0, 50, 30))
            return img
        elif kind == "pothole":
            img = pygame.Surface((34, 22), pygame.SRCALPHA)
            pygame.draw.ellipse(img, (20, 20, 20), (0, 0, 34, 22))
            pygame.draw.ellipse(img, (50, 40, 30), (4, 4, 26, 14))
            return img
        else:  # speed bump
            img = pygame.Surface((70, 18), pygame.SRCALPHA)
            pygame.draw.rect(img, BUMP_COL, (0, 0, 70, 18), border_radius=5)
            for i in range(0, 70, 10):
                pygame.draw.line(img, (200, 160, 60), (i, 0), (i, 18), 3)
            return img

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.kill()



class NitroStrip(pygame.sprite.Sprite):
    """A horizontal strip that briefly boosts the player."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((ROAD_RIGHT - ROAD_LEFT, 14), pygame.SRCALPHA)
        self.image.fill((*NITRO_STRIP, 180))
        for i in range(0, ROAD_RIGHT - ROAD_LEFT, 20):
            pygame.draw.rect(self.image, (255, 255, 255, 100), (i, 0, 10, 14))
        self.rect = self.image.get_rect(topleft=(ROAD_LEFT, -20))

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()



class MovingBarrier(pygame.sprite.Sprite):
    """Horizontally oscillating barrier."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((80, 18), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (220, 60, 0), (0, 0, 80, 18), border_radius=4)
        for i in range(0, 80, 14):
            pygame.draw.line(self.image, (255, 200, 0), (i, 0), (i+7, 18), 3)
        self.rect     = self.image.get_rect(center=(200, -20))
        self.dx       = random.choice([-2, 2])
        self.base_spd = 0

    def move(self, speed):
        self.rect.move_ip(0, speed)
        self.rect.move_ip(self.dx, 0)
        if self.rect.left < ROAD_LEFT or self.rect.right > ROAD_RIGHT:
            self.dx *= -1
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()



class HUD:
    def __init__(self):
        self.fnt_big   = pygame.font.SysFont("Verdana", 22, bold=True)
        self.fnt_small = pygame.font.SysFont("Verdana", 16)
        self.fnt_tiny  = pygame.font.SysFont("Verdana", 13)

    def draw(self, surf, score, coins, distance, finish_dist,
             active_pu, pu_remaining_ms, speed_val):
        self._label(surf, f"Score:  {score}",    10, 10)
        self._label(surf, f"Coins:  {coins}",    10, 32)
        self._label(surf, f"Speed: {speed_val:.0f}", 10, 54)

        bx, by, bw, bh = 100, 8, 200, 14
        pygame.draw.rect(surf, GRAY,  (bx, by, bw, bh), border_radius=4)
        pct = min(1.0, distance / finish_dist)
        pygame.draw.rect(surf, GREEN, (bx, by, int(bw * pct), bh), border_radius=4)
        pygame.draw.rect(surf, WHITE, (bx, by, bw, bh), 1, border_radius=4)
        lbl = self.fnt_tiny.render(
            f"{distance}m / {finish_dist}m", True, WHITE)
        surf.blit(lbl, (bx + bw//2 - lbl.get_width()//2, by + 17))

        if active_pu:
            pu_sec = max(0, pu_remaining_ms) // 1000
            col = PowerUp.INFO[active_pu]["color"]
            txt = f"{PowerUp.INFO[active_pu]['desc']}  {pu_sec}s"
            lbl = self.fnt_small.render(txt, True, col)
            pygame.draw.rect(surf, (30, 30, 30),
                             (SCREEN_WIDTH - lbl.get_width() - 16,
                              8, lbl.get_width() + 12, 22),
                             border_radius=5)
            surf.blit(lbl, (SCREEN_WIDTH - lbl.get_width() - 10, 11))

    def _label(self, surf, text, x, y):
        shadow = self.fnt_small.render(text, True, BLACK)
        surf.blit(shadow, (x+1, y+1))
        lbl = self.fnt_small.render(text, True, WHITE)
        surf.blit(lbl, (x, y))



class GameSession:

    FINISH_DISTANCE = 2000   # metres to finish line

    def __init__(self, settings: dict):
        diff   = settings.get("difficulty", "normal")
        color  = settings.get("car_color",  "red")
        cfg    = DIFFICULTY[diff]

        self.base_speed      = cfg["base_speed"]
        self.current_speed   = float(self.base_speed)
        self.score           = 0
        self.coins           = 0
        self.distance        = 0        # metres
        self.dist_accum      = 0.0      # pixel accumulator
        self.active_pu       = None     # current power-up type
        self.pu_end_ms       = 0
        self.oil_slowed      = False
        self.oil_slow_end    = 0
        self.alive           = True

        self.road      = Road()
        self.player    = Player(color)
        self.hud       = HUD()

        # sprite groups
        self.enemies   = pygame.sprite.Group()
        self.coins_grp = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.powerups  = pygame.sprite.Group()
        self.events    = pygame.sprite.Group()
        self.all_spr   = pygame.sprite.Group()

        self.all_spr.add(self.player)

        for _ in range(cfg["enemies"]):
            e = Enemy(self.player.rect)
            self.enemies.add(e)
            self.all_spr.add(e)

        for _ in range(3):
            c = Coin(self.player.rect)
            self.coins_grp.add(c)
            self.all_spr.add(c)

        for _ in range(cfg["obstacles"]):
            kind = random.choice(["oil", "pothole", "speed_bump"])
            o = Obstacle(kind, self.player.rect)
            self.obstacles.add(o)
            self.all_spr.add(o)

        # spawn timers
        self.next_pu_spawn  = pygame.time.get_ticks() + random.randint(5000, 10000)
        self.next_ev_spawn  = pygame.time.get_ticks() + random.randint(8000, 15000)
        self.speed_tick     = pygame.time.get_ticks()
        self.score_tick     = pygame.time.get_ticks()
        self.diff_level     = 0

    def update(self):
        now   = pygame.time.get_ticks()
        speed = self._effective_speed(now)

        # distance
        self.dist_accum += speed
        if self.dist_accum >= 10:
            metres = int(self.dist_accum // 10)
            self.distance    += metres
            self.dist_accum  %= 10

        # time-based score
        if now - self.score_tick > 500:
            self.score      += 1
            self.score_tick  = now

        # gradual speed increase every 3 s
        if now - self.speed_tick > 3000:
            self.current_speed = min(self.base_speed + 6,
                                     self.current_speed + 0.3)
            self.speed_tick = now

        # difficulty scaling
        new_level = self.distance // 300
        if new_level > self.diff_level:
            self.diff_level = new_level
            self._scale_difficulty()

        # road scroll
        self.road.update(speed)

        # move entities
        self.player.update()
        self.player.move()

        for e in self.enemies:
            e.move(speed, self.player.rect)
        for c in self.coins_grp:
            c.move(speed, self.player.rect)
        for o in self.obstacles:
            o.move(speed)
        for pu in self.powerups:
            pu.move(speed)
        for ev in self.events:
            ev.move(speed)

        # power-up timeout
        if self.active_pu and now > self.pu_end_ms:
            self.active_pu = None

        # spawn power-up
        if now > self.next_pu_spawn and not self.powerups:
            kind = random.choice(POWERUP_TYPES)
            pu   = PowerUp(kind, self.player.rect)
            self.powerups.add(pu)
            self.all_spr.add(pu)
            self.next_pu_spawn = now + random.randint(8000, 16000)

        # spawn road event
        if now > self.next_ev_spawn:
            self._spawn_event()
            self.next_ev_spawn = now + random.randint(6000, 14000)

        # collisions
        return self._check_collisions(now)

    def _effective_speed(self, now):
        spd = self.current_speed
        if self.player.nitro:
            spd *= 1.8
        if self.oil_slowed and now < self.oil_slow_end:
            spd *= 0.5
        elif self.oil_slowed:
            self.oil_slowed = False
        return spd

    def _scale_difficulty(self):
        if self.diff_level % 2 == 0 and len(self.enemies) < 6:
            e = Enemy(self.player.rect)
            self.enemies.add(e)
            self.all_spr.add(e)
        if len(self.obstacles) < 5:
            kind = random.choice(["oil", "pothole", "speed_bump"])
            o = Obstacle(kind, self.player.rect)
            self.obstacles.add(o)
            self.all_spr.add(o)

    def _spawn_event(self):
        kind = random.choice(["nitro_strip", "barrier"])
        if kind == "nitro_strip":
            ev = NitroStrip()
        else:
            ev = MovingBarrier()
        self.events.add(ev)
        self.all_spr.add(ev)

    def _check_collisions(self, now):
        # collect coins
        for c in pygame.sprite.spritecollide(self.player, self.coins_grp, True):
            self.coins += c.value
            self.score += c.value * 10
            nc = Coin(self.player.rect)
            self.coins_grp.add(nc)
            self.all_spr.add(nc)

        for pu in pygame.sprite.spritecollide(self.player, self.powerups, True):
            self._apply_powerup(pu.kind, now)

        for ev in pygame.sprite.spritecollide(self.player, self.events, False):
            if isinstance(ev, NitroStrip):
                self.player.activate_nitro(3000)
                self.active_pu  = "nitro"
                self.pu_end_ms  = now + 3000
                ev.kill()

        for obs in pygame.sprite.spritecollide(self.player, self.obstacles, True):
            if obs.kind == "oil":
                self.oil_slowed  = True
                self.oil_slow_end = now + 2500
            elif obs.kind == "pothole":
                if self.player.shield:
                    self.player.shield_absorb()
                    self.active_pu = None
                else:
                    self.score = max(0, self.score - 30)
            else:
                self.oil_slowed   = True
                self.oil_slow_end = now + 1000
            # respawn obstacle
            kind = random.choice(["oil", "pothole", "speed_bump"])
            no = Obstacle(kind, self.player.rect)
            self.obstacles.add(no)
            self.all_spr.add(no)

        if pygame.sprite.spritecollideany(self.player, self.enemies):
            if self.player.shield:
                self.player.shield_absorb()
                self.active_pu = None
            elif not self.player.shield_on_cooldown():
                self.alive = False
                return False

        for ev in pygame.sprite.spritecollide(self.player, self.events, False):
            if isinstance(ev, MovingBarrier):
                if self.player.shield:
                    self.player.shield_absorb()
                    self.active_pu = None
                    ev.kill()
                elif not self.player.shield_on_cooldown():
                    self.alive = False
                    return False

        return True

    def _apply_powerup(self, kind, now):
        if kind == "nitro":
            self.player.activate_nitro(4000)
            self.active_pu = "nitro"
            self.pu_end_ms = now + 4000
        elif kind == "shield":
            self.player.activate_shield()
            self.active_pu = "shield"
            self.pu_end_ms = now + 30_000   # shield lasts until hit
        elif kind == "repair":
            self.oil_slowed    = False
            self.player.shield = False      
            self.score        += 50
            self.active_pu     = None       # instant

    def draw(self, surf):
        self.road.draw(surf)

        for spr in self.all_spr:
            if spr is not self.player:
                surf.blit(spr.image, spr.rect)

        self.player.draw_overlay(surf)
        surf.blit(self.player.image, self.player.rect)

        remaining_pu_ms = self.pu_end_ms - pygame.time.get_ticks()
        self.hud.draw(surf, self.score, self.coins, self.distance,
                      self.FINISH_DISTANCE, self.active_pu,
                      remaining_pu_ms, self.current_speed)

    @property
    def finished(self):
        return self.distance >= self.FINISH_DISTANCE

    def final_score(self):
        bonus = (self.FINISH_DISTANCE - self.distance) // 10 if self.finished else 0
        return self.score + bonus + self.coins * 5