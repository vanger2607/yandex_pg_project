import pygame as pg
import pygame_gui
from pygame import *
import time as t
import sys

pg.init()


def terminate():
    pg.quit()
    sys.exit()


def start_screen():
    fon = pg.transform.scale(img, (width, height))
    screen.blit(fon, (0, 0))


reload_time = True
f = pg.font.Font(None, 100)
WEAPONS = ['first_gun', 'second_gun']
weapon = WEAPONS[0]
all_time = t.time()
now = t.time()
my_event = pg.USEREVENT + 1
fire_to_all = pg.USEREVENT + 2
walls_for_battle = pg.sprite.Group()


class Portal(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites_for_save)
        self.image = pg.image.load('portal.png')
        self.rect = self.image.get_rect()
        print(self.rect)
        self.rect.x = x
        self.rect.y = y
        self.type = 'p'


class Bullet(pg.sprite.Sprite):
    # В разработке
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


first_weapon_dmg = 15
bullets = pg.sprite.Group()
enemy_bullets = pg.sprite.Group()

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
        elif move_to == 'right':
            where = self.rect.right
        elif move_to == 'up':
            where, up_down = self.rect.midtop
        elif move_to == 'down':
            where, up_down = self.rect.midbottom
        bullet = Bullet('bullet.png', 5, first_weapon_dmg, where, up_down, move_to)
        bullets.add(bullet)
        bullet.update(move_to)

    def update(self, *args):

        if args[0] == 'right' and self.rect.x + self.speed < width - list(self.rect)[2]:
            self.rect.x += self.speed
            block_hit_list = pg.sprite.spritecollide(self, walls, False)
            for block in block_hit_list:
                self.rect.right = block.rect.left
        if args[0] == 'left' and self.rect.x - self.speed > 0:
            self.rect.x -= self.speed
            block_hit_list = pg.sprite.spritecollide(self, walls, False)
            for block in block_hit_list:
                self.rect.left = block.rect.right
        if args[0] == 'up' and self.rect.y - self.speed > 0:
            self.rect.y -= self.speed
            block_hit_list = pg.sprite.spritecollide(self, walls, False)
            for block in block_hit_list:
                self.rect.top = block.rect.bottom

        if args[0] == 'down' and self.rect.y + self.speed < height - list(self.rect)[3]:
            self.rect.y += self.speed
            block_hit_list = pg.sprite.spritecollide(self, walls, False)
            for block in block_hit_list:
                self.rect.bottom = block.rect.top


class Enemy(pg.sprite.Sprite):
    """общий класс для всех врагов"""

    def __init__(self, img, speed, hp, attack, x, y):
        super().__init__(all_sprites, all_sprites_for_save)
        self.image = pg.image.load(img)
        self.speed = speed
        self.hp = hp
        self.attack = attack
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.where = ''
        self.can_see_y = 423
        self.type = 'e'

    def attacking(self):
        pass

    def update(self, *args):

        if self.hp <= 0:
            self.kill()
        if args[0][0] > self.rect.x and args[0][1] >= self.can_see_y:
            self.where = 'right'
            self.rect.x += self.speed
        if args[0][0] < self.rect.x and args[0][1] >= self.can_see_y:
            if self.rect.x != 0 and args[0][0] % self.rect.x != 0:
                self.rect.x -= 1
            self.where = 'left'
            self.rect.x -= self.speed
        if args[0][1] > self.rect.y and args[0][1] >= self.can_see_y:
            if self.rect.y != 0 and args[0][1] % self.rect.y != 0:
                self.rect.y -= 1
            self.rect.y += self.speed
            self.where = 'down'
        if args[0][1] < self.rect.y and args[0][1] >= self.can_see_y:
            self.where = 'up'
            self.rect.y -= self.speed

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
        if self.bullet_len >= abs(hero_rect.x - self.rect.x) and (self.bullet_len >= abs(hero_rect.y - self.rect.y)) \
                and hero_rect[1] >= self.can_see_y:
            there = self.rect.x
            up_down = self.rect.y
            if self.where == 'left':
                there = self.rect.left
                move_to_enemy = 'left'
            elif self.where == 'right':
                there = self.rect.right
                move_to_enemy = 'right'
            elif self.where == 'up':
                move_to_enemy = 'up'
                there, up_down = self.rect.midtop
            elif self.where == 'down':
                move_to_enemy = 'down'
                there, up_dow = self.rect.midbottom
            enemy_bullet = Bullet('enemy_bullets.png', 10, first_weapon_dmg, there, up_down, move_to_enemy)
            enemy_bullets.add(enemy_bullet)

    def update(self, *args):
        if self.hp <= 0:
            self.kill()
        if args[0][0] > self.rect.x and args[0][1] >= self.can_see_y:
            self.where = 'right'
            self.rect.x += self.speed
        elif args[0][0] < self.rect.x and args[0][1] >= self.can_see_y:
            if self.rect.x != 0 and args[0][0] % self.rect.x != 0:
                self.rect.x -= 1
            self.where = 'left'
            self.rect.x -= self.speed
        elif args[0][1] > self.rect.y and args[0][1] >= self.can_see_y:
            if self.rect.y !=0 and args[0][0] % self.rect.y != 0:
                self.rect.y -= 1
            self.rect.y += self.speed
            self.where = 'down'
        elif args[0][1] < self.rect.y and args[0][1] >= self.can_see_y:
            self.where = 'up'
            self.rect.y -= self.speed


