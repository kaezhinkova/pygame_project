import pygame

pygame.init()

# library of game const
white = (255, 255, 255)
black = (0, 0, 0)
gray = (120, 120, 120)
WIDTH = 400
HEIGHT = 600
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
        self.jump = False
        self.jump_1 = False
        self.jump_height = 100
        self.jump_width = 100
        self.curr_block = 0
        self.direction = 'right'
        self.gravity_y = 15
        self.gravity_x = 2

    def check_fall(self, x, y):
        return x > WIDTH or x < 0 or y > HEIGHT - 60

    def current_block(self, rect_list):
        for i in range(len(rect_list)):
            if rect_list[i].colliderect([self.player_x + 10, self.player_y, 40, 40]):
                return i
            if rect_list[i].colliderect([self.player_x - 10, self.player_y, 40, 40]):
                return i

    def check_collisions(self, rect_list, j):
        for i in range(len(rect_list)):
            if rect_list[i].colliderect([self.player_x, self.player_y, 40, 40]) and rect_list[self.curr_block][0] < self.player_x and i != self.curr_block:# platform left
                self.curr_block = i


                return True

            if rect_list[i].colliderect([self.player_x, self.player_y, 40, 40]) and rect_list[self.curr_block][0] > self.player_x and i != self.curr_block:
                self.curr_block = i
                self.player_x = rect_list[i][0] + 10
                return True

    def one_click(self, x_pos, y_pos):
        if cat.jump:
            y_pos -= self.gravity_y
            if platforms[self.curr_block][0] > x_pos:
                x_pos -= self.gravity_x
            else:
                x_pos += self.gravity_x
            self.gravity_y -= 1
            return x_pos, y_pos

    def slip(self):
        self.player_y += 0.3


fps = 60
flip = False
# font = pygame.font.Font('font1.tff', 16)
timer = pygame.time.Clock()

# game variables

platforms = [[100, 479, 10, 130], [200, 410, 10, 130], [100, 310, 10, 130], [200, 200, 10, 130]]

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
    if cat.check_fall(cat.player_x, cat.player_y):
        cat.jump = False
        screen.blit(cat.image_dead, (cat.player_x, cat.player_y))
    elif cat.jump:
        screen.blit(cat.image, (cat.player_x, cat.player_y))
    else:
        curr_block = cat.current_block(blocks)
        if blocks[curr_block][1] > cat.player_y:
            screen.blit(cat.image_r, (cat.player_x, cat.player_y))
        elif blocks[curr_block][0] <= cat.player_x:
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


    if cat.jump_1 and cat.jump and not cat.check_collisions(blocks, cat.curr_block) and not cat.check_fall(cat.player_x, cat.player_y):
        cat.player_x, cat.player_y = cat.one_click(cat.player_x, cat.player_y)
    if cat.check_collisions(blocks, cat.curr_block):
        cat.jump = False


    # player_x, player_y = update_player(player_x, player_y)

    pygame.display.flip()
pygame.quit()
