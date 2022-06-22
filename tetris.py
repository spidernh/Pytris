import pygame
from random import randrange
from constants.rotation import TetrisRotation
from constants.board import TetrisBoard
from math import floor

WIDTH, HEIGHT = 780, 1000
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pytris")

BOARD_OFFSET = (50, 50)
TILE_SIZE = 45
BOARD_SIZE = (TILE_SIZE * 10, TILE_SIZE * 20)
NEXT_OFFSET = (BOARD_OFFSET[0] + BOARD_SIZE[0] + 50, BOARD_OFFSET[1])
NEXT_SIZE = (TILE_SIZE * 4, TILE_SIZE * 4)

FPS = 60

BACKGROUND_COLOR = (10, 10, 10)
GRID_COLOR = (30, 30, 30)
BORDER_COLOR = (200, 200, 200)
TEXT_COLOR = (230, 230, 230)

# Piece colors
COLOR_1 = (28, 207, 225) # I
COLOR_2 = (28, 40, 225) #  J
COLOR_3 = (224, 151, 13) # L
COLOR_4 = (224, 211, 13) # O
COLOR_5 = (29, 224, 13) #  S
COLOR_6 = (170, 13, 224) # T
COLOR_7 = (234, 25, 25) #  Z
PIECE_COLORS = [BACKGROUND_COLOR, COLOR_1, COLOR_2, COLOR_3, COLOR_4, COLOR_5, COLOR_6, COLOR_7]

board = TetrisBoard.board

LEVEL_SPEEDS = [48, 43, 38, 33, 28, 23, 18, 13, 8, 6, 5, 5, 5, 4, 4, 4, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]

score = 0
lines = 0
level = 1

piece_num = 0
last_piece_num = 0
next_piece_num = 0
piece_rotation = 0
piece_position = (0, 0)
piece_size = (0, 0)
piece_size_offset = (0, 0)
piece_array = [[0, 0],
                [0, 0]]

das_counter = 0
frames_since_last_drop = 0
frames_since_last_piece = 0

ccw_last_frame = False
cw_last_frame = False
left_last_frame = False
right_last_frame = False
spawn_last_frame = False
release_down_since_last_piece = True

run = True
wall_charged = False

def get_piece_array(rotation=piece_rotation, piece=piece_num):
    global piece_num
    global piece_rotation
    piece_array = 0
    if (piece == 0):
        piece_array = TetrisRotation.none
    elif (piece == 1):
        if (rotation == 0 or rotation == 2):
            piece_array = TetrisRotation.i_0
        elif (rotation == 1 or rotation == 3):
            piece_array = TetrisRotation.i_1
    elif (piece == 2):
        if (rotation == 0):
            piece_array = TetrisRotation.j_0
        elif (rotation == 1):
            piece_array = TetrisRotation.j_1
        elif (rotation == 2):
            piece_array = TetrisRotation.j_2
        elif (rotation == 3):
            piece_array = TetrisRotation.j_3
    elif (piece == 3):
        if (rotation == 0):
            piece_array = TetrisRotation.l_0
        elif (rotation == 1):
            piece_array = TetrisRotation.l_1
        elif (rotation == 2):
            piece_array = TetrisRotation.l_2
        elif (rotation == 3):
            piece_array = TetrisRotation.l_3
    elif (piece == 4):
        piece_array = TetrisRotation.o_0
    elif (piece == 5):
        if (rotation == 0 or rotation == 2):
            piece_array = TetrisRotation.s_0
        elif (rotation == 1 or rotation == 3):
            piece_array = TetrisRotation.s_1
    elif (piece == 6):
        if (rotation == 0):
            piece_array = TetrisRotation.t_0
        elif (rotation == 1):
            piece_array = TetrisRotation.t_1
        elif (rotation == 2):
            piece_array = TetrisRotation.t_2
        elif (rotation == 3):
            piece_array = TetrisRotation.t_3
    elif (piece == 7):
        if (rotation == 0 or rotation == 2):
            piece_array = TetrisRotation.z_0
        elif (rotation == 1 or rotation == 3):
            piece_array = TetrisRotation.z_1
    return piece_array

