"""
Snake Eater - LAN Multiplayer
Player 1 / Host
Made with PyGame
"""

import pygame
import sys
import time
import random
import socket
import threading
import pickle


# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 25
boi

# Network settings
HOST = '0.0.0.0'
PORT = 5555


# Window size
frame_size_x = 720
frame_size_y = 480


# Checks for errors encountered
check_errors = pygame.init()

if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Initialise game window
pygame.display.set_caption('Snake Eater - LAN - Player 1')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# FPS controller
fps_controller = pygame.time.Clock()


# =========================================================
# NETWORK
# =========================================================

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(1)

print()
print('====================================')
print('       SNAKE EATER - LAN HOST')
print('====================================')
print(f'Puerto: {PORT}')
print('Esperando al Player 2...')
print()

client_socket, client_address = server.accept()

print(f'[+] Player 2 conectado desde: {client_address}')
print()


# =========================================================
# VARIABLES DE RED
# =========================================================

player_2_connected = True

player_2_command = 'LEFT'

network_lock = threading.Lock()


# =========================================================
# RECIBIR DATOS DEL PLAYER 2
# =========================================================

def receive_player_2():

    global player_2_command
    global player_2_connected

    buffer = b''

    while player_2_connected:

        try:

            data = client_socket.recv(1024)

            if not data:
                player_2_connected = False
                break

            buffer += data

            while b'\n' in buffer:

                message, buffer = buffer.split(b'\n', 1)

                command = message.decode().strip()

                if command in ['UP', 'DOWN', 'LEFT', 'RIGHT']:

                    with network_lock:
                        player_2_command = command

        except:

            player_2_connected = False
            break


# =========================================================
# INICIAR HILO DE RED
# =========================================================

network_thread = threading.Thread(
    target=receive_player_2,
    daemon=True
)

network_thread.start()


# =========================================================
# GAME VARIABLES
# =========================================================

# Player 1
snake_pos_1 = [100, 50]

snake_body_1 = [
    [100, 50],
    [90, 50],
    [80, 50]
]

direction_1 = 'RIGHT'
change_to_1 = direction_1

score_1 = 0


# Player 2
snake_pos_2 = [600, 400]

snake_body_2 = [
    [600, 400],
    [610, 400],
    [620, 400]
]

direction_2 = 'LEFT'
change_to_2 = direction_2

score_2 = 0


