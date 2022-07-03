import pygame
import sys # for the exit function (to exit the program)
import os # for the listdir function (to convert a directory/folder to a list)
import random # for the sample function (to generate a random order for the cards)
import math # for the sqrt function (to find the square root of a number)

from button import Button # importing the button class I created in a separate python file
pygame.init() # initializing pygame

# setting up the window
WINDOW_SIZE = (1100, 570)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Animals Memory Game")

# colors
DARK_BLUE = "#2f00aa"
BLACK = (0, 0, 0)
LIGHT_BLUE = "#9cf7ff"
RED = (255, 0, 0)
LIGHT_PURPLE = "#d8c3ff"

# 2D list that contains each animal image and the name of the animal
animals_imgs = [[pygame.image.load(f"animals/{img}"), img.replace(".png", "")] for img in os.listdir("animals")]
# os.listdir --> converts a directory to a list

# lose and win images
lose_img = pygame.transform.scale(pygame.image.load("you_lost.png"), (440, 200))
win_img = pygame.transform.scale(pygame.image.load("congrats.png"), (440, 200))
tie_img = pygame.transform.scale(pygame.image.load("tie.png"), (440, 200))

collect_sound = pygame.mixer.Sound("collect.wav") # a sound that is played when two cards are matched


class Card:
    def __init__(self, surface, x, y, width, height, img, color, disabled, animal):
        """
        creating a card object
        :param surface: the pygame window --> pygame.Surface
        :param x: the x position of the card --> int
        :param y: the y position of the card --> int
        :param width: the width of the card --> int
        :param height: the height of the card --> int
        :param img: the animal image displayed on the card --> pygame.Surface
        :param color: the color of the back of the card --> str/tuple (hex or rgb)
        :param disabled: the state of the card: if the user can click on the card or not --> bool
        :param animal: the name of the animal displayed on the card --> str
        """
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = pygame.transform.scale(img, (self.width, self.height))
        self.color = color
        self.disabled = disabled
        self.animal = animal

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.flipped = False

    def draw(self):
        """
        displaying the card object on the screen
        :return: None
        """
        if self.flipped:
            pygame.draw.rect(window, self.color, self.rect, 2, 3)
            self.surface.blit(self.img, (self.x, self.y))
        else:
            pygame.draw.rect(window, self.color, self.rect, 0, 3)
            pygame.draw.rect(window, BLACK, self.rect, 4, 3)

    def clicked(self):
        """
        checking whether the card can be flipped
        :return: None
        """
        if not self.flipped and not self.disabled:
            self.flipped = True