class FiretoallEnemy(FireEnemy):
    """враг стреляющей во все стороны"""

    def __init__(self, img, speed, hp, damage, x, y):
        super().__init__(img, speed, hp, damage, x, y)
        self.type = 'F'

    def attacking(self, hero_rect):
        if hero_rect[1] >= self.can_see_y:
            enemy_bullet = Bullet('enemy_bullets.png', 10, first_weapon_dmg, self.rect.left, self.rect.y, 'left')
            enemy_bullets.add(enemy_bullet)
            enemy_bullet = Bullet('enemy_bullets.png', 10, first_weapon_dmg, self.rect.right, self.rect.y, 'right')
            enemy_bullets.add(enemy_bullet)
            enemy_bullet = Bullet('enemy_bullets.png', 10, first_weapon_dmg,
                                  self.rect.midtop[0], self.rect.midtop[1], 'up')
            enemy_bullets.add(enemy_bullet)
            enemy_bullet = Bullet('enemy_bullets.png', 10, first_weapon_dmg,
                                  self.rect.midbottom[0], self.rect.midbottom[1], 'down')
            enemy_bullets.add(enemy_bullet)


tile_images = {
    'wall': pg.image.load('wall (3).png'),
    'empty': pg.image.load('grass.png')
}
size = width, height = 1300, 750
total_level_width = 30 * 40
total_level_height = 21 * 40
tiles_group = pg.sprite.Group()
walls = pg.sprite.Group()
all_sprites = pg.sprite.Group()
player_group = pg.sprite.Group()
enemies = pg.sprite.Group()
fire_enemies = pg.sprite.Group()
Fire_enemies = pg.sprite.Group()
pg.display.set_caption('way to freedom')
screen = pg.display.set_mode(size)
running = True
position = [300, 500]
heroes = pg.sprite.Group()
empty = []
all_sprites_for_save = pg.sprite.Group()


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, flag):
        super().__init__(all_sprites_for_save)
        self.image = tile_images[tile_type]
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.type1 = tile_type
        self.rect = self.image.get_rect().move(
            10 * pos_x, 10 * pos_y)

        if self.type1 == 'wall' and flag:
            walls.add(self)
            print(self.rect)
            self.type = '#'
            all_sprites.add(self)

        if self.type1 == 'empty':
            self.type = '.'
            empty.append((self.rect.x, self.rect.y))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y, False)
            elif level[y][x] == '#':
                Tile('wall', x, y, True)
            elif level[y][x] == '@':
                Tile('empty', x, y, False)
                new_player = Hero('hero_left_step1 (2).png', 10, 100, 5, x * 10, y * 10)
                heroes.add(new_player)
            elif level[y][x] == 'e':
                enemies.add(Enemy('testenemy.png', 5, 20, 1, x * 10, y * 10))
            elif level[y][x] == 'F':
                Fire_enemies.add(FiretoallEnemy('testenemy.png', 1, 20, 1, x * 10, y * 10))
            elif level[y][x] == 'f':
                fire_enemies.add(FireEnemy('testenemy.png', 3, 20, 15, x * 10, y * 10))
    return new_player, x, y


class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pg.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_func(camera, target_rect):
    l = -target_rect.x + 1000
    t = -target_rect.y + 650
    w, h = camera.width, camera.height

    return pg.Rect(l, t, w, h)


camera = Camera(camera_func, total_level_width, total_level_height)

