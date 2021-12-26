import pygame as pg
import time as t
import sys

move_to = 'right'

WEAPONS = ['first_gun', 'second_gun']
weapon = WEAPONS[0]
pg.init()
all_time = t.time()
now = t.time()


class Bullet(pg.sprite.Sprite):
    # В разработке
    def __init__(self, img, speed, damage, x, y):
        super().__init__(all_sprites)

        self.image = pg.image.load(img)
        self.rect = self.image.get_rect()
        self.damage = damage
        self.rect.x = x
        self.rect.y = y
        self.where = move_to
        self.speed = speed

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


first_weapon_dmg = 1
bullets = pg.sprite.Group()
enemy_bullets = pg.sprite.Group()


class Hero(pg.sprite.Sprite):
    """класс для главного героя нашей игры"""

    def __init__(self, img, speed, hp, attack, x, y):
        super().__init__(all_sprites)
        self.image = pg.image.load(img)
        self.speed = speed
        self.hp = hp
        self.attack = attack
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)
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
        bullet = Bullet('bullet.png', 5, first_weapon_dmg, where, up_down)
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
        super().__init__(all_sprites)
        self.image = pg.image.load(img)
        self.speed = speed
        self.hp = hp
        self.attack = attack
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.where = ''

    def attacking(self):
        pass

    def update(self, *args):

        if self.hp <= 0:
            self.kill()
        if args[0][0] > self.rect.x:
            self.where = 'right'
            self.rect.x += self.speed
        if args[0][0] < self.rect.x:
            self.where = 'left'
            self.rect.x -= self.speed
        if args[0][1] > self.rect.y:
            self.rect.y += self.speed
            self.where = 'down'
        if args[0][1] < self.rect.y:
            self.where = 'up'
            self.rect.y -= self.speed

    def dead(self, damage):
        self.hp -= damage


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class FireEnemy(Enemy):
    """класс для стреляющего врага, который выпускает пули в одном направлении в одном направление"""

    def __init__(self, img, speed, hp, damage, x, y):
        super().__init__(img, speed, hp, damage, x, y)
        self.bullet_len = 40

    def attacking(self, hero_rect):
        if self.bullet_len >= abs(hero_rect.x - self.rect.x):
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
            enemy_bullet = Bullet('enemy_bullets.png', 5, first_weapon_dmg, there, up_down)
            enemy_bullets.add(enemy_bullet)
            enemy_bullet.update(self.where)

    def update(self, *args):
        if self.hp <= 0:
            self.kill()
        if args[0][0] > self.rect.x:
            self.where = 'right'
            self.rect.x += self.speed
        if args[0][0] < self.rect.x:
            self.where = 'left'
            self.rect.x -= self.speed
        if args[0][1] > self.rect.y:
            self.rect.y += self.speed
            self.where = 'down'
        if args[0][1] < self.rect.y:
            self.where = 'up'
            self.rect.y -= self.speed

            self.attacking(args[0])


tile_images = {
    'wall': pg.image.load('meteor-wall.png'),
    'empty': pg.image.load('grass.png')
}
size = width, height = 1300, 750
tile_width = tile_height = 15
tiles_group = pg.sprite.Group()
walls = pg.sprite.Group()
all_sprites = pg.sprite.Group()
player_group = pg.sprite.Group()


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.type = tile_type

        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

        if self.type == 'wall':
            walls.add(self)
            all_sprites.add(self)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Hero('hero.png', 15, 100, 5, x, y)
                heroes.add(new_player)
            elif level[y][x] == 'e':
                enemies.add(Enemy('testenemy.png', 5, 20, 1, x * tile_width, y * tile_height))
            elif level[y][x] == 'F':
                fire_enemies.add(FireEnemy('testenemy.png', 5, 20, 1, x * tile_width, y * tile_height))
    return new_player, x, y


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


camera = Camera()

FPS = 30
clock = pg.time.Clock()


def terminate():
    pg.quit()
    sys.exit()


def start_screen():
    fon = pg.transform.scale(pg.image.load('fon.png'), (width, height))
    screen.blit(fon, (0, 0))


enemies = pg.sprite.Group()
fire_enemies = pg.sprite.Group()
pg.display.set_caption('way to freedom')
screen = pg.display.set_mode(size)
running = True
position = [300, 500]
heroes = pg.sprite.Group()

reload_time = True
f = pg.font.Font(None, 100)
while True:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            terminate()
        elif event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
            player, level_x, level_y = generate_level(load_level('map.txt'))
            hero = player
            while running:
                screen.blit(pg.image.load('fon.png'), (0, 0))
                clock.tick(FPS)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False
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
                if hero.hp <= 0:
                    w = f.render('GAME OVER', True,
                                 pg.Color('red'))
                    screen.blit(w, (100, 100))
                    pg.display.update()
                    pg.time.delay(1000)
                    running = False
                if len(enemies) == 0 and len(fire_enemies) == 0:
                    w = f.render('YOU WON', True,
                                 pg.Color('green'))
                    screen.blit(w, (100, 100))
                    pg.display.update()
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
                bullets.update(move_to)
                camera.update(hero)
                enemy_bullets.update()
                enemy_bullets.draw(screen)
                fire_enemies.update(hero.rect)
                for hit in pg.sprite.groupcollide(heroes, enemy_bullets, False, True):
                    hit.hp -= 1
                for sprite in all_sprites:
                    camera.apply(sprite)
                all_sprites.draw(screen)
                pg.display.update()
