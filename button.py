import pygame

class Button:
    def __init__(self, surface, text, bg, fg, x, y, width, height):
        """
        creating a button object
        :param surface: the pygame window --> pygame.Surface
        :param text: the text displayed on the button --> str
        :param bg: the color of the button --> str/tuple (hex or rgb)
        :param fg: the color of the text on the button --> str/tuple (hex or rgb)
        :param x: the x position of the button --> int
        :param y: the y position of the button --> int
        :param width: the width of the button --> int
        :param height: the height of the button --> int
        """
        self.surface = surface
        self.bg = bg
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        font = pygame.font.SysFont("Arial", height//2, "bold")
        self.label = font.render(text, True, fg)

    def draw(self):
        """
        displaying the button on the screen
        :return: None
        """
        pygame.draw.rect(self.surface, self.bg, self.rect)
        self.surface.blit(self.label, (self.x + self.width * 0.09,
                                       self.y + self.height*0.25))
