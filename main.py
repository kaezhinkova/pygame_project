import pygame
import random

pygame.init()

# library of game const
white = (255, 255, 255)
black = (0, 0, 0)
gray = (120, 120, 120)
WIDTH = 400
HEIGHT = 600
platform_length = 130
platform_width = 10
all_platforms = pygame.sprite.Group()
background = white
player = pygame.transform.scale(pygame.image.load('cat.png'), (40, 40))
player_r = pygame.transform.flip(pygame.transform.rotate(player, 90), True, False)
player_l = pygame.transform.flip(player_r, True, False)
dead = pygame.transform.scale(pygame.image.load('died_cat.jpg'), (40, 40))

last_block = 0


class Block(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load('block.png'), (10, 130))
    image2 = pygame.transform.flip(image, True, False)

    def __init__(self, group):
        global last_block
        super().__init__(group)
        self.rect = self.image.get_rect()
        if last_block:
            if 110 <= last_block.rect.x <= 150:
                self.image = Block.image2
                self.rect.x = 230
                a = random.randrange(60, 71, 10)
                self.rect.y = last_block.rect.y - a
            else:
                self.image = Block.image
                self.rect.x = 120
                self.rect.y = last_block.rect.y - 130
        self.curr = False
        self.start = False
        last_block = self

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
        self.player_x = 130
        self.player_y = 500
        self.image_dead = dead
        self.dead = False
        self.jump = False
        self.jump_counter = 0
        self.jump_1 = False
        self.jump_height = 100
        self.jump_width = 100
        self.curr_block = self.current_block()  # спрайт текущего блока
        self.direction = 'right'
        self.gravity_y = 15
        self.gravity_x = 2
        self.check_2_jump = False
        self.is_slip = False

    def check_fallen(self):  # кот коснулся предела окна
        return self.player_x > WIDTH or self.player_x < 0 or self.player_y + 40 > HEIGHT

    def check_fall(self):  # находится в падении
        return self.curr_block.rect[1] + platform_length < self.player_y + 20 and \
               (self.curr_block.rect[0] == self.player_x + 40 or self.curr_block.rect[0] == self.player_x - 10)

    def check_slip(self):
        if self.curr_block.rect.colliderect([self.player_x + 10, self.player_y, 40, 40]) or \
                self.curr_block.rect.colliderect([self.player_x - 10, self.player_y, 40,
                                                  40]) and not self.curr_block.start:
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
            if el.rect.colliderect([self.player_x, self.player_y, 40, 40]) and el.rect.x > WIDTH // 2 \
                    and not self.is_slip:
                el.curr = True
                self.curr_block = el
                self.player_x = el.rect.x - 40
                return True
            if el.rect.colliderect([self.player_x, self.player_y, 40, 40]) and el.rect.x < WIDTH // 2 \
                    and not self.is_slip:
                el.curr = True
                self.curr_block = el
                self.player_x = el.rect.x + 10
                return True

    def one_click(self):
        if cat.jump_counter == 1 and not self.check_2_jump:
            cat.gravity_y = 10
            self.gravity_x = -self.gravity_x
            self.check_2_jump = True
        if cat.jump:
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


def update_platforms():
    global t
    if cat.player_y < 400 and cat.gravity_y > 0 and cat.jump:
        for el in all_platforms:
            el.rect.y += cat.gravity_y
    else:
        pass
    for el in all_platforms:
        if el.rect.y + platform_length > 600:
            Block(all_platforms)


# create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('cat jump')
cat = Cat()
running = True
first_block = Block(all_platforms)
first_block.rect = pygame.Rect(120, 460, platform_width, platform_length)
first_block.rect.x = 120
first_block.rect.y = 460
last_block = first_block
first_block.start = True
for i in range(5):
    Block(all_platforms)
level_platforms = len(all_platforms)
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
        elif cat.curr_block.rect[1] > cat.player_y and cat.curr_block.rect[0] < WIDTH // 2 and cat.player_x + 20 \
                < cat.curr_block.rect[0]:
            cat.player_x = cat.curr_block.rect[0] + 10
            screen.blit(cat.image_r, (cat.player_x, cat.player_y))
        elif cat.curr_block.rect[1] > cat.player_y and cat.curr_block.rect[0] > WIDTH // 2 and \
                cat.player_x - 20 > cat.curr_block.rect[0] + 10:  # вернуться, когда будет длинный прыжок
            cat.player_x = cat.curr_block.rect[0] - 40
            screen.blit(cat.image_l, (cat.player_x, cat.player_y))
        elif cat.curr_block.rect[0] < WIDTH // 2:
            screen.blit(cat.image_r, (cat.player_x, cat.player_y))
        else:
            screen.blit(cat.image_l, (cat.player_x, cat.player_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not cat.check_fall():
                if cat.jump:
                    cat.jump_counter += 1
                else:
                    cat.gravity_y = 10
                    cat.gravity_x = 2
                    cat.jump_counter = 0
                    cat.jump_1 = True
                    cat.check_2_jump = False
            else:
                cat.jump = False

    if cat.check_collisions():
        cat.jump = False
        cat.jump_1 = False
        cat.is_slip = True
        cat.slip()

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
        # print(cat.gravity_y) изменить прыжок
        cat.one_click()

    update_platforms()

    pygame.display.flip()
pygame.quit()
