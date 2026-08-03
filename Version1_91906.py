# Marrisa Pheng - 91906 personalised skincare checker version 1
import tkinter as tk
from tkinter import messagebox
from product_database import product_database

# Skin types and Skin concerns lists
skin_type = ["normal","dry","oily","combination","sensitive"]
skin_concerns = [
    "acne",
    "dull",
    "dry",
    "sensitive",
    "fine lines",
    "clogged pores",
    "texture",
    "loose skin",
]

# Global variables used by different functions
window = None
main_frame = None
skin_type_var = None
skin_concerns_var = {}
# Variables to store the user's answers
skin_type = ""
skin_concerns = []
recommended_products = []  

# Data and recommendation functions

def load_products():
    return product_database

def get_skin_type():
    return skin_type_var.get()

def validate_skin_type(selected_skin_type):
    if selected_skin_type in skin_type:
        return True
    else:
        return False

def get_skin_concerns():
    selected_concerns = []
    for concern in skin_concerns_var:
        if skin_concerns_var[concern].get():
            selected_concerns.append(concern)
    return selected_concerns

def validate_skin_concerns():
    selected_concerns = get_skin_concerns()
    # Checks if at least one skin concern is selected
    if len(selected_concerns) > 0:
        return True
    else:
        return False
    
def get_recommended_products(selected_skin_type, selected_concerns):
    # Search through product_database tp find suitable match
    products = load_products()
    matches = []

    for product in products:
        skin_type_matches = selected_skin_type in product["suitable_skin_types"]
        skin_concerns_matches = False

        for concern in selected_concerns:
            if concern in product["targeted_skin_concerns"]:
                skin_concerns_matches = True
                
        if skin_type_matches == True and skin_concerns_matches == True:
            matches.append(product)

    return matches

# GUI functions

# Delete current page before showing new page
def clear_screen():
    for widget in main_frame.winfo_children():
        widget.destroy()

def make_label(text, size):
    # Create a white label with background
    label = tk.Label(main_frame, text=text, bg="111111", fg="white", font=("Arial", size))
    label.pack(pady=10)
    return label

def make_button(parent, text, command):
    # Create consistent buttons
    button = tk.Button(parent, main_frame, command=command, text=text, bg="111111", fg="white", font=("Arial", 12))
    button.pack(pady=5)
    return button

def make_navigation(back_command, next_command):
    # Create navigation buttons
    navigation_frame = tk.Frame(main_frame, bg="111111")
    navigation_frame.pack(pady=10)

    back_button = tk.Button(navigation_frame, text="Back", command=back_command, bg="111111", fg="white", font=("Arial", 12))
    back_button.pack(side=tk.LEFT, padx=5)

    next_button = tk.Button(navigation_frame, text="Next", command=next_command, bg="111111", fg="white", font=("Arial", 12))
    next_button.pack(side=tk.RIGHT, padx=5)

