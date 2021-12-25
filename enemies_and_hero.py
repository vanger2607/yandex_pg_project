import pygame as pg

move_to = 'right'

import pygame
import sys

pg.init()
now = 5
all_time = 4


class Bullet(pg.sprite.Sprite):
    # В разработке
    def __init__(self, img, damage, x, y):
        super().__init__()

        self.image = pg.image.load(img)
        self.rect = self.image.get_rect()
        self.damage = damage
        self.rect.x = x
        self.rect.y = y
        self.where = move_to

    def update(self, *args):
        if self.where == 'left':
            self.rect.x -= 1
        elif self.where == 'right':
            self.rect.x += 1

        if self.rect.x <= 10 or self.rect.x >= width - 10:
            self.kill()


bullets = pg.sprite.Group()


class Hero(pg.sprite.Sprite):
    """класс для главного героя нашей игры"""

    def __init__(self, img, speed, hp, attack, x, y):
        super().__init__()
        self.image = pg.image.load(img)
        self.speed = speed
        self.hp = hp
        self.attack = attack
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)

    def attacking(self, weapon):
        # В разработке
        global bullets
        bullet = Bullet('bullet.png', 1, self.rect.centerx, self.rect.top)
        bullets.add(bullet)
        bullet.update(move_to)

    def update(self, *args):

        if args[0] == 'right' and self.rect.x + self.speed < width - list(self.rect)[2]:
            self.rect.x += self.speed
            block_hit_list = pygame.sprite.spritecollide(self, walls, False)
            for block in block_hit_list:
                self.rect.right = block.rect.left
        if args[0] == 'left' and self.rect.x - self.speed > 0:
            self.rect.x -= self.speed
            block_hit_list = pygame.sprite.spritecollide(self, walls, False)
            for block in block_hit_list:
                self.rect.left = block.rect.right
        if args[0] == 'up' and self.rect.y - self.speed > 0:
            self.rect.y -= self.speed
            block_hit_list = pygame.sprite.spritecollide(self, walls, False)
            for block in block_hit_list:
                self.rect.top = block.rect.bottom

        if args[0] == 'down' and self.rect.y + self.speed < height - list(self.rect)[3]:
            self.rect.y += self.speed
            block_hit_list = pygame.sprite.spritecollide(self, walls, False)
            for block in block_hit_list:
                self.rect.bottom = block.rect.top


class Enemy(pg.sprite.Sprite):
    """общий класс для всех врагов"""

    def __init__(self, img, speed, hp, attack, x, y):
        super().__init__()
        self.image = pg.image.load(img)
        self.speed = speed
        self.hp = hp
        self.attack = attack
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def attacking(self):
        pass

    def update(self, *args):

        if self.hp <= 0:
            self.kill()
        if args[0][0] > self.rect.x:
            self.rect.x += self.speed
        if args[0][0] < self.rect.x:
            self.rect.x -= self.speed
        if args[0][1] > self.rect.y:
            self.rect.y += self.speed
        if args[0][1] < self.rect.y:
            self.rect.y -= self.speed

    def dead(self, damage):
        self.hp -= damage


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': pg.image.load('meteor-wall.png'),
    'empty': pg.image.load('grass.png')
}

tile_width = tile_height = 15
tiles_group = pg.sprite.Group()
walls = pg.sprite.Group()
all_sprites = pg.sprite.Group()
player_group = pg.sprite.Group()


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.type = tile_type

        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

        if self.type == 'wall':
            walls.add(self)


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
            elif level[y][x] == 'e':
                enemies.add(Enemy('testenemy.png', 5, 20, 1, x * tile_width, y * tile_height))
    return new_player, x, y


FPS = 50
clock = pg.time.Clock()


def terminate():
    pg.quit()
    sys.exit()


def start_screen():
    fon = pg.transform.scale(pg.image.load('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pg.font.Font(None, 30)
    text_coord = 50


enemies = pg.sprite.Group()
size = width, height = 800, 600
pg.display.set_caption('way to freedom')
screen = pg.display.set_mode(size)
running = True
position = [300, 500]

clock = pg.time.Clock()
bullet = Bullet('bullet.png', 5, 30, 40)
reload_time = True
f = pg.font.Font(None, 100)
while True:
    start_screen()
    pg.display.flip()
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            terminate()
        elif event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
            player, level_x, level_y = generate_level(load_level('map.txt'))
            hero = player
            while running:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False

                start_screen()
                walls.update()
                walls.draw(screen)
                bullets.update()
                bullets.draw(screen)
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
                    hero.update('up')
                if keys[pg.K_DOWN]:
                    hero.update('down')

                if pg.sprite.spritecollide(hero, enemies, False):
                    hero.hp -= 1

                for hit in pg.sprite.groupcollide(enemies, bullets, False, True):
                    hit.dead(5)
                if hero.hp <= 0:
                    w = f.render('GAME OVER', True,
                                 pg.Color('red'))
                    screen.blit(w, (100, 100))
                    pg.display.update()
                    pg.time.delay(1000)
                    running = False
                if len(enemies) == 0:
                    w = f.render('YOU WON', True,
                                 pg.Color('green'))
                    screen.blit(w, (100, 100))
                    pg.display.update()
                    pg.time.delay(1000)
                    running = False
                enemies.update(hero.rect)

                screen.blit(hero.image, hero.rect)
                count_hp = f.render(str(hero.hp), True, pg.Color('red'))
                screen.blit(count_hp, (0, 0))
                enemies.draw(screen)
                if now - all_time <= 3:
                    now += 0.1
                    reload_time = True

                elif now - all_time > 3:
                    reload_time = False
                    all_time += 0.25

                if keys[pg.K_SPACE] and not reload_time:
                    # В разработке
                    hero.attacking('cubes')
                pg.display.update()