def sleep(ms):
    """
    function that acts as a countdown timer
    :param ms: amount of time to wait (in milliseconds)
    :return: None
    """
    while ms > 0:
        pygame.time.delay(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        ms -= 10


def create_singleplayer_cards():
    """
    creating the cards for the single player game mode
    :return: cards: the list of cards for the game --> list
    """
    cards = []
    x = 310
    y = 120
    sample1 = random.sample(animals_imgs, len(animals_imgs))
    sample2 = random.sample(animals_imgs, len(animals_imgs))
    sample1.extend(sample2)
    count = 0
    for i in range(len(animals_imgs) * 2):
        count += 1
        rand_animal = sample1[count - 1]

        card = Card(window, x, y, 100, 100, rand_animal[0], DARK_BLUE, True, rand_animal[1])
        cards.append(card)

        if i != 0 and (i + 1) % math.sqrt(len(animals_imgs) * 2) == 0:
            x = 310
            y += 110
        else:
            x += 110

    return cards


def singleplayer():
    """
    the single player game mode
    :return: None
    """
    cards = create_singleplayer_cards()

    turn_font = pygame.font.SysFont("Arial", 80, "bold")
    score_font = pygame.font.SysFont("Arial", 30, "bold")

    player_score = 0
    computer_score = 0

    # for determining whose turn it is
    count = 0

    player_clicks = 0
    flipped = []

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    menu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if count % 2 == 0:
                    for card in cards:
                        if card.rect.collidepoint(event.pos) and player_clicks < 2 and \
                            not card.flipped and not card.disabled:
                            card.clicked()
                            player_clicks += 1
                            flipped.append(card)

        window.fill(LIGHT_BLUE)

        if count % 2 == 0:
            window.blit(turn_font.render("Your Turn", True, DARK_BLUE), (340, 0))
        else:
            window.blit(turn_font.render("Computer's Turn", True, RED), (225, 0))

            unflipped_cards = [card for card in cards if not card.flipped]

            if len(unflipped_cards) == 2:
                rand_cards = unflipped_cards.copy()
            else:
                rand_cards = random.sample(unflipped_cards, 2)

            flipped = rand_cards.copy()
            flipped[0].clicked()
            flipped[1].clicked()

        window.blit(score_font.render(f"Your Score: {player_score}", True, DARK_BLUE), (10, 520))
        window.blit(score_font.render(f"Computer Score: {computer_score}", True, RED), (760, 520))

        for card in cards:
            card.draw()

            if count % 2 == 0:
                card.disabled = False
            else:
                card.disabled = True

        pygame.display.update()

        if player_clicks >= 2 or count % 2 == 1:
            player_clicks = 0

            if flipped[0].animal == flipped[1].animal:
                if count % 2 == 0:
                    player_score += 1
                else:
                    computer_score += 1
                    count += 1
                collect_sound.play()
            else:
                sleep(1000)
                for card in flipped:
                    card.flipped = False
                count += 1
            flipped.clear()

        if all([card.flipped for card in cards]):
            if player_score > computer_score:
                winner = "you"
            elif computer_score > player_score:
                winner = "the computer"
            else:
                winner = "tie"

            singleplayer_victory(winner, player_score, computer_score)

    pygame.quit()
    sys.exit(0)


def singleplayer_victory(winner, player_score, computer_score):
    """
    displaying the winner of the single player game on the screen
    :param winner: the winner of the game --> str
    :param player_score: the player's score --> int
    :param computer_score: the computer's score --> int
    :return: None
    """
    winner_font = pygame.font.SysFont("Berlin Sans FB Demi", 80, "bold")
    score_font = pygame.font.SysFont("Arial", 40, "bold")

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    menu()

        window.fill(LIGHT_PURPLE)

        if winner != "tie":
            if winner == "computer":
                window.blit(winner_font.render(f"{winner} won!".upper(), True, DARK_BLUE), (260, 10))
                window.blit(lose_img, (330, 250))
            else:
                window.blit(winner_font.render(f"{winner} won!".upper(), True, DARK_BLUE), (360, 10))
                window.blit(win_img, (330, 250))
        else:
            window.blit(winner_font.render("TIE!", True, DARK_BLUE), (480, 10))
            window.blit(tie_img, (330, 250))

        window.blit(score_font.render(f"Computer Score: {computer_score}", True, RED), (380, 100))
        window.blit(score_font.render(f"Player Score: {player_score}", True, DARK_BLUE), (380, 150))

        window.blit(score_font.render("Press m to return to the menu", True, DARK_BLUE), (10, 520))

        pygame.display.update()

    pygame.quit()
    sys.exit(0)


def create_multiplayer_cards():
    """
    creating the cards for the multiplayer game mode
    :return: player1_cards, player2_cards: the lists of cards for each player --> list
    """
    player1_cards = []
    player2_cards = []
    cards_list = player1_cards
    x = 130
    y = 160
    sample1 = random.sample(animals_imgs, len(animals_imgs))
    sample2 = random.sample(animals_imgs, len(animals_imgs))
    sample1.extend(sample2)
    count = 0
    for i in range(2):
        for j in range(len(animals_imgs) * 2):
            count += 1
            rand_animal = sample1[count - 1]

            card = Card(window, x, y, 80, 80, rand_animal[0], DARK_BLUE, True, rand_animal[1])
            cards_list.append(card)

            if j != 0 and (j + 1) % math.sqrt(len(animals_imgs) * 2) == 0:
                if x <= 615:
                    x = 130
                else:
                    x = 615

                y += 90
            else:
                x += 90
        x = 615
        y = 160
        count = 0
        cards_list = player2_cards

    return player1_cards, player2_cards


def multiplayer():
    """
    the multiplayer game mode
    :return: None
    """
    player1_cards, player2_cards = create_multiplayer_cards()
    player_font = pygame.font.SysFont("Arial", 80, "bold")
    turn_font = pygame.font.SysFont("Arial", 40)
    score_font = pygame.font.SysFont("Arial", 30, "bold")

    player1_score = 0
    player2_score = 0

    # for determining whose turn it is
    count = 0

    player1_clicks = 0
    player2_clicks = 0

    flipped = []

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    menu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for player1_card, player2_card in zip(player1_cards, player2_cards):
                    if player1_card.rect.collidepoint(event.pos) and player1_clicks < 2 and \
                            not player1_card.disabled and not player1_card.flipped:
                        player1_card.clicked()
                        player1_clicks += 1
                        flipped.append(player1_card)

                    elif player2_card.rect.collidepoint(event.pos) and player2_clicks < 2 and \
                            not player2_card.disabled and not player2_card.flipped:
                        player2_card.clicked()
                        player2_clicks += 1
                        flipped.append(player2_card)

        window.fill(LIGHT_BLUE)
        window.blit(player_font.render("Player1", True, DARK_BLUE), (160, 0))
        window.blit(player_font.render("Player2", True, RED), (650, 0))

        window.blit(score_font.render(f"Player1 Score: {player1_score}", True, DARK_BLUE), (180, 520))
        window.blit(score_font.render(f"Player2 Score: {player2_score}", True, RED), (680, 520))

        if count % 2 == 0:
            window.blit(turn_font.render("Your Turn", True, DARK_BLUE), (220, 100))
            window.blit(turn_font.render("Player1's Turn", True, RED), (680, 100))
        else:
            window.blit(turn_font.render("Player2's Turn", True, DARK_BLUE), (190, 100))
            window.blit(turn_font.render("Your Turn", True, RED), (720, 100))

        # iterating over both of the card lists simultaneously instead of two separate loops (zip)
        for player1_card, player2_card in zip(player1_cards, player2_cards):
            player1_card.draw()
            player2_card.draw()

            if count % 2 == 0:
                player1_card.disabled = False
                player2_card.disabled = True
            else:
                player2_card.disabled = False
                player1_card.disabled = True

        pygame.display.update()

        if player1_clicks >= 2 or player2_clicks >= 2:
            player1_clicks = 0
            player2_clicks = 0

            if flipped[0].animal == flipped[1].animal:
                if count % 2 == 0:
                    player1_score += 1

                    for player2_card in player2_cards:
                        if player2_card.animal == flipped[0].animal:
                            player2_card.flipped = True
                else:
                    player2_score += 1

                    for player1_card in player1_cards:
                        if player1_card.animal == flipped[0].animal:
                            player1_card.flipped = True
                collect_sound.play()
            else:
                sleep(1000)
                for card in flipped:
                    card.flipped = False
                count += 1
            flipped.clear()

        if all([card.flipped for card in player1_cards]):
            if player1_score > player2_score:
                winner = "player 1"
            elif player2_score > player1_score:
                winner = "player 2"
            else:
                winner = "tie"

            multiplayer_victory(winner, player1_score, player2_score)

    pygame.quit()
    sys.exit(0)


def multiplayer_victory(winner, player1_score, player2_score):
    """
    displaying the winner of the multiplayer game on the screen
    :param winner: the winner of the game --> str
    :param player1_score: player1's score --> int
    :param player2_score: player2's score --> int
    :return: None
    """
    winner_font = pygame.font.SysFont("Berlin Sans FB Demi", 80, "bold")
    score_font = pygame.font.SysFont("Arial", 40, "bold")

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    menu()

        window.fill(LIGHT_PURPLE)

        if winner != "tie":
            window.blit(winner_font.render(f"{winner} won!".upper(), True, DARK_BLUE), (270, 10))
            window.blit(win_img, (330, 250))
        else:
            window.blit(winner_font.render("TIE!", True, DARK_BLUE), (480, 10))
            window.blit(tie_img, (330, 250))

        window.blit(score_font.render(f"Player1 Score: {player1_score}", True, DARK_BLUE), (400, 100))
        window.blit(score_font.render(f"Player2 Score: {player2_score}", True, RED), (400, 150))

        window.blit(score_font.render("Press m to return to the menu", True, DARK_BLUE), (10, 520))

        pygame.display.update()

    pygame.quit()
    sys.exit(0)


def menu():
    """
    the menu of the game, where the user picks the game mode
    :return: None
    """
    multiplayer_button = Button(window, "Multiplayer", DARK_BLUE, BLACK, 360, 350, 400, 120)
    singleplayer_button = Button(window, "Singleplayer", DARK_BLUE, BLACK, 360, 200, 400, 120)

    title_font = pygame.font.SysFont("Berlin Sans FB Demi", 80, "bold")
    subtitle_font = pygame.font.SysFont("Arial", 35, "bold")

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if singleplayer_button.rect.collidepoint(event.pos):
                    singleplayer()
                elif multiplayer_button.rect.collidepoint(event.pos):
                    multiplayer()

        window.fill(LIGHT_BLUE)
        title = title_font.render("Memory Game", True, DARK_BLUE)
        window.blit(title, (300, 10))
        subtitle = subtitle_font.render("Choose a Game Mode", True, DARK_BLUE)
        window.blit(subtitle, (380, 95))

        singleplayer_button.draw()
        multiplayer_button.draw()

        pygame.display.update()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    menu()
