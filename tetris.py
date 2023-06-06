from time import perf_counter as clock
from random import choice as random
import json
import os
try:
    import pygame
except:
    print('Unable to import necessary package "pygame".')
    while True: pass
try:
    from bext import bg
except:
    bext = False
else:
    bext = True

filename = 'tetris highscore.json'
fps = 16
width = 10
height = 12
black = (0, 0, 0)
white = (255, 255, 255)
board = [[' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .'], [' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .'], [' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .'], [' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .'], [' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .'], [' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .'], [' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .'], [' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .'], [' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .'], [' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .'], [' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .'], [' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .', ' .']]
shapes = [[[0, -1], [0, 0], [0, 1], [0, 2]],
          [[0, 0], [1, 0], [0, 1], [1, 1]],
          [ [0, -1], [0, 0], [0, 1], [1, 1]],
          [[0, 1], [0, 0], [1, 0], [0, -1]],
          [[0, 0], [0, -1], [1, 0], [1, 1]],
          [[0, 0], [0, -1], [0, 1], [-1, 1]]]
colors = ('red', 'green', 'blue', 'magenta', 'yellow')

class Block(str):
    def init_color(self, color):
        self.color = color

def print_color(value):
    if bext:
        bg(getattr(value, 'color', 'reset'))
    print(value, end='')

def save_highscore():
    with open(filename, 'w') as file:
        json.dump(highscore, file)

try:
    with open(filename) as file: highscore = json.load(file)
except FileNotFoundError:
    highscore = 0
    save_highscore()

speed = 0.4
score = 0
shape = None
next_shape = random(shapes)
next_color = random(colors)
pygame.init()
screen = pygame.display.set_mode((900, 900))
pygame.display.set_caption('Tetris event detector')
icon = pygame.Surface((30, 30))
icon.fill(white)
icon_rect = icon.get_rect()
block = pygame.Rect(0, 0, 30, 10)
block.bottomleft = icon_rect.bottomleft
pygame.draw.rect(icon, (0, 0, 255), block)
block = pygame.Rect(0, 0, 10, 10)
block.midright = icon_rect.midright
pygame.draw.rect(icon, (0, 0, 255), block)
block = pygame.Rect(0, 0, 20, 20)
block.topleft = icon_rect.topleft
pygame.draw.rect(icon, (0, 255, 0), block)
pygame.display.set_icon(icon)
screen.fill(white)
font = pygame.font.SysFont(None, 50)
image = font.render("Mouse goes in here!! Click when you're ready.", True, black, white)
image_rect = image.get_rect()
image_rect.center = screen.get_rect().center
screen.blit(image, image_rect)
pygame.display.flip()
tick = pygame.time.Clock().tick
clicked = s = False
last_dropped = last_sped_up = clock()

def print_board():
    if os.name == 'nt:
        os.system('cls')
    else:
        os.system('clear')
    for y in range(height):
        if bext:
            bg('reset')
        print('([', end='')
        for x in range(width):
            printed_block = False
            try:
                for point in shape:
                    if [point[0] + shapex - 1, point[1] + shapey] == [x, y]:
                        if bext:
                            block = Block('  ')
                        else:
                            block = Block('##')
                        block.init_color(color)
                        print_color(block)
                        printed_block = True
            except:
                pass
            if not printed_block:
                if bext:
                    bg('reset')
                print_color(board[y][x])
        if bext:
            bg('reset')
        print('])')
    print(f"{' ' + '~~' * (width + 1)}\nScore: {score}\nHighscore: {highscore}\n([ .Next .])")
    for row in range(4):
        print('([', end='')
        for column in range(4):
            block = False
            for x, y in next_shape:
                if (y + 1, x + 1) == (row, column):
                    bg(next_color)
                    print('  ', end='')
                    bg('reset')
                    block = True
                    break
            if not block:
                print(' .', end='')
        print('])')
    print(' ' + '~' * 10)

while not clicked:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if x < 900 and x > 0 and y < 900 and y > 0:
                clicked = True
                break

while True:
    if shape is None:
        shape = next_shape[:]
        next_shape = random(shapes)[:]
        color = next_color
        next_color = random(colors)
        shapex = width // 2
        shapey = -1
        for x, y in shape:
            for row in range(width):
                for column in range(height):
                    if hasattr(board[column][row], 'color') and (x + shapex, y + shapey) == (row, column):
                        raise SystemExit
    for i, row in enumerate(board):
        all_blocks = True
        row_colors = []
        for string in row:
            if hasattr(string, 'color'):
                row_colors.append(string.color)
            if string == ' .':
                all_blocks = False
                break
        if all_blocks:
            score += 20 * width
            if score > highscore:
                highscore = score
                save_highscore()
            row.clear()
            for _ in range(width):
                row.append(' .')
            for i2, row in enumerate(board[:i]):
                board[i2 + 1] = row[:]
            print_board()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                raise SystemExit
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                try:
                    hit_wall = False
                    for x, y in shape:
                        if x + shapex == width:
                            hit_wall = True
                            break
                        for row in range(width):
                            for column in range(height):
                                if hasattr(board[column][row], 'color') and (x + shapex, y + shapey) == (row, column):
                                    hit_wall = True
                    if not hit_wall:
                        shapex += 1
                        print_board()
                except:
                    pass
            if event.key in (pygame.K_LEFT, pygame.K_a):
                try:
                    hit_wall = False
                    for x, y in shape:
                        if x + shapex == 1:
                            hit_wall = True
                            break
                        for row in range(width):
                            for column in range(height):
                                if hasattr(board[column][row], 'color') and (x + shapex - 2, y + shapey) == (row, column):
                                    hit_wall = True
                                    break
                    if not hit_wall:
                        shapex -= 1
                        print_board()
                except:
                    pass
            if event.key in (pygame.K_UP, pygame.K_w):
                test_shape = shape[:]
                collided = False
                for i, point in enumerate(test_shape):
                    x, y = point
                    test_shape[i] = y, -x
                    x, y = test_shape[i]
                    if x + shapex <= 0 or x + shapex - 1 >= width or y + shapey >= height:
                        collided = True
                    for row in range(width):
                        for column in range(height):
                            if hasattr(board[column][row], 'color') and (x + shapex - 1, y + shapey) == (row, column):
                                collided = True
                if not collided:
                    shape = test_shape[:]
                    print_board()
            if event.key in (pygame.K_DOWN, pygame.K_s):
                s = True
        if event.type == pygame.KEYUP and event.key in (pygame.K_DOWN, pygame.K_s):
            s = False
    if clock() - last_dropped >= speed or s:
        if clock() - last_dropped >= speed:
            last_dropped = clock()
        hit_floor = False
        for x, y in shape:
            if y + shapey == height - 1:
                hit_floor = True
                break
            for row in range(width):
                for column in range(height):
                    if hasattr(board[column][row], 'color') and (x + shapex - 1, y + shapey + 1) == (row, column):
                        hit_floor = True
                        break
        if not hit_floor:
            shapey += 1
            print_board()
        else:
            above = 0
            for x, y in shape:
                if y + shapey <= 0:
                    above += 1
                if bext:
                    block = Block('  ')
                else:
                    block = Block('##')
                block.init_color(color)
                try:
                    if not y + shapey < 0:
                        board[y + shapey][x + shapex - 1] = block
                except:
                    pass
            if above == 4:
                raise SystemExit
            shape = None
    if clock() - last_sped_up >= 50:
        last_sped_up = clock()
        speed -= 0.05
    tick(fps)
