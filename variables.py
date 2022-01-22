from imports import *
pg.init()
with open('map_for_second_level2.txt', 'r') as f:
    WALLS_AND_TILES_SECOND_LEVEL = []
    file = f.readlines()
    for i in file[:-3]:
        WALLS_AND_TILES_SECOND_LEVEL.append(i.strip())
tile_images = {
    'wall': pg.image.load('wall (3).png'),
    'empty': pg.image.load('grass.png')
}
empty = []
window = pg.display.set_mode((0, 0), pg.FULLSCREEN)
enemies_hp = []
save_for_second_level = []
with open('map_for_second_level2.txt', 'r') as f:
    file = f.readlines()
    for i in file:
        save_for_second_level.append(i.strip())

move_to_bullet = ''
size = width, height = window.get_rect()[2], window.get_rect()[3]
reload_time = True
fontt = pg.font.Font(None, 100)
WEAPONS = ['first_gun']
weapon = WEAPONS[0]
all_time = t.time()
now = t.time()
fire_sound = pg.mixer.Sound('odnokratnyiy-piu.mp3')
summon_event = pg.USEREVENT + 1
first_weapon_dmg = 15
# создание групп спрайтов
screen = pg.display.set_mode(size)
bullets = pg.sprite.Group()
enemy_bullets = pg.sprite.Group()
walls_for_battle = pg.sprite.Group()
tiles_group = pg.sprite.Group()
walls = pg.sprite.Group()
all_sprites = pg.sprite.Group()
player_group = pg.sprite.Group()
enemies = pg.sprite.Group()
enemies_for_save = pg.sprite.Group()
all_sprites_for_save = pg.sprite.Group()
fire_enemies = pg.sprite.Group()
Fire_enemies = pg.sprite.Group()
heroes = pg.sprite.Group()
all_sprites_for_save = pg.sprite.Group()
green_gads = pg.sprite.Group()
