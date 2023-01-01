import pygame
import random

pygame.init()

# library of game const
white = (255, 255, 255)
black = (0, 0, 0)
gray = (120, 120, 120)
WIDTH = 500
HEIGHT = 600
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


class Block(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load('block.png'), (10, 130))
    image2 = pygame.transform.flip(image, True, False)
    long_image = pygame.transform.scale(pygame.image.load('long_platform.png'), (10, 200))
    long_image2 = pygame.transform.flip(long_image, True, False)
    start_image = pygame.transform.scale(pygame.image.load('start.block.png'), (10, 130))

    def __init__(self, group):
        global last_block
        global count_platforms
        super().__init__(group)
        if last_block:
            if last_block.rect.x < WIDTH // 2:
                a = random.randint(1, 2)
                if a == 1:
                    b = random.randrange(90, 91, 10)
                    self.image = Block.image2
                    self.block_length = platform_length
                    self.rect = self.image.get_rect()
                else:
                    b = random.randrange(100, 121, 10)
                    self.image = Block.long_image2
                    self.block_length = long_platform_length
                    self.rect = self.long_image.get_rect()
                self.rect.x = 310
                self.rect.y = last_block.rect.y - b
            else:
                a = random.randint(1, 2)
                if a == 1:
                    self.image = Block.image
                    self.block_length = platform_length
                    b = random.randrange(130, 171, 10)
                    self.rect = self.image.get_rect()
                else:
                    self.image = Block.long_image
                    self.block_length = long_platform_length
                    b = random.randrange(200, 221, 10)
                    self.rect = self.long_image.get_rect()
                self.rect.x = 190
                self.rect.y = last_block.rect.y - b
        else:
            self.block_length = platform_length
        self.start = False
        if count_platforms >= 21:
            count_platforms = 1
            self.image = Block.start_image
            self.block_length = platform_length
            self.rect = self.image.get_rect()
            self.rect.x = 190
            self.rect.y = last_block.rect.y - 200
            self.start = True
        last_block = self
        self.replace = False
        self.curr = False

    def update_platforms(self, my_list, y_pos, change):
        pass

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
        self.jump_height = 100
        self.jump_width = 100
        self.curr_block = self.current_block()  # спрайт текущего блока
        self.direction = 2  # left
        self.gravity_y = 15
        self.gravity_x = 2
        self.check_2_jump = False
        self.is_slip = False

    def check_fallen(self):  # кот коснулся предела окна
        return self.player_x > WIDTH or self.player_x < 0 or self.player_y + 40 > HEIGHT

    def check_fall(self):  # находится в падении
        return self.curr_block.rect[1] + self.curr_block.block_length < self.player_y + 20 and \
               (self.curr_block.rect[0] == self.player_x + 40 or self.curr_block.rect[0] == self.player_x - 10)

    def check_slip(self):
        if self.curr_block.rect.colliderect([self.player_x + 10, self.player_y, 40, 40]) or \
                self.curr_block.rect.colliderect([self.player_x - 10, self.player_y, 40,
                                                  40]) and not self.curr_block.start and not self.jump:
            # где не равен нулю сделать спец блоки для начала уровня
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
            if el.rect.colliderect([self.player_x, self.player_y, 40, 40]):
                el.curr = True
                self.curr_block = el
                if el.rect.x < self.player_x + 10:
                    self.player_x = el.rect.x + 10
                else:
                    self.player_x = el.rect.x - 40
                return True

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
            self.gravity_y = 15
            self.gravity_x = -self.gravity_x
            self.check_2_jump = True
        if self.jump:
            self.player_y -= self.gravity_y
            if self.curr_block.rect[0] > self.player_x:
                self.player_x -= self.gravity_x
            else:
                self.player_x += self.gravity_x
            self.gravity_y -= 1

    def slip(self):
        self.player_y += 0.3

    def fall(self):
        self.player_y += 1.1
        return True

    def update_platforms(self):
        global count_platforms
        if self.player_y < 400 and self.gravity_y > 0 and self.jump:
            for el in all_platforms:
                el.rect.y += self.gravity_y * 1.2
        else:
            pass
        for el in all_platforms:
            if el.rect.y + platform_length > 600 and not el.replace:
                Block(all_platforms)
                count_platforms += 1
                el.replace = True

    def clear_platforms(self):
        for el in all_platforms:
            if el.rect.x >= 500 or el.rect.x < 0 or el.rect.y >= 600:
                all_platforms.remove(el)


fps = 60
flip = False
# font = pygame.font.Font('font1.tff', 16)
timer = pygame.time.Clock()

# game variables

platforms = [[120, 460, platform_width, platform_length], [220, 400, platform_width, platform_length],
             [120, 270, platform_width, platform_length], [220, 200, platform_width, platform_length],
             [130, 70, platform_width, platform_length], [210, 20, platform_width, platform_length]]

v = 50
t = 1


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
count_platforms += 6
while running:
    timer.tick(fps)
    screen.fill(background)
    all_platforms.draw(screen)
    if cat.check_fallen():
        cat.jump = False
        cat.dead = True
        screen.blit(cat.image_dead, (cat.player_x, cat.player_y))
    elif cat.jump or cat.current_block() is None:
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

        if event.type == pygame.MOUSEBUTTONDOWN:
            cat.direction = 3 - cat.direction
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # правая кнопка мыши
            cat.jump_1 = False
            if not cat.check_fall():
                cat.jump_2 = True
                if cat.jump:
                    cat.jump_counter += 1
                else:
                    cat.gravity_y = 15
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

    if cat.check_fall() and not cat.dead:
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