def draw_window():
    global piece_array, TEXT_COLOR, score, lines, level
    WINDOW.fill(BACKGROUND_COLOR)
    
    # Draw tiles
    for y in range(20):
        for x in range(10):
            if (board[y][x] == 0):
                continue
            pygame.draw.rect(WINDOW, PIECE_COLORS[board[y][x]], pygame.Rect(x * TILE_SIZE + BOARD_OFFSET[0], y * TILE_SIZE + BOARD_OFFSET[1], TILE_SIZE, TILE_SIZE))

    # Get current piece array
    
    # Draw current piece
    if (piece_num != 0):
        for y in range(len(piece_array)):
            if (y + piece_position[1] < 0):
                continue
            for x in range(len(piece_array[y])):
                if (piece_array[y][x] == 0):
                    continue
                pygame.draw.rect(WINDOW, PIECE_COLORS[piece_num], pygame.Rect(x * TILE_SIZE + piece_position[0] * TILE_SIZE + BOARD_OFFSET[0], y * TILE_SIZE + piece_position[1] * TILE_SIZE + BOARD_OFFSET[1], TILE_SIZE, TILE_SIZE))

    # Draw next piece
    piece_array = get_piece_array(rotation=0, piece=next_piece_num)
    x_offset = 0
    y_offset = 0
    if (len(piece_array[0]) == 2): x_offset = TILE_SIZE
    elif (len(piece_array[0]) == 3): x_offset = round(TILE_SIZE * 0.5)
    elif (len(piece_array[0]) == 4): x_offset = 0
    # if (len(piece_array) == 1): y_offset = round(TILE_SIZE * -3)
    if (len(piece_array) == 2): y_offset = TILE_SIZE
    elif (len(piece_array) == 4): y_offset = round(TILE_SIZE * -0.5)
    # if (next_piece_num == 4): y_offset = TILE_SIZE
    for y in range(len(piece_array)):
        for x in range(len(piece_array[y])):
            if (piece_array[y][x] == 0):
                continue
            pygame.draw.rect(WINDOW, PIECE_COLORS[next_piece_num], pygame.Rect(x * TILE_SIZE + NEXT_OFFSET[0] + x_offset, y * TILE_SIZE + NEXT_OFFSET[1] + y_offset, TILE_SIZE, TILE_SIZE))


    # Draw grid
    for x in range(11):
        pygame.draw.line(WINDOW, GRID_COLOR, (TILE_SIZE * x + BOARD_OFFSET[0], BOARD_OFFSET[1]), (TILE_SIZE * x + BOARD_OFFSET[0], BOARD_SIZE[1] + BOARD_OFFSET[1]), 2)
    for y in range(21):
        pygame.draw.line(WINDOW, GRID_COLOR, (BOARD_OFFSET[0], TILE_SIZE * y + BOARD_OFFSET[1]), (BOARD_SIZE[0] + BOARD_OFFSET[0], TILE_SIZE * y + BOARD_OFFSET[1]), 2)
    pygame.draw.rect(WINDOW, BORDER_COLOR, pygame.Rect(BOARD_OFFSET[0] - 1, BOARD_OFFSET[1] - 1, BOARD_SIZE[0] + 2, BOARD_SIZE[1] + 2), 4)
    pygame.draw.rect(WINDOW, BORDER_COLOR, pygame.Rect(NEXT_OFFSET[0] - 1, NEXT_OFFSET[1] - 1, NEXT_SIZE[0] + 2, NEXT_SIZE[1] + 2), 4)
    
    # Display statistics
    # 550-730 is our area
    # 180 px wide
    font_size = 48
    font = pygame.font.SysFont("impact", font_size)
    score_text = font.render("SCORE", True, TEXT_COLOR)
    score_disp = font.render(str(score), True, TEXT_COLOR)
    line_text = font.render("LINE", True, TEXT_COLOR)
    line_disp = font.render(str(lines), True, TEXT_COLOR)
    level_text = font.render("LEVEL", True, TEXT_COLOR)
    level_disp = font.render(str(level), True, TEXT_COLOR)
    WINDOW.blit(score_text, (NEXT_SIZE[0] / 2.0 - score_text.get_width() / 2.0 + NEXT_OFFSET[0], 10 + NEXT_OFFSET[1] + NEXT_SIZE[1]))
    WINDOW.blit(score_disp, (NEXT_SIZE[0] / 2.0 - score_disp.get_width() / 2.0 + NEXT_OFFSET[0], 10 + NEXT_OFFSET[1] + NEXT_SIZE[1] + font_size))
    WINDOW.blit(line_text, (NEXT_SIZE[0] / 2.0 - line_text.get_width() / 2.0 + NEXT_OFFSET[0], 30 + NEXT_OFFSET[1] + NEXT_SIZE[1] + 2 * font_size))
    WINDOW.blit(line_disp, (NEXT_SIZE[0] / 2.0 - line_disp.get_width() / 2.0 + NEXT_OFFSET[0], 30 + NEXT_OFFSET[1] + NEXT_SIZE[1] + 3 * font_size))
    WINDOW.blit(level_text, (NEXT_SIZE[0] / 2.0 - level_text.get_width() / 2.0 + NEXT_OFFSET[0], 50 + NEXT_OFFSET[1] + NEXT_SIZE[1] + 4 * font_size))
    WINDOW.blit(level_disp, (NEXT_SIZE[0] / 2.0 - level_disp.get_width() / 2.0 + NEXT_OFFSET[0], 50 + NEXT_OFFSET[1] + NEXT_SIZE[1] + 5 * font_size))

    pygame.display.update()


