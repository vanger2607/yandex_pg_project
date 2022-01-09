import pygame as pg
import pygame_gui
from pygame_gui.elements import UIDropDownMenu
from pygame import *
import time as t
import shutil
import sys
PAUSE = False
pg.init()
enemies_hp = []

def terminate():
    pg.quit()
    sys.exit()


reload_time = True
fontt = pg.font.Font(None, 100)
WEAPONS = ['first_gun', 'second_gun']
weapon = WEAPONS[0]
all_time = t.time()
now = t.time()
my_event = pg.USEREVENT + 1
fire_to_all = pg.USEREVENT + 2



class Fon(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites_for_save)
        self.image = pg.image.load('portal.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = 'p'


class Portal(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites_for_save)
        self.image = pg.image.load('portal.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = 'p'


class Bullet(pg.sprite.Sprite):
    def __init__(self, img, speed, damage, x, y, where):
        super().__init__(all_sprites)

        self.image = pg.image.load(img)
        self.rect = self.image.get_rect()
        self.damage = damage
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.where = where

    def update(self, *args):
        if self.where == 'left':
            self.rect.x -= self.speed
        elif self.where == 'right':
            self.rect.x += self.speed
        elif self.where == 'down':
            self.rect.y += self.speed
        elif self.where == 'up':
            self.rect.y -= self.speed
        if self.rect.x <= 10 or self.rect.x >= width - 10:
            self.kill()
        if pg.sprite.spritecollide(self, walls, False):
            self.kill()


first_weapon_dmg = 15
pg.time.set_timer(my_event, 360)
pg.time.set_timer(fire_to_all, 750)


class Hero(pg.sprite.Sprite):
    """класс для главного героя нашей игры"""

    def __init__(self, img, speed, hp, attack, x, y):
        super().__init__(all_sprites, all_sprites_for_save)
        self.image = pg.image.load(img)
        self.speed = speed
        self.hp = hp
        self.attack = attack
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.right_move = 0
        self.left_move = 0
        self.rect = self.image.get_rect().move(
            1 * x, 1 * y)
        self.type = '@'
        all_sprites.add(self)

    def attacking(self, weapon, ):
        # В разработке
        global bullets
        where = self.rect.x
        up_down = self.rect.y
        if move_to == 'left':
            where = self.rect.left
            img = 'fireball_left.png'
        elif move_to == 'right':
            img = 'fireball_right.png'
            where = self.rect.right

        bullet = Bullet(img, 15, first_weapon_dmg, where, up_down, move_to)

        bullets.add(bullet)
        bullet.update(move_to)

    def update(self, *args):
        if args[0] == 'right' and self.rect.x + self.speed < width - list(self.rect)[2]:
            self.right_move += 1
            if self.right_move > 2:
                self.right_move = 0
            if self.right_move == 0:
                self.image = pg.image.load('hero_right_step1.png')
            elif self.right_move == 1:
                self.image = pg.image.load('hero_right_step2.png')
            elif self.right_move == 2:
                self.image = pg.image.load('hero_right_step3.png')
            self.rect.x += self.speed
            block_hit_list = pg.sprite.spritecollide(self, walls, False)
            strange_walls = pg.sprite.spritecollide(self, walls_for_battle, False)
            for block in block_hit_list:
                self.rect.right = block.rect.left
            for block in strange_walls:
                self.rect.right = block.rect.left
        if args[0] == 'left' and self.rect.x - self.speed > 0:
            self.left_move += 1
            if self.left_move > 2:
                self.left_move = 0
            if self.left_move == 0:
                self.image = pg.image.load('hero_left_step2.png')
            if self.left_move == 1:
                self.image = pg.image.load('hero_left_step3.png')
            if self.left_move == 2:
                self.image = pg.image.load('hero_left_step4.png')

            self.rect.x -= self.speed
            """проверка на столкновение со стеной и реализация его"""
            block_hit_list = pg.sprite.spritecollide(self, walls, False)
            strange_walls = pg.sprite.spritecollide(self, walls_for_battle, False)
            for block in block_hit_list:
                self.rect.left = block.rect.right
            for block in strange_walls:
                self.rect.left = block.rect.right
        if args[0] == 'up' and self.rect.y - self.speed > 0:
            self.rect.y -= self.speed
            block_hit_list = pg.sprite.spritecollide(self, walls, False)
            strange_walls = pg.sprite.spritecollide(self, walls_for_battle, False)
            for block in block_hit_list:
                self.rect.top = block.rect.bottom
            for block in strange_walls:
                self.rect.top = block.rect.bottom

        if args[0] == 'down' and self.rect.y + self.speed < height - list(self.rect)[3]:
            self.rect.y += self.speed
            block_hit_list = pg.sprite.spritecollide(self, walls, False)
            strange_walls = pg.sprite.spritecollide(self, walls_for_battle, False)
            for block in block_hit_list:
                self.rect.bottom = block.rect.top
            for block in strange_walls:
                self.rect.bottom = block.rect.top


class Enemy(pg.sprite.Sprite):
    """просто бегающий за игроком враг"""

    def __init__(self, img, speed, hp, attack, x, y):
        super().__init__(all_sprites, all_sprites_for_save, enemies_for_save)
        self.image = pg.image.load(img)
        self.speed = speed
        self.hp = hp
        self.attack = attack
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.where = ''
        self.can_see_y = 150
        self.type = 'e'
        self.all_time = t.time()
        self.now = t.time()
        self.reload_time = False

    def reload(self, how_long):
        if self.now - self.all_time < how_long:
            self.now = t.time()

            self.reload_time = True

        elif self.now - self.all_time > how_long:
            self.reload_time = False

    def attacking(self):
        pass

    def update(self, *args):
        if self.hp <= 0:
            self.kill()
        if args[0][0] > self.rect.x and abs(args[0][1] - self.rect.y) <= self.can_see_y:
            self.where = 'right'
            self.rect.x += self.speed
            block_hit_list = pg.sprite.spritecollide(self, walls, False)
            strange_walls = pg.sprite.spritecollide(self, walls_for_battle, False)
            for block in block_hit_list:
                self.rect.right = block.rect.left
            for block in strange_walls:
                self.rect.right = block.rect.left
        if args[0][0] < self.rect.x and abs(args[0][1] - self.rect.y) <= self.can_see_y:
            if self.rect.x != 0 and args[0][0] % self.rect.x != 0:
                self.rect.x -= 1
            self.where = 'left'
            self.rect.x -= self.speed
            block_hit_list = pg.sprite.spritecollide(self, walls, False)
            strange_walls = pg.sprite.spritecollide(self, walls_for_battle, False)
            for block in block_hit_list:
                self.rect.left = block.rect.right
            for block in strange_walls:
                self.rect.left = block.rect.right
        if args[0][1] > self.rect.y and abs(args[0][1] - self.rect.y) <= self.can_see_y:
            if self.rect.y != 0 and args[0][1] % self.rect.y != 0:
                self.rect.y -= 1
            self.rect.y += self.speed
            self.where = 'down'
            block_hit_list = pg.sprite.spritecollide(self, walls, False)
            strange_walls = pg.sprite.spritecollide(self, walls_for_battle, False)
            for block in block_hit_list:
                self.rect.bottom = block.rect.top
            for block in strange_walls:
                self.rect.bottom = block.rect.top

        if args[0][1] < self.rect.y and abs(args[0][1] - self.rect.y) <= self.can_see_y:
            self.where = 'up'
            self.rect.y -= self.speed
            block_hit_list = pg.sprite.spritecollide(self, walls, False)
            strange_walls = pg.sprite.spritecollide(self, walls_for_battle, False)
            for block in block_hit_list:
                self.rect.top = block.rect.bottom
            for block in strange_walls:
                self.rect.top = block.rect.bottom

    def dead(self, damage):
        self.hp -= damage


x_map = 0
y_map = 0


def load_level(filename):
    global x_map, y_map
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        level_map = list(map(lambda x: x.ljust(max_width, '.'), level_map))
        x_map = len(level_map[0])
        y_map = len(level_map)
        return level_map


class FireEnemy(Enemy):
    """класс для стреляющего врага, который выпускает пули в одном направлении в одном направление"""

    def __init__(self, img, speed, hp, damage, x, y):
        super().__init__(img, speed, hp, damage, x, y)
        self.bullet_len = 175
        self.type = 'f'

    def attacking(self, hero_rect):
        # перереботать механику выпуска пуль
        self.reload(3)
        move_to_bullet = 'right'
        if hero_rect[0] > self.rect.x:
            move_to_bullet = 'right'
        elif hero_rect[0] < self.rect.x:
            move_to_bullet = 'left'
        if not self.reload_time:
            move_to_enemy = 'right'
            self.all_time = t.time()
            self.now = t.time()
            if (self.bullet_len >= abs(hero_rect.y - self.rect.y)) \
                    and hero_rect[1] >= self.can_see_y:
                there = self.rect.x
                up_down = self.rect.y
                if self.where == 'left':
                    there = self.rect.left
                elif self.where == 'right':
                    there = self.rect.right
                elif self.where == 'up':
                    there, up_down = self.rect.midtop
                elif self.where == 'down':
                    there, up_dow = self.rect.midbottom

                if not reload_time:
                    self.all_time = t.time()
                    self.now = t.time()
                    enemy_bullet = Bullet('enemy_bullets.png', 10, first_weapon_dmg, there, up_down, move_to_bullet)
                    enemy_bullets.add(enemy_bullet)

    def update(self, *args):
        if self.hp <= 0:
            self.kill()
        elif args[0][1] < self.rect.y and abs(args[0][1] - self.rect.y) <= self.can_see_y:
            self.rect.y -= self.speed
            block_hit_list = pg.sprite.spritecollide(self, walls, False)
            strange_walls = pg.sprite.spritecollide(self, walls_for_battle, False)
            self.where = 'up'
            for block in block_hit_list:
                self.rect.top = block.rect.bottom
            for block in strange_walls:
                self.rect.top = block.rect.bottom
        if args[0][1] > self.rect.y and abs(args[0][1] - self.rect.y) <= self.can_see_y:
            if self.rect.y != 0 and args[0][1] % self.rect.y != 0:
                self.rect.y -= 1
            self.rect.y += self.speed
            self.where = 'down'
            block_hit_list = pg.sprite.spritecollide(self, walls, False)
            strange_walls = pg.sprite.spritecollide(self, walls_for_battle, False)
            for block in block_hit_list:
                self.rect.bottom = block.rect.top
            for block in strange_walls:
                self.rect.bottom = block.rect.top
        elif args[0][0] < self.rect.x and abs(args[0][1] - self.rect.y) <= self.can_see_y:
            if self.rect.x != 0 and args[0][0] % self.rect.x != 0:
                self.rect.x -= 1
            self.where = 'left'
            self.rect.x -= self.speed
            block_hit_list = pg.sprite.spritecollide(self, walls, False)
            strange_walls = pg.sprite.spritecollide(self, walls_for_battle, False)
            for block in block_hit_list:
                self.rect.left = block.rect.right
            for block in strange_walls:
                self.rect.left = block.rect.right
        elif args[0][0] > self.rect.x and abs(args[0][1] - self.rect.y) <= self.can_see_y:
            self.where = 'right'
            self.rect.x += self.speed
            block_hit_list = pg.sprite.spritecollide(self, walls, False)
            strange_walls = pg.sprite.spritecollide(self, walls_for_battle, False)
            for block in block_hit_list:
                self.rect.right = block.rect.left
            for block in strange_walls:
                self.rect.right = block.rect.left


class FiretoallEnemy(Enemy):
    """враг стреляющей во все стороны"""

    def __init__(self, img, speed, hp, damage, x, y):
        super().__init__(img, speed, hp, damage, x, y)
        self.type = 'F'

    def attacking(self, hero_rect):
        self.reload(3)
        if hero_rect[1] >= self.can_see_y and not (self.reload_time):
            self.all_time = t.time()
            self.now = t.time()
            enemy_bullet = Bullet('enemy_bullets.png', 10, 5, self.rect.left, self.rect.y, 'left')
            enemy_bullets.add(enemy_bullet)
            enemy_bullet = Bullet('enemy_bullets.png', 10, 5, self.rect.right, self.rect.y, 'right')
            enemy_bullets.add(enemy_bullet)
            enemy_bullet = Bullet('enemy_bullets.png', 10, 5,
                                  self.rect.midtop[0], self.rect.midtop[1], 'up')
            enemy_bullets.add(enemy_bullet)
            enemy_bullet = Bullet('enemy_bullets.png', 10, first_weapon_dmg,
                                  self.rect.midbottom[0], self.rect.midbottom[1], 'down')
            enemy_bullets.add(enemy_bullet)


tile_images = {
    'wall': pg.image.load('wall (3).png'),
    'empty': pg.image.load('grass.png')
}

# создание групп спрайтов

bullets = pg.sprite.Group()
enemy_bullets = pg.sprite.Group()
walls_for_battle = pg.sprite.Group()
tiles_group = pg.sprite.Group()
walls = pg.sprite.Group()
all_sprites = pg.sprite.Group()
player_group = pg.sprite.Group()
enemies = pg.sprite.Group()
enemies_for_save = pg.sprite.Group()
fire_enemies = pg.sprite.Group()
Fire_enemies = pg.sprite.Group()
heroes = pg.sprite.Group()
all_sprites_for_save = pg.sprite.Group()
green_gads = pg.sprite.Group()
pg.display.set_caption('way to freedom')
window = pg.display.set_mode((0, 0), pg.FULLSCREEN)
size = width, height = window.get_rect()[2], window.get_rect()[3]

running = True
position = [300, 500]
empty = []


class Tile(pg.sprite.Sprite):
    """класс клетка - создает стены и пустые клетки для нашего поля"""

    def __init__(self, tile_type, pos_x, pos_y, flag):
        super().__init__(all_sprites_for_save)
        self.image = tile_images[tile_type]
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.type = '.'
        self.type1 = tile_type
        self.rect = self.image.get_rect().move(
            10 * pos_x, 10 * pos_y)

        if self.type1 == 'wall' and flag:
            walls.add(self)
            self.type = '#'
            all_sprites.add(self)

        if self.type1 == 'empty':
            self.type = '.'
            empty.append((self.rect.x, self.rect.y))


def generate_level(level):
    """создает уровень"""
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y, False)
            elif level[y][x] == '#':
                Tile('wall', x, y, True)
            elif level[y][x] == '@':
                Tile('empty', x, y, False)
                new_player = Hero('hero_left_step2.png', 10, 100, 5, x * 10, y * 10)
                heroes.add(new_player)
            elif level[y][x] == 'e':
                enemies.add(Enemy('pinky_gad.png', 5, 20, 1, x * 10, y * 10))
            elif level[y][x] == 'F':
                Fire_enemies.add(FiretoallEnemy('pinky_gad.png', 2, 20, 1, x * 10, y * 10))
            elif level[y][x] == 'f':
                fire_enemies.add(FireEnemy('pinky_gad.png', 3, 20, 1, x * 10, y * 10))
            elif level[y][x] == 'G':
                enemies.add(Green_gad('green_gad_right_step1.png', 4, 50, 3, x * 10, y * 10))
    return new_player, x, y


class Green_gad(Enemy):
    """как обычный враг, только больше"""

    def __init__(self, img, speed, hp, damage, x, y):
        super().__init__(img, speed, hp, damage, x, y)
        self.right_move = -1
        self.left_move = -1
        self.type = 'G'
        self.can_see_y = 250
        green_gads.add(self)

    def update(self, *args):

        if self.hp <= 0:
            self.kill()
        if args[0][0] > self.rect.x and abs(args[0][1] - self.rect.y) <= self.can_see_y:
            self.right_move += 1
            self.left_move = -1
            if self.right_move == 0:
                self.image = pg.image.load('green_gad_right_step1.png')
            if self.right_move == 1:
                self.image = pg.image.load('green_gad_right_step2.png')
            if self.right_move == 2:
                self.image = pg.image.load('green_gad_right_step3.png')
            if self.right_move > 2:
                self.right_move = -1

            self.where = 'right'
            self.rect.x += self.speed
            block_hit_list = pg.sprite.spritecollide(self, walls, False)
            strange_walls = pg.sprite.spritecollide(self, walls_for_battle, False)
            for block in block_hit_list:
                self.rect.right = block.rect.left
            for block in strange_walls:
                self.rect.right = block.rect.left

        if args[0][0] < self.rect.x and abs(args[0][1] - self.rect.y) <= self.can_see_y:
            self.right_move = -1
            self.left_move += 1
            if self.left_move == 0:
                self.image = pg.image.load('green_gad_left_step1.png')
            if self.left_move == 1:
                self.image = pg.image.load('green_gad_left_step2.png')
            if self.left_move == 2:
                self.image = pg.image.load('green_gad_left_step3.png')
            if self.left_move > 2:
                self.left_move = -1
            if self.rect.x != 0 and args[0][0] % self.rect.x != 0:
                self.rect.x -= 1
            self.where = 'left'
            self.rect.x -= self.speed
            block_hit_list = pg.sprite.spritecollide(self, walls, False)
            strange_walls = pg.sprite.spritecollide(self, walls_for_battle, False)
            for block in block_hit_list:
                self.rect.left = block.rect.right
            for block in strange_walls:
                self.rect.left = block.rect.right
        if args[0][1] > self.rect.y and abs(args[0][1] - self.rect.y) <= self.can_see_y:
            if self.rect.y != 0 and args[0][1] % self.rect.y != 0:
                self.rect.y -= 1
            self.rect.y += self.speed
            self.where = 'down'
            block_hit_list = pg.sprite.spritecollide(self, walls, False)
            strange_walls = pg.sprite.spritecollide(self, walls_for_battle, False)
            for block in block_hit_list:
                self.rect.bottom = block.rect.top
            for block in strange_walls:
                self.rect.bottom = block.rect.top

        if args[0][1] < self.rect.y and abs(args[0][1] - self.rect.y) <= self.can_see_y:
            self.where = 'up'
            self.rect.y -= self.speed
            block_hit_list = pg.sprite.spritecollide(self, walls, False)
            strange_walls = pg.sprite.spritecollide(self, walls_for_battle, False)
            for block in block_hit_list:
                self.rect.top = block.rect.bottom
            for block in strange_walls:
                self.rect.top = block.rect.bottom


class Camera:
    """класс камера - класс создающий видимость присутствия обзора у нашего персонажа
    на самом деле просто перемещает главное окно"""

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pg.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def player_move(keys):
    """двигает персонажа когда пользователь нажимает на соответствующие кнопки"""
    global move_to
    if keys[pg.K_LEFT]:
        hero.update('left')
        move_to = 'left'
    if keys[pg.K_RIGHT]:
        hero.update('right')
        move_to = 'right'
    if keys[pg.K_UP]:
        hero.update('up')
    if keys[pg.K_DOWN]:
        hero.update('down')


def camera_func(camera, target_rect):
    l = -target_rect.x + 1000
    t = -target_rect.y + 650
    w, h = camera.width, camera.height

    return pg.Rect(l, t, w, h)


total_level_width = width * 2
total_level_height = height * 2
camera = Camera(camera_func, total_level_width, total_level_height)

FPS = 30

virtual_surface = Surface(size)
manager = pygame_gui.UIManager((width, height))
screen = pg.display.set_mode(size)
current_size = screen.get_size()
img = pg.image.load('fon2.gif')
img = transform.scale(img, (width, height))
pg.display.set_caption('SIM')
switch_start = pygame_gui.elements.UIButton(
    relative_rect=pg.Rect((120, 10), (150, 100)),
    text='START',
    manager=manager)
switch_exit = pygame_gui.elements.UIButton(
    relative_rect=pg.Rect((120, 110), (150, 100)),
    text='EXIT',
    manager=manager)
switch_Settings = pygame_gui.elements.UIButton(
    relative_rect=pg.Rect((120, 210), (150, 100)),
    text='SETTINGS',
    manager=manager)
difficulty = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
    options_list=['Easy', 'Medium', 'Hard', 'Very Hard'], starting_option='Easy',
    relative_rect=pg.Rect((120, 320), (150, 100)),
    manager=manager)
