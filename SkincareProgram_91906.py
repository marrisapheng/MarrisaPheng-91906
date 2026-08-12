# Marrisa Pheng - 91906 personalised skincare checker version 1
import tkinter as tk
from tkinter import messagebox
from product_database import product_database

# Skin types and Skin concerns lists
skin_type_options = ["normal","dry","oily","combination","sensitive"]
skin_concern_options = [
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
user_name = ""
user_age = ""
name_entry = None # Global variables for name and age so they can be accessed by other functions
age_entry = None

# Variables to store the user's answers
selected_skin_type = ""
selected_skin_concerns = []
recommended_products = []

# Data and recommendation functions to help programmers understand

def load_products():
    return product_database

def get_skin_type():
    return skin_type_var.get()

def validate_skin_type(selected_skin_type):
    if selected_skin_type in skin_type_options:
        return True
    else:
        return False

def get_skin_concerns():
    selected_concerns = []
    for concern in skin_concerns_var:
        if skin_concerns_var[concern].get():
            selected_concerns.append(concern)
    return selected_concerns

def validate_skin_concerns(answer):
    selected_concerns = get_skin_concerns()
    # Checks if at least one skin concern is selected
    if len(selected_concerns) > 0:
        return True
    else:
        return False
    
def get_recommended_products(selected_skin_type, selected_concerns):
    # Search through product_database to find suitable match
    products = load_products() # Loads product from the product_database
    matches = []

    for product in products:
        skin_type_matches = selected_skin_type in product["suitable_skin_types"]
        skin_concerns_matches = False

        for concern in selected_concerns:
            if concern in product["targeted_skin_concerns"]:
                skin_concerns_matches = True
                
        if skin_type_matches == True and skin_concerns_matches == True:
            matches.append(product)
        
        # If no matches are found, the program searches for products that match the skin type only
        if len(matches) == 0:
            for product in products:
                if selected_skin_type in product["suitable_skin_types"]:
                    matches.append(product)

    return matches

# GUI functions

# Delete current page before showing new page
def clear_screen():
    for widget in main_frame.winfo_children():
        widget.destroy()

def make_label(text, size):
    # Create a white label with background
    label = tk.Label(main_frame, text=text, bg="#111111", fg="white", font=("Arial", size))
    label.pack(pady=10)
    return label

def make_button(parent, text, command):
    # Create consistent buttons
    button = tk.Button(parent, command=command, text=text, bg="white", fg="black", font=("Arial", 12))
    button.pack(pady=5)
    return button

def make_navigation(back_command, next_text, next_command):
    # Create navigation buttons
    navigation_frame = tk.Frame(main_frame, bg="#111111")
    navigation_frame.pack(pady=10)

    back_button = tk.Button(navigation_frame, text="Back", command=back_command, bg="white", fg="black", font=("Arial", 12))
    back_button.pack(side=tk.LEFT, padx=5)

    next_button = tk.Button(navigation_frame, text=next_text, command=next_command, bg="white", fg="black", font=("Arial", 12))
    next_button.pack(side=tk.RIGHT, padx=5)

# Home page
def show_home():
    clear_screen()
    welcome_label = make_label("Welcome to the Skincare Checker!", 20)
    welcome_label.pack(pady=20)

    instruction_label = make_label("Get started with building your personalised skincare routine.", 14)
    instruction_label.pack(pady=10)

    start_button = make_button(main_frame, "Get started", show_about_you)
    start_button.pack(pady=20)

# Show about you page
def show_about_you():
    global name_entry, age_entry
    clear_screen()

    heading = make_label("Tell us about yourself", 20)
    heading.pack(pady=10)

    # Enter name input
    name_label = tk.Label(main_frame, text="Name:", bg="#111111", fg="white", font=("Arial", 14))
    name_label.pack(pady=5)

    name_entry = tk.Entry(main_frame, bg="white", fg="black", font=("Arial", 12))
    name_entry.pack(pady=5)

    # Enter age input
    age_label = tk.Label(main_frame, text="Age:", bg="#111111", fg="white", font=("Arial", 14))
    age_label.pack(pady=5)

    age_entry = tk.Entry(main_frame, bg="white", fg="black", font=("Arial", 12))
    age_entry.pack(pady=5)

    make_navigation(show_home, "Next", check_about_you)
# About you page validation
def check_about_you():
    global user_name, user_age
    name = name_entry.get()
    age = age_entry.get()

    # Check that a name has been entered
    if name == "":
        messagebox.showerror("Error", "Please enter your name.")
        return
    # Check that an age has been entered
    if age == "":
        messagebox.showerror("Error", "Please enter your age.")
        return
    
    user_name = name
    user_age = age

    show_skin_type()

# Show skin type page
def show_skin_type():
    clear_screen()

    heading = make_label("What is your skin type?", 20)
    heading.pack(pady=10)

    instruction_label = make_label("Select your skin type", 14)
    instruction_label.pack(pady=10)

    # Creates radio buttons for skin types
    for option in skin_type_options:
        radio_button = tk.Radiobutton(
            main_frame,
            text=option,
            value=option,
            variable=skin_type_var,
            bg="black",
            fg="white",
        )
        radio_button.pack(anchor="w", padx=20)

    make_navigation(show_about_you, "Next", check_skin_type)

# Checking if skin type is valid
def check_skin_type():
    global selected_skin_type
    # Gets the user's selected skin type
    selected_skin_type = get_skin_type()
    # Error message if no valid skin type is selected
    if validate_skin_type(selected_skin_type) == False:
        messagebox.showerror("Error", "Please select a skin type.")
    else:
        show_skin_concerns()

# Skin concerns page
def show_skin_concerns():
    clear_screen()

    heading = make_label("What are your skin concerns?", 20)
    heading.pack(pady=10)

    instruction_label = make_label("Select your skin concerns", 14)
    instruction_label.pack(pady=10)

    # Creates checkboxes for skin concerns
    for concern in skin_concern_options:
        skin_concerns_var[concern] = tk.BooleanVar()
        checkbox = tk.Checkbutton(
            main_frame,
            text=concern,
            variable=skin_concerns_var[concern],
            bg="#111111",
            fg="white",
        )
        checkbox.pack(anchor="w", padx=20)

    make_navigation(show_skin_type, "Next", check_skin_concerns)

def check_skin_concerns():
    global selected_skin_concerns, recommended_products
    answer = get_skin_concerns()
    if validate_skin_concerns(answer) == False:
        messagebox.showerror("Error", "Please select at least one skin concern.")
    else:
        selected_skin_concerns = answer
        recommended_products = get_recommended_products(selected_skin_type, selected_skin_concerns)
        show_results()

# Results page
def show_results():
    clear_screen()

    heading = make_label("Your Recommended Products", 20)
    heading.pack(pady=10)

    # Frame to hold the canvas and scrollbar
    scroll_area = tk.Frame(main_frame, bg="#111111")
    scroll_area.pack(fill=tk.BOTH, expand=True)

    # Creates a canvas to display all recommended products
    canvas = tk.Canvas(scroll_area, bg="#111111", height=400, width=500)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Creates a scrollbar for the canvas
    scrollbar = tk.Scrollbar(scroll_area, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    product_frame = tk.Frame(canvas, bg="#111111")
    canvas.create_window((0, 0), window=product_frame, anchor="nw")


    # Displays each product in a simple box
    for product in recommended_products:

        product_box = tk.Frame(product_frame, bg="#222222", padx=10, pady=10)
        product_box.pack(pady=5, fill=tk.X)

        # Frame for product info on the left
        information_frame = tk.Frame(product_box, bg="#222222")
        information_frame.pack(side=tk.LEFT, padx =5)
        
        product_name = tk.Label(information_frame, text=product["name"], bg="#222222", fg="white", font=("Arial", 14))
        product_name.pack(anchor="w")

        product_description = tk.Label(information_frame, text=product["description"], bg="#222222", fg="white", font=("Arial", 12), wraplength=450, justify="left")
        product_description.pack(anchor="w")

        product_ingredients = tk.Label(information_frame, text="Key ingredients: " + str(product["key_ingredients"]), bg="#222222", fg="white", font=("Arial", 12), wraplength=450, justify="left")
        product_ingredients.pack(anchor="w")

        product_price = tk.Label(information_frame, text="Price: $" + str(product["price"]), bg="#222222", fg="white", font=("Arial", 12))
        product_price.pack(anchor="w")

        # Frame for where to buy button for each product on the right
        button_frame = tk.Frame(product_box, bg="#222222")
        button_frame.pack(side=tk.RIGHT, padx=10)

        # Buy button
        buy_button = tk.Button(button_frame, text="Buy", command=lambda selected_product=product: show_where_to_buy(selected_product), bg="white", fg="black", font=("Arial", 12))
        buy_button.pack(pady=5)

    # Updates the scrollbar to match the size of the canvas
    product_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
        
    # Navigation buttons to go back or save results
    make_navigation(show_skin_concerns, "Save results", save_results)

# Where to buy page
def show_where_to_buy(product):
    clear_screen()

    heading = make_label("Where to buy", 20)
    heading.pack(pady=10)

    # Display product name
    product_name = tk.Label(main_frame, text=product["name"], bg="#111111", fg="white", font=("Arial", 14))
    product_name.pack(anchor="w")

    # Display product price
    product_price = tk.Label(main_frame, text="Price: $"+str(product["price"]), bg="#111111", fg="white", font=("Arial", 12))
    product_price.pack(anchor="w")

    # Information about where to buy the product
    instruction_label = make_label("Where to buy this product:", 12)
    instruction_label.pack(anchor="w")
    
    # Navigation buttons to go back to results page and home page
    make_navigation(show_results, "Home", show_home)

# Save the user's answers and results to a text file
def save_results():
    results_file = open("skincare_results.txt", "w")
    results_file.write("Personalised Skincare Checker Results\n")
    results_file.write("Name: " + user_name + "\n")
    results_file.write("Age: " + user_age + "\n")
    results_file.write("Skin Type: " + selected_skin_type + "\n")
    results_file.write("Skin concerns: " + ", ".join(selected_skin_concerns) + "\n")

    results_file.write("Recommended Products:\n")

    for product in recommended_products:
        results_file.write("- " + product["name"] + ": " + product["description"] + "\n")
        results_file.write("Price: $" + str(product["price"]) + "\n")
        results_file.write("Key ingredients: " + str(product["key_ingredients"]) + "\n")

    results_file.close()
    messagebox.showinfo("Results saved", "Your results have been saved")

# Main program
def main():
    global window, main_frame, skin_type_var

    # Create the main window
    window = tk.Tk()
    window.title("Personalised Skincare Checker")
    window.geometry("800x600")
    window.configure(bg="#111111")

    # Create the main frame
    main_frame = tk.Frame(window, bg="#111111")
    main_frame.pack(padx=20, pady=20)

    # Variable to store the selected skin type
    skin_type_var = tk.StringVar()

    show_home()
    window.mainloop()

main()
