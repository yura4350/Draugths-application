import threading
import pygame
import tkinter as tk
import customtkinter as ctk
import os

# Pygame setup
os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'  # Offset for where the pygame window appears


def run_pygame():
    pygame_part.init()
    screen = pygame_part.display.set_mode((600, 600))
    pygame_part.display.set_caption("Pygame Draughts Game")
    running = True
    while running:
        for event in pygame_part.event.get():
            if event.type == pygame_part.QUIT:
                running = False
        screen.fill((0, 0, 0))  # Placeholder for your game logic
        pygame_part.display.flip()
    pygame_part.quit()


# Tkinter setup
def start_game():
    # Start the Pygame thread when the user clicks 'Start Game'
    pygame_thread = threading.Thread(target=run_pygame, daemon=True)
    pygame_thread.start()

    # Optionally, disable the button after starting the game
    start_game_button.configure(state="disabled")


app = ctk.CTk()
app.geometry('800x600')  # Tkinter window size

start_game_button = ctk.CTkButton(app, text="Start Game", command=start_game)
start_game_button.pack(pady=20)

# Main loop
app.mainloop()