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

MYEVENTTYPE = pygame.USEREVENT + 1
pygame.time.set_timer(MYEVENTTYPE, 1000)
platform_length = 130
long_platform_length = 200
platform_width = 10
all_platforms = pygame.sprite.Group()
count_platforms = 0

background = white
player = pygame.transform.scale(pygame.image.load('cat.png'), (40, 40))
player_r = pygame.transform.flip(pygame.transform.rotate(player, 90), True, False)
player_l = pygame.transform.flip(player_r, True, False)
dead = pygame.transform.scale(pygame.image.load('died_cat.jpg'), (40, 40))

last_block = 0
LEVEL = 1
block_w_teeth = 0


class Block(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load('block.png'), (10, 130))
    image2 = pygame.transform.flip(image, True, False)
    long_image = pygame.transform.scale(pygame.image.load('long_platform.png'), (10, 200))
    long_image2 = pygame.transform.flip(long_image, True, False)
    start_image = pygame.transform.scale(pygame.image.load('start.block.png'), (10, 130))
    teeth_image_r = pygame.transform.scale(pygame.image.load('зуб.png'), (10, 130))
    teeth_image_l = pygame.transform.flip(teeth_image_r, True, False)

    def __init__(self, group):
        super().__init__(group)
        global last_block
        global count_platforms
        global axis
        global LEVEL
        global block_w_teeth
        count_platforms += 1
        self.a = random.randint(1, 2)
        if count_platforms == 9 and last_block.rect.x < axis and axis == 250:  # сдвиг влево
            axis = 190
        elif count_platforms == 9 and last_block.rect.x > axis and axis == 250:
            axis = 310
        elif count_platforms == 15:
            axis = 250
        self.start = False
        self.teeth = False
        self.get_image()
        if count_platforms >= 17:
            count_platforms = 1
            LEVEL += 1
            block_w_teeth = random.randrange(4, 17)
            while block_w_teeth == 8 or block_w_teeth == 9 or block_w_teeth == 14 or block_w_teeth == 15:
                block_w_teeth = random.randrange(4, 16)
            self.image = Block.start_image
            self.block_length = platform_length
            self.rect = self.image.get_rect()
            self.start = True
        if LEVEL > 1:
            if count_platforms == block_w_teeth:
                if (last_block.rect.x < axis and (axis == 250 or axis == 190)) or (
                        last_block.rect.x <= axis and axis == 310):
                    self.image = Block.teeth_image_l
                else:
                    self.image = Block.teeth_image_r
                self.block_length = platform_length
                self.rect = self.image.get_rect()
                self.teeth = True
        # if count_platforms == 3:
        #     self.image = Block.teeth_image
        #     self.block_length = platform_length
        #     self.rect = self.image.get_rect()
        #     self.teeth = True
        self.coord()
        self.replace = False
        self.curr = False
        self.turn = False
        if count_platforms == 8 or count_platforms == 14:
            self.turn = True
        last_block = self

    def coord(self):
        b = 0
        if count_platforms == 10 or count_platforms == 16:
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
                                              40])) and not self.curr_block.start and not self.jump:
            return True
        return False

    def current_block(self):  # текущая платформа
        for el in all_platforms:
            if el.rect.colliderect([self.player_x + 10, self.player_y, 40, 40]):
                return el
            if el.rect.colliderect([self.player_x - 10, self.player_y, 40, 40]):
                return el

    def check_collisions(self):
        for el in all_platforms:
            if el.rect.colliderect([self.player_x, self.player_y, 40, 40]) and not el.teeth:
                el.curr = True
                self.curr_block = el
                if el.rect.x < self.player_x + 10:
                    self.player_x = el.rect.x + 10
                else:
                    self.player_x = el.rect.x - 40
                return True
            elif el.rect.colliderect([self.player_x, self.player_y, 40, 40]) and el.teeth:
                el.curr = True
                self.curr_block = el
                self.hurt = True
                self.gravity_y = 6
                self.gravity_x = 1

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
        self.player_y += 1.5
        return True

    def update_platforms(self):
        global count_platforms
        if self.player_y < 480 and self.gravity_y > 0 and self.jump:
            for el in all_platforms:
                el.rect.y += self.gravity_y * 1.3
        else:
            pass
        for el in all_platforms:
            if el.rect.y + platform_length > HEIGHT and not el.replace:
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
# font = pygame.font.Font('font1.tff', 16)
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
for i in range(5):
    Block(all_platforms)
while running:
    timer.tick(fps)
    screen.fill(background)
    all_platforms.draw(screen)
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
            cat.update_turn()
        if event.type == pygame.MOUSEBUTTONDOWN:
            cat.direction = 3 - cat.direction
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
            cat.gravity_y = 0

    if cat.check_collisions():
        cat.jump = False
        cat.jump_1 = False
        cat.jump_2 = False
        cat.is_slip = True
        cat.is_fall = False

    if cat.hurt and not cat.is_fall and not cat.dead:
        cat.jump_back()
        if cat.gravity_y == 10:
            cat.is_fall = True

    if cat.check_fall() and not cat.dead:
        cat.is_fall = True
        cat.fall()
        cat.jump = False

    if cat.check_slip() and not cat.dead:
        cat.is_slip = True
        cat.slip()
    else:
        cat.is_slip = False

    if cat.jump_1 and not cat.check_collisions() and not cat.check_fallen() and not cat.check_fall():
        cat.jump = True
        cat.one_click()
    elif cat.jump_2 and not cat.check_collisions() and not cat.check_fallen() and not cat.check_fall():
        cat.jump = True
        cat.two_click()

    cat.update_platforms()
    cat.clear_platforms()

    pygame.display.flip()
pygame.quit()
