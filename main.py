import pygame
import random

pygame.init()

# library of game const
white = (255, 255, 255)
black = (0, 0, 0)
gray = (120, 120, 120)
WIDTH = 500
HEIGHT = 600
axis = WIDTH // 2  # разница между блоками 120

MYEVENTTYPE = pygame.USEREVENT  # для поворачивающихся блоков
pygame.time.set_timer(MYEVENTTYPE, 1000)
MYEVENTTYPE1 = pygame.USEREVENT + 1  # для блоков с током
pygame.time.set_timer(MYEVENTTYPE1, 2000)
platform_length = 130
long_platform_length = 200
platform_width = 10
all_platforms = pygame.sprite.Group()
count_platforms = 0
difficult_platforms_count = 1

all_moneys = pygame.sprite.Group()
count_money = 0
platforms_for_money = []

background = pygame.transform.scale(pygame.image.load('fon.jpg'), (500, 600))
player = pygame.transform.scale(pygame.image.load('cat.png'), (40, 40))
player_r = pygame.transform.flip(pygame.transform.rotate(player, 90), True, False)
player_l = pygame.transform.flip(player_r, True, False)
dead = pygame.transform.scale(pygame.image.load('died_cat.jpg'), (40, 40))

last_block = 0
LEVEL = 1
screen_LEVEL = 1
block_w_teeth = []
block_w_tok = []
turn1 = random.randint(3, 9)
turn2 = turn1 + 6


class Money(pygame.sprite.Sprite):
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

    def hide(self):
        global count_money
        count_money += 1
        all_moneys.remove(self)


class Block(pygame.sprite.Sprite):
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
        elif count_platforms == turn1 + 1 and last_block.rect.x > axis and axis == 250:
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
        self.get_image()
        if count_platforms >= 17:
            platforms_for_money = random.sample(range(2, 17), 6)
            turn1 = random.randint(3, 9)
            turn2 = turn1 + 6
            count_platforms = 1
            LEVEL += 1
            if LEVEL == 5:
                difficult_platforms_count = 2
            # elif LEVEL == 1:
            #     difficult_platforms_count = 3
            block_w_teeth0 = random.sample(range(3, 17, 2), difficult_platforms_count)
            block_w_teeth = []
            for el in block_w_teeth0:
                while el == turn1 or el == turn1 + 1 or el == turn2 or el == turn2 + 1 or el in block_w_teeth:
                    el = random.randrange(3, 17, 2)
                block_w_teeth.append(el)
            block_w_tok = []
            block_w_tok0 = random.sample(range(3, 17), difficult_platforms_count)
            for el in block_w_tok0:
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
        if LEVEL == 1:
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
                if s in block_w_tok:
                    block_w_tok.remove(s)
            elif count_platforms in block_w_teeth:
                s = 0
                for el in block_w_teeth:
                    if el == count_platforms:
                        s = el
                        if (last_block.rect.x < axis and (axis == 250 or axis == 190)) or (
                                last_block.rect.x <= axis and axis == 310):
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
        # if count_platforms == 3:
        #     self.image = Block.teeth_image
        #     self.block_length = platform_length
        #     self.rect = self.image.get_rect()
        #     self.teeth = True
        self.coord()
        self.replace = False
        self.curr = False
        self.turn = False
        if count_platforms == turn1 or count_platforms == turn2:
            self.turn = True
        last_block = self
        self.do_money()

    def do_money(self):
        for el in platforms_for_money:
            if count_platforms == el:
                if (last_block.rect.x < axis and (axis == 250 or axis == 190)) or (
                        last_block.rect.x <= axis and axis == 310):
                    direct = 'right'
                else:
                    direct = 'left'
                Money(all_moneys, self, direct)

    def coord(self):
        b = 0
        if count_platforms == turn1 + 2 or count_platforms == turn2 + 2:
            b = 220
        elif count_platforms == turn1 + 1 or count_platforms == turn2 + 1:
            b = 200
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

    def get_image(self):
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

    def update(self):
        if self.tok:
            if self.is_tok:
                self.image = self.image0
                self.is_tok = False
            else:
                self.is_tok = True

    def do_tok(self):
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

    '''
    def check_col(self):
        if pygame.sprite.spritecollideany(self, not_all_sprites):
            return True
        else:
            not_all_sprites.add(self)
        return False
    '''


