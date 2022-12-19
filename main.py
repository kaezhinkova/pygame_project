import pygame

pygame.init()

# library of game const
white = (255, 255, 255)
black = (0, 0, 0)
gray = (120, 120, 120)
WIDTH = 400
HEIGHT = 600
platform_length = 130
platform_width = 10
background = white
player = pygame.transform.scale(pygame.image.load('cat.png'), (40, 40))
player_r = pygame.transform.flip(pygame.transform.rotate(player, 90), True, False)
player_l = pygame.transform.flip(player_r, True, False)
dead = pygame.transform.scale(pygame.image.load('died_cat.jpg'), (40, 40))


class Cat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player
        self.image_r = player_r
        self.image_l = player_l
        self.player_x = 110
        self.player_y = 500
        self.image_dead = dead
        self.dead = False
        self.jump = False
        self.jump_1 = False
        self.jump_height = 100
        self.jump_width = 100
        self.curr_block = 0
        self.direction = 'right'
        self.gravity_y = 15
        self.gravity_x = 2

    def check_fallen(self):  # кот коснулся предела окна
        return self.player_x > WIDTH or self.player_x < 0 or self.player_y> HEIGHT - 40

    def check_fall(self, rect_list):  # находится в падении
        return rect_list[self.curr_block][1] + platform_length < self.player_y

    def current_block(self, rect_list):  # текущая платформа
        for i in range(len(rect_list)):
            if rect_list[i].colliderect([self.player_x + 10, self.player_y, 40, 40]):
                return i
            if rect_list[i].colliderect([self.player_x - 10, self.player_y, 40, 40]):
                return i

    def check_collisions(self, rect_list, j):
        for i in range(len(rect_list)):
            if rect_list[i].colliderect([self.player_x, self.player_y, 40, 40]) and rect_list[self.curr_block][0] \
                    < self.player_x and i != self.curr_block:  # platform left # под вопросм при возвращении
                self.curr_block = i
                return True

            if rect_list[i].colliderect([self.player_x, self.player_y, 40, 40]) and rect_list[self.curr_block][
                0] > self.player_x and i != self.curr_block:
                self.curr_block = i
                self.player_x = rect_list[i][0] + 10
                return True

    def one_click(self):
        if cat.jump:
            self.player_y -= self.gravity_y
            if platforms[self.curr_block][0] > self.player_x:
                self.player_x -= self.gravity_x
            else:
                self.player_x += self.gravity_x
            self.gravity_y -= 1


    def slip(self):
        self.player_y += 0.2

    def fall(self):
        self.player_y += 1


fps = 60
flip = False
# font = pygame.font.Font('font1.tff', 16)
timer = pygame.time.Clock()

# game variables

platforms = [[100, 460, platform_width, platform_length], [200, 410, platform_width, platform_length],
             [100, 270, platform_width, platform_length], [200, 200, platform_width, platform_length]]

v = 50

# create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('cat jump')
cat = Cat()
running = True
while running:
    timer.tick(fps)
    screen.fill(background)
    blocks = []
    for i in range(len(platforms)):
        block = pygame.draw.rect(screen, black, platforms[i], 0, 2)
        blocks.append(block)
    if cat.check_fallen():
        cat.jump = False
        cat.dead = True
        screen.blit(cat.image_dead, (cat.player_x, cat.player_y))
    elif cat.jump or cat.current_block(blocks) is None:
        screen.blit(cat.image, (cat.player_x, cat.player_y))
    else:
        cat.curr_block = cat.current_block(blocks)
        if blocks[cat.curr_block][1] > cat.player_y and blocks[cat.curr_block][0] <= cat.player_x:
            cat.player_x = blocks[cat.curr_block][0] + 10
            screen.blit(cat.image_r, (cat.player_x, cat.player_y))
        elif blocks[cat.curr_block][1] > cat.player_y and blocks[cat.curr_block][0] >= cat.player_x:
            cat.player_x = blocks[cat.curr_block][0] - 40
            screen.blit(cat.image_l, (cat.player_x, cat.player_y))
        elif blocks[cat.curr_block][0] <= cat.player_x:
            screen.blit(cat.image_r, (cat.player_x, cat.player_y))
        else:
            screen.blit(cat.image_l, (cat.player_x, cat.player_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            cat.gravity_y = 15
            cat.gravity_x = 2
            cat.jump = True
            cat.jump_1 = True

    if cat.jump_1 and cat.jump and not cat.check_collisions(blocks, cat.curr_block) and not cat.check_fallen():
        cat.one_click()
    if cat.check_collisions(blocks, cat.curr_block):
        cat.jump = False

    if not cat.jump and not cat.check_fall(blocks) and cat.curr_block != 0:
        cat.slip()
    elif cat.check_fall(blocks) and not cat.dead:
        cat.fall()

    pygame.display.flip()
pygame.quit()