# Food
food_pos = [
    random.randrange(1, frame_size_x // 10) * 10,
    random.randrange(1, frame_size_y // 10) * 10
]

food_spawn = True


# =========================================================
# RESET GAME
# =========================================================

def reset_game():

    global snake_pos_1
    global snake_body_1
    global direction_1
    global change_to_1
    global score_1

    global snake_pos_2
    global snake_body_2
    global direction_2
    global change_to_2
    global score_2

    global food_pos
    global food_spawn

    # Player 1
    snake_pos_1 = [100, 50]

    snake_body_1 = [
        [100, 50],
        [90, 50],
        [80, 50]
    ]

    direction_1 = 'RIGHT'
    change_to_1 = direction_1
    score_1 = 0


    # Player 2
    snake_pos_2 = [600, 400]

    snake_body_2 = [
        [600, 400],
        [610, 400],
        [620, 400]
    ]

    direction_2 = 'LEFT'
    change_to_2 = direction_2
    score_2 = 0


    # New food
    food_pos = [
        random.randrange(1, frame_size_x // 10) * 10,
        random.randrange(1, frame_size_y // 10) * 10
    ]

    food_spawn = True


# =========================================================
# SCORE
# =========================================================

def show_score(choice, color, font, size):

    score_font = pygame.font.SysFont(font, size)

    if choice == 1:

        score_surface = score_font.render(
            'Player 1 Score : ' + str(score_1),
            True,
            color
        )

        score_rect = score_surface.get_rect()

        score_rect.midtop = (
            frame_size_x / 10,
            15
        )


    elif choice == 2:

        score_surface = score_font.render(
            'Player 2 Score : ' + str(score_2),
            True,
            color
        )

        score_rect = score_surface.get_rect()

        score_rect.midtop = (
            frame_size_x - frame_size_x / 10,
            15
        )


    else:

        score_surface = score_font.render(
            'Player 1: ' + str(score_1) +
            '    Player 2: ' + str(score_2),
            True,
            color
        )

        score_rect = score_surface.get_rect()

        score_rect.midtop = (
            frame_size_x / 2,
            frame_size_y / 1.25
        )

    game_window.blit(score_surface, score_rect)


# =========================================================
# GAME OVER
# =========================================================

def game_over(winner):

    my_font = pygame.font.SysFont(
        'times new roman',
        70
    )

    if winner == 1:

        message = 'PLAYER 1 WINS!'
        color = green

    elif winner == 2:

        message = 'PLAYER 2 WINS!'
        color = blue

    else:

        message = 'DRAW!'
        color = red


    game_over_surface = my_font.render(
        message,
        True,
        color
    )

    game_over_rect = game_over_surface.get_rect()

    game_over_rect.midtop = (
        frame_size_x / 2,
        frame_size_y / 4
    )


    game_window.fill(black)

    game_window.blit(
        game_over_surface,
        game_over_rect
    )

    show_score(
        0,
        white,
        'times',
        20
    )

    pygame.display.flip()

    time.sleep(3)

    reset_game()


# =========================================================
# SEND GAME STATE TO PLAYER 2
# =========================================================

def send_game_state():

    game_state = {

        'snake_body_1': snake_body_1,

        'snake_body_2': snake_body_2,

        'food_pos': food_pos,

        'score_1': score_1,

        'score_2': score_2

    }

    try:

        data = pickle.dumps(game_state)

        client_socket.sendall(
            len(data).to_bytes(4, 'big') + data
        )

    except:

        pass


# =========================================================
# MAIN LOGIC
# =========================================================

while True:

    # =====================================================
    # EVENTS
    # =====================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()

            try:
                client_socket.close()
                server.close()
            except:
                pass

            sys.exit()


        elif event.type == pygame.KEYDOWN:

            # Player 1
            # Arrow Up
            if event.key == pygame.K_UP:
                change_to_1 = 'UP'

            # Arrow Down
            if event.key == pygame.K_DOWN:
                change_to_1 = 'DOWN'

            # Arrow Left
            if event.key == pygame.K_LEFT:
                change_to_1 = 'LEFT'

            # Arrow Right
            if event.key == pygame.K_RIGHT:
                change_to_1 = 'RIGHT'


            # ESC
            if event.key == pygame.K_ESCAPE:

                pygame.event.post(
                    pygame.event.Event(pygame.QUIT)
                )


    # =====================================================
    # PLAYER 1 DIRECTION
    # =====================================================

    if change_to_1 == 'UP' and direction_1 != 'DOWN':
        direction_1 = 'UP'

    if change_to_1 == 'DOWN' and direction_1 != 'UP':
        direction_1 = 'DOWN'

    if change_to_1 == 'LEFT' and direction_1 != 'RIGHT':
        direction_1 = 'LEFT'

    if change_to_1 == 'RIGHT' and direction_1 != 'LEFT':
        direction_1 = 'RIGHT'


    # =====================================================
    # PLAYER 2 DIRECTION
    # =====================================================

    with network_lock:

        change_to_2 = player_2_command


    if change_to_2 == 'UP' and direction_2 != 'DOWN':
        direction_2 = 'UP'

    if change_to_2 == 'DOWN' and direction_2 != 'UP':
        direction_2 = 'DOWN'

    if change_to_2 == 'LEFT' and direction_2 != 'RIGHT':
        direction_2 = 'LEFT'

    if change_to_2 == 'RIGHT' and direction_2 != 'LEFT':
        direction_2 = 'RIGHT'


    # =====================================================
    # MOVE PLAYER 1
    # =====================================================

    if direction_1 == 'UP':
        snake_pos_1[1] -= 10

    if direction_1 == 'DOWN':
        snake_pos_1[1] += 10

    if direction_1 == 'LEFT':
        snake_pos_1[0] -= 10

    if direction_1 == 'RIGHT':
        snake_pos_1[0] += 10


    # =====================================================
    # MOVE PLAYER 2
    # =====================================================

    if direction_2 == 'UP':
        snake_pos_2[1] -= 10

    if direction_2 == 'DOWN':
        snake_pos_2[1] += 10

    if direction_2 == 'LEFT':
        snake_pos_2[0] -= 10

    if direction_2 == 'RIGHT':
        snake_pos_2[0] += 10


    # =====================================================
    # PLAYER 1 BODY
    # =====================================================

    snake_body_1.insert(
        0,
        list(snake_pos_1)
    )


    if (
        snake_pos_1[0] == food_pos[0]
        and
        snake_pos_1[1] == food_pos[1]
    ):

        score_1 += 1

        food_spawn = False

    else:

        snake_body_1.pop()


    # =====================================================
    # PLAYER 2 BODY
    # =====================================================

    snake_body_2.insert(
        0,
        list(snake_pos_2)
    )


    if (
        snake_pos_2[0] == food_pos[0]
        and
        snake_pos_2[1] == food_pos[1]
    ):

        score_2 += 1

        food_spawn = False

    else:

        snake_body_2.pop()


    # =====================================================
    # SPAWN FOOD
    # =====================================================

    if not food_spawn:

        food_pos = [
            random.randrange(
                1,
                frame_size_x // 10
            ) * 10,

            random.randrange(
                1,
                frame_size_y // 10
            ) * 10
        ]

    food_spawn = True


    # =====================================================
    # GRAPHICS
    # =====================================================

    game_window.fill(black)


    # Player 1
    for pos in snake_body_1:

        pygame.draw.rect(
            game_window,
            green,
            pygame.Rect(
                pos[0],
                pos[1],
                10,
                10
            )
        )


    # Player 2
    for pos in snake_body_2:

        pygame.draw.rect(
            game_window,
            blue,
            pygame.Rect(
                pos[0],
                pos[1],
                10,
                10
            )
        )


    # Food
    pygame.draw.rect(
        game_window,
        white,
        pygame.Rect(
            food_pos[0],
            food_pos[1],
            10,
            10
        )
    )


    # =====================================================
    # COLLISIONS
    # =====================================================

    # Player 1 - walls
    if snake_pos_1[0] < 0 or snake_pos_1[0] > frame_size_x - 10:

        game_over(2)

        continue


    if snake_pos_1[1] < 0 or snake_pos_1[1] > frame_size_y - 10:

        game_over(2)

        continue


    # Player 2 - walls
    if snake_pos_2[0] < 0 or snake_pos_2[0] > frame_size_x - 10:

        game_over(1)

        continue


    if snake_pos_2[1] < 0 or snake_pos_2[1] > frame_size_y - 10:

        game_over(1)

        continue


    # Player 1 - own body
    for block in snake_body_1[1:]:

        if (
            snake_pos_1[0] == block[0]
            and
            snake_pos_1[1] == block[1]
        ):

            game_over(2)

            break


    # Player 2 - own body
    for block in snake_body_2[1:]:

        if (
            snake_pos_2[0] == block[0]
            and
            snake_pos_2[1] == block[1]
        ):

            game_over(1)

            break


    # Player 1 hits Player 2
    for block in snake_body_2:

        if (
            snake_pos_1[0] == block[0]
            and
            snake_pos_1[1] == block[1]
        ):

            game_over(2)

            break


    # Player 2 hits Player 1
    for block in snake_body_1:

        if (
            snake_pos_2[0] == block[0]
            and
            snake_pos_2[1] == block[1]
        ):

            game_over(1)

            break


    # =====================================================
    # SCORES
    # =====================================================

    show_score(
        1,
        green,
        'consolas',
        20
    )

    show_score(
        2,
        blue,
        'consolas',
        20
    )


    # =====================================================
    # SEND GAME STATE
    # =====================================================

    send_game_state()


    # =====================================================
    # REFRESH
    # =====================================================

    pygame.display.update()

    fps_controller.tick(difficulty)