"""
Snake Eater
Made with PyGame
"""

import pygame, sys, time, random


# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 25

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
pygame.display.set_caption('Snake Eater - 2 Players')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


# Game variables - Player 1
snake_pos_1 = [100, 50]
snake_body_1 = [[100, 50], [100-10, 50], [100-(2*10), 50]]

direction_1 = 'RIGHT'
change_to_1 = direction_1

score_1 = 0


# Game variables - Player 2
snake_pos_2 = [600, 400]
snake_body_2 = [[600, 400], [600+10, 400], [600+(2*10), 400]]

direction_2 = 'LEFT'
change_to_2 = direction_2

score_2 = 0


# Food
food_pos = [
    random.randrange(1, (frame_size_x//10)) * 10,
    random.randrange(1, (frame_size_y//10)) * 10
]

food_spawn = True


# Reset Game
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
        [100-10, 50],
        [100-(2*10), 50]
    ]

    direction_1 = 'RIGHT'
    change_to_1 = direction_1
    score_1 = 0


    # Player 2
    snake_pos_2 = [600, 400]
    snake_body_2 = [
        [600, 400],
        [600+10, 400],
        [600+(2*10), 400]
    ]

    direction_2 = 'LEFT'
    change_to_2 = direction_2
    score_2 = 0


    # New food
    food_pos = [
        random.randrange(1, (frame_size_x//10)) * 10,
        random.randrange(1, (frame_size_y//10)) * 10
    ]

    food_spawn = True


# Game Over
def game_over(winner):
    my_font = pygame.font.SysFont('times new roman', 70)

    if winner == 1:
        message = 'PLAYER 1 WINS!'
        color = green

    elif winner == 2:
        message = 'PLAYER 2 WINS!'
        color = blue

    else:
        message = 'DRAW!'
        color = red

    game_over_surface = my_font.render(message, True, color)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)

    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)

    show_score(0, white, 'times', 20)

    pygame.display.flip()

    # Esperar 3 segundos
    time.sleep(3)

    # Reiniciar la partida
    reset_game()


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)

    if choice == 1:

        score_surface = score_font.render(
            'Player 1 Score : ' + str(score_1),
            True,
            color
        )

        score_rect = score_surface.get_rect()
        score_rect.midtop = (frame_size_x/10, 15)


    elif choice == 2:

        score_surface = score_font.render(
            'Player 2 Score : ' + str(score_2),
            True,
            color
        )

        score_rect = score_surface.get_rect()
        score_rect.midtop = (
            frame_size_x - frame_size_x/10,
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
            frame_size_x/2,
            frame_size_y/1.25
        )

    game_window.blit(score_surface, score_rect)


# Main logic
while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:


            # Player 1
            # Arrow Up -> Up
            # Arrow Down -> Down
            # Arrow Left -> Left
            # Arrow Right -> Right

            if event.key == pygame.K_UP:
                change_to_1 = 'UP'

            if event.key == pygame.K_DOWN:
                change_to_1 = 'DOWN'

            if event.key == pygame.K_LEFT:
                change_to_1 = 'LEFT'

            if event.key == pygame.K_RIGHT:
                change_to_1 = 'RIGHT'


            # Player 2
            # W -> Up
            # S -> Down
            # A -> Left
            # D -> Right

            if event.key == pygame.K_w:
                change_to_2 = 'UP'

            if event.key == pygame.K_s:
                change_to_2 = 'DOWN'

            if event.key == pygame.K_a:
                change_to_2 = 'LEFT'

            if event.key == pygame.K_d:
                change_to_2 = 'RIGHT'


            # Esc -> Quit
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(
                    pygame.event.Event(pygame.QUIT)
                )


    # Making sure Player 1 cannot move in the opposite direction
    if change_to_1 == 'UP' and direction_1 != 'DOWN':
        direction_1 = 'UP'

    if change_to_1 == 'DOWN' and direction_1 != 'UP':
        direction_1 = 'DOWN'

    if change_to_1 == 'LEFT' and direction_1 != 'RIGHT':
        direction_1 = 'LEFT'

    if change_to_1 == 'RIGHT' and direction_1 != 'LEFT':
        direction_1 = 'RIGHT'


    # Making sure Player 2 cannot move in the opposite direction
    if change_to_2 == 'UP' and direction_2 != 'DOWN':
        direction_2 = 'UP'

    if change_to_2 == 'DOWN' and direction_2 != 'UP':
        direction_2 = 'DOWN'

    if change_to_2 == 'LEFT' and direction_2 != 'RIGHT':
        direction_2 = 'LEFT'

    if change_to_2 == 'RIGHT' and direction_2 != 'LEFT':
        direction_2 = 'RIGHT'


    # Moving Player 1
    if direction_1 == 'UP':
        snake_pos_1[1] -= 10

    if direction_1 == 'DOWN':
        snake_pos_1[1] += 10

    if direction_1 == 'LEFT':
        snake_pos_1[0] -= 10

    if direction_1 == 'RIGHT':
        snake_pos_1[0] += 10


    # Moving Player 2
    if direction_2 == 'UP':
        snake_pos_2[1] -= 10

    if direction_2 == 'DOWN':
        snake_pos_2[1] += 10

    if direction_2 == 'LEFT':
        snake_pos_2[0] -= 10

    if direction_2 == 'RIGHT':
        snake_pos_2[0] += 10


    # Snake body growing mechanism - Player 1
    snake_body_1.insert(0, list(snake_pos_1))

    if snake_pos_1[0] == food_pos[0] and snake_pos_1[1] == food_pos[1]:

        score_1 += 1
        food_spawn = False

    else:
        snake_body_1.pop()


    # Snake body growing mechanism - Player 2
    snake_body_2.insert(0, list(snake_pos_2))

    if snake_pos_2[0] == food_pos[0] and snake_pos_2[1] == food_pos[1]:

        score_2 += 1
        food_spawn = False

    else:
        snake_body_2.pop()


    # Spawning food on the screen
    if not food_spawn:

        food_pos = [
            random.randrange(1, (frame_size_x//10)) * 10,
            random.randrange(1, (frame_size_y//10)) * 10
        ]

    food_spawn = True


    # GFX
    game_window.fill(black)


    # Player 1 Snake
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


    # Player 2 Snake
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


    # Snake food
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


    # Game Over conditions

    # Player 1 getting out of bounds
    if snake_pos_1[0] < 0 or snake_pos_1[0] > frame_size_x-10:

        game_over(2)

    if snake_pos_1[1] < 0 or snake_pos_1[1] > frame_size_y-10:

        game_over(2)


    # Player 2 getting out of bounds
    if snake_pos_2[0] < 0 or snake_pos_2[0] > frame_size_x-10:

        game_over(1)

    if snake_pos_2[1] < 0 or snake_pos_2[1] > frame_size_y-10:

        game_over(1)


    # Player 1 touching its own snake body
    for block in snake_body_1[1:]:

        if snake_pos_1[0] == block[0] and snake_pos_1[1] == block[1]:

            game_over(2)


    # Player 2 touching its own snake body
    for block in snake_body_2[1:]:

        if snake_pos_2[0] == block[0] and snake_pos_2[1] == block[1]:

            game_over(1)


    # Player 1 touching Player 2
    for block in snake_body_2:

        if snake_pos_1[0] == block[0] and snake_pos_1[1] == block[1]:

            game_over(2)


    # Player 2 touching Player 1
    for block in snake_body_1:

        if snake_pos_2[0] == block[0] and snake_pos_2[1] == block[1]:

            game_over(1)


    # Scores
    show_score(1, green, 'consolas', 20)
    show_score(2, blue, 'consolas', 20)


    # Refresh game screen
    pygame.display.update()

    # Refresh rate
    fps_controller.tick(difficulty)