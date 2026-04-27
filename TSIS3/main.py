import pygame, sys, os, time
from pygame.locals import *

from racer       import GameSession, SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from ui          import MainMenu, NameEntry, SettingsScreen, GameOverScreen, LeaderboardScreen
from persistence import load_settings, save_settings, load_leaderboard, add_leaderboard_entry


pygame.init()
pygame.mixer.init()

SURF  = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RACER — TSIS3")
CLOCK = pygame.time.Clock()

ASSETS_DIR = "assets"


MUSIC_FILE = os.path.join(ASSETS_DIR, "background.wav")

def start_music():
    """Start looping background music."""
    if not os.path.exists(MUSIC_FILE):
        return
    try:
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except Exception:
        pass

def stop_music():
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass






def run_game(settings: dict, username: str):
    session = GameSession(settings)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return "quit", session

        alive = session.update()

        session.draw(SURF)
        pygame.display.flip()
        CLOCK.tick(FPS)

        if not alive:

            pygame.time.wait(600)
            return "dead", session

        if session.finished:
            return "finished", session



def main():
    settings = load_settings()
    username = ""

    main_menu = MainMenu()
    go_screen = GameOverScreen()
    lb_screen = LeaderboardScreen()

    state = "menu"

    while True:
        if state == "menu":
            choice = main_menu.run(SURF, CLOCK)

            if choice == "quit":
                break

            elif choice == "play":
                if not username:
                    ne = NameEntry()
                    username = ne.run(SURF, CLOCK)
                state = "game"

            elif choice == "leaderboard":
                entries = load_leaderboard()
                lb_screen.run(SURF, CLOCK, entries)

            elif choice == "settings":
                ss = SettingsScreen(settings)
                settings = ss.run(SURF, CLOCK)
                save_settings(settings)

        elif state == "game":
            if settings.get("sound", True):
                start_music()
            outcome, session = run_game(settings, username)
            stop_music()

            if outcome == "quit":
                break

            final = session.final_score()
            add_leaderboard_entry(username, final,
                                  session.distance, session.coins)

            if outcome == "finished":
                SURF.fill((30, 120, 30))
                fnt = pygame.font.SysFont("Verdana", 48, bold=True)
                lbl = fnt.render("FINISH!", True, (255, 240, 60))
                SURF.blit(lbl, lbl.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
                pygame.display.flip()
                pygame.time.wait(2000)

            result = go_screen.run(SURF, CLOCK,
                                   final, session.distance, session.coins)
            if result == "retry":
                state = "game"
            elif result == "menu":
                state = "menu"
            else:
                break

    stop_music()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()