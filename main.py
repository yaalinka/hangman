import pygame
from math import sqrt
from random import choice

# setup display
pygame.init()
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")
# colors
WHITE = (225, 225, 225)
BLACK = (0, 0, 0)
# buttons
RADIUS = 24
GAP = 15
letters = []
start_x = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
start_y = 400
A = 65
for i in range(26):
    x = start_x + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = start_y + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

LETTER_FONT = pygame.font.SysFont('comicsans', 36)
WORD_FONT = pygame.font.SysFont('comicsans', 50)

# load images
images = []
for i in range(7):
    image = pygame.image.load('images/hangman' + str(i) + '.png')
    images.append(image)

# game variables
hangman_status = 0
words = ['INTERVIEW', "DEVELOPER", "PACKAGE", "MODULE", "GENERATOR", "ITERATOR", "FUNCTION"]
word = choice(words)
guessed = []


# draw
def draw():
    WIN.fill(WHITE)

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + ' '
        else:
            display_word += '_ '
    text = WORD_FONT.render(display_word, True, BLACK)
    WIN.blit(text, (400, 200))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(WIN, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, True, BLACK)
            WIN.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))
    WIN.blit(images[hangman_status], (150, 90))
    pygame.display.update()


# text when game ends
def display_message(message):
    pygame.time.delay(1000)
    WIN.fill(WHITE)
    text = WORD_FONT.render(message, True, BLACK)
    WIN.blit(text, WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2)
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    global hangman_status
    FPS = 60
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dis < RADIUS:
                            letter[3] = False  # when pressed make letter invisible
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            display_message('You WON!')
            break

        if hangman_status == 6:
            display_message('You LOST!')
            break


main()

pygame.quit()
