import pygame
import random
import sys

pygame.init()

WIDTH = 500
HEIGHT = 600
axis = WIDTH // 2  # разница между блоками 120
background = pygame.transform.scale(pygame.image.load('fon.jpg'), (500, 600))

pygame.mixer.pre_init(44100, 16, 2, 4096)  # звук
sound1 = pygame.mixer.Sound('sound6_fon.mp3')
sound1.set_volume(0.3)
sound_coin = pygame.mixer.Sound('money1.mp3')
sound_new_level = pygame.mixer.Sound('win.mp3')
sound_d = pygame.mixer.Sound('dead.mp3')

# константы для платформ
MYEVENTTYPE = pygame.USEREVENT  # для поворачивающихся блоков
pygame.time.set_timer(MYEVENTTYPE, 1000)
MYEVENTTYPE1 = pygame.USEREVENT + 1  # для блоков с током
pygame.time.set_timer(MYEVENTTYPE1, 2000)
MYEVENTTYPE2 = pygame.USEREVENT + 2
platform_length = 130
long_platform_length = 200
platform_width = 10
all_platforms = pygame.sprite.Group()
count_platforms = 0
difficult_platforms_count = 1
last_block = 0
LEVEL = 1
screen_LEVEL = 1
block_w_teeth = []
block_w_tok = []
turn1 = random.randint(3, 9)
turn2 = turn1 + 6

# консанты для монет
all_moneys = pygame.sprite.Group()
count_money = 0
platforms_for_money = []

# картинки
player = pygame.transform.scale(pygame.image.load('cat.png'), (40, 40))
player_r = pygame.transform.flip(pygame.transform.rotate(player, 90), True, False)
player_l = pygame.transform.flip(player_r, True, False)
dead = pygame.transform.scale(pygame.image.load('died_cat.jpg'), (40, 40))
start_fon = pygame.transform.scale(pygame.image.load('start.png'), (200, 60))
rule = pygame.transform.scale(pygame.image.load('rules.png'), (200, 60))
restart = pygame.transform.scale(pygame.image.load('restart.png'), (200, 60))


class Money(pygame.sprite.Sprite):  # монетки
    image = pygame.transform.scale(pygame.image.load('money.png'), (30, 30))

    def __init__(self, group, block, direction):
        super().__init__(group)
        self.image = Money.image
        self.rect = self.image.get_rect()
        if direction == 'right':
            self.rect.x = block.rect.x + platform_width + 10
        else:
            self.rect.x = block.rect.x - platform_width - 40
        random_y = random.randrange(block.rect.y + block.block_length, block.rect.y - 60, -10)
        self.rect.y = random_y

    def hide(self):  # исчезание монет при контакте с игроком
        global count_money
        count_money += 1
        all_moneys.remove(self)


