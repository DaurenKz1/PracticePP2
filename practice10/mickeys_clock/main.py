import pygame
import clock

pygame.init()

screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Mickey Clock")

clock_fps = pygame.time.Clock()
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((255, 255, 255))  

    clock.draw_hands(screen)

    pygame.display.flip()
    clock_fps.tick(60)

pygame.quit()