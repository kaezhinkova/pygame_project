import pygame

pygame.init()

# library of game const
white = (255, 255, 255)
black = (0, 0, 0)
gray = (120, 120, 120)
WIDTH = 400
HEIGHT = 500
background = white

player = pygame.transform.scale(pygame.image.load('cat.png'), (50, 40))
player_r = pygame.transform.flip(pygame.transform.rotate(player, 90), True, False)
player_l = pygame.transform.flip(player_r, True, False)
fps = 60
flip = False
# font = pygame.font.Font('font1.tff', 16)
timer = pygame.time.Clock()

# game variables
player_x = 110
player_y = 400
platforms = [[100, 370, 10, 100], [200, 310, 10, 100], [100, 240, 10, 100], [200, 100, 10, 100]]
jump = False
jump_1 = False
v = 50
jump_height = 100
jump_width = 100
curr_block = 0
direction = 'right'
# create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('cat jump')


def check_fall(x, y):
    return x > WIDTH or x < 0 or y > HEIGHT - 60


def current_block(rect_list):
    global player_x
    global player_y
    for i in range(len(rect_list)):
        if rect_list[i].colliderect([player_x + 10, player_y, 50, 40]):
            return i
        if rect_list[i].colliderect([player_x - 10, player_y, 50, 40]):
            return i


def check_collisions(rect_list, j):
    global player_x
    global player_y
    global player
    for i in range(len(rect_list)):
        if rect_list[i].colliderect([player_x - 10, player_y, 50, 40]) and i != j and platforms[j][
            0] < player_x:  # platform left
            return True

        if rect_list[i].colliderect([player_x, player_y, 50, 40]) and i != j and platforms[j][0] > player_x:
            return True



# update player y pos
def one_click(x_pos, y_pos, curr_block):
    global gravity_y
    if jump:
        y_pos -= gravity_y
        if platforms[curr_block][0] > x_pos:
            x_pos -= gravity_x
        else:
            x_pos += gravity_x
        gravity_y -= 1
        return x_pos, y_pos


running = True
while running:
    timer.tick(fps)
    screen.fill(background)

    blocks = []

    for i in range(len(platforms)):
        block = pygame.draw.rect(screen, black, platforms[i], 0, 2)
        blocks.append(block)

    if jump:
        screen.blit(player, (player_x, player_y))
    else:
        curr_block = current_block(blocks)
        if blocks[curr_block][0] <= player_x:
            screen.blit(player_r, (player_x, player_y))
        else:
            screen.blit(player_l, (player_x, player_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            gravity_y = 15
            gravity_x = 2
            jump = True
            jump_1 = True
            curr_block = current_block(blocks)

    if check_fall(player_x, player_y):
        jump = False
    if jump_1 and jump:
        player_x, player_y = one_click(player_x, player_y, curr_block)
    if check_collisions(blocks, curr_block):
        jump = False

    # player_x, player_y = update_player(player_x, player_y)

    pygame.display.flip()
pygame.quit()
