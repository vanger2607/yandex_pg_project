from classes_for_game import *
import pygame as pg

warnings.filterwarnings('ignore')
with open('map_for_second_level2.txt', 'r') as f:
    WALLS_AND_TILES_SECOND_LEVEL = []
    file = f.readlines()
    for i in file[:-3]:
        WALLS_AND_TILES_SECOND_LEVEL.append(i.strip())
pg.init()
fire_sound = pg.mixer.Sound('odnokratnyiy-piu.mp3')
summon_event = pg.USEREVENT + 1
pg.time.set_timer(summon_event, 1080 * 3)


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        level_map = list(map(lambda x: x.ljust(max_width, '.'), level_map))
        return level_map


pg.display.set_caption('way to freedom')
window = pg.display.set_mode((0, 0), pg.FULLSCREEN)


def generate_level(level, can_see_purple=450, can_see_green=370, can_see_boss=1000):
    """создает уровень"""
    new_player, x, y = None, None, None
    if level_id == 2:
        print('ok')
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty', x, y, False)
                elif level[y][x] == '#':
                    Tile('wall', x, y, True)
                elif level[y][x] == '@':
                    Tile('empty', x, y, False)
                    new_player = Hero('hero_left_step2.png', 10, 100, 5, x * 10, y * 10, 'left')
                    heroes.add(new_player)
                elif level[y][x] == 'e':
                    enemies.add(Enemy('pinky_gad.png', 5, 20, 1, x * 10, y * 10, can_see_purple))
                elif level[y][x] == 'F':
                    Fire_enemies.add(FiretoallEnemy('pinky_gad.png', 2, 80, 1, 15, x * 10, y * 10, can_see_purple))
                elif level[y][x] == 'f':
                    fire_enemies.add(FireEnemy('pinky_gad.png', 3, 20, 1, 20, x * 10, y * 10, can_see_purple))
                elif level[y][x] == 'G':
                    enemies.add(Green_gad('green_gad_right_step1.png', 4, 50, 3, x * 10, y * 10, can_see_green))

        return new_player, x, y
    if level_id == 3:
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty', x, y, False)
                elif level[y][x] == '#':
                    Tile('wall', x, y, True)
                elif level[y][x] == '@':
                    Tile('empty', x, y, False)
                    new_player = Hero('hero_left_step2.png', 10, 100, 5, x * 10, y * 10, 'left')
                    heroes.add(new_player)
                elif level[y][x] == 'e':
                    enemies.add(Enemy('mini_gad.png', 5, 20, 1, x * 10, y * 10))
                elif level[y][x] == 'F':
                    Fire_enemies.add(FiretoallEnemy('mini_gad.png', 2, 80, 1, 15, x * 10, y * 10))
                elif level[y][x] == 'f':
                    fire_enemies.add(FireEnemy('mini_gad.png', 3, 20, 1, 20, x * 10, y * 10))
                elif level[y][x] == 'G':
                    enemies.add(Green_gad('green_gad_right_step1.png', 4, 50, 3, x * 10, y * 10))
                elif level[y][x] == 'B':
                    Fire_enemies.add(Boss('Boss.png', 2, 50, 3, 20, x * 10, y * 10, can_see_boss))
        return new_player, x, y

    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y, False)
            elif level[y][x] == '#':
                Tile('wall', x, y, True)
            elif level[y][x] == '@':
                Tile('empty', x, y, False)
                new_player = Hero('hero_left_step2.png', 10, 100, 5, x * 10, y * 10, 'left')
                heroes.add(new_player)
            elif level[y][x] == 'e':
                enemies.add(Enemy('pinky_gad.png', 5, 20, 1, x * 10, y * 10))
            elif level[y][x] == 'F':
                Fire_enemies.add(FiretoallEnemy('pinky_gad.png', 2, 80, 1, 15, x * 10, y * 10))
            elif level[y][x] == 'f':
                fire_enemies.add(FireEnemy('pinky_gad.png', 3, 20, 1, 20, x * 10, y * 10))
            elif level[y][x] == 'G':
                enemies.add(Green_gad('green_gad_right_step1.png', 4, 50, 3, x * 10, y * 10))
            elif level[y][x] == 'B':
                Fire_enemies.add(Boss('Boss.png', 2, 50, 3, 20, x * 10, y * 10, can_see_boss))
    return new_player, x, y