class Block(pygame.sprite.Sprite):
    # картинки для блоков
    image = pygame.transform.scale(pygame.image.load('block.png'), (10, 130))
    image2 = pygame.transform.flip(image, True, False)
    long_image = pygame.transform.scale(pygame.image.load('long_platform.png'), (10, 200))
    long_image2 = pygame.transform.flip(long_image, True, False)
    start_image = pygame.transform.scale(pygame.image.load('start.block.png'), (10, 130))
    teeth_image_r = pygame.transform.scale(pygame.image.load('зуб.png'), (10, 130))
    teeth_image_l = pygame.transform.flip(teeth_image_r, True, False)
    tok1_image = pygame.transform.scale(pygame.image.load('tok1.png'), (10, 130))
    tok2_image = pygame.transform.scale(pygame.image.load('tok2.png'), (10, 130))
    tok3_image = pygame.transform.scale(pygame.image.load('tok3.png'), (10, 130))
    tok1_image_l = pygame.transform.scale(pygame.image.load('tok1.png'), (10, 200))
    tok2_image_l = pygame.transform.scale(pygame.image.load('tok2.png'), (10, 200))
    tok3_image_l = pygame.transform.scale(pygame.image.load('tok3.png'), (10, 200))

    def __init__(self, group):
        super().__init__(group)
        global last_block
        global count_platforms
        global axis
        global LEVEL
        global block_w_teeth
        global block_w_tok
        global turn1
        global turn2
        global platforms_for_money
        global difficult_platforms_count
        count_platforms += 1
        self.a = random.randint(1, 2)
        if count_platforms == turn1 + 1 and last_block.rect.x < axis and axis == 250:  # сдвиг влево
            axis = 190
        elif count_platforms == turn1 + 1 and last_block.rect.x > axis and axis == 250:  # сдвиг вправо
            axis = 310
        elif count_platforms == turn2 + 1:
            axis = 250
        self.start = False
        self.start_flag = False
        self.teeth = False
        self.teeth_r = False
        self.teeth_l = False
        self.tok = False
        self.count_for_tok = 0
        self.is_tok = False
        self.fade = False
        self.rect = pygame.Rect(-10, -10, 0, 0)
        self.get_image()
        if count_platforms >= 17:  # новый уровень, новые константы для уровня
            platforms_for_money = random.sample(range(2, 17), 6)
            turn1 = random.randint(3, 9)
            turn2 = turn1 + 6
            count_platforms = 1
            LEVEL += 1
            if LEVEL == 3:
                difficult_platforms_count = 2  # количество платформ с усложнением
            block_w_teeth0 = random.sample(range(3, 17, 2), difficult_platforms_count)
            block_w_teeth = []
            for el in block_w_teeth0:  # выбор платформы с зубчиками
                while el == turn1 or el == turn1 + 1 or el == turn2 or el == turn2 + 1 or el in block_w_teeth:
                    el = random.randrange(3, 17, 2)
                block_w_teeth.append(el)
            block_w_tok = []
            block_w_tok0 = random.sample(range(3, 17), difficult_platforms_count)
            for el in block_w_tok0:  # выбор платформы с током
                while el == turn1 + 1 or el == turn2 + 1 or \
                        el in block_w_teeth:
                    el = random.randrange(3, 17)
                block_w_tok.append(el)
            block_w_tok.sort()
            self.image = Block.start_image
            self.block_length = platform_length
            self.rect = self.image.get_rect()
            self.start = True
            self.start_flag = False
        if LEVEL == 1:  # платформы с монетками
            platforms_for_money = random.sample(range(2, 17), 6)
        if LEVEL > 1:
            if count_platforms in block_w_tok:
                s = 0
                for el in block_w_tok:
                    if el == count_platforms:
                        s = el
                        self.image0 = self.image  # запоминание начального image с током
                        self.rect = self.image.get_rect()
                        self.tok = True
                        self.is_tok = False
                        self.count_for_tok = 1
                    break
                if s in block_w_tok:  # чтобы не повторялись блоки с током
                    block_w_tok.remove(s)
            elif count_platforms in block_w_teeth:
                s = 0
                for el in block_w_teeth:
                    if el == count_platforms:
                        s = el
                        if (last_block.rect.x < axis and (axis == 250 or axis == 190)) or (
                                last_block.rect.x <= axis and axis == 310):  # определение оси
                            self.image = Block.teeth_image_l
                            self.teeth_l = True
                        else:
                            self.image = Block.teeth_image_r
                            self.teeth_r = True
                        self.block_length = platform_length
                        self.rect = self.image.get_rect()
                        self.teeth = True
                    break
                if s in block_w_teeth:
                    block_w_teeth.remove(s)
        self.coord()
        self.replace = False
        self.curr = False
        self.turn = False
        if count_platforms == turn1 or count_platforms == turn2:
            self.turn = True
        last_block = self
        self.do_money()

    def do_money(self):  # генерирование местоположения монеток
        for el in platforms_for_money:
            if count_platforms == el:
                if (last_block.rect.x < axis and (axis == 250 or axis == 190)) or (
                        last_block.rect.x <= axis and axis == 310):
                    direct = 'right'
                else:
                    direct = 'left'
                Money(all_moneys, self, direct)

    def coord(self):  # генерирование координат платформ
        b = 0
        if count_platforms == turn1 + 2 or count_platforms == turn2 + 2:
            b = 220
        elif count_platforms == turn1 + 1 or count_platforms == turn2 + 1:
            b = 220
        if last_block:
            if (last_block.rect.x < axis and (axis == 250 or axis == 190)) or (
                    last_block.rect.x <= axis and axis == 310):
                if self.a == 1:
                    if not b:
                        b = random.randrange(90, 131)
                else:
                    if not b:
                        b = random.randrange(160, 201)
                self.rect.x = axis + 60
                self.rect.y = last_block.rect.y - b
            else:
                if self.a == 1:
                    if not b:
                        b = random.randrange(100, 131)
                else:
                    if not b:
                        b = random.randrange(160, 201)
                self.rect.x = axis - 60
                self.rect.y = last_block.rect.y - b

    def get_image(self):  # генерирование картинки блока
        if last_block:
            if (last_block.rect.x < axis and (axis == 250 or axis == 190)) or (
                    last_block.rect.x <= axis and axis == 310):
                if self.a == 1:
                    self.image = Block.image2
                    self.block_length = platform_length
                    self.rect = self.image.get_rect()
                else:
                    self.image = Block.long_image2
                    self.block_length = long_platform_length
                    self.rect = self.long_image.get_rect()
            else:
                if self.a == 1:
                    self.image = Block.image
                    self.block_length = platform_length
                    self.rect = self.image.get_rect()
                else:
                    self.image = Block.long_image
                    self.block_length = long_platform_length
                    self.rect = self.long_image.get_rect()
        else:
            self.block_length = platform_length

    def update(self):  # обновление для платформ с электричеством
        if self.tok:
            if self.is_tok:
                self.image = self.image0
                self.is_tok = False
            else:
                self.is_tok = True

    def do_tok(self):  # смена картинок для электричества
        if self.block_length == platform_length:
            if self.count_for_tok == 1:
                self.image = Block.tok2_image
            elif self.count_for_tok == 2:
                self.image = Block.tok3_image
            else:
                self.image = Block.tok1_image
        else:
            if self.count_for_tok == 1:
                self.image = Block.tok2_image_l
            elif self.count_for_tok == 2:
                self.image = Block.tok3_image_l
            else:
                self.image = Block.tok1_image_l
        self.count_for_tok += 1
        if self.count_for_tok == 4:
            self.count_for_tok = 1