def spawn_piece(piece_index: int):
    global piece_num, piece_rotation, piece_position, run
    # print("Spawning piece #" + str(piece_index))
    if (piece_index == 1):
        piece_num = 1
        piece_rotation = 0
        piece_position = (3, -2)
    if (piece_index == 2):
        piece_num = 2
        piece_rotation = 0
        piece_position = (4, -1)
    if (piece_index == 3):
        piece_num = 3
        piece_rotation = 0
        piece_position = (4, -1)
    if (piece_index == 4):
        piece_num = 4
        piece_rotation = 0
        piece_position = (4, 0)
    if (piece_index == 5):
        piece_num = 5
        piece_rotation = 0
        piece_position = (4, -1)
    if (piece_index == 6):
        piece_num = 6
        piece_rotation = 0
        piece_position = (4, -1)
    if (piece_index == 7):
        piece_num = 7
        piece_rotation = 0
        piece_position = (4, -1)
    if (check_if_piece_collides(piece_position, piece_rotation)):
        run = False

def clear_lines(line_indices):
    # Start at that line, make it the line above
    # Go to the next line, same thing
    # line_index = 0
    # line_indices[line_index] = 19
    # go to line 19, 18, 17, 16 ... 2, 1, set 0 to all 0s
    # 0  -> 19
    # 1  -> 18
    # 2  -> 17
    # 3  -> 16
    # 4  -> 15
    # 5  -> 14
    # 6  -> 13
    # 7  -> 12
    # 8  -> 11
    # 9  -> 10
    # 10 -> 9
    # 11 -> 8
    # 12 -> 7
    # 13 -> 6
    # 14 -> 5
    # 15 -> 4
    # 16 -> 3
    # 17 -> 2
    # 18 -> 1
    # 19 -> 0
    for line_index in range(len(line_indices)):
        for line in range(line_indices[line_index] + 1):
            # line_index - line
            for x in range(len(board[0])):
                if (line_indices[line_index] - line == 0):
                    board[0][x] = 0
                else:
                    board[line_indices[line_index] - line][x] = board[line_indices[line_index] - line - 1][x]

