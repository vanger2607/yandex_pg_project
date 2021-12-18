import pygame as pg

move_to = 'right'


class Bullet(pg.sprite.Sprite):
    # В разработке
    def __init__(self, img, damage, x, y):
        pg.sprite.Sprite.__init__(self)

        self.icon = pg.image.load(img)
        self.rect = self.icon.get_rect()
        self.damage = damage
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        if args[0] == 'left':
            self.rect.x -= 1
        elif args[0] == 'right':
            self.rect.x += 1
        if self.rect.x <= 10 or self.rect.x >= width - 10:
            self.kill()


bullets = pg.sprite.Group()


class Hero(pg.sprite.Sprite):
    """класс для главного героя нашей игры"""

    def __init__(self, img, speed, hp, attack, x, y):
        pg.sprite.Sprite.__init__(self)
        self.icon = pg.image.load(img)
        self.speed = speed
        self.hp = hp
        self.attack = attack
        self.rect = self.icon.get_rect()
        self.rect.x = x
        self.rect.y = y

    def attacking(self, weapon):
        # В разработке
        global bullets
        bullet = Bullet('bullet.png', 1, self.rect.centerx, self.rect.top)
        bullets.add(bullet)
        for i in bullets:
            i.update(move_to)
            screen.blit(i.icon, i.rect)

    def update(self, *args):
        if args[0] == 'right' and self.rect.x + self.speed < width - list(self.rect)[2]:
            self.rect.x += self.speed
        if args[0] == 'left' and self.rect.x - self.speed > 0:
            self.rect.x -= self.speed
        if args[0] == 'up' and self.rect.y - self.speed > 0:
            self.rect.y -= self.speed
        if args[0] == 'down' and self.rect.y + self.speed < height - list(self.rect)[3]:
            self.rect.y += self.speed


class Enemy(pg.sprite.Sprite):
    """общий класс для всех врагов"""

    def __init__(self, img, speed, hp, attack, x, y):
        pg.sprite.Sprite.__init__(self)
        self.icon = pg.image.load(img)
        self.speed = speed
        self.hp = hp
        self.attack = attack
        self.rect = self.icon.get_rect()
        self.rect.x = x
        self.rect.y = y

    def attacking(self):
        pass

    def update(self, *args):
        pg.time.delay(20)
        if args[0][0] > self.rect.x:
            self.rect.x += self.speed
        if args[0][0] < self.rect.x:
            self.rect.x -= self.speed
        if args[0][1] > self.rect.y:
            self.rect.y += self.speed
        if args[0][1] < self.rect.y:
            self.rect.y -= self.speed


pg.init()
f = pg.font.Font(None, 100)

enemy = Enemy('testenemy.png', 5, 20, 1, 20, 100)
size = width, height = 800, 600
pg.display.set_caption('way to freedom')
screen = pg.display.set_mode(size)
running = True
position = [300, 500]
hero = Hero('hero.png', 15, 100, 30, 500, 300)
clock = pg.time.Clock()
bullet = Bullet('bullet.png', 5, 30, 40)
clock.tick(60)
while running:

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

    if pg.sprite.collide_rect(enemy, hero):
        hero.hp -= 1
    if hero.hp <= 0:
        w = f.render('GAME OVER', True,
                     pg.Color('red'))
        screen.blit(w, (100, 100))
        pg.display.update()
        pg.time.delay(1000)
        running = False
    enemy.update(hero.rect)
    screen.fill((0, 0, 0))
    screen.blit(hero.icon, hero.rect)
    screen.blit(enemy.icon, enemy.rect)

    if keys[pg.K_SPACE]:
        # В разработке
        hero.attacking('cubes')

    pg.display.update()
