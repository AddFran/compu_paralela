"""
Snake Eater - LAN Multiplayer
Player 2 / Client
Made with PyGame
"""

import pygame
import sys
import socket
import pickle


# =========================================================
# NETWORK SETTINGS
# =========================================================

# CAMBIA ESTA IP POR LA IP DEL PLAYER 1
SERVER_IP = '192.168.1.4'

SERVER_PORT = 5555


# =========================================================
# WINDOW
# =========================================================

frame_size_x = 720
frame_size_y = 480


# =========================================================
# PYGAME
# =========================================================

check_errors = pygame.init()

if check_errors[1] > 0:

    print(
        f'[!] Had {check_errors[1]} errors when initialising game, exiting...'
    )

    sys.exit(-1)

else:

    print('[+] Game successfully initialised')


pygame.display.set_caption(
    'Snake Eater - LAN - Player 2'
)

game_window = pygame.display.set_mode(
    (frame_size_x, frame_size_y)
)


# =========================================================
# COLORS
# =========================================================

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# =========================================================
# FPS
# =========================================================

fps_controller = pygame.time.Clock()


# =========================================================
# CONNECT TO SERVER
# =========================================================

client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

print()
print('====================================')
print('       SNAKE EATER - PLAYER 2')
print('====================================')
print()
print(f'Conectando a {SERVER_IP}:{SERVER_PORT}...')


try:

    client_socket.connect(
        (SERVER_IP, SERVER_PORT)
    )

except:

    print()
    print('[!] No se pudo conectar al servidor.')
    print()
    print('Comprueba:')
    print('1. Que Player 1 haya iniciado el servidor.')
    print('2. Que la IP sea correcta.')
    print('3. Que ambos esten en la misma red.')
    print('4. Que el firewall permita Python.')
    print()

    sys.exit()


print('[+] Conectado al Player 1!')
print()
print('Controles:')
print('W = Arriba')
print('S = Abajo')
print('A = Izquierda')
print('D = Derecha')
print()


# =========================================================
# GAME VARIABLES
# =========================================================

snake_body_1 = []

snake_body_2 = []

food_pos = [0, 0]

score_1 = 0

score_2 = 0


# =========================================================
# RECEIVE GAME STATE
# =========================================================

def receive_game_state():

    global snake_body_1
    global snake_body_2
    global food_pos
    global score_1
    global score_2

    try:

        # Primero recibimos 4 bytes
        # que indican el tamaño del paquete

        header = b''

        while len(header) < 4:

            data = client_socket.recv(
                4 - len(header)
            )

            if not data:
                return False

            header += data


        data_size = int.from_bytes(
            header,
            'big'
        )


        # Ahora recibimos el paquete completo

        data = b''

        while len(data) < data_size:

            packet = client_socket.recv(
                min(
                    4096,
                    data_size - len(data)
                )
            )

            if not packet:
                return False

            data += packet


        # Convertimos los datos

        game_state = pickle.loads(data)


        snake_body_1 = game_state[
            'snake_body_1'
        ]

        snake_body_2 = game_state[
            'snake_body_2'
        ]

        food_pos = game_state[
            'food_pos'
        ]

        score_1 = game_state[
            'score_1'
        ]

        score_2 = game_state[
            'score_2'
        ]

        return True


    except:

        return False


# =========================================================
# SEND MOVEMENT
# =========================================================

def send_command(command):

    try:

        message = command + '\n'

        client_socket.sendall(
            message.encode()
        )

    except:

        pygame.quit()
        sys.exit()


# =========================================================
# SCORE
# =========================================================

def show_score(
    choice,
    color,
    font,
    size
):

    score_font = pygame.font.SysFont(
        font,
        size
    )


    if choice == 1:

        score_surface = score_font.render(
            'Player 1 Score : ' +
            str(score_1),
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
            'Player 2 Score : ' +
            str(score_2),
            True,
            color
        )

        score_rect = score_surface.get_rect()

        score_rect.midtop = (
            frame_size_x -
            frame_size_x / 10,
            15
        )


    else:

        score_surface = score_font.render(
            'Player 1: ' +
            str(score_1) +
            '    Player 2: ' +
            str(score_2),
            True,
            color
        )

        score_rect = score_surface.get_rect()

        score_rect.midtop = (
            frame_size_x / 2,
            frame_size_y / 1.25
        )


    game_window.blit(
        score_surface,
        score_rect
    )


# =========================================================
# MAIN LOOP
# =========================================================

while True:


    # =====================================================
    # RECEIVE GAME
    # =====================================================

    if not receive_game_state():

        print()
        print('[!] Se perdio la conexion con Player 1.')

        pygame.quit()

        sys.exit()


    # =====================================================
    # EVENTS
    # =====================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()

            client_socket.close()

            sys.exit()


        elif event.type == pygame.KEYDOWN:


            # Player 2
            # W = Up
            if event.key == pygame.K_w:

                send_command('UP')


            # S = Down
            if event.key == pygame.K_s:

                send_command('DOWN')


            # A = Left
            if event.key == pygame.K_a:

                send_command('LEFT')


            # D = Right
            if event.key == pygame.K_d:

                send_command('RIGHT')


            # ESC
            if event.key == pygame.K_ESCAPE:

                pygame.event.post(
                    pygame.event.Event(
                        pygame.QUIT
                    )
                )


    # =====================================================
    # DRAW
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
    # SCORE
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
    # REFRESH
    # =====================================================

    pygame.display.update()

    fps_controller.tick(60)