def player_move(keys):
    """двигает персонажа когда пользователь нажимает на соответствующие кнопки"""
    global move_to
    if keys[pg.K_LEFT]:
        hero.update('left')
        hero.move_to = 'left'
    if keys[pg.K_RIGHT]:
        hero.update('right')
        hero.move_to = 'right'
    if keys[pg.K_UP]:
        hero.update('up')
    if keys[pg.K_DOWN]:
        hero.update('down')


def camera_func(camera, target_rect):
    """возвращает координаты, на которые сдвинулась камера"""
    left = -target_rect.x + 1000
    top = -target_rect.y + 650
    width, height = camera.width, camera.height

    return pg.Rect(left, top, width, height)


def level_window():
    global switch_start, switch_exit, switch_Settings, volume, img
    global first_level, second_level, third_level
    manager.clear_and_reset()
    switch_start, switch_exit, switch_Settings, volume, img = None, None, None, None, None
    first_level, second_level, third_level = None, None, None
    img = pygame.image.load('fon.png')
    img = transform.scale(img, size)
    screen.blit(img, (0, 0))
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


def main_renderer():
    global first_level, second_level, third_level
    global switch_start, switch_exit, switch_Settings, volume, img
    manager.clear_and_reset()
    switch_start, switch_exit, switch_Settings, volume, img = None, None, None, None, None
    first_level, second_level, third_level = None, None, None
    img = transform.scale(pygame.image.load('SIM.png'), size)
    pygame.display.set_caption('SIM')
    switch_start = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((120, 450), (300, 150)),
        text='START',
        manager=manager)
    switch_exit = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((120, 650), (300, 150)),
        text='EXIT',
        manager=manager)
    switch_Settings = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((120, 850), (300, 150)),
        text='SETTINGS',
        manager=manager)
    screen.blit(img, (0, 0))