class Cat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player
        self.rect = self.image.get_rect()
        self.image_r = player_r
        self.image_l = player_l
        self.player_x = 200
        self.player_y = 500
        self.image_dead = dead
        self.dead = False
        self.jump = False
        self.jump_counter = 0
        self.jump_1 = False
        self.jump_2 = False
        self.curr_block = self.current_block()  # спрайт текущего блока
        self.direction = 2  # left
        self.gravity_y = 15
        self.gravity_x = 2
        self.check_2_jump = False
        self.is_slip = False
        self.is_fall = False
        self.hurt = False

    def start_move(self, button):  # движение кота на заставке
        if self.player_x > button.rect.x + 200 and self.player_y - 60 < button.rect.y:
            self.player_y += 0.1
            self.image = pygame.transform.flip(player_r, False, True)
        elif self.player_x - 5 <= button.rect.x - 40 and self.player_y > button.rect.y - 30:
            self.image = player_l
            self.player_y -= 0.1
        elif button.rect.x - 5 < self.player_x + 40 < button.rect.x + 240 and self.player_y < button.rect.y:
            self.player_x += 0.1
            self.image = player
        elif button.rect.x - 40 < self.player_x - 5 < button.rect.x + 200 and self.player_y > button.rect.y:
            self.player_x -= 0.1
            self.image = pygame.transform.flip(player, True, True)

    def update_rect(self):
        self.rect = self.image.get_rect()

    def check_fallen(self):  # кот коснулся предела окна
        a = self.player_x > WIDTH or self.player_x < 0 or self.player_y + 40 > HEIGHT
        if a and not self.dead and not self.hurt:
            sound_d.play()
        return a

    def check_fall(self):  # находится в падении
        return self.curr_block.rect[1] + self.curr_block.block_length < self.player_y + 20 and \
               (self.curr_block.rect[0] == self.player_x + 40 or self.curr_block.rect[0] == self.player_x - 10)

    def check_slip(self):  # проверка на скольжение
        if (self.curr_block.rect.colliderect([self.player_x + 10, self.player_y, 40, 40]) or
            self.curr_block.rect.colliderect([self.player_x - 10, self.player_y, 40,
                                              40])) and not self.curr_block.start and not self.jump and \
                not self.curr_block.is_tok and not (
                (self.curr_block.teeth_r and self.player_x >= self.curr_block.rect.x) or (
                self.curr_block.teeth_l and self.player_x < self.curr_block.rect.x)):
            return True
        if (self.curr_block.is_tok or (self.curr_block.teeth_r and self.player_x >= self.curr_block.rect.x) or (
                self.curr_block.teeth_l and self.player_x < self.curr_block.rect.x)) and not self.hurt and not self.jump:  # если на не обычной платформе
            self.hurt = True
            sound_d.play()
            self.is_fall = False
            self.gravity_y = 6
            self.gravity_x = 1
        return False

    def current_block(self):  # текущая платформа
        for el in all_platforms:
            if el.rect.colliderect([self.player_x + 10, self.player_y, 40, 40]):
                return el
            if el.rect.colliderect([self.player_x - 10, self.player_y, 40, 40]):
                return el

    def check_collisions(self):  # проверка пересечения с платформой
        global screen_LEVEL
        for el in all_platforms:
            if el.rect.colliderect([self.player_x, self.player_y, 40, 40]) and el.start:
                if not el.start_flag:
                    el.start_flag = True
                    screen_LEVEL += 1
                    sound_new_level.play()
            if el.rect.colliderect([self.player_x, self.player_y, 40, 40]) and \
                    (not self.curr_block.teeth or (
                            self.curr_block.teeth_r and self.player_x < self.curr_block.rect.x) or
                     (self.curr_block.teeth_l and self.player_x > self.curr_block.rect.x)) and not el.is_tok:
                el.curr = True
                self.curr_block = el
                if el.rect.x < self.player_x + 10:
                    self.player_x = el.rect.x + 10
                else:
                    self.player_x = el.rect.x - 40
                return True
            elif el.rect.colliderect([self.player_x, self.player_y, 40, 40]) and \
                    ((self.curr_block.teeth_r and self.player_x >= self.curr_block.rect.x) or
                     (self.curr_block.teeth_l and self.player_x < self.curr_block.rect.x) or el.is_tok):
                el.curr = True
                self.curr_block = el
                self.is_fall = False
                self.hurt = True
                sound_d.play()
                self.gravity_y = 6
                self.gravity_x = 1

    def check_money(self):  # пересечение с монеткой
        for el in all_moneys:
            if el.rect.colliderect([self.player_x, self.player_y, 40, 40]):
                el.hide()
                pygame.mixer.Channel(1).play(sound_coin)

    def jump_back(self):  # отскок назад при ранении
        self.player_y -= self.gravity_y
        if self.curr_block.rect[0] > self.player_x:
            self.player_x -= self.gravity_x
        else:
            self.player_x += self.gravity_x
        self.gravity_y += 0.2

    def one_click(self):  # короткий прыжок
        if self.jump_counter == 1 and not self.check_2_jump:  # если уже был прыжок (для двойного)
            self.gravity_y = 10
            self.gravity_x = -self.gravity_x
            self.check_2_jump = True
        if self.jump:
            self.player_y -= self.gravity_y
            if self.curr_block.rect[0] > self.player_x:
                self.player_x -= self.gravity_x
            else:
                self.player_x += self.gravity_x
            self.gravity_y -= 1

    def two_click(self):  # длинный прыжок
        if self.jump_counter == 1 and not self.check_2_jump:
            self.gravity_y = 14
            self.gravity_x = -self.gravity_x
            self.check_2_jump = True
        if self.jump:
            self.player_y -= self.gravity_y
            if self.gravity_y:
                if self.curr_block.rect[0] > self.player_x:
                    self.player_x -= self.gravity_x
                else:
                    self.player_x += self.gravity_x
            self.gravity_y -= 1

    def slip(self):  # скольжение
        self.player_y += 0.3

    def fall(self):  # падение
        self.player_y += 2
        return True

    def update_platforms(self):  # обновление координат плафторм
        if self.player_y < 200 and self.gravity_y > 0 and self.jump:
            for el in all_platforms:
                el.rect.y += self.gravity_y * 1.8
            for el in all_moneys:
                el.rect.y += self.gravity_y * 1.8
        elif self.player_y < 480 and self.gravity_y > 0 and self.jump:
            for el in all_platforms:
                el.rect.y += self.gravity_y * 1.3
            for el in all_moneys:
                el.rect.y += self.gravity_y * 1.3
        else:
            pass
        for el in all_platforms:
            if el.tok and el.is_tok:
                el.do_tok()
            if el.rect.y + el.block_length > HEIGHT and not el.replace:  # создание новых платформ
                Block(all_platforms)
                el.replace = True

    def update_turn(self):  # поворачивание платформ
        for el in all_platforms:
            if el.turn:
                el.image = pygame.transform.flip(el.image, True, False)
        if self.curr_block.turn and self.is_slip:
            if self.player_x < self.curr_block.rect.x:
                self.player_x = self.curr_block.rect.x + platform_width
            else:
                self.player_x = self.curr_block.rect.x - 40

    def clear_platforms(self):  # очистка старых платформ
        for el in all_platforms:
            if el.rect.x >= WIDTH or el.rect.x < 0 or el.rect.y >= HEIGHT:
                all_platforms.remove(el)


