import pygame

pygame.init()


class BTN(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


width = 600
height = 480
size = (width, height)
screen = pygame.display.set_mode(size)
img = pygame.image.load('SIM.png')
start_button = BTN(250, 200, 'start.png')
exit_button = BTN(250, 300, 'exit.png')
pygame.display.set_caption('SIM')
running = True
screen.blit(img, (0, 0))
screen.blit(start_button.image, start_button.rect)
screen.blit(exit_button.image, exit_button.rect)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.rect.collidepoint(event.pos):
                print('START')
            elif exit_button.rect.collidepoint(event.pos):
                print('EXIT')
    pygame.display.update()
pygame.quit()