running_1 = True
with open('map.txt', 'r') as f:
    save = f.readlines()
    save = [i.strip() for i in save]
fon = Fon(0, 0)
clock = pg.time.Clock()
while running_1:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            information_dialog = pygame_gui.windows.UIConfirmationDialog(
                rect=pg.Rect((250, 200), (300, 200)),
                manager=manager,
                window_title='Подтверждение',
                action_long_desc='Are you seriously?',
                action_short_name='Yes',
                blocking=True)
        elif event.type == VIDEORESIZE:
            current_size = event.size
        if event.type == pg.USEREVENT:
            if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                running_1 = False
            else:
                screen.blit(img, (0, 0))
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                print('difficulty:', event.text)
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == switch_exit:
                    print('EXIT')
                    running_1 = False
                if event.ui_element == switch_Settings:
                    print('SETTINGS')
                if event.ui_element == switch_start:
                    print('START')
                    # pg.mixer.music.stop()
                    # pg.display.set_caption('SIM')
                    # pg.mixer.music.load('level_sound.mp3')
                    # pg.mixer.music.set_volume(0.8)
                    # pg.mixer.music.play(-1)
                    size = (width, height)
                    manager = pygame_gui.UIManager((1980, 1080))
                    screen = pg.display.set_mode(size, RESIZABLE)
                    img = pg.image.load('fon2.gif')
                    img = transform.scale(img, (1980, 1080))
                    screen.blit(img, (0, 0))
                    first_level = pygame_gui.elements.UIButton(
                        relative_rect=pg.Rect((10, 10), (120, 100)),
                        text='1',
                        manager=manager)
                    second_level = pygame_gui.elements.UIButton(
                        relative_rect=pg.Rect((130, 10), (120, 100)),
                        text='2',
                        manager=manager)
                    third_level = pygame_gui.elements.UIButton(
                        relative_rect=pg.Rect((250, 10), (120, 100)),
                        text='3',
                        manager=manager)
                    fourth_level = pygame_gui.elements.UIButton(
                        relative_rect=pg.Rect((370, 10), (120, 100)),
                        text='4',
                        manager=manager)
                    fifth_level = pygame_gui.elements.UIButton(
                        relative_rect=pg.Rect((490, 10), (110, 100)),
                        text='5',
                        manager=manager)
                    # noinspection PyUnboundLocalVariable
                    while True:
                        for event in pg.event.get():
                            if event.type == pg.USEREVENT:
                                if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == first_level:
                                    print('Please waiting, 1 level are loading')
                                    running = True
                                    player, level_x, level_y = generate_level(load_level('map2.txt'))
                                    hero = player
                                    with open('map2.txt', 'r') as f:
                                        file = f.readlines()
                                        file = ''.join(file).split('\n')
                                        hero.hp = int((file[-3]))
                                        for num, i in enumerate(enemies_for_save):
                                            i.hp = int(file[-2].split()[num])
                                    portal = Portal(950, 210)
                                    while running:
                                        screen.blit(img, (0, 0))
                                        clock.tick(FPS)
                                        for event in pg.event.get():
                                            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                                                y = 0

                                                while y < level_y:
                                                    save = [['.'] * 123 for _ in range(66)]
                                                    y += 1
                                                    x = 0
                                                    lst = []
                                                    for sprite in all_sprites_for_save:
                                                        if sprite:
                                                            try:
                                                                if sprite.type == '@':
                                                                    save[sprite.rect.y // 10][sprite.rect.x // 10] = '@'
                                                                if sprite.type == 'e':
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
                                                                        sprite.rect.x // 10] != 'G':
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
                                                with open('map2.txt', 'w') as f:
                                                    print(text, file=f)
                                                    print(hero.hp, file=f)
                                                    print(' '.join(map(str, enemies_hp)), file=f)

                                                enemies_hp = []
                                                running = False
                                            if event.type == my_event:
                                                for sprite in fire_enemies:
                                                    sprite.attacking(hero.rect)
                                            if event.type == fire_to_all:
                                                for sprite in Fire_enemies:
                                                    sprite.attacking(hero.rect)
                                        keys = pg.key.get_pressed()
                                        player_move(keys)
                                        for i in pg.sprite.spritecollide(hero, enemies_for_save, False):
                                            hero.hp -= i.attack
                                            # каким-то чудом работающая система удара врага о героя и не вылета врага за стены
                                            if i.where == 'left':
                                                try:
                                                    if save[i.rect.y // 10][
                                                        (i.rect.x + hero.speed * 2) // 10 + 7] != '#':
                                                        i.rect.x += hero.speed * 2

                                                except IndexError:
                                                    pass
                                            if i.where == 'right':
                                                try:
                                                    if save[i.rect.y // 10][
                                                        (i.rect.x - hero.speed * 2) // 10 - 1] != '#':
                                                        i.rect.x -= hero.speed * 2
                                                except IndexError:
                                                    pass
                                            if i.where == 'up':
                                                try:
                                                    if save[(i.rect.y + hero.speed * 3) // 10 + 4][
                                                        i.rect.x // 10] != '#' \
                                                            and (i.rect.y + hero.speed * 3) // 10 + 4 != 40 \
                                                            and (i.rect.y + hero.speed * 3) // 10 + 4 != 41 \
                                                            and (i.rect.y + hero.speed * 3) // 10 + 4 != 64 \
                                                            and (i.rect.y + hero.speed * 3) // 10 + 4 != 63 \
                                                            and (i.rect.y + hero.speed * 3) // 10 + 4 != 65:
                                                        i.rect.y += hero.speed * 2
                                                except IndexError as e:
                                                    pass
                                            if i.where == 'down':
                                                try:
                                                    if save[(i.rect.y - hero.speed * 2) // 10 - 2][
                                                        i.rect.x // 10] != '#' \
                                                            and (i.rect.y - hero.speed * 2) // 10 - 2 != 1 \
                                                            and (i.rect.y - hero.speed * 2) // 10 - 2 != 39 \
                                                            and (i.rect.y - hero.speed * 2) // 10 - 2 != 40:
                                                        i.rect.y -= hero.speed * 2
                                                except IndexError:
                                                    pass
                                            hero.image = pg.image.load('hero_right_damaged.png')

                                        for hit in pg.sprite.groupcollide(enemies_for_save, bullets, False, True):
                                            hit.dead(first_weapon_dmg)
                                        if hero.hp <= 0:
                                            w = fontt.render('GAME OVER', True,
                                                             pg.Color('red'))
                                            screen.blit(w, (100, 100))
                                            pg.display.update()
                                            pg.time.delay(1000)
                                            running = False
                                            shutil.copyfile("map.txt", "map2.txt")
                                            save = [['.'] * 123 for _ in range(66)]
                                            for i in all_sprites_for_save:
                                                i.kill()
                                            for i in all_sprites:
                                                i.kill()

                                        if len(enemies) == 0 and len(fire_enemies) == 0 and len(Fire_enemies) == 0:
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
                                                running = False
                                                shutil.copyfile("map.txt", "map2.txt")
                                                save = [['.'] * 123 for _ in range(66)]
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
                                if event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == second_level:
                                    running = True
                                    player, level_x, level_y = generate_level(load_level('map_for_second_level2.txt'))
                                    print(len(green_gads))
                                    hero = player
                                    for i in range(29, 89):
                                        walls_for_battle.add(Tile('wall', i, 35, False))

                                    with open('map_for_second_level2.txt', 'r') as f:
                                        file = f.readlines()
                                        file = ''.join(file).split('\n')
                                        hero.hp = int((file[-3]))
                                        for num, i in enumerate(enemies_for_save):
                                            i.hp = int(file[-2].split()[num])
                                    portal = Portal(950, 210)
                                    while running:
                                        screen.blit(img, (0, 0))
                                        clock.tick(FPS)
                                        for event in pg.event.get():
                                            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                                                y = 0

                                                while y < level_y:
                                                    save = [['.'] * 123 for _ in range(66)]
                                                    y += 1
                                                    x = 0
                                                    lst = []
                                                    for sprite in all_sprites_for_save:
                                                        if sprite:
                                                            try:
                                                                if sprite.type == '@':
                                                                    save[sprite.rect.y // 10][sprite.rect.x // 10] = '@'
                                                                if sprite.type == 'e':
                                                                    save[sprite.rect.y // 10][sprite.rect.x // 10] = 'e'
                                                                if sprite.type == 'F':
                                                                    save[sprite.rect.y // 10][sprite.rect.x // 10] = 'F'


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
                                                                        sprite.rect.x // 10] != 'f':
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
                                                with open('map_for_second_level2.txt', 'w') as f:
                                                    print(text, file=f)
                                                    print(hero.hp, file=f)
                                                    print(' '.join(map(str, enemies_hp)), file=f)

                                                enemies_hp = []
                                                running = False
                                            if event.type == my_event:
                                                for sprite in fire_enemies:
                                                    sprite.attacking(hero.rect)
                                            if event.type == fire_to_all:
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
                                                        if save[i.rect.y // 10][
                                                            (i.rect.x + hero.speed * 2) // 10 + 7] != '#':
                                                            i.rect.x += hero.speed * 2

                                                    except IndexError:
                                                        pass
                                                if i.where == 'right':
                                                    try:
                                                        if save[i.rect.y // 10][
                                                            (i.rect.x - hero.speed * 2) // 10 - 1] != '#':
                                                            i.rect.x -= hero.speed * 2
                                                    except IndexError:
                                                        pass
                                                if i.where == 'up':
                                                    try:
                                                        if save[(i.rect.y + hero.speed * 3) // 10 + 4][
                                                            i.rect.x // 10] != '#' \
                                                                and (i.rect.y + hero.speed * 3) // 10 + 4 != 40 \
                                                                and (i.rect.y + hero.speed * 3) // 10 + 4 != 41 \
                                                                and (i.rect.y + hero.speed * 3) // 10 + 4 != 64 \
                                                                and (i.rect.y + hero.speed * 3) // 10 + 4 != 63 \
                                                                and (i.rect.y + hero.speed * 3) // 10 + 4 != 65:
                                                            i.rect.y += hero.speed * 2
                                                    except IndexError:
                                                        pass
                                                if i.where == 'down':
                                                    try:
                                                        if save[(i.rect.y - hero.speed * 2) // 10 - 2][
                                                            i.rect.x // 10] != '#':
                                                            i.rect.y -= hero.speed * 2
                                                    except IndexError:
                                                        pass
                                            elif i.type == 'G':
                                                if i.where == 'left':
                                                    try:
                                                        if save[hero.rect.y // 10][
                                                            (hero.rect.x + hero.speed) // 10 + 10] != '#' \
                                                                and (hero.rect.x + hero.speed) // 10 + 10 != 12:
                                                            hero.rect.x -= hero.speed - 1

                                                    except IndexError:
                                                        pass
                                                if i.where == 'right':
                                                    try:
                                                        if save[hero.rect.y // 10][
                                                            (hero.rect.x + hero.speed * 2) // 10 + 6] != '#':
                                                            hero.rect.x += hero.speed - 1
                                                    except IndexError:
                                                        pass
                                                if i.where == 'up':
                                                    try:
                                                        if save[hero.rect.y // 10 - 1][
                                                            hero.rect.x // 10] != '#' and hero.rect.y // 10 - 1 >= 2:
                                                            hero.rect.y -= hero.speed - 1
                                                    except IndexError:
                                                        pass
                                                if i.where == 'down':
                                                    try:
                                                        print(hero.rect.y // 10 + 13)
                                                        print(hero.rect.x // 10)
                                                        if save[hero.rect.y // 10 + 13][
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
                                            w = fontt.render('GAME OVER', True,
                                                             pg.Color('red'))
                                            screen.blit(w, (100, 100))
                                            pg.display.update()
                                            pg.time.delay(1000)
                                            running = False
                                            shutil.copyfile("map_for_second_level.txt", "map_for_second_level2.txt")
                                            save = [['.'] * 123 for _ in range(66)]
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
                                        if len(enemies) == 0 and len(fire_enemies) == 0 and len(Fire_enemies) == 0:
                                            portal = Portal(10, 10)
                                            screen.blit(portal.image, camera.apply(portal))
                                        if pg.sprite.spritecollide(portal, heroes, False, False):
                                            w = fontt.render('WON', True,
                                                             pg.Color('red'))
                                            screen.blit(w, (550, 200))
                                            pg.time.delay(100)
                                            running = False
                                            shutil.copyfile("map_for_second_level.txt", "map_for_second_level2.txt")
                                            save = [['.'] * 123 for _ in range(66)]
                                            for i in all_sprites_for_save:
                                                i.kill()
                                            for i in all_sprites:
                                                i.kill()

                                        for sprite in all_sprites:
                                            screen.blit(sprite.image, camera.apply(sprite))
                                        for sprite in walls_for_battle:
                                            screen.blit(sprite.image, camera.apply(sprite))
                                        pg.display.update()
                                if event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == third_level:
                                    print('Please waiting, 3 level are loading')
                                # noinspection PyUnboundLocalVariable
                                if event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == fourth_level:
                                    print('Please waiting, 4 level are loading')
                                # noinspection PyUnboundLocalVariable
                                if event.type == USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == fifth_level:
                                    print('Please waiting, 5 level are loading')
                                manager.process_events(event)
                                manager.update(100000)
                                pg.display.update()
                        screen.blit(img, (0, 0))
                        manager.process_events(event)
                        manager.update(10000)
                        manager.draw_ui(screen)

                        pg.display.update()
                if event.ui_element == switch_exit:
                    print('EXIT')
                    information_dialog = pygame_gui.windows.UIConfirmationDialog(
                        rect=pg.Rect((250, 200), (300, 200)),
                        manager=manager,
                        window_title='Подтверждение',
                        action_long_desc='Are you seriously?',
                        action_short_name='Yes',
                        blocking=True)
                if event.ui_element == switch_Settings:
                    print('SETTINGS')
                    # pg.display.set_caption('SIM')
                    # pg.mixer.music.load('Main_sound.mp3')
                    # pg.mixer.music.set_volume(0.2)
                    # pg.mixer.music.play(-1)
                    size = (width, height)
                    manager = pygame_gui.UIManager((1980, 1080))
                    screen = pg.display.set_mode(size, RESIZABLE)
                    img = pg.image.load('fon.png')
                    img = transform.scale(img, (700, 480))
                    screen.blit(img, (0, 0))
                    volume: UIDropDownMenu = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
                        options_list=['0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1'],
                        starting_option='Change volume',
                        relative_rect=pg.Rect((200, 150), (250, 100)),
                        manager=manager)
        manager.process_events(event)
        manager.update(1000)
        virtual_surface.blit(img, (0, 0))
        scaled_surface = transform.scale(virtual_surface, current_size)
        screen.blit(scaled_surface, (0, 0))
        manager.draw_ui(screen)
        pg.display.update()
