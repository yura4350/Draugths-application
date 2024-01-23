import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import sqlite3

def query_database(db_file, query):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def load_data_into_treeview(treeview, db_file, query):
    treeview.delete(*treeview.get_children())
    rows = query_database(db_file, query)
    for row in rows:
        treeview.insert('', tk.END, values=row)

def load_game_history():
    root = ctk.CTk()
    root.title("Game History")

    # Using standard ttk.Treeview here as customtkinter does not have CTkTreeview
    tree = ttk.Treeview(root, columns=("col1", "col2", "col3", "col4", "col5"), show='headings')
    tree.heading('col1', text='Game number')
    tree.heading('col2', text='Player 1')
    tree.heading('col3', text='Player 2')
    tree.heading('col4', text='Results')
    tree.heading('col5', text='Date of the game')
    tree.pack(fill='both', expand=True)

    load_data_into_treeview(tree, 'game_results.db', 'SELECT * FROM game_results')

    return_button = ctk.CTkButton(root, text="Return to Main Menu", command=root.destroy)
    return_button.pack(pady=20)

    root.mainloop()

