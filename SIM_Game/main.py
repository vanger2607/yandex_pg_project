import pygame
import pygame_gui
from pygame import *

pygame.init()
width = 600
height = 480
size = (width, height)
virtual_surface = Surface(size)
manager = pygame_gui.UIManager((600, 480))
screen = pygame.display.set_mode(size, RESIZABLE)
current_size = screen.get_size()
img = pygame.image.load('SIM.png')
img = transform.scale(img, (600, 480))
pygame.display.set_caption('SIM')
pygame.mixer.music.load('Main_sound.mp3')
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play(-1)
switch_start = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((120, 10), (150, 100)),
    text='START',
    manager=manager)
switch_exit = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((120, 110), (150, 100)),
    text='EXIT',
    manager=manager)
switch_Settings = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((120, 210), (150, 100)),
    text='SETTINGS',
    manager=manager)
difficulty = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
    options_list=['Easy', 'Medium', 'Hard', 'Very Hard'], starting_option='Easy',
    relative_rect=pygame.Rect((120, 320), (150, 100)),
    manager=manager)
running = True
screen.blit(img, (0, 0))
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        time_delta = clock.tick(60) / 1000.0
        if event.type == pygame.QUIT:
            information_dialog = pygame_gui.windows.UIConfirmationDialog(
                rect=pygame.Rect((250, 200), (300, 200)),
                manager=manager,
                window_title='Подтверждение',
                action_long_desc='Are you seriously?',
                action_short_name='Yes',
                blocking=True)
        elif event.type == VIDEORESIZE:
            current_size = event.size
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                running = False
            else:
                screen.blit(img, (0, 0))
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                print('difficulty:', event.text)
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == switch_start:
                    print('START')
                    size = (width, height)
                    virtual_surface = Surface(size)
                    manager = pygame_gui.UIManager((1980, 1080))
                    screen = pygame.display.set_mode(size, RESIZABLE)
                    first_level = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((10, 10), (120, 100)),
                        text='1',
                        manager=manager)
                    second_level = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((130, 10), (120, 100)),
                        text='2',
                        manager=manager)
                    third_level = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((250, 10), (120, 100)),
                        text='3',
                        manager=manager)
                    fourth_level = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((370, 10), (120, 100)),
                        text='4',
                        manager=manager)
                    fifth_level = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((490, 10), (110, 100)),
                        text='5',
                        manager=manager)
                    if event.ui_element == first_level:
                        print('asa')
                    if event.ui_element == second_level:
                        print('asa')
                    if event.ui_element == third_level:
                        print('asa')
                    if event.ui_element == fourth_level:
                        print('asa')
                    if event.ui_element == fifth_level:
                        print('asa')
                if event.ui_element == switch_exit:
                    print('EXIT')
                    information_dialog = pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect((250, 200), (300, 200)),
                        manager=manager,
                        window_title='Подтверждение',
                        action_long_desc='Are you seriously?',
                        action_short_name='Yes',
                        blocking=True)
                if event.ui_element == switch_Settings:
                    print('SETTINGS')
        manager.process_events(event)
        manager.update(time_delta)
    virtual_surface.blit(img, (0, 0))
    scaled_surface = transform.scale(virtual_surface, current_size)
    screen.blit(scaled_surface, (0, 0))
    manager.draw_ui(screen)
    pygame.display.update()
pygame.quit()