def get_piece_size():
    global piece_size, piece_size_offset
    if (piece_num == 1):
        if (piece_rotation == 0 or piece_rotation == 2):
            piece_size = (4, 1)
            piece_size_offset = (0, 2)
        elif (piece_rotation == 1 or piece_rotation == 3):
            piece_size_offset = (2, 0)
            piece_size = (1, 4)
    if (piece_num == 2 or piece_num == 3 or piece_num == 6):
        if (piece_rotation == 0):
            piece_size = (3, 2)
            piece_size_offset = (0, 1)
        elif (piece_rotation == 1):
            piece_size = (2, 3)
            piece_size_offset = (0, 0)
        elif (piece_rotation == 2):
            piece_size = (3, 2)
            piece_size_offset = (0, 0)
        elif (piece_rotation == 3):
            piece_size = (2, 3)
            piece_size_offset = (1, 0)
    if (piece_num == 4):
        piece_size = (2, 2)
        piece_size_offset = (0, 0)
    if (piece_num == 5 or piece_num == 7):
        if (piece_rotation == 0 or piece_rotation == 2):
            piece_size = (3, 2)
            piece_size_offset = (0, 1)
        elif (piece_rotation == 1 or piece_rotation == 3):
            piece_size = (2, 3)
            piece_size_offset = (1, 0)

def imprint_piece():
    global frames_since_last_piece, piece_num, release_down_since_last_piece, last_piece_num, piece_array, piece_rotation

    piece_array = get_piece_array(rotation=piece_rotation, piece=piece_num)
    for y in range(len(piece_array)):
        if (y + piece_position[1] < 0 or y + piece_position[1] > 19):
            continue
        for x in range(len(piece_array[0])):
            if (x + piece_position[0] < 0 or x + piece_position[0] > 9 or piece_array[y][x] == 0):
                continue
            board[y + piece_position[1]][x + piece_position[0]] = piece_array[y][x]

    # print("Im imprinted")
    frames_since_last_piece = 0
    last_piece_num = piece_num
    piece_num = 0
    release_down_since_last_piece = False

def check_if_piece_collides(position: tuple, rotation: int):
    piece_array = get_piece_array(rotation=rotation, piece=piece_num)
    for y in range(len(piece_array)):
        for x in range(len(piece_array[y])):
            if (y + position[1] > 19 or x + position[0] < 0 or x + position[0] > 9):
                if (piece_array[y][x] != 0):
                    return True
            elif (y + position[1] < 0):
                continue
            if (piece_array[y][x] != 0 and board[y + position[1]][x + position[0]] != 0):
                return True
    return False

def attempt_transform_piece(translation: tuple, rotation: int):
    global piece_position, piece_rotation, piece_array, das_counter, wall_charged
    if (piece_num == 0): pass

    # Horizontal Translation
    hoz_trans = (piece_position[0] + translation[0], piece_position[1])
    if (check_if_piece_collides(hoz_trans, piece_rotation)):
        das_counter = 16
        wall_charged = True
    else:
        piece_position = (hoz_trans[0], piece_position[1])
        wall_charged = False
    # print("DAS: " + str(das_counter))
    
    # Rotation
    rot = rotation + piece_rotation
    if (rot > 3):
        rot = 0
    if (rot < 0):
        rot = 3
    # print("current: " + str(piece_rotation))
    # print("new    : " + str(rot))
    if (not check_if_piece_collides(piece_position, rot)):
        piece_rotation = rot
    else:
        # print("ROTATION FAILED")
        pass
    
    # Vertical Translation
    vert_trans = (piece_position[0], piece_position[1] + translation[1])
    if (check_if_piece_collides(vert_trans, piece_rotation)):
        imprint_piece()
    else:
        piece_position = (piece_position[0], vert_trans[1])

def generate_piece(previous: int):
    random = randrange(7) + 1
    if (random == previous):
        random = randrange(7) + 1
    return random