def settings_render():
    global first_level, second_level, third_level
    global switch_start, switch_exit, switch_Settings, volume, img
    manager.clear_and_reset()
    switch_start, switch_exit, switch_Settings, volume, img = None, None, None, None, None
    first_level, second_level, third_level = None, None, None
    pygame.display.set_caption('SIM')
    img = pygame.image.load('fon.png')
    img = transform.scale(img, size)
    screen.blit(img, (0, 0))
    button_layout_rect = pygame.Rect(0, 0, 0, 0)
    button_layout_rect.size = (450, size[0] // 15)
    button_layout_rect.center = [size[0] // 2, size[1] // 2 - 300]
    UITextBox(html_text="<font size=7>   Настройки</font>",
              relative_rect=button_layout_rect,
              manager=manager,
              anchors={'left': 'left',
                       'right': 'right',
                       'top': 'top',
                       'bottom': 'bottom'})

    button_layout_rect.center = [size[0] // 2, size[1] // 2 - 150]
    UITextBox(html_text="<font size=7>   Громкость</font>",
              relative_rect=button_layout_rect,
              manager=manager,
              anchors={'left': 'left',
                       'right': 'right',
                       'top': 'top',
                       'bottom': 'bottom'})

    button_layout_rect.center = [size[0] // 2, size[1] // 2]
    volume = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(
        relative_rect=button_layout_rect,
        value_range=(0, 1),
        start_value=0.1,
        click_increment=0.1,
        manager=manager)


def saving(all_sprites_for_save=all_sprites_for_save,
           walls_for_battle=walls_for_battle, enemies_for_save=enemies_for_save, son='map1.txt'):
    """сохраняет уровень если игрок вышел во время игрового процесса"""

    def check():
        """проверяет если враг или герой находится "внутри" друг друга то сдвигает
        на одну клетку вправо, чтобы после сохранения песронаж или враг не исчез"""
        if sprite.type in important_types \
                and save[sprite.rect.y // 10][
            sprite.rect.x // 10] != '.' \
                and save[sprite.rect.y // 10][
            sprite.rect.x // 10] != '#':
            if sprite.rect.x // 10 != 1100:
                sprite.rect.x += 10
            else:
                sprite.rect.x -= 10

    save = [['.'] * 123 for _ in range(66)]
    important_types = ['@', 'F', 'f', 'e', 'G', 'B']
    for sprite in all_sprites_for_save:
        if sprite:
            try:
                check()
                if sprite.rect.x // 10 == 1 and sprite.type in important_types:
                    sprite.rect.x += 40
                elif sprite.rect.y // 10 == 42 and sprite.type in important_types:
                    sprite.rect.x += 40

                if sprite.type == '@':
                    save[sprite.rect.y // 10][sprite.rect.x // 10] = '@'
                if sprite.type == 'B':
                    save[sprite.rect.y // 10][sprite.rect.x // 10] = 'B'
                elif sprite.type == 'e':
                    save[sprite.rect.y // 10][sprite.rect.x // 10] = 'e'
                if sprite.type == 'F':
                    save[sprite.rect.y // 10][sprite.rect.x // 10] = 'F'
                if sprite.type == 'G':
                    save[sprite.rect.y // 10][sprite.rect.x // 10] = 'G'
                elif sprite.type == 'p':
                    save[sprite.rect.y // 10][sprite.rect.x // 10] = '.'

                else:
                    if save[sprite.rect.y // 10][
                        sprite.rect.x // 10] != '@' \
                            and save[sprite.rect.y // 10][
                        sprite.rect.x // 10] != 'F' \
                            and save[sprite.rect.y // 10][
                        sprite.rect.x // 10] != 'e' \
                            and save[sprite.rect.y // 10][
                        sprite.rect.x // 10] != 'f' \
                            and save[sprite.rect.y // 10][
                        sprite.rect.x // 10] != 'G' \
                            and save[sprite.rect.y // 10][
                        sprite.rect.x // 10] != 'B':
                        save[sprite.rect.y // 10][
                            sprite.rect.x // 10] = sprite.type
            except IndexError:
                pass
        for sprite in walls_for_battle:
            save[sprite.rect.y // 10][
                sprite.rect.x // 10] = sprite.type
        for i in enemies_for_save:
            enemies_hp.append(i.hp)
        text = ''
        for i in save:
            text += ''.join(i) + '\n'

        for i in all_sprites_for_save:
            i.kill()
        for i in all_sprites:
            i.kill()

        with open(son, 'w') as f:
            print(text, file=f)
            print(hero.hp, file=f)
            print(' '.join(map(str, enemies_hp)), file=f)


def main_menu_for():
    global first_level, second_level, third_level, level_id
    global switch_start, switch_exit, switch_Settings, volume, img
    manager.clear_and_reset()
    switch_start, switch_exit, switch_Settings, volume, img = None, None, None, None, None
    first_level, second_level, third_level = None, None, None
    main_renderer()
    current_size_menu = screen.get_size()
    menu_clock = pygame.time.Clock()
    while True:
        for menu_event in pygame.event.get():
            menu_time_delta = menu_clock.tick(60) / 1000.0
            if menu_event.type == pygame.QUIT:
                pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((250, 200), (300, 200)),
                    manager=manager,
                    window_title='Подтверждение',
                    action_long_desc='Are you serious?',
                    action_short_name='Yes',
                    blocking=True)
            elif menu_event.type == VIDEORESIZE:
                current_size_menu = menu_event.size
            elif menu_event.type == pygame.KEYUP:
                if menu_event.key == K_ESCAPE:
                    main_renderer()
            elif menu_event.type == pygame.USEREVENT:
                if menu_event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if menu_event.ui_element == switch_start:
                        level_window()
                    elif menu_event.ui_element == switch_exit:
                        pygame_gui.windows.UIConfirmationDialog(
                            rect=pygame.Rect((250, 200), (300, 200)),
                            manager=manager,
                            window_title='Подтверждение',
                            action_long_desc='Are you serious?',
                            action_short_name='Yes',
                            blocking=True)
                    elif menu_event.ui_element == switch_Settings:
                        settings_render()
                    elif menu_event.ui_object_id == 'horizontal_slider.#right_button':
                        pygame.mixer.music.set_volume(float(volume.get_current_value()) + 0.1)
                    elif menu_event.ui_object_id == 'horizontal_slider.#left_button':
                        pygame.mixer.music.set_volume(float(volume.get_current_value()) - 0.1)
                    elif menu_event.ui_element == first_level:
                        level_id = 1
                        return
                    elif menu_event.ui_element == second_level:
                        level_id = 2
                        return
                    elif menu_event.ui_element == third_level:
                        level_id = 3
                        return
                    elif menu_event.ui_object_id == '#confirmation_dialog.#confirm_button':
                        sys.exit(0)
            if not menu_event.__dict__ == {}:
                manager.process_events(menu_event)
            manager.update(menu_time_delta)

        virtual_surface.blit(img, (0, 0))
        scaled_surface = transform.scale(virtual_surface, current_size_menu)
        screen.blit(scaled_surface, (0, 0))
        manager.draw_ui(screen)
        pygame.display.update()
        menu_clock.tick(30)


def esc_menu_for():
    manager.clear_and_reset()
    pygame.display.set_caption('SIM')
    menu_window(manager)
    current_size_menu = screen.get_size()
    menu_clock = pygame.time.Clock()

    flag = False
    while True:
        for menu_event in pygame.event.get():
            menu_time_delta = menu_clock.tick(60) / 1000.0
            if menu_event.type == pygame.QUIT:
                pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((250, 200), (300, 200)),
                    manager=manager,
                    window_title='Подтверждение',
                    action_long_desc='Are you serious?',
                    action_short_name='Yes',
                    blocking=True)
            elif menu_event.type == pygame.KEYUP:
                if menu_event.key == K_ESCAPE:
                    if flag:
                        return 'resume'
                    else:
                        flag = True
            elif menu_event.type == pygame.USEREVENT:
                if menu_event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if menu_event.ui_object_id in ['#menu_dialog.#cancel_button', '#menu_dialog.#close_button']:
                        return 'resume'
                    elif menu_event.ui_object_id == '#menu_dialog.#confirm_button':
                        return 'menu'
                    elif menu_event.ui_object_id == '#menu_dialog.#save_button':
                        return 'save'

            if not menu_event.__dict__ == {}:
                manager.process_events(menu_event)
            manager.update(menu_time_delta)
        scaled_surface = transform.scale(virtual_surface, current_size_menu)
        screen.blit(scaled_surface, (0, 0))
        manager.draw_ui(screen)
        pygame.display.update()
        menu_clock.tick(30)


def first_level_for():
    global hero, now, all_time, enemies_hp, all_sprites, all_sprites_for_save, enemies, fire_enemies, fire_to_all
    total_level_width = width * 2
    total_level_height = height * 2
    camera = Camera(camera_func, total_level_width, total_level_height)
    flag = True
    FPS = 30

    img = pg.image.load('fon2.gif')
    img = transform.scale(img, (width, height))
    pg.display.set_caption('SIM')

    running = True
    player, level_x, level_y = generate_level(load_level(f'map{level_id}.txt'))
    hero = player

    with open(f'map{level_id}.txt', 'r') as f:
        file = f.readlines()
        file = ''.join(file).split('\n')
        hero.hp = int((file[-3]))
        print(file[-2])
        for num, i in enumerate(enemies_for_save):
            i.hp = int(file[-2].split()[num])
    portal = Portal(950, 210)
    clock = pg.time.Clock()
    while running:
        screen.blit(img, (0, 0))
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                esc = esc_menu_for()
                print(esc)
                if esc == 'resume':
                    continue
                if esc == 'menu':
                    shutil.copyfile("map.txt", "map1.txt")
                    for i in all_sprites_for_save:
                        i.kill()
                    for i in all_sprites:
                        i.kill()
                    for i in enemies_for_save:
                        i.kill()
                    flag = False
                    running = False
                    break
                if esc == 'save':
                    saving()
                    flag = False
                return

            for sprite in fire_enemies:
                sprite.attacking(hero.rect)

            for sprite in Fire_enemies:
                sprite.attacking(hero.rect)

        keys = pg.key.get_pressed()
        player_move(keys)
        for i in pg.sprite.spritecollide(hero, enemies_for_save, False):
            hero.hp -= i.attack
            # каким-то чудом работающая система удара врага о героя и не вылета врага за стены
            if i.where == 'left':
                if i.rect.x < 1120 and i.rect.x != 90:
                    i.rect.x += hero.speed * 2
            if i.where == 'right':
                try:
                    if i.rect.x > 40 and i.rect.x != 90:
                        i.rect.x -= hero.speed * 2
                except IndexError:
                    pass
            if i.where == 'up':
                if i.rect.y < 568:
                    i.rect.y += hero.speed * 2
            if i.where == 'down':
                if i.rect.y > 446:
                    i.rect.y -= hero.speed * 2

            hero.image = pg.image.load('hero_right_damaged.png')

        for hit in pg.sprite.groupcollide(enemies_for_save, bullets, False, True):
            hit.dead(first_weapon_dmg)
        if hero.hp <= 0:
            flag = False
            w = fontt.render('GAME OVER', True,
                             pg.Color('red'))
            screen.blit(w, (100, 100))
            pg.display.update()
            pg.time.delay(1000)

            shutil.copyfile("map.txt", "map1.txt")
            for i in all_sprites_for_save:
                i.kill()
            for i in all_sprites:
                i.kill()
            break

        if len(enemies) == 0 and len(fire_enemies) == 0 and len(Fire_enemies) == 0 and flag:
            screen.blit(portal.image, camera.apply(portal))
            for sprite in walls_for_battle:
                walls_for_battle.remove(sprite)
            walls_for_battle.update()
            walls_for_battle.draw(screen)

            if pg.sprite.spritecollide(portal, heroes, False, False):

                w = fontt.render('WON', True,
                                 pg.Color('red'))
                screen.blit(w, (550, 200))
                pg.time.delay(100)

                shutil.copyfile("map.txt", "map1.txt")
                for i in all_sprites_for_save:
                    i.kill()
                for i in all_sprites:
                    i.kill()
                break
        enemies.update(hero.rect)

        count_hp = fontt.render(str(hero.hp), True, pg.Color('red'))
        screen.blit(count_hp, (0, 0))

        if now - all_time < 2:
            now = t.time()

            reload_time = True

        elif now - all_time > 2:
            reload_time = False

        if keys[pg.K_SPACE] and not reload_time:
            hero.attacking('cubes')
            all_time = t.time()
            now = t.time()
        bullets.update()
        camera.update(hero)
        fire_enemies.update(hero.rect)
        Fire_enemies.update(hero.rect)
        if hero.rect[1] >= 435 and len(enemies) + len(fire_enemies) + len(
                Fire_enemies) > 0 \
                and not walls_for_battle:
            walls_for_battle.add(Tile('wall', 79, 41, False))
            walls_for_battle.add(Tile('wall', 80, 41, False))
            walls_for_battle.add(Tile('wall', 81, 41, False))
            walls_for_battle.add(Tile('wall', 82, 41, False))
            walls_for_battle.add(Tile('wall', 83, 41, False))
            walls_for_battle.add(Tile('wall', 84, 41, False))
            walls_for_battle.add(Tile('wall', 85, 41, False))
            walls_for_battle.add(Tile('wall', 86, 41, False))
            walls_for_battle.add(Tile('wall', 87, 41, False))
            walls_for_battle.add(Tile('wall', 88, 41, False))
            walls_for_battle.add(Tile('wall', 89, 41, False))
            walls_for_battle.add(Tile('wall', 90, 41, False))
            walls_for_battle.add(Tile('wall', 91, 41, False))
            walls_for_battle.add(Tile('wall', 92, 41, False))
            walls_for_battle.add(Tile('wall', 93, 41, False))
            walls_for_battle.add(Tile('wall', 94, 41, False))
            walls_for_battle.add(Tile('wall', 95, 41, False))

        enemy_bullets.update()
        for hit in pg.sprite.groupcollide(enemy_bullets, heroes, True, False):
            hero.hp -= hit.damage
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))
        for sprite in walls_for_battle:
            screen.blit(sprite.image, camera.apply(sprite))
        pg.display.update()


def second_level_for():
    global hero, now, all_time, enemies_hp, all_sprites, all_sprites_for_save, enemies, fire_enemies, fire_to_all
    running = True
    flag = True
    player, level_x, level_y = generate_level(load_level('map2.txt'), 260)
    hero = player
    clock = pg.time.Clock()
    FPS = 30
    total_level_width = width * 2
    total_level_height = height * 2
    camera = Camera(camera_func, total_level_width, total_level_height)
    for i in range(29, 89):
        walls_for_battle.add(Tile('wall', i, 35, False))

    with open('map2.txt', 'r') as f:
        file = f.readlines()
        file = ''.join(file).split('\n')
        hero.hp = int((file[-3]))
        for num, i in enumerate(enemies_for_save):
            i.hp = int(file[-2].split()[num])
    while running:
        screen.blit(img, (0, 0))
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                esc = esc_menu_for()
                if esc == 'resume':
                    continue
                if esc == 'menu':
                    shutil.copyfile("map_for_second_level2.txt", "map2.txt")
                    for i in all_sprites_for_save:
                        i.kill()
                    for i in all_sprites:
                        i.kill()
                    for i in enemies_for_save:
                        i.kill()
                    flag = False

                    running = False
                    break
                if esc == 'save':
                    saving(son='map2.txt')
                    flag = False
                return

            for sprite in fire_enemies:
                sprite.attacking(hero.rect)
            for sprite in Fire_enemies:
                sprite.attacking(hero.rect)
        keys = pg.key.get_pressed()
        player_move(keys)
        for i in pg.sprite.spritecollide(hero, enemies_for_save, False):
            hero.hp -= i.attack
            if i.type != 'G':
                # каким-то чудом работающая система удара врага о героя и не вылета врага за стены
                if i.where == 'left':
                    try:
                        if save_for_second_level[i.rect.y // 10][(i.rect.x + hero.speed * 2) // 10 + 6] != '#' \
                                and save_for_second_level[i.rect.y // 10][(i.rect.x + hero.speed * 2) // 10 + 5] \
                                != '#' \
                                and save_for_second_level[i.rect.y // 10][(i.rect.x + hero.speed * 2) // 10 + 4] \
                                != '#' \
                                and save_for_second_level[i.rect.y // 10][(i.rect.x + hero.speed * 2) // 10 + 3] \
                                != '#' \
                                and save_for_second_level[i.rect.y // 10][(i.rect.x + hero.speed * 2) // 10 + 2] \
                                != '#' \
                                and save_for_second_level[i.rect.y // 10][(i.rect.x + hero.speed * 2) // 10 + 1] \
                                != '#' \
                                and save_for_second_level[i.rect.y // 10][(i.rect.x + hero.speed * 2) // 10] != '#':
                            i.rect.x += hero.speed * 2
                    except IndexError:
                        pass
                if i.where == 'right':
                    try:
                        if save_for_second_level[i.rect.y // 10][(i.rect.x - hero.speed * 2) // 10 - 1] != '#' \
                                and i.rect.x - hero.speed * 2 != 89 and i.rect.x - hero.speed * 2 != 90 \
                                and save_for_second_level[i.rect.y // 10][(i.rect.x - hero.speed * 2) // 10 - 2] != '#':
                            i.rect.x -= hero.speed * 2
                    except IndexError:
                        pass
                if i.where == 'up':
                    try:
                        print((i.rect.y + hero.speed * 2) // 10)
                        if save_for_second_level[(i.rect.y + hero.speed * 2) // 10][i.rect.x // 10] != '#' \
                                and save_for_second_level[(i.rect.y + hero.speed * 2) // 10 + 1][i.rect.x // 10] != '#' \
                                and save_for_second_level[(i.rect.y + hero.speed * 2) // 10 + 2][i.rect.x // 10] != '#' \
                                and save_for_second_level[(i.rect.y + hero.speed * 2) // 10 + 3][i.rect.x // 10] != '#' \
                                and save_for_second_level[(i.rect.y + hero.speed * 2) // 10 + 4][i.rect.x // 10] != '#' \
                                and save_for_second_level[(i.rect.y + hero.speed * 2) // 10 + 5][i.rect.x // 10] != '#' \
                                and save_for_second_level[(i.rect.y + hero.speed * 2) // 10 + 6][i.rect.x // 10] != '#' \
                                and save_for_second_level[(i.rect.y + hero.speed * 2) // 10 + 7][i.rect.x // 10] != '#':
                            i.rect.y += hero.speed * 2
                    except IndexError:
                        pass
                if i.where == 'down':
                    try:
                        if save_for_second_level[(i.rect.y - hero.speed * 2) // 10 - 2][
                            i.rect.x // 10] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10 - 2][
                            i.rect.x // 10 + 1] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10 - 2][
                            i.rect.x // 10 + 2] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10 - 2][
                            i.rect.x // 10 - 2] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10 - 2][
                            i.rect.x // 10 - 1] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10 - 2][
                            i.rect.x // 10 + 3] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10 - 2][
                            i.rect.x // 10 - 3] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10 - 2][
                            i.rect.x // 10 - 4] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10 - 2][
                            i.rect.x // 10 - 5] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10 - 2][
                            i.rect.x // 10 - 6] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10 - 2][
                            i.rect.x // 10 + 4] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10 - 2][
                            i.rect.x // 10 + 5] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10 - 2][
                            i.rect.x // 10 + 6] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10 - 2][
                            i.rect.x // 10 - 7] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10 - 1][i.rect.x // 10] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10 - 1][
                            i.rect.x // 10 + 1] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10 - 1][
                            i.rect.x // 10 + 2] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10 - 1][
                            i.rect.x // 10 + 3] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10 - 1][
                            i.rect.x // 10 - 1] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10 - 1][
                            i.rect.x // 10 - 2] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10 - 1][
                            i.rect.x // 10 - 3] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10 - 2][i.rect.x // 10] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10 + 1][i.rect.x // 10] != '#' \
                                and save_for_second_level[(i.rect.y - hero.speed * 2) // 10][i.rect.x // 10] != '#':
                            i.rect.y -= hero.speed * 2
                    except IndexError:
                        pass
            elif i.type == 'G':
                if i.where == 'left':
                    try:
                        if save_for_second_level[hero.rect.y // 10][
                            (hero.rect.x + hero.speed) // 10 + 10] != '#' \
                                and (hero.rect.x + hero.speed) // 10 + 10 != 12:
                            hero.rect.x -= hero.speed - 1

                    except IndexError:
                        pass
                if i.where == 'right':
                    try:
                        if save_for_second_level[hero.rect.y // 10][
                            (hero.rect.x + hero.speed * 2) // 10 + 6] != '#':
                            hero.rect.x += hero.speed - 1
                    except IndexError:
                        pass
                if i.where == 'up':
                    try:
                        if save_for_second_level[hero.rect.y // 10 - 1][
                            hero.rect.x // 10] != '#' and hero.rect.y // 10 - 1 >= 2:
                            hero.rect.y -= hero.speed - 1
                    except IndexError:
                        pass
                if i.where == 'down':
                    try:
                        if save_for_second_level[hero.rect.y // 10 + 13][
                            hero.rect.x // 10] != '#' \
                                and (i.rect.y - hero.speed) // 10 + 15 != 47 \
                                and (i.rect.y - hero.speed) // 10 + 15 != 46 \
                                and (i.rect.y - hero.speed) // 10 + 15 != 45 \
                                and (i.rect.y - hero.speed) // 10 + 15 != 44 \
                                and (i.rect.y - hero.speed) // 10 + 15 != 43 \
                                and (i.rect.y - hero.speed) // 10 + 15 != 42 \
                                and (i.rect.y - hero.speed) // 10 + 15 != 41 \
                                and (i.rect.y - hero.speed) // 10 + 15 != 40 \
                                and (i.rect.y - hero.speed) // 10 + 15 != 39 \
                                and (i.rect.y - hero.speed) // 10 + 15 != 38:
                            hero.rect.y += hero.speed - 1
                    except IndexError:
                        pass
            hero.image = pg.image.load('hero_right_damaged.png')

        for hit in pg.sprite.groupcollide(enemies_for_save, bullets, False, True):
            hit.dead(first_weapon_dmg)
        if hero.hp <= 0:
            flag = False
            w = fontt.render('GAME OVER', True,
                             pg.Color('red'))
            screen.blit(w, (100, 100))
            pg.display.update()
            pg.time.delay(1000)
            running = False
            shutil.copyfile("map_for_second_level2.txt", "map2.txt")
            for i in all_sprites_for_save:
                i.kill()
            for i in all_sprites:
                i.kill()
        enemies.update(hero.rect)
        count_hp = fontt.render(str(hero.hp), True, pg.Color('red'))
        screen.blit(count_hp, (0, 0))

        if now - all_time < 2:
            now = t.time()

            reload_time = True

        elif now - all_time > 2:
            reload_time = False

        if keys[pg.K_SPACE] and not reload_time:
            hero.attacking('cubes')
            all_time = t.time()
            now = t.time()
        bullets.update()
        camera.update(hero)
        fire_enemies.update(hero.rect)
        Fire_enemies.update(hero.rect)
        enemy_bullets.update()
        for hit in pg.sprite.groupcollide(enemy_bullets, heroes, True, False):
            hero.hp -= hit.damage

        if len(green_gads) == 0:
            for sprite in walls_for_battle:
                sprite.kill()
        if len(enemies) == 0 and len(fire_enemies) == 0 and len(Fire_enemies) == 0 and flag:
            portal = Portal(10, 10)
            screen.blit(portal.image, camera.apply(portal))
            if pg.sprite.spritecollide(portal, heroes, False, False):
                w = fontt.render('WON', True,
                                 pg.Color('red'))
                screen.blit(w, (750, 750))
                pg.time.delay(100)
                running = False
                shutil.copyfile("map_for_second_level2.txt", "map2.txt")
                for i in all_sprites_for_save:
                    i.kill()
                for i in all_sprites:
                    i.kill()

        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))
        for sprite in walls_for_battle:
            screen.blit(sprite.image, camera.apply(sprite))
        pg.display.update()


def third_level_for():
    global hero, now, all_time, enemies_hp, all_sprites, all_sprites_for_save, enemies, fire_enemies, fire_to_all
    total_level_width = width * 2
    total_level_height = height * 2
    camera = Camera(camera_func, total_level_width, total_level_height)
    flag = True
    FPS = 30

    img = pg.image.load('fon2.gif')
    img = transform.scale(img, (width, height))
    pg.display.set_caption('SIM')

    running = True
    player, level_x, level_y = generate_level(load_level(f'map{level_id}.txt'))
    hero = player

    with open(f'map{level_id}.txt', 'r') as f:
        file = f.readlines()
        file = ''.join(file).split('\n')
        hero.hp = int((file[-3]))
        for num, i in enumerate(enemies_for_save):
            i.hp = int(file[-2].split()[num])
    portal = Portal(950, 210)
    clock = pg.time.Clock()
    while running:
        screen.blit(img, (0, 0))
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                esc = esc_menu_for()
                if esc == 'resume':
                    continue
                if esc == 'menu':
                    shutil.copyfile("map3_start.txt", "map3.txt")
                    for i in all_sprites_for_save:
                        i.kill()
                    for i in all_sprites:
                        i.kill()
                    for i in enemies_for_save:
                        i.kill()
                    flag = False
                    running = False
                    break

                if esc == 'save':
                    saving(son='map3.txt')
                    flag = False
                return
            if event.type == summon_event:
                for sprite in Fire_enemies:
                    sprite.summon()
        keys = pg.key.get_pressed()
        player_move(keys)
        for i in pg.sprite.spritecollide(hero, enemies_for_save, False):
            hero.hp -= i.attack
            if i.type == 'B':
                if i.where == 'left':
                    if hero.rect.x > 30:
                        hero.rect.x -= hero.speed
                if i.where == 'right':
                    if hero.rect.x < 1100:
                        hero.rect.x += hero.speed
                if i.where == 'up':
                    if hero.rect.y > 30:
                        hero.rect.y -= hero.speed
                if i.where == 'down':
                    if hero.rect.y < 580:
                        hero.rect.y += hero.speed
            hero.image = pg.image.load('hero_right_damaged.png')
        for hit in pg.sprite.groupcollide(enemies_for_save, bullets, False, True):
            hit.dead(first_weapon_dmg)
        if hero.hp <= 0:
            flag = False
            w = fontt.render('GAME OVER', True,
                             pg.Color('red'))
            screen.blit(w, (100, 100))
            pg.display.update()
            pg.time.delay(1000)
            running = False
            shutil.copyfile("map3_start.txt", "map3.txt")
            for i in all_sprites_for_save:
                i.kill()
            for i in all_sprites:
                i.kill()
        enemies.update(hero.rect)
        count_hp = fontt.render(str(hero.hp), True, pg.Color('red'))
        screen.blit(count_hp, (0, 0))

        if now - all_time < 2:
            now = t.time()

            reload_time = True

        elif now - all_time > 2:
            reload_time = False
        for sprite in Fire_enemies:
            sprite.attacking(hero.rect)
        if keys[pg.K_SPACE] and not reload_time:
            hero.attacking('cubes')
            all_time = t.time()
            now = t.time()
        bullets.update()
        camera.update(hero)
        fire_enemies.update(hero.rect)
        Fire_enemies.update(hero.rect)
        enemy_bullets.update()
        for hit in pg.sprite.groupcollide(enemy_bullets, heroes, True, False):
            hero.hp -= hit.damage
        if len(enemies) == 0 and len(fire_enemies) == 0 and len(Fire_enemies) == 0 and flag:
            portal = Portal(10, 10)
            screen.blit(portal.image, camera.apply(portal))
            if pg.sprite.spritecollide(portal, heroes, False, False):
                w = fontt.render('WON', True,
                                 pg.Color('red'))
                screen.blit(w, (750, 750))
                pg.time.delay(100)
                running = False
                shutil.copyfile("map3_start.txt", "map3.txt")
                for i in all_sprites_for_save:
                    i.kill()
                for i in all_sprites:
                    i.kill()

        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))
        for sprite in walls_for_battle:
            screen.blit(sprite.image, camera.apply(sprite))
        pg.display.update()


if __name__ == '__main__':
    pygame.init()
    virtual_surface = Surface(size)
    manager = pygame_gui.UIManager((1920, 1080))
    screen = pg.display.set_mode(size)
    switch_start, switch_exit, switch_Settings, volume, img, information_dialog = None, None, None, None, None, None
    first_level, second_level, third_level = None, None, None
    level_id = 1
    pygame.mixer.music.load('Main_sound.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    while True:
        main_menu_for()
        if level_id == 1:
            first_level_for()
        elif level_id == 2:
            second_level_for()
        elif level_id == 3:
            third_level_for()