FPS = 30
width = 1300
height = 750
size = (width, height)
virtual_surface = Surface(size)
manager = pygame_gui.UIManager((1300, 750))
screen = pg.display.set_mode(size)
print(screen.get_rect())
current_size = screen.get_size()
img = pg.image.load('fon2.gif')
img = transform.scale(img, (1300, 750))
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
save = [[0] * 123 for _ in range(66)]
print(save)
screen.blit(img, (0, 0))
clock = pg.time.Clock()
while running_1:
    for event in pg.event.get():
        time_delta = clock.tick(60) / 1000.0
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
                    running = True
                    player, level_x, level_y = generate_level(load_level('map.txt'))
                    hero = player
                    portal = Portal(950, 210)
                    while running:
                        screen.blit(img, (0, 0))
                        clock.tick(FPS)
                        for event in pg.event.get():
                            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                                y = 0
                                while y < level_y:
                                    y += 1
                                    x = 0
                                    lst = []
                                    for sprite in all_sprites_for_save:
                                        if sprite.type == '@':
                                            print(sprite.rect.y // 10)
                                            save[sprite.rect.y // 10][sprite.rect.x // 10] = '@'
                                            print(save[34][18])

                                        elif sprite.type == 'p':
                                            save[sprite.rect.y // 10][sprite.rect.x // 10] = '.'

                                        else:
                                            if save[sprite.rect.y // 10][sprite.rect.x // 10] != '@':
                                                save[sprite.rect.y // 10][sprite.rect.x // 10] = sprite.type

                                text = ''
                                for i in save:
                                    text += ''.join(i) + '\n'
                                print(save)
                                with open('map2.txt', 'w') as f:
                                    print(text, file=f)

                                running = False
                            if event.type == my_event:
                                for sprite in fire_enemies:
                                    sprite.attacking(hero.rect)
                            if event.type == fire_to_all:
                                for sprite in Fire_enemies:
                                    sprite.attacking(hero.rect)
                        keys = pg.key.get_pressed()
                        if keys[pg.K_LEFT]:
                            hero.update('left')
                            move_to = 'left'
                        if keys[pg.K_RIGHT]:
                            hero.update('right')
                            move_to = 'right'
                        if keys[pg.K_UP]:
                            move_to = 'up'
                            hero.update('up')
                        if keys[pg.K_DOWN]:
                            move_to = 'down'
                            hero.update('down')

                        if pg.sprite.spritecollide(hero, enemies, False):
                            hero.hp -= 1

                        for hit in pg.sprite.groupcollide(enemies, bullets, False, True):
                            hit.dead(first_weapon_dmg)
                        for hit in pg.sprite.groupcollide(fire_enemies, bullets, False, True):
                            hit.dead(first_weapon_dmg)
                        for hit in pg.sprite.groupcollide(Fire_enemies, bullets, False, True):
                            hit.dead(first_weapon_dmg)
                        if hero.hp <= 0:
                            w = f.render('GAME OVER', True,
                                         pg.Color('red'))
                            screen.blit(w, (100, 100))
                            pg.display.update()
                            pg.time.delay(1000)
                            running = False
                        if len(enemies) == 0 and len(fire_enemies) == 0 and len(Fire_enemies) == 0:
                            screen.blit(portal.image, camera.apply(portal))
                            for sprite in walls_for_battle:
                                walls_for_battle.remove(sprite)
                            walls_for_battle.update()
                            walls_for_battle.draw(screen)
                            if pg.sprite.spritecollide(portal, heroes, False, False):
                                w = f.render('WON', True,
                                             pg.Color('red'))
                                screen.blit(w, (650, 375))
                                pg.time.delay(1000)
                                running = False
                        enemies.update(hero.rect)

                        count_hp = f.render(str(hero.hp), True, pg.Color('red'))
                        screen.blit(count_hp, (0, 0))

                        if now - all_time < 1:
                            now = t.time()

                            reload_time = True

                        elif now - all_time > 1:
                            reload_time = False

                        if keys[pg.K_SPACE] and not reload_time:
                            hero.attacking('cubes')
                            all_time = t.time()
                            now = t.time()
                        bullets.update()
                        camera.update(hero)
                        fire_enemies.update(hero.rect)
                        Fire_enemies.update(hero.rect)
                        if hero.rect[1] >= 447 and len(enemies) + len(fire_enemies) + len(Fire_enemies) > 0:
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
                        print(hero.rect)

                        for hit in pg.sprite.groupcollide(heroes, enemy_bullets, False, True):
                            hit.hp -= 1
                        for sprite in all_sprites:
                            screen.blit(sprite.image, camera.apply(sprite))

                        for sprite in walls_for_battle:
                            screen.blit(sprite.image, camera.apply(sprite))
                        pg.display.update()

        manager.process_events(event)
        manager.update(time_delta)
    virtual_surface.blit(img, (0, 0))
    scaled_surface = transform.scale(virtual_surface, current_size)
    screen.blit(scaled_surface, (0, 0))
    manager.draw_ui(screen)
    pg.display.update()
pg.quit()
