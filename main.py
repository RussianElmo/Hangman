import time
import pygame
import random

pygame.init()
pygame.font.init()

size = width, height = 750, 500
screen = pygame.display.set_mode(size)  # initialize pygame window
pygame.display.set_caption('Hangman')
pygame.display.flip()

alpha_list = [chr(x) for x in range(ord('a'), ord('z') + 1)]


def render_text(text, font, font_size, position, color):
    f = pygame.font.SysFont(font, font_size)
    obj = f.render(text, True, color)
    t_rect = obj.get_rect()
    t_rect.center = position
    screen.blit(obj, t_rect)


def read_file(d):
    if d == 'easy':
        file_name = 'easy_words.txt'
    elif d == 'medium':
        file_name = 'medium_words.txt'
    elif d == 'hard':
        file_name = 'hard_words.txt'
    f = open(file_name, 'r')
    words = f.read().split()
    return words


def pick_word(words):
    w = random.choice(words)
    words.remove(w)
    return w


def process_click(letter_positions, mouse_pos):
    radius = 25
    for i in range(len(letter_positions)):
        if radius + letter_positions[i][0] > mouse_pos[0] > letter_positions[i][0] - radius and radius + \
                letter_positions[i][1] > mouse_pos[1] > letter_positions[i][1] - radius:
            letter_positions.pop(i)
            letter = alpha_list[i]
            alpha_list.pop(i)
            return letter


def add_letters(letter_pos):
    for i in range(len(letter_pos)):
        pygame.draw.circle(screen, (196, 47, 196), letter_pos[i], 25)
        render_text(alpha_list[i], 'comicsansms', 25, letter_pos[i], (212, 212, 212))


def create_circle_centers():
    circle_center = [50, 350]
    circle_centers = [[] for i in range(26)]
    for i in range(26):
        circle_centers[i].extend(circle_center)
        circle_center[0] += 55
        if i == 12:
            circle_center[1] += 60
            circle_center[0] = 50
    return circle_centers


def start_screen():
    running = True
    easy = pygame.Rect(100, 400, 100, 40)
    medium = pygame.Rect(325, 400, 100, 40)
    hard = pygame.Rect(550, 400, 100, 40)
    grey = (212, 212, 212)

    while running:
        screen.fill((61, 60, 56))
        logo = pygame.image.load(r'logo.png')
        screen.blit(logo, (250, 0))  # adds pygame image to start screen
        render_text('Hangman', 'comicsansms', 50, (375, 330), (227, 149, 41))

        pygame.draw.rect(screen, (76, 186, 217), easy)  # these three lines draw easy, medium, and hard buttons
        pygame.draw.rect(screen, (196, 47, 196), medium)
        pygame.draw.rect(screen, (0, 255, 64), hard)

        render_text('Easy', 'comicsansms', 20, easy.center, grey)
        render_text('Medium', 'comicsansms', 20, medium.center, grey)
        render_text('Hard', 'comicsansms', 20, hard.center, grey)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if easy.collidepoint(mouse_pos):
                    return 'easy'
                elif medium.collidepoint(mouse_pos):
                    return 'medium'
                elif hard.collidepoint(mouse_pos):
                    return 'hard'
        pygame.display.flip()


def update_word(l, w, u):
    index_pos_list = []
    if l is None:
        return u
    for i in range(len(w)):
        if w[i] == l:
            index_pos_list.append(i)
    for i in index_pos_list:
        u = u[:i] + l + u[i + 1:]
    return u


def check_word(l, w):
    if l is None:
        return True
    if l in w:
        return True
    return False


def draw_game_screen(circle_centers, astericks, guesses):
    pics = ['gallows.png', 'head.png', 'torso.png', 'left_arm.png', 'right_arm.png', 'left_leg.png', 'logo.png']
    current_pic = pics[guesses]
    screen.fill((61, 60, 56))
    add_letters(circle_centers)
    render_text(astericks, 'comicsansms', 40, (width / 2, 460), (212, 212, 212))
    pic = pygame.image.load(current_pic)
    screen.blit(pic, (250, 0))
    pygame.display.flip()


def game_screen(word):
    win = False
    screen.fill((61, 60, 56))
    guesses = 0
    unknown = '*' * len(word)
    letter_positions = create_circle_centers()
    running = True
    draw_game_screen(letter_positions, unknown, guesses)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                letter = process_click(letter_positions, mouse_pos)
                if check_word(letter, word):
                    unknown = update_word(letter, word, unknown)
                else:
                    guesses += 1
        draw_game_screen(letter_positions, unknown, guesses)
        if unknown == word:
            win = True
            running = False
        if guesses == 6:
            unknown = word
            draw_game_screen(letter_positions, unknown, guesses)
            time.sleep(4)
            running = False
    if win:
        win_screen()


def win_screen():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((61, 60, 56))
        trophy = pygame.image.load('trophy.png')
        screen.blit(trophy, (275, 50))
        render_text('You Win!', 'comicsansms', 40, (375, 400), (255, 215, 0))
        pygame.display.flip()


word_list = read_file(start_screen())
word = pick_word(word_list)
game_screen(word)
