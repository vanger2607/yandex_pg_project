import pygame
import button

pygame.init()

width = 600
height = 480
size = (width, height)
screen = pygame.display.set_mode(size)
img = pygame.image.load('SIM.png')
start_img = pygame.image.load('start.png').convert_alpha()
exit_img = pygame.image.load('exit.png').convert_alpha()
start_button = button.BTN(250, 200, start_img, 1)
exit_button = button.BTN(250, 300, exit_img, 1)
pygame.display.set_caption('SIM')
running = True

while running:
    if start_button.draw(screen):
        print('START')
    if exit_button.draw(screen):
        print('EXIT')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        screen.blit(img, (0, 0))
    pygame.display.update()
pygame.quit()