fps = 60
flip = False
font = pygame.font.Font('Lilita.ttf', 20)
font_name = pygame.font.Font('Lilita.ttf', 40)
timer = pygame.time.Clock()
fon = pygame.transform.scale(pygame.image.load('fon.jpg'), (WIDTH, HEIGHT))


def terminate():
    pygame.quit()
    sys.exit()


def rules():  # правила игры
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.blit((fon), (0, 0))
    pygame.display.set_caption('cat jump')
    intro_text = ["left mouse button - short jump,", '',
                  "right mouse button - long jump,", '',
                  "two clicks in a row - double jump,", '',
                  "beware of electricity and anything sharp.", '']
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
        pygame.display.flip()


def text():
    string_rendered = font_name.render("Game CAT JUMP", 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 10
    intro_rect.x = 110
    intro_rect.y = 40
    screen.blit(string_rendered, intro_rect)


def text2(text):
    text_coord = 50
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def start_game():  # начало игры
    screen.blit((fon), (0, 0))
    start_fon_sp = pygame.sprite.Sprite()
    start_fon_sp.image = start_fon
    start_fon_sp.rect = pygame.Rect(155, 400, 200, 60)
    que = pygame.sprite.Sprite()
    que.image = rule
    que.rect = pygame.Rect(155, 200, 200, 60)
    cat1 = Cat()
    cat1.player_x = 200
    cat1.player_y = 370
    cat1.image = player

    while True:
        screen.blit((fon), (0, 0))
        text()
        screen.blit(start_fon_sp.image, (155, 400))
        screen.blit(que.image, (155, 200))
        screen.blit(cat1.image, (cat1.player_x, cat1.player_y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # попадание на кнопку
                if start_fon_sp.rect.x <= event.pos[0] <= start_fon_sp.rect.x + 200 and \
                        start_fon_sp.rect.y <= event.pos[1] <= start_fon_sp.rect.y + 60:
                    return True
                elif que.rect.x <= event.pos[0] <= que.rect.x + 200 and \
                        que.rect.y <= event.pos[1] <= que.rect.y + 60:
                    rules()
        cat1.start_move(start_fon_sp)
        pygame.display.flip()


def game_over():  # запись рекорда в файл
    f = open("result.txt", encoding='utf8')
    res = f.readlines()
    record = res[0]
    intro_text = ["All collected coins:", str(count_money), '',
                  "Count levels:", str(screen_LEVEL), '']
    if count_money > int(record):
        intro_text.append('You broke the record!')
        intro_text.append('')
        f.close()
        f = open("result.txt", 'w')
        f.write(str(count_money))
        record = count_money
        f.close()
    f.close()
    intro_text.append('Record: ')
    intro_text.append(str(record))
    rstart = pygame.sprite.Sprite()
    rstart.image = restart
    rstart.rect = pygame.Rect(155, 400, 200, 60)
    while True:
        screen.blit((fon), (0, 0))
        screen.blit(rstart.image, (155, 400))
        text2(intro_text)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rstart.rect.x <= event.pos[0] <= rstart.rect.x + 200 and \
                        rstart.rect.y <= event.pos[1] <= rstart.rect.y + 60:
                    start()
                    return True
        pygame.display.flip()
        timer.tick(30)


def start():  # обновление констант пр новой игре
    global cat, running, first_block, last_block, first_block, all_platforms, count_platforms, \
        difficult_platforms_count, all_moneys, count_money, platforms_for_money, LEVEL, screen_LEVEL, block_w_teeth, \
        block_w_tok, turn2, turn1, axis, screen
    LEVEL = 1
    screen_LEVEL = 1
    block_w_teeth = []
    block_w_tok = []
    turn1 = random.randint(3, 9)
    turn2 = turn1 + 6
    axis = WIDTH // 2
    all_platforms = pygame.sprite.Group()
    count_platforms = 0
    difficult_platforms_count = 1
    all_moneys = pygame.sprite.Group()
    count_money = 0
    platforms_for_money = []
    cat = Cat()
    running = True
    first_block = Block(all_platforms)
    first_block.rect = pygame.Rect(190, 460, platform_width, platform_length)
    first_block.start = True
    first_block.start_flag = True
    for i in range(5):
        Block(all_platforms)
    return


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('cat jump')
cat = Cat()
running = True
first_block = Block(all_platforms)
first_block.rect = pygame.Rect(190, 460, platform_width, platform_length)
first_block.rect.x = 190
first_block.rect.y = 460
last_block = first_block
first_block.start = True
first_block.start_flag = True
for i in range(5):
    Block(all_platforms)

pygame.mixer.Channel(0).play(sound1, loops=-1)
start_game()
while running:
    timer.tick(fps)
    screen.blit(background, (0, 0))
    all_platforms.draw(screen)
    all_moneys.draw(screen)
    text = font.render(f"Collected coins: {count_money}", True, (0, 0, 0))
    text_x = 15
    text_y = 10
    text_level = font.render(f"LEVEL: {screen_LEVEL}", True, (0, 0, 0))
    text_level_x = 15
    text_level_y = HEIGHT - 30
    screen.blit(text, (text_x, text_y))
    screen.blit(text_level, (text_level_x, text_level_y))
    # проверка на картинку кота
    if cat.check_fallen():
        cat.jump = False
        cat.dead = True
        screen.blit(cat.image_dead, (cat.player_x, cat.player_y))
    elif cat.jump or cat.current_block() is None or cat.hurt:
        screen.blit(cat.image, (cat.player_x, cat.player_y))
    else:
        cat.curr_block = cat.current_block()
        if cat.check_fall():
            screen.blit(cat.image, (cat.player_x, cat.player_y))
        elif cat.curr_block.rect.x < cat.player_x:
            screen.blit(cat.image_r, (cat.player_x, cat.player_y))
        else:
            screen.blit(cat.image_l, (cat.player_x, cat.player_y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MYEVENTTYPE:
            if not cat.dead:
                cat.update_turn()
        if event.type == MYEVENTTYPE1:
            all_platforms.update()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not cat.hurt:
            cat.jump_2 = False
            if not cat.check_fall():
                cat.jump_1 = True
                if cat.jump:
                    cat.jump_counter += 1
                else:
                    cat.gravity_y = 10
                    cat.gravity_x = 2
                    cat.jump_counter = 0
                    cat.check_2_jump = False
            else:
                cat.jump = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and not cat.hurt:  # правая кнопка мыши
            cat.jump_1 = False
            if not cat.check_fall():
                cat.jump_2 = True
                if cat.jump:
                    cat.jump_counter += 1
                else:
                    cat.gravity_y = 14
                    cat.gravity_x = 3
                    cat.jump_counter = 0
                    cat.check_2_jump = False
            else:
                cat.jump = False
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3 and cat.jump:
            cat.jump_2 = True
            cat.gravity_y = -1

    cat.check_money()

    if cat.check_collisions() and not cat.hurt:  # пересечение с блоком
        cat.jump = False
        cat.jump_1 = False
        cat.jump_2 = False
        cat.is_slip = True
        cat.is_fall = False

    if cat.hurt and not cat.is_fall and not cat.dead:  # получение ранения
        cat.jump_back()
        cat.gravity_y -= 1

    if cat.check_fall() and not cat.dead:  # падение
        cat.is_fall = True
        cat.fall()
        cat.jump = False

    if cat.check_slip() and not cat.dead:  # скольжение
        cat.is_slip = True
        cat.slip()
    else:
        cat.is_slip = False

    # прыжки
    if cat.jump_1 and not cat.check_collisions() and not cat.check_fallen() and not cat.check_fall() and not cat.hurt:
        cat.jump = True
        cat.one_click()
    elif cat.jump_2 and not cat.check_collisions() and not cat.check_fallen() and not cat.check_fall() and not cat.hurt:
        cat.jump = True
        cat.two_click()

    cat.update_platforms()
    cat.clear_platforms()

    pygame.display.flip()
    if cat.dead:
        screen.blit(cat.image_dead, (cat.player_x, cat.player_y))
        pygame.time.delay(1000)
        game_over()
pygame.quit()