class Cat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player
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

    def check_fallen(self):  # кот коснулся предела окна
        return self.player_x > WIDTH or self.player_x < 0 or self.player_y + 40 > HEIGHT

    def check_fall(self):  # находится в падении
        return self.curr_block.rect[1] + self.curr_block.block_length < self.player_y + 20 and \
               (self.curr_block.rect[0] == self.player_x + 40 or self.curr_block.rect[0] == self.player_x - 10)

    def check_slip(self):
        if (self.curr_block.rect.colliderect([self.player_x + 10, self.player_y, 40, 40]) or
            self.curr_block.rect.colliderect([self.player_x - 10, self.player_y, 40,
                                              40])) and not self.curr_block.start and not self.jump and \
                not self.curr_block.is_tok and not self.curr_block.teeth:
            return True
        if (self.curr_block.is_tok or (self.curr_block.teeth_r and self.player_x >= self.curr_block.rect.x) or (
                self.curr_block.teeth_l and self.player_x < self.curr_block.rect.x)) and not self.hurt and not self.jump:
            self.hurt = True
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

    def check_collisions(self):
        global screen_LEVEL
        for el in all_platforms:
            if el.rect.colliderect([self.player_x, self.player_y, 40, 40]) and el.start:
                if not el.start_flag:
                    el.start_flag = True
                    screen_LEVEL += 1
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
                self.gravity_y = 6
                self.gravity_x = 1

    def check_money(self):
        for el in all_moneys:
            if el.rect.colliderect([self.player_x, self.player_y, 40, 40]):
                el.hide()

    def jump_back(self):
        self.player_y -= self.gravity_y
        if self.curr_block.rect[0] > self.player_x:
            self.player_x -= self.gravity_x
        else:
            self.player_x += self.gravity_x
        self.gravity_y += 0.2

    def one_click(self):
        if self.jump_counter == 1 and not self.check_2_jump:
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

    def two_click(self):
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

    def slip(self):
        self.player_y += 0.3

    def fall(self):
        self.player_y += 1.8
        return True

    def update_platforms(self):
        global count_platforms
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
            if el.rect.y > HEIGHT and not el.replace:
                Block(all_platforms)
                el.replace = True

    def update_turn(self):
        for el in all_platforms:
            if el.turn:
                el.image = pygame.transform.flip(el.image, True, False)
                if self.curr_block.turn and self.is_slip:
                    if self.player_x < el.rect.x:
                        self.player_x = el.rect.x + platform_width
                    else:
                        self.player_x = el.rect.x - 40

    def clear_platforms(self):
        for el in all_platforms:
            if el.rect.x >= WIDTH or el.rect.x < 0 or el.rect.y >= HEIGHT:
                all_platforms.remove(el)


fps = 60
flip = False
font = pygame.font.Font('Lilita.ttf', 20)
timer = pygame.time.Clock()

# game variables


# create screen
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
        # elif cat.curr_block.rect[1] > cat.player_y and cat.curr_block.rect[0] < WIDTH // 2 and cat.player_x + 20 \
        #         < cat.curr_block.rect[0]:
        #     print(6)
        #     cat.player_x = cat.curr_block.rect[0] + 10
        #     screen.blit(cat.image_r, (cat.player_x, cat.player_y))
        # elif cat.curr_block.rect[1] > cat.player_y and cat.curr_block.rect[0] > WIDTH // 2 and \
        #         cat.player_x - 20 > cat.curr_block.rect[0] + 10:  # вернуться, когда будет длинный прыжок
        #     cat.player_x = cat.curr_block.rect[0] - 40
        #     screen.blit(cat.image_l, (cat.player_x, cat.player_y))
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

    if cat.check_collisions() and not cat.hurt:
        cat.jump = False
        cat.jump_1 = False
        cat.jump_2 = False
        cat.is_slip = True
        cat.is_fall = False

    if cat.hurt and not cat.is_fall and not cat.dead:
        cat.jump_back()
        cat.gravity_y -= 1

    if cat.check_fall() and not cat.dead:
        cat.is_fall = True
        cat.fall()
        cat.jump = False

    if cat.check_slip() and not cat.dead:
        cat.is_slip = True
        cat.slip()
    else:
        cat.is_slip = False

    if cat.jump_1 and not cat.check_collisions() and not cat.check_fallen() and not cat.check_fall() and not cat.hurt:
        cat.jump = True
        cat.one_click()
    elif cat.jump_2 and not cat.check_collisions() and not cat.check_fallen() and not cat.check_fall() and not cat.hurt:
        cat.jump = True
        cat.two_click()

    cat.update_platforms()
    cat.clear_platforms()

    pygame.display.flip()
pygame.quit()
