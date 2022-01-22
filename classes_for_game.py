from variables import *
class Fon(pg.sprite.Sprite):
    def __init__(self, y, x):
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


class Hero(pg.sprite.Sprite):
    """класс для главного героя нашей игры"""

    def __init__(self, img, speed, hp, attack, x, y, move_to):
        super().__init__(all_sprites, all_sprites_for_save)
        self.image = pg.image.load(img)
        self.imag = 'fireball_right.png'
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
        self.move_to = move_to
        all_sprites.add(self)

    def attacking(self, weapon ):
        global bullets
        fire_sound.play()
        where = self.rect.x
        up_down = self.rect.y
        if self.move_to == 'left':
            where = self.rect.left
            self.imag = 'fireball_left.png'
        elif self.move_to == 'right':
            self.imag = 'fireball_right.png'
            where = self.rect.right
        bullet = Bullet(self.imag, 15, first_weapon_dmg, where, up_down, self.move_to)

        bullets.add(bullet)
        bullet.update(self.move_to)

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

    def __init__(self, img, speed, hp, attack, x, y, can_see=150):
        super().__init__(all_sprites, all_sprites_for_save, enemies_for_save)
        self.image = pg.image.load(img)
        self.speed = speed
        self.hp = hp
        self.attack = attack
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.where = ''
        self.can_see_y = can_see
        self.type = 'e'
        self.all_time = t.time()
        self.now = t.time()
        self.reload_time = False

    def reload(self, how_long):
        """перезарядка для стреляющих врагов"""
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
class FireEnemy(Enemy):
    """класс для стреляющего врага, который выпускает пули в одном направлении"""

    def __init__(self, img, speed, hp, damage, bullet_damage, x, y, can_see=150):
        super().__init__(img, speed, hp, damage, x, y, can_see)
        self.bullet_len = 175
        self.type = 'f'
        self.bullet_damage = bullet_damage

    def attacking(self, hero_rect):
        self.reload(1)
        if abs(hero_rect.y - self.rect.y) <= self.can_see_y and not (self.reload_time):
            move_to_bullet = 'right'
            if hero_rect[0] < self.rect.x:
                move_to_bullet = 'left'
            if not self.reload_time:
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

                    self.all_time = t.time()
                    self.now = t.time()
                    enemy_bullet = Bullet('enemy_bullets.png', 10, self.bullet_damage, there, up_down, move_to_bullet)
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

    def __init__(self, img, speed, hp, damage, bullet_damage, x, y, can_see=150):
        super().__init__(img, speed, hp, damage, x, y, can_see)
        self.type = 'F'
        self.bullet_damage = bullet_damage

    def attacking(self, hero_rect):
        self.reload(3)
        if abs(hero_rect.y - self.rect.y) <= self.can_see_y and not (self.reload_time):
            self.all_time = t.time()
            self.now = t.time()
            enemy_bullet = Bullet('enemy_bullets.png', 10, self.bullet_damage, self.rect.left, self.rect.y, 'left')
            enemy_bullets.add(enemy_bullet)
            enemy_bullet = Bullet('enemy_bullets.png', 10, self.bullet_damage, self.rect.right, self.rect.y, 'right')
            enemy_bullets.add(enemy_bullet)
            enemy_bullet = Bullet('enemy_bullets.png', 10, self.bullet_damage,
                                  self.rect.midtop[0], self.rect.midtop[1], 'up')
            enemy_bullets.add(enemy_bullet)
            enemy_bullet = Bullet('enemy_bullets.png', 10, self.bullet_damage,
                                  self.rect.midbottom[0], self.rect.midbottom[1], 'down')
            enemy_bullets.add(enemy_bullet)


class Boss(FiretoallEnemy):
    """Босс нашей игры, может призывать приспешников"""
    def __init__(self, img, speed, hp, attack, bullet_damage, x, y, can_see):
        super().__init__(img, speed, hp, attack, bullet_damage, x, y, can_see)
        self.type = 'B'

    def summon(self):
        enemies.add(Enemy('mini_gad.png', randint(3, 6), 15, 2, self.rect.x + 20, self.rect.y, self.can_see_y))

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

class Green_gad(Enemy):
    """как обычный враг, только больше"""

    def __init__(self, img, speed, hp, damage, x, y, can_see=400):
        super().__init__(img, speed, hp, damage, x, y)
        self.right_move = -1
        self.left_move = -1
        self.type = 'G'
        self.can_see_y = can_see
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

class menu_window(pygame_gui.elements.ui_window.UIWindow):
    def __init__(self, manager_func: IUIManagerInterface,
                 object_id: Union[ObjectID, str] = ObjectID('#menu_dialog', None)):
        inf = display.Info()
        widow_size = inf.current_w, inf.current_h
        size_1 = [widow_size[0] // 2.5, widow_size[1] // 1.5]
        rectangle = pygame.Rect(0, 0, 0, 0)
        rectangle.size = size_1
        rectangle.center = (widow_size[0] // 2, widow_size[1] // 2)
        super().__init__(rectangle, manager_func,
                         window_display_title='Меню',
                         object_id=object_id,
                         resizable=False,
                         visible=1)
        self.set_blocking(True)

        button_layout_rect = pygame.Rect(0, 0, 0, 0)
        button_layout_rect.size = (450, size_1[0] // 10)
        button_layout_rect.center = [size_1[1] // 2, size_1[1] // 2 - 150]

        self.confirmation_text = UITextBox(html_text="<font size=7>       Меню паузы</font>",
                                           relative_rect=pygame.Rect(5, 5, size_1[0] - 45, size_1[0] // 10),
                                           manager=self.ui_manager,
                                           container=self,
                                           anchors={'left': 'left',
                                                    'right': 'right',
                                                    'top': 'top',
                                                    'bottom': 'bottom'})

        self.cancel_button = UIButton(relative_rect=button_layout_rect,
                                      text='Продолжить',
                                      manager=self.ui_manager,
                                      container=self,
                                      object_id=ObjectID(class_id='@cancel_button', object_id='#cancel_button'),
                                      )

        button_layout_rect.center = [size_1[1] // 2, size_1[1] // 2 - 50]

        self.save_button = UIButton(relative_rect=button_layout_rect,
                                    text='Сохранить и выйти',
                                    manager=self.ui_manager,
                                    container=self,
                                    object_id='#save_button',
                                    anchors={'left': 'left',
                                             'right': 'right',
                                             'top': 'top',
                                             'bottom': 'bottom'})

        button_layout_rect.center = [size_1[1] // 2, size_1[1] // 2 + 50]

        self.confirm_button = UIButton(relative_rect=button_layout_rect,
                                       text='Назад в главное меню',
                                       manager=self.ui_manager,
                                       container=self,
                                       object_id='#confirm_button',
                                       anchors={'left': 'left',
                                                'right': 'right',
                                                'top': 'top',
                                                'bottom': 'bottom'})

    def process_event(self, event_func: pygame.event.Event) -> bool:
        consumed_event = super().process_event(event_func)

        if event_func.type == UI_BUTTON_PRESSED and event_func.ui_element == self.cancel_button:
            self.kill()

        if event_func.type == UI_BUTTON_PRESSED and event_func.ui_element == self.confirm_button:
            event_data = {'user_type': OldType(UI_CONFIRMATION_DIALOG_CONFIRMED),
                          'ui_element': self,
                          'ui_object_id': self.most_specific_combined_id}
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, event_data))

        return consumed_event
