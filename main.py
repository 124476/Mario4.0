import os
import pygame
import sys


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50

CELL_SIZE = 50


#  описание классов воды, непроходимых стен и разрешенной для ходьбы дороги
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        self.pos_x = pos_x
        self.tile_type = tile_type
        self.pos_y = pos_y
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            CELL_SIZE * pos_x, CELL_SIZE * pos_y)

    #  получение названия текущего объекта
    def get_tile_type(self):
        return self.tile_type

    #  возврат координат текущего объекста
    def get_pos(self):
        return self.pos_x, self.pos_y

    # удаление изображения кристалла в момент его помещения в сундук
    def del_crystal(self):
        self.image = tile_images['empty']
        self.tile_type = 'empty'


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    #  текущие координаты сундука
    def get_pos(self):
        return self.pos_x, self.pos_y

    #  перемещение сундука по экрану
    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y
        if pygame.sprite.spritecollide(self, tiles_group, False)[0].get_tile_type() == 'wall':
            if x > 0:
                self.rect.x -= x
            elif x < 0:
                self.rect.x += x
            elif y > 0:
                self.rect.y -= y
            elif y < 0:
                self.rect.y += y


# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


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
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


player, level_x, level_y = generate_level(load_level('map.txt'))

clock = pygame.time.Clock()

FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = [""]

    fon = pygame.transform.scale(load_image('fon.jpg'), (500, 500))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Движущийся круг 2')
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)

    running = True
    start_screen()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if player.rect.x - CELL_SIZE >= 0:
                        player.rect.x -= CELL_SIZE
                        if pygame.sprite.spritecollide(player, tiles_group, False)[0].get_tile_type() == 'wall':
                            player.rect.x += CELL_SIZE
                if event.key == pygame.K_RIGHT:
                    if player.rect.x + CELL_SIZE < width:
                        player.rect.x += CELL_SIZE
                        if pygame.sprite.spritecollide(player, tiles_group, False)[0].get_tile_type() == 'wall':
                            player.rect.x -= CELL_SIZE
                if event.key == pygame.K_UP:
                    if player.rect.y - CELL_SIZE >= 0:
                        player.rect.y -= CELL_SIZE
                        if pygame.sprite.spritecollide(player, tiles_group, False)[0].get_tile_type() == 'wall':
                            player.rect.y += CELL_SIZE
                if event.key == pygame.K_DOWN:
                    if player.rect.y + CELL_SIZE < height:
                        player.update(0, 50)
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
