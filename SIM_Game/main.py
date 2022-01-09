from typing import Union

import pygame
import pygame_gui
from pygame import *
from pygame_gui.core import ObjectID
from pygame_gui._constants import UI_CONFIRMATION_DIALOG_CONFIRMED, UI_BUTTON_PRESSED, OldType
from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui.elements import UIButton


class menu_window(pygame_gui.elements.ui_window.UIWindow):
    def __init__(self, manager: IUIManagerInterface, object_id: Union[ObjectID, str] = ObjectID('#menu_dialog', None)):
        inf = display.Info()
        widow_size = inf.current_w, inf.current_h
        size = [widow_size[0] // 2.5, widow_size[1] // 1.5]
        rectangle = pygame.Rect(0, 0, 0, 0)
        rectangle.size = size
        rectangle.center = (widow_size[0] // 2, widow_size[1] // 2)
        super().__init__(rectangle, manager,
                         window_display_title='Меню',
                         object_id=object_id,
                         resizable=True,
                         visible=1)
        self.set_blocking(True)

        button_layout_rect = pygame.Rect(0, 0, 0, 0)
        button_layout_rect.size = (size[0], size[0] // 10)
        button_layout_rect.center = [size[1] // 2, size[1] // 2]

        self.cancel_button = UIButton(relative_rect=button_layout_rect,
                                      text='Продолжить',
                                      manager=self.ui_manager,
                                      container=self,
                                      object_id='#cancel_button',
                                      )

        self.confirm_button = UIButton(relative_rect=button_layout_rect,
                                       text='назад к выбору уровня',
                                       manager=self.ui_manager,
                                       container=self,
                                       object_id='#confirm_button',
                                       anchors={'left': 'right',
                                                'right': 'right',
                                                'top': 'top',
                                                'bottom': 'bottom'})
        self.confirm_button.hide()

    def process_event(self, event: pygame.event.Event) -> bool:
        consumed_event = super().process_event(event)

        if event.type == UI_BUTTON_PRESSED and event.ui_element == self.cancel_button:
            self.kill()

        if event.type == UI_BUTTON_PRESSED and event.ui_element == self.confirm_button:
            # old event - to be removed in 0.8.0
            event_data = {'user_type': OldType(UI_CONFIRMATION_DIALOG_CONFIRMED),
                          'ui_element': self,
                          'ui_object_id': self.most_specific_combined_id}
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, event_data))
            # new event
            event_data = {'ui_element': self,
                          'ui_object_id': self.most_specific_combined_id}
            pygame.event.post(pygame.event.Event(UI_CONFIRMATION_DIALOG_CONFIRMED, event_data))

        return consumed_event


pygame.init()


def level_window():
    # pygame.mixer.music.stop()
    pygame.display.set_caption('SIM')
    # pygame.mixer.music.load('level_sound.mp3')
    # pygame.mixer.music.set_volume(0.8)
    # pygame.mixer.music.play(-1)
    width = 600
    height = 480
    size = (width, height)
    manager = pygame_gui.UIManager((1980, 1080))
    screen = pygame.display.set_mode(size, RESIZABLE)
    img = pygame.image.load('fon.png')
    img = transform.scale(img, (700, 480))
    screen.blit(img, (0, 0))
    virtual_surface = Surface(size)
    current_size = screen.get_size()
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
    # noinspection PyUnboundLocalVariable
    menu_ui = None
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            time_delta = clock.tick(60) / 1000.0
            if event.type == pygame.QUIT:
                pygame_gui.windows.UIConfirmationDialog(
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
                    if not event.ui_element == menu_ui:
                        running = False
                else:
                    screen.blit(img, (0, 0))
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == first_level:
                        menu_ui = menu_window(manager=manager)
                    if event.ui_element == second_level:
                        print('Please waiting, 2 level are loading')
                    # noinspection PyUnboundLocalVariable
                    if event.ui_element == third_level:
                        print('Please waiting, 3 level are loading')
                    # noinspection PyUnboundLocalVariable
                    if event.ui_element == fourth_level:
                        print('Please waiting, 4 level are loading')
                    # noinspection PyUnboundLocalVariable
                    if event.ui_element == fifth_level:
                        print('Please waiting, 5 level are loading')
            manager.process_events(event)
            manager.update(time_delta)
        virtual_surface.blit(img, (0, 0))
        scaled_surface = transform.scale(virtual_surface, current_size)
        screen.blit(scaled_surface, (0, 0))
        manager.draw_ui(screen)
        pygame.display.update()


def Main_window():
    pygame.init()
    width = 600
    height = 480
    size = (width, height)
    virtual_surface = Surface(size)
    manager = pygame_gui.UIManager((1920, 1080))
    screen = pygame.display.set_mode(size, RESIZABLE)
    current_size = screen.get_size()
    img = pygame.image.load('SIM.png')
    img = transform.scale(img, (600, 480))
    pygame.display.set_caption('SIM')
    # pygame.mixer.music.load('Main_sound.mp3')
    # pygame.mixer.music.set_volume(0.2)
    # pygame.mixer.music.play(-1)
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
    running = True
    screen.blit(img, (0, 0))
    clock = pygame.time.Clock()
    while running:
        for i in pygame.event.get():
            time_delta = clock.tick(60) / 1000.0
            if i.type == pygame.QUIT:
                information_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((250, 200), (300, 200)),
                    manager=manager,
                    window_title='Подтверждение',
                    action_long_desc='Are you seriously?',
                    action_short_name='Yes',
                    blocking=True)
            elif i.type == VIDEORESIZE:
                current_size = i.size
            if i.type == pygame.USEREVENT:
                if i.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    running = False
                else:
                    screen.blit(img, (0, 0))
                if i.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if i.ui_element == volume:
                        pygame.mixer.music.set_volume(float(i.text))
                if i.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if i.ui_element == switch_start:
                        print('START')
                        level_window()
                    if i.ui_element == switch_exit:
                        print('EXIT')
                        information_dialog = pygame_gui.windows.UIConfirmationDialog(
                            rect=pygame.Rect((250, 200), (300, 200)),
                            manager=manager,
                            window_title='Подтверждение',
                            action_long_desc='Are you seriously?',
                            action_short_name='Yes',
                            blocking=True)
                    if i.ui_element == switch_Settings:
                        print('SETTINGS')
                        pygame.display.set_caption('SIM')
                        pygame.mixer.music.load('Main_sound.mp3')
                        pygame.mixer.music.set_volume(0.2)
                        pygame.mixer.music.play(-1)
                        size = (width, height)
                        manager = pygame_gui.UIManager((1980, 1080))
                        screen = pygame.display.set_mode(size, RESIZABLE)
                        img = pygame.image.load('fon.png')
                        img = transform.scale(img, (700, 480))
                        screen.blit(img, (0, 0))
                        volume = pygame_gui.elements.ui_horizontal_slider.UI_HORIZONTAL_SLIDER_MOVED(
                            value_range=tuple('1'),
                            start_value='0',
                            starting_option='Change volume',
                            relative_rect=pygame.Rect((200, 150), (250, 100)),
                            manager=manager)
            manager.process_events(i)
            manager.update(time_delta)
        virtual_surface.blit(img, (0, 0))
        scaled_surface = transform.scale(virtual_surface, current_size)
        screen.blit(scaled_surface, (0, 0))
        manager.draw_ui(screen)
        pygame.display.update()
    pygame.quit()


while Main_window():
    Main_window()
