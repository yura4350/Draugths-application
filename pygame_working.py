import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Draughts Game')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)


# Button class
class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win):
        # Call this method to draw the button on the screen
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, True, BLACK)
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


# Function to handle button events
def button_event(button, event):
    pos = pygame.mouse.get_pos()

    if event.type == pygame.MOUSEBUTTONDOWN:
        if button.is_over(pos):
            print(f"{button.text} Button clicked!")


# Create buttons
surrender_button = Button(RED, 650, 100, 100, 50, 'Surrender')
draw_button = Button(BLUE, 650, 200, 100, 50, 'Draw')
return_button = Button(GREEN, 650, 300, 100, 50, 'Return')

buttons = [surrender_button, draw_button, return_button]

# Game loop
running = True
while running:
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for button in buttons:
            button_event(button, event)

    for button in buttons:
        button.draw(screen)

    pygame.display.update()

pygame.quit()
sys.exit()