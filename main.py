import sqlite3
import customtkinter as ctk
import tkinter.messagebox
import sys
import pygame
import threading
import os
import tkinter as tk
from pygame_part import *
from checkers.constants import *
import shared_state
from datetime import datetime

def setup_users_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

setup_users_database()

def setup_game_results_database():
    conn = sqlite3.connect('game_results.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_results (
            id INTEGER PRIMARY KEY,
            player1 TEXT NOT NULL,
            player2 TEXT NOT NULL,
            result TEXT NOT NULL,
            game_date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

setup_game_results_database()

def check_credentials(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username=?', (username,))
    result = cursor.fetchone()
    conn.close()

    if result and result[0] == password:
        return True
    else:
        return False

def add_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    if cursor.fetchone():
        return False  # User already exists
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()
    return True

def show_registration_form():
    clear_window()
    app.title('Register New User')

    username_reg_entry = ctk.CTkEntry(app, placeholder_text="Username")
    username_reg_entry.pack(pady=10)

    password_reg_entry = ctk.CTkEntry(app, placeholder_text="Password", show="*")
    password_reg_entry.pack(pady=10)

    def attempt_registration():
        username = username_reg_entry.get()
        password = password_reg_entry.get()
        if add_user(username, password):
            tkinter.messagebox.showinfo("Registration", "Registration successful!")
            show_main_menu()  # Or any other appropriate action
        else:
            tkinter.messagebox.showerror("Registration", "Username already exists!")

    register_button = ctk.CTkButton(app, text="Register", command=attempt_registration)
    register_button.pack(pady=10)

    back_button = ctk.CTkButton(app, text="Sign-in", command=show_main_menu)
    back_button.pack(pady=10)


# Example users
add_user("user1", "pass1")
add_user("user2", "pass2")

app = ctk.CTk()
app.title('Draughts Game Login')
app.geometry('1000x800')

username_entry = ctk.CTkEntry(app, placeholder_text="Username")
username_entry.pack(pady=10)

password_entry = ctk.CTkEntry(app, placeholder_text="Password", show="*")
password_entry.pack(pady=10)

register_button = ctk.CTkButton(app, text="Register New User", command=show_registration_form)
register_button.pack(pady=10)

status_label = ctk.CTkLabel(app, text="")
status_label.pack(pady=10)

def attempt_login():
    username = username_entry.get()
    password = password_entry.get()
    if check_credentials(username, password):
        status_label.configure(text="Login Successful!")
        show_main_menu()
    else:
        status_label.configure(text="Login Failed. Try again.")

login_button = ctk.CTkButton(app, text="Login", command=attempt_login)
login_button.pack(pady=10)

def start_game():
    choose_game_type()

def load_game():
    tkinter.messagebox.showinfo("Load Game", "Loading a game...")

def quit_to_desktop():
    sys.exit()

# This function will be called after a successful login
def show_main_menu():
    clear_window()

    app.title('Main Menu')

    main_menu_label = ctk.CTkLabel(app, text="The Main Menu", font=("Roboto Medium", 16))
    main_menu_label.pack(pady=20)

    start_game_button = ctk.CTkButton(app, text="Start a Game", command=start_game)
    start_game_button.pack(pady=10)

    load_game_button = ctk.CTkButton(app, text="Load a Game", command=load_game)
    load_game_button.pack(pady=10)

    quit_button = ctk.CTkButton(app, text="Quit to the Desktop", command=quit_to_desktop)
    quit_button.pack(pady=10)


def choose_game_type():
    # Clear the previous menu
    clear_window()

    # Create the new title and buttons for game type selection
    title_label = ctk.CTkLabel(app, text="Choose a type of game", font=("Roboto Medium", 16))
    title_label.pack(pady=20)

    against_computer_button = ctk.CTkButton(app, text="Against a computer", command=play_game_vs_computer)
    against_computer_button.pack(pady=10)

    against_friend_button = ctk.CTkButton(app, text="Against a friend", command=play_game_vs_player)
    against_friend_button.pack(pady=10)


# Define the functions that are called when the buttons are pressed
def play_game_vs_computer():
    # Here you would call the function that starts the game against the computer
    create_game_vs_computer_settings()  # Placeholder action


def play_game_vs_player():
    # Here you would call the function that starts the game against another player
    create_game_vs_player_settings()  # Placeholder action


def start_game_with_settings(mode = None, color=None, difficulty=None, board_size=None):
    # Placeholder function to start the game with the chosen settings
    print(f"Starting game with settings: Color: {color}, Difficulty: {difficulty}, Board Size: {board_size}")
    # Here you should call the actual game starting function and pass these settings
    if mode == "player_vs_computer":
        create_game_vs_computer_interface(mode=mode, color=color, difficulty=difficulty, board_size=board_size)
    else:
        create_game_vs_player_interface(mode=mode, board_size=board_size)


def create_game_vs_computer_settings():
    clear_window()

    title_label = ctk.CTkLabel(app, text="Create the new game against computer: settings", font=("Roboto Medium", 16))
    title_label.pack(pady=20)

    # Pick a color
    color_label = ctk.CTkLabel(app, text="Pick a color:")
    color_label.pack()
    color_var = ctk.StringVar(value="Red")
    color_frame = ctk.CTkFrame(app)
    color_frame.pack(pady=10)
    red_button = ctk.CTkRadioButton(color_frame, text="Red", variable=color_var, value="Red")
    red_button.pack(side='left', padx=10)
    white_button = ctk.CTkRadioButton(color_frame, text="White", variable=color_var, value="White")
    white_button.pack(side='left', padx=10)

    # Choose the level of difficulty
    difficulty_label = ctk.CTkLabel(app, text="Choose the level of difficulty:")
    difficulty_label.pack()
    difficulty_var = ctk.StringVar(value="1")
    difficulty_optionmenu = ctk.CTkOptionMenu(app, variable=difficulty_var, values=["1", "2", "3"])
    difficulty_optionmenu.pack(pady=10)

    # Choose the board size
    board_size_label = ctk.CTkLabel(app, text="Choose the board:")
    board_size_label.pack()
    board_size_var = ctk.StringVar(value="8x8")
    board_size_optionmenu = ctk.CTkOptionMenu(app, variable=board_size_var, values=["8x8", "10x10", "12x12"])
    board_size_optionmenu.pack(pady=10)

    # Start Game button
    start_game_button = ctk.CTkButton(app, text="Start Game", command=lambda: start_game_with_settings(mode="player_vs_computer",
        color=color_var.get(), difficulty=difficulty_var.get(), board_size=board_size_var.get()))
    start_game_button.pack(pady=20)


def create_game_vs_player_settings():
    clear_window()

    title_label = ctk.CTkLabel(app, text="Create the new human vs human game: settings", font=("Roboto Medium", 16))
    title_label.pack(pady=20)

    # Choose the board size
    board_size_label = ctk.CTkLabel(app, text="Choose the board:")
    board_size_label.pack()
    board_size_var = ctk.StringVar(value="8x8")
    board_size_optionmenu = ctk.CTkOptionMenu(app, variable=board_size_var, values=["8x8", "10x10", "12x12"])
    board_size_optionmenu.pack(pady=10)

    # Start Game button
    start_game_button = ctk.CTkButton(app, text="Start Game", command=lambda: start_game_with_settings(mode="player_vs_player",
        board_size=board_size_var.get()))
    start_game_button.pack(pady=20)

# Helper function to clear the window
def clear_window():
    for widget in app.winfo_children():
        widget.destroy()


# Placeholder functions for setting the color and starting the game
def set_color(color):
    print(f"Color chosen: {color}")  # Placeholder action

def create_game_vs_computer_interface(mode, color, difficulty, board_size):
    clear_window()

    #Place for
    # This frame would be where the Pygame window is embedded or displayed
    game_frame = tk.Frame(app, width=600, height=600)
    game_frame.pack(side="left")

    # Start the Pygame loop in a new thread
    # Control buttons setup
    control_frame = ctk.CTkFrame(app)
    control_frame.pack(side="right", fill="both", expand=True)

    draw_button = ctk.CTkButton(control_frame, text="Offer a Draw", command=offer_draw)
    draw_button.pack(pady=10)

    surrender_button = ctk.CTkButton(control_frame, text="Surrender", command=surrender)
    surrender_button.pack(pady=10)

    analysis_bar_button = ctk.CTkButton(control_frame, text="Hide the Analysis Bar", command=toggle_analysis_bar)
    analysis_bar_button.pack(pady=10)

    return_button = ctk.CTkButton(control_frame, text="Return to the Main Menu", command=return_to_main_menu)
    return_button.pack(pady=10)

    start_pygame_thread(mode=mode, color=color, difficulty=difficulty, board_size=board_size)

def create_game_vs_player_interface(mode, board_size):
    clear_window()

    # Pygame integration setup
    # This frame would be where the Pygame window is embedded or displayed
    game_frame = tk.Frame(app, width=600, height=600)
    game_frame.pack(side="left")
    # run_pygame_loop() is a placeholder for your function to integrate Pygame

    # Control buttons setup
    control_frame = ctk.CTkFrame(app)
    control_frame.pack(side="right", fill="both", expand=True)

    draw_button = ctk.CTkButton(control_frame, text="Draw", command=draw)
    draw_button.pack(pady=10)

    surrender_button = ctk.CTkButton(control_frame, text="Red surrender", command=red_surrender)
    surrender_button.pack(pady=10)

    surrender_button = ctk.CTkButton(control_frame, text="White surrender", command=white_surrender)
    surrender_button.pack(pady=10)

    analysis_bar_button = ctk.CTkButton(control_frame, text="Hide the Analysis Bar", command=toggle_analysis_bar)
    analysis_bar_button.pack(pady=10)

    return_button = ctk.CTkButton(control_frame, text="Return to the Main Menu", command=return_to_main_menu)
    return_button.pack(pady=10)

    start_pygame_thread(mode=mode, board_size=board_size)

def draw():
    shared_state.game_actions["draw"] = True
    save_game("1-1")


def white_surrender():
    shared_state.game_actions["white_surrender"] = True
    save_game("0-2")


def red_surrender():
    shared_state.game_actions["red_surrender"] = True
    save_game("2-0")

def offer_draw():
    shared_state.game_actions["offer_draw"] = True

def surrender():
    shared_state.game_actions["surrender"] = True
    show_main_menu()

def toggle_analysis_bar():
    # Implement the functionality to show/hide the analysis bar
    pass

def return_to_main_menu():
    # Implement the functionality to return to the main menu
    shared_state.game_actions["end_game"] = True
    show_main_menu()

def save_game(result):
    save_window = ctk.CTkToplevel(app)
    save_window.title("Save Game Result")
    save_window.geometry("300x200")

    ctk.CTkLabel(save_window, text="Player 1 Name:").pack(pady=5)
    player1_entry = ctk.CTkEntry(save_window)
    player1_entry.pack(pady=5)

    ctk.CTkLabel(save_window, text="Player 2 Name:").pack(pady=5)
    player2_entry = ctk.CTkEntry(save_window)
    player2_entry.pack(pady=5)

    def submit_result():
        player1 = player1_entry.get()
        player2 = player2_entry.get()
        game_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_result_to_db(player1, player2, result, game_date)
        save_window.destroy()
        show_main_menu()

    submit_button = ctk.CTkButton(save_window, text="Submit", command=submit_result)
    submit_button.pack(pady=10)

def save_result_to_db(player1, player2, result, game_date):
    conn = sqlite3.connect('game_results.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO game_results (player1, player2, result, game_date) VALUES (?, ?, ?, ?)',
                   (player1, player2, result, game_date))
    conn.commit()
    conn.close()


app.mainloop()
