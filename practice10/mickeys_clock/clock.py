import pygame
import datetime

CENTER = (250, 200)

right_hand_img = pygame.image.load("images/right_hand.png")
left_hand_img = pygame.image.load("images/left_hand.png")

right_hand_img = pygame.transform.scale(right_hand_img, (40, 160))
left_hand_img = pygame.transform.scale(left_hand_img, (30, 220))


def get_time_angles():
    now = datetime.datetime.now()
    seconds = now.second
    minutes = now.minute

    sec_angle = seconds * 6
    min_angle = minutes * 6

    return sec_angle, min_angle


def draw_hands(screen):
    sec_angle, min_angle = get_time_angles()

    left_hand = pygame.transform.rotate(left_hand_img, -sec_angle)   
    right_hand = pygame.transform.rotate(right_hand_img, -min_angle) 
    left_rect = left_hand.get_rect(center=CENTER)
    right_rect = right_hand.get_rect(center=CENTER)

    screen.blit(right_hand, right_rect)
    screen.blit(left_hand, left_rect)