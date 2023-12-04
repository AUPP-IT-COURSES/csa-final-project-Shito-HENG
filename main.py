import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# Load images
images = []
for i in range(7):
    image = pygame.image.load(f"hangman{i}.png")
    image = pygame.transform.scale(image,(250, 250))
    images.append(image)

# Game variables
hangman_status = 0
with open("words.txt", "r") as file:
    lines = file.readlines()

# Select a random line from the file
random_line = random.choice(lines).strip()
word, description = random_line.split(",") # Split the line into word and description
word = word.strip().upper()
description = description.strip()

guessed = []

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
LETTER_FONT = pygame.font.SysFont("comicsans", 40)
WORD_FONT = pygame.font.SysFont("comicsans", 60)
TITLE_FONT = pygame.font.SysFont("comicsans", 70)

# Button variables
RADIUS = 20
GAP = 15
letters = []
start_x = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
start_y = 450
A = 65
for i in range(26):
    x = start_x + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = start_y + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])


# Draw the game
def draw():
    win.fill(WHITE)

    # Draw title
    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    # Draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    text = pygame.transform.scale(text, (300, 50))
    win.blit(text, (400, 200))

    # Draw description
    description_text = WORD_FONT.render(description, 1, BLACK)
    description_text = pygame.transform.scale(description_text, (400, 50))
    win.blit(description_text, (400, 300))

    # Draw buttons
    for letter in letters:
        x, y, char, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(char, 1, BLACK)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    # Draw hangman image
    win.blit(images[hangman_status], (100, 150))
    pygame.display.update()


# Display a message for the given result (win/lose)
def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


# Game loop
FPS = 60
clock = pygame.time.Clock()
run = True

while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for letter in letters:
                x, y, char, visible = letter
                if visible:
                    distance = ((x - mouse_x) ** 2 + (y - mouse_y) ** 2) ** 0.5
                    if distance < RADIUS:
                        letter[3] = False
                        guessed.append(char)
                        if char not in word:
                            hangman_status += 1

    draw()

    # Check win/loss conditions
    won = True
    for letter in word:
        if letter not in guessed:
            won = False
            break

    if won:
        display_message("You won!")
        pygame.time.delay(2000)
        response = input("Do you want to play again? (yes/no): ").lower()
        if response != 'yes':
            run = False
        else:
            # Reset game variables for a new game
            hangman_status = 0
            word = random.choice(lines).strip().split(",")[0].strip().upper()
            guessed = []
            for letter in letters:
                letter[3] = True
        continue

    if hangman_status == 6:
        display_message("You lost!")
        pygame.time.delay(2000)
        response = input("Do you want to play again? (yes/no): ").lower()
        if response != 'yes':
            run = False
        else:
            # Reset game variables for a new game
            hangman_status = 0
            word = random.choice(lines).strip().split(",")[0].strip().upper()
            guessed = []
            for letter in letters:
                letter[3] = True
        continue

pygame.quit()