def main():
    global lines, level, score
    global piece_num, piece_rotation, piece_position, last_piece_num, piece_array, next_piece_num
    global ccw_last_frame, cw_last_frame, left_last_frame, right_last_frame, spawn_last_frame, release_down_since_last_piece
    global das_counter, frames_since_last_drop, frames_since_last_piece, run, wall_charged
    pygame.init()
    clock = pygame.time.Clock()
    run = True
    while (run):
        clock.tick(FPS)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                run = False
        keys_pressed = pygame.key.get_pressed()

        if (keys_pressed[pygame.K_c] and not spawn_last_frame):
            spawn_piece(next_piece_num)
            next_piece_num = generate_piece(next_piece_num)
            continue

        if (piece_num == 0):
            if (frames_since_last_piece < 6):
                frames_since_last_piece += 1
                continue
            else:
                spawn_piece(next_piece_num)
                next_piece_num = generate_piece(next_piece_num)
                continue

        if (keys_pressed[pygame.K_z] and not ccw_last_frame):
            attempt_transform_piece((0, 0), -1)
        if (keys_pressed[pygame.K_x] and not cw_last_frame):
            attempt_transform_piece((0, 0), 1)
        
        if (keys_pressed[pygame.K_LEFT]):
            if (left_last_frame):
                das_counter += 1
            else:
                das_counter = 0
                attempt_transform_piece((-1, 0), 0)
        if (keys_pressed[pygame.K_RIGHT]):
            if (right_last_frame):
                das_counter += 1
            else:
                das_counter = 0
                attempt_transform_piece((1, 0), 0)
        if (das_counter >= 16):
            if (keys_pressed[pygame.K_LEFT]):
                das_counter = 10
                attempt_transform_piece((-1, 0), 0)
            if (keys_pressed[pygame.K_RIGHT]):
                das_counter = 10
                attempt_transform_piece((1, 0), 0)
        if (das_counter > 16):
            das_counter = 16
        
        frames_since_last_drop += 1
        if (frames_since_last_drop >= LEVEL_SPEEDS[level] or frames_since_last_drop >= 2 and keys_pressed[pygame.K_DOWN] and release_down_since_last_piece):
            attempt_transform_piece((0, 1), 0)
            frames_since_last_drop = 0

        piece_array = get_piece_array(rotation=piece_rotation, piece=piece_num)
        
        line_count = 0
        for y in board:
            full = True
            for x in y:
                if (x == 0):
                    full = False
                    break
            if (full):
                line_count += 1
        if (line_count != 0):
            line_list = [None] * line_count
            for y in range(len(board)):
                full = True
                for x in board[y]:
                    if (x == 0):
                        full = False
                        break
                if (full):
                    for i in range(len(line_list)):
                        if (line_list[i] == None):
                            line_list[i] = y
                            break
            clear_lines(line_list)
            lines += line_count
            if (line_count == 1):
                score += (40 * (level + 1))
            elif (line_count == 2):
                score += (100 * (level + 1))
            elif (line_count == 3):
                score += (300 * (level + 1))
            elif (line_count == 4):
                score += (1200 * (level + 1))
            else:
                print("WHAT THE HECK HOW DID YOU CLEAR MORE THAN FOUR OR LESS THAN ZERO LINES?????")
            if (floor(lines / 10.0) > level):
                level = floor(lines / 10.0)

        get_piece_size()
        
        ccw_last_frame = keys_pressed[pygame.K_z]
        cw_last_frame = keys_pressed[pygame.K_x]
        left_last_frame = keys_pressed[pygame.K_LEFT]
        right_last_frame = keys_pressed[pygame.K_RIGHT]
        spawn_last_frame = keys_pressed[pygame.K_c]
        release_down_since_last_piece = (not keys_pressed[pygame.K_DOWN]) or release_down_since_last_piece
        
        piece_array = get_piece_array(rotation=piece_rotation, piece=piece_num)
        draw_window()
    pygame.quit()

    # Prints
    print("Lines: " + str(lines))
    print("Score: " + str(score))
    print("Level: " + str(level))

if (__name__ == "__main__"):
    main()