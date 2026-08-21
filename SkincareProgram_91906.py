# Marrisa Pheng - 91906 personalised skincare checker version 1
import tkinter as tk
from tkinter import messagebox
from product_database import product_database
from PIL import Image, ImageTk
import webbrowser # Allows links to be opened in the user's default web browser

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

# Class for storing user info
class SkincareChecker:
    def __init__(self):
        # Stores the user's personal info
        self.user_name=""
        self.user_age=""
        # Stores the user's selections
        self.selected_skin_type=""
        self.selected_skin_concerns=[]
        # Stores recommended products
        self.recommended_products=[]
        # Stores the selected skin concerns
        self.skin_concerns_var={}
        # Stores the selected ingredient warning preferences
        self.ingredient_preferences_var={}

    # Data and recommendation functions to help programmers understand
    def load_products(self):
        return product_database

    def get_skin_type(self):
        return self.skin_type_var.get()

    def validate_skin_type(self, selected_skin_type):
        if selected_skin_type in skin_type_options:
            return True
        else:
            return False

    def get_skin_concerns(self):
        selected_concerns = []
        for concern in self.skin_concerns_var:
            if self.skin_concerns_var[concern].get():
                selected_concerns.append(concern)
        return selected_concerns

    def validate_skin_concerns(self, answer):
        # Checks if at least one skin concern is selected
        if len(answer) > 0:
            return True
        else:
            return False

    # Gets the user's ingredient preferences that they want to avoid
    def get_ingredient_preferences(self):
        selected_preferences = []
        # Checks each ingredient to see if it has been selected
        for ingredient in self.ingredient_preferences_var:
            if self.ingredient_preferences_var[ingredient].get():
                # Adds selected preference to list
                selected_preferences.append(ingredient)
        return selected_preferences # Returns list of ingredients user wants to avoid
    
    # Removes products containing ingredients the user wants to avoid
    def filter_products_by_preferences(self, products):
        selected_preferences = self.get_ingredient_preferences()

        # If "None of the above" is selected, no products need to be removed
        if "None of the above" in selected_preferences:
            return products
        
        filtered_products = []

        for product in products:
            # Convert product ingredients to lowercase text
            product_ingredients = str(product["key_ingredients"]).lower()
            # Assume the product is suitable unless a warning ingredient is found
            contains_warning = False
            
            for ingredient in selected_preferences:
                if ingredient.lower() in product_ingredients:
                    contains_warning = True
            
            # Only keep products that dont contain a selected ingredient
            if contains_warning == False:
                filtered_products.append(product)

        return filtered_products
    def get_recommended_products(self, selected_skin_type, selected_concerns):
        # Search through product_database to find suitable match
        products = self.load_products() # Loads product from the product_database
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

# Class for the GUI
class SkincareGUI:
    def __init__(self, checker):
        global main_frame

        # Conncet the GUI to the checker
        self.checker = checker
        # Create the main window
        self.window = tk.Tk()
        self.window.title("Personalised Skincare Checker")
        self.window.geometry("1200x800")
        self.window.configure(bg="#FFF4F6")
        # Stores the selected skin type 
        self.checker.skin_type_var = tk.StringVar()
        # Create the main frame
        self.main_frame = tk.Frame(self.window, bg="#FFF4F6")
        self.main_frame.pack(padx=20,pady=10)
        # Connect older functions to keep them working
        main_frame = self.main_frame
        # Store the name and age input
        self.name_entry = None
        self.age_entry = None
        # Show the home page
        self.show_home()
    
    # Delete current page before showing new page
    def clear_screen(self):
        # Gets all widgets inside the main frame so they can be removed
        for widget in self.main_frame.winfo_children():
            widget.destroy()


    # GUI functions
    # Create MyGlow header for every page
    def make_header(self):
        header = tk.Label(self.main_frame, text="MyGlow", bg="#FFF4F6", fg="#3B2929", font=("Times", 26, "bold"))
        header.pack(pady=10)
        return header

    # Create a consistent label for every page
    def make_label(self, text, size):
        # Create a white label with background
        label = tk.Label(self.main_frame, text=text, bg="#FFF4F6", fg="#3B2929", font=("Times", size + 5, "bold")) # Increased all font size by 5 for better visibility
        label.pack(pady=10)
        return label

    # Create a consistent product image display
    def make_product_image(self, parent, image_path):
        # Load the product image and resize it to fit the GUI
        image = Image.open(image_path)
        image = image.resize((130, 130))  # Resize the image to fit within 130x130 pixels consistently

        # Convert the image to a format that Tkinter can use
        product_image = ImageTk.PhotoImage(image)

        # Create a label to display the image
        image_label = tk.Label(parent, image=product_image, bg="#F7EAE6")
        image_label.image = product_image  # Keep a reference to avoid garbage collection

        image_label.pack()
        return image_label

    # Home page
    def show_home(self):
        self.clear_screen()
        self.make_header()

        # Main box containing the logo and quote
        home_box = tk.Frame(self.main_frame, bg="#F7BAC9", width=1050, height=550)
        home_box.pack(padx=10, pady=10)
        home_box.pack_propagate(False)  # Prevent the frame from resizing to fit the content

        logo_box = tk.Frame(home_box, bg="#E493A9", width=330, height=500)
        logo_box.place(x=15, y=25)
        logo_box.grid_propagate(False)  # Prevent the frame from resizing to fit the content

        # Add MyGlow logo
        logo_image = Image.open("images/MyGlow_logo.png")
        logo_image = resize_decorative_image(logo_image,270,250)
        # Convert the image into a format that Tkinter can display
        logo_photo = ImageTk.PhotoImage(logo_image)
        # Create a label to display the logo image
        logo_label = tk.Label(logo_box, image=logo_photo, bg="#F7BAC9")
        logo_label.image = logo_photo # Keep a reference to the image
        logo_label.place(anchor="center", relx = 0.5, rely= 0.5) # Centre the logo

        # Quote area on the right side of the box
        quote_frame = tk.Frame(home_box, bg="#F7BAC9", width=660, height=500)
        quote_frame.place(x=370, y=25)
        quote_frame.grid_propagate(False)

        # Quote displayed beside the logo
        quote_label = tk.Label(quote_frame, text="Discover personalised skincare recommendations for you.", bg="#F7BAC9", fg="#3B2929", font=("Times", 50, "italic"), wraplength=520, justify="left")
        quote_label.place(x=30,y=25)

        # Add the decorative pink flower to the bottom right of the quote box
        flower_image = Image.open("images/pink_flower.png")
        flower_image = resize_decorative_image(flower_image,170,170)
        # Convert the flower image into a format Tkinter can display
        flower_photo = ImageTk.PhotoImage(flower_image)
        # Display the flower in the quote frame
        flower_label = tk.Label(quote_frame, image=flower_photo, bg="#F7BAC9")
        flower_label.image = flower_photo # Keep a reference so the image stays visible
        flower_label.place(x=465,y=320) # Position near bottom right

        # Start button
        make_button(self.main_frame, "Get started", self.show_about_you)

    # Show about you page
    def show_about_you(self):
        self.clear_screen()
        self.make_header()

        heading = self.make_label("Tell us about yourself", 20)

        # Enter name input
        name_label = tk.Label(self.main_frame, text="Name:", bg="#FFF4F6", fg="#3B2929", font=("Times", 20))
        name_label.pack(pady=5)

        self.name_entry = tk.Entry(self.main_frame, bg="#FCE4EA", fg="#3B2929", font=("Arial", 17), highlightbackground="white", highlightcolor="white", highlightthickness=2) # Added white widget border
        self.name_entry.pack(pady=5)

        # Enter age input
        age_label = tk.Label(self.main_frame, text="Age:", bg="#FFF4F6", fg="#3B2929", font=("Times", 20))
        age_label.pack(pady=5)

        self.age_entry = tk.Entry(self.main_frame, bg="#FCE4EA", fg="#3B2929", font=("Times", 17), highlightbackground="white", highlightcolor="white", highlightthickness=2) # Added white widget border
        self.age_entry.pack(pady=5)

        make_navigation(self.show_home, "Next", self.check_about_you)

    # About you page validation, checks the user's name and age
    def check_about_you(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        # Check that a name has been entered
        if name.strip() == "":
            messagebox.showerror("Error", "Please enter your name.")
            return
        # Check that an age has been entered
        if age == "":
            messagebox.showerror("Error", "Please enter your age.")
            return
        
        # Check that age is a valid number
        if age.isdigit() == False:
            messagebox.showerror("Error", "Please enter a valid age")
            return
        
        # Check that age is within a reasonable range
        if int(age) < 10 or int(age) > 100:
            messagebox.showerror("Error", "Please enter an age between 10 and 100")
            return
        
        # Store the info
        self.checker.user_name = name
        self.checker.user_age = age

        self.show_skin_type()

    # Show skin type page
    def show_skin_type(self):
        self.clear_screen()
        self.make_header()

        heading = self.make_label("What is your skin type?", 20)
        heading.pack(pady=10)

        instruction_label = self.make_label("Select your skin type", 14)
        instruction_label.pack(pady=10)

        # Create a fixed area for the images and skin type options
        skin_type_area = tk.Frame(self.main_frame, bg="#FFF4F6", width=1100, height=300)
        skin_type_area.pack(pady=10)
        skin_type_area.pack_propagate(False)
        # Add decorative face image on the left side of the skin type option
        left_face_image = Image.open("images/LadyFrontFace.png")
        left_face_image = resize_decorative_image(left_face_image,250,250)
        # Convert the left face image into a format Tkinter can display
        left_face_photo = ImageTk.PhotoImage(left_face_image)
        # Display the left face image
        left_face_label = tk.Label(skin_type_area, image=left_face_photo, bg="#FFF4F6")
        left_face_label.image = left_face_photo # Reference
        left_face_label.place(x=180, y=145, anchor="center")
        # Add decorative face image on the right side of the skin type option
        right_face_image = Image.open("images/LadyFrontFace.png")
        right_face_image = resize_decorative_image(right_face_image,250,250)
        # Convert the right face image into a format Tkinter can display
        right_face_photo = ImageTk.PhotoImage(right_face_image)
        # Display the right face image
        right_face_label = tk.Label(skin_type_area, image=right_face_photo, bg="#FFF4F6")
        right_face_label.image = right_face_photo # Reference
        right_face_label.place(x=920, y=145, anchor="center")

        # Create a frame to hold the skin type options
        options_frame = tk.Frame(skin_type_area, bg="#FFF4F6")
        options_frame.place(x=550, y=145, anchor="center")
        # Creates radio buttons for skin types
        for option in skin_type_options:
            radio_button = tk.Radiobutton(options_frame, text=option, value=option, variable=self.checker.skin_type_var, bg="#FFF4F6", fg="#3B2929", font=("Times", 20), anchor="w")
            radio_button.pack(anchor="w", pady=5)

        make_navigation(self.show_about_you, "Next", self.check_skin_type)

    # Checking if skin type is valid
    def check_skin_type(self):
        self.checker.selected_skin_type = (self.checker.get_skin_type())
        # Check if a skin type was selected
        if self.checker.validate_skin_type(self.checker.selected_skin_type) == False:
            messagebox.showerror("Error", "Please select a skin type.") # Error message
        else:
            self.show_skin_concerns()

    # Skin concerns page
    def show_skin_concerns(self):
        self.clear_screen()
        self.make_header()

        heading = self.make_label("What are your skin concerns?", 20)
        heading.pack(pady=10)

        instruction_label = self.make_label("Select your skin concerns", 14)
        instruction_label.pack(pady=10)

        # A fixed area for the image and skin concern options
        skin_concern_area = tk.Frame(self.main_frame, bg="#FFF4F6", width=1100, height=400)
        skin_concern_area.pack(pady=10)
        skin_concern_area.pack_propagate(False)

        # Add the decorative side face image to the left of the skin concern options
        side_face_image = Image.open("images/LadySideFace.png")
        side_face_image = resize_decorative_image(side_face_image,400,400)
        # Convert the image into a format Tkinter can display
        side_face_photo = ImageTk.PhotoImage(side_face_image)
        # Display the side face image
        side_face_label = tk.Label(skin_concern_area, image=side_face_photo, bg="#FFF4F6")
        side_face_label.image = side_face_photo # Reference
        side_face_label.place(x=150, y=200, anchor="center")

        # Create a frame to hold the skin concern options
        concerns_frame = tk.Frame(skin_concern_area, bg="#FFF4F6")
        concerns_frame.place(x=550, y=200, anchor="center")
        # Creates checkboxes for skin concerns
        for concern in skin_concern_options:
            self.checker.skin_concerns_var[concern] = tk.BooleanVar() # Creates a BooleanVar for each skin concern to track if it is selected or not
            checkbox = tk.Checkbutton(concerns_frame, text=concern, variable=self.checker.skin_concerns_var[concern], bg="#FFF4F6", fg="#3B2929", font=("Times", 20), anchor="w")
            checkbox.pack(anchor="w", padx=4)

        make_navigation(self.show_skin_type, "Next", self.check_skin_concerns)

    def check_skin_concerns(self):
        answer = self.checker.get_skin_concerns()
        if self.checker.validate_skin_concerns(answer) == False:
            messagebox.showerror("Error", "Please select at least one skin concern.")
        else:
            self.checker.selected_skin_concerns = answer
            self.show_ingredient_preferences()
    
    # Ingredient warnings and preferences page
    def show_ingredient_preferences(self):
        self.clear_screen()
        self.make_header()

        heading = self.make_label("Ingredient warnings & preferences", 20)
        heading.pack(pady=10)

        instruction_label = self.make_label("Let us know if you want to avoid certain ingredients", 12)
        instruction_label.pack(pady=5)

        # Create a frame to hold the preference options
        preferences_frame = tk.Frame(self.main_frame, bg="#FFF4F6")
        preferences_frame.pack(pady=10)

        # List of ingredient warning preferences
        ingredient_options = [
            "Parabens",
            "Fragrances",
            "Alcohol",
            "Sulfates",
            "Retinol",
            "None of the above"
        ]

        # Create checkboxes for each preference
        for ingredient in ingredient_options:
            self.checker.ingredient_preferences_var[ingredient] = tk.BooleanVar() # Boolean to store whether the ingredient is selected
            # Checkbox for preferences
            checkbox = tk.Checkbutton(preferences_frame, text=ingredient, variable=self.checker.ingredient_preferences_var[ingredient], bg="#FFF4F6", fg="#3B2929", font=("Times", 20), anchor="w")
            checkbox.pack(anchor="w", pady=3)
        
        # Navigation buttons
        make_navigation(self.show_skin_concerns, "Next", self.check_ingredient_preferences)
    
    # Check ingredient preferences and filters the recommended products
    def check_ingredient_preferences(self):
        # Find products matching the user's skin type and skin concerns
        recommended_products = self.checker.recommended_products = self.checker.get_recommended_products(self.checker.selected_skin_type, self.checker.selected_skin_concerns)
        
        # Remove products which contain ingredient sthe user wants to avoid
        self.checker.recommended_products = self.checker.filter_products_by_preferences(recommended_products)

        # Show the filtered products in results page
        self.show_results()

    # Results page
    def show_results(self):
        self.clear_screen()
        self.make_header()

        heading = self.make_label("Your Recommended Products", 20)
        heading.pack(pady=10)

        # Add the pink flower to the top left of the results page
        flower_image = Image.open("images/pink_flower.png")
        flower_image = resize_decorative_image(flower_image,100,100)
        # Convert the flower image into a format Tkinter can display
        flower_photo = ImageTk.PhotoImage(flower_image)
        # Display the flower on the top lef side of the results page
        flower_label = tk.Label(main_frame, image=flower_photo, bg="#FFF4F6")
        flower_label.image = flower_photo # Reference
        flower_label.place(x=30, y=105)

        # Frame to hold the canvas and scrollbar
        scroll_area = tk.Frame(self.main_frame, bg="#FFF4F6", width=1100, height=430)
        scroll_area.pack(padx=10, pady=5)
        scroll_area.pack_propagate(False)  # Prevent the frame from resizing to fit the canvas

        # Creates a canvas to display all recommended products
        canvas = tk.Canvas(scroll_area, bg="#FFF4F6", height=500)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Creates a scrollbar for the canvas
        scrollbar = tk.Scrollbar(scroll_area, orient=tk.VERTICAL, command=canvas.yview, bg="#E493A9")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)

        product_frame = tk.Frame(canvas, bg="#FFF4F6")
        # Put the product_frame inside the canvas
        canvas_window = canvas.create_window((0, 0), window=product_frame, anchor="nw")

    # Function to make the product boxes automatically stretch to the width of the canvas
        def resize_product_frame(event):
            # Changes the width of the product frame to match the width of the canvas
            canvas.itemconfig(canvas_window, width=event.width)
        # Calls the resize_product_frame function whenever the canvas is resized
        canvas.bind("<Configure>", resize_product_frame)

        # Displays each product in a simple box
        for product in self.checker.recommended_products:

            product_box = tk.Frame(product_frame, bg="#F7BAC9", height=170, padx=15, pady=15)
            product_box.pack(padx=5, pady=5, fill=tk.X)
            product_box.pack_propagate(False)  # Prevent the frame from resizing to fit the content
            product_box.grid_columnconfigure(1, weight=1)  # Make the product info expand to fill available space

            # Frame for product image on the left
            image_frame = tk.Frame(product_box, bg="#F7EAE6", width=130, height=130)
            image_frame.grid(row=0, column=0, padx=5, pady=15, sticky="n")
            image_frame.grid_propagate(False)  # Prevent the frame from resizing to fit the image

            # Display specific product image
            self.make_product_image(image_frame, product["image"])

            # Frame for product info on the left
            information_frame = tk.Frame(product_box, bg="#F7BAC9")
            information_frame.grid(row=0, column=1, padx=5, pady=15, sticky="nsew")
            information_frame.grid_propagate(False)
            
            product_name = tk.Label(information_frame, text=product["name"], bg="#F7BAC9", fg="#3B2929", font=("Times", 16, "bold"), wraplength=600, justify="left")
            product_name.pack(anchor="w", pady=5)

            product_description = tk.Label(information_frame, text=product["description"], bg="#F7BAC9", fg="#3B2929", font=("Times", 14), wraplength=600, justify="left")
            product_description.pack(anchor="w", pady=5)

            product_ingredients = tk.Label(information_frame, text="Key ingredients: " + str(product["key_ingredients"]), bg="#F7BAC9", fg="#3B2929", font=("Times", 14), wraplength=600, justify="left")
            product_ingredients.pack(anchor="w", pady=5)

            product_price = tk.Label(information_frame, text="Price: $" + str(product["price"]), bg="#F7BAC9", fg="#3B2929", font=("Times", 14), justify="left")
            product_price.pack(anchor="w", pady=5)

            # Frame for where to buy button for each product on the right
            button_frame = tk.Frame(product_box, bg="#F7BAC9", width=180, height=140)
            button_frame.grid(row=0, column=2, padx=10, pady=15, sticky="nsew")
            button_frame.grid_propagate(False)

            # White border around the "Buy" button
            buy_border = tk.Frame(button_frame, bg="white", padx=1, pady=1)
            buy_border.place(relx=0.5, rely=0.5, anchor="center")
            # Buy button
            buy_button = tk.Label(buy_border, text="Buy", bg="#E493A9", fg="#3B2929", font=("Times", 35)) # Changed buy button to a label for consistency with other buttons
            buy_button.pack(pady=5, padx=5)
            # Makes the buy button clickable
            buy_button.bind("<Button-1>", lambda event, selected_product=product: self.show_where_to_buy(selected_product))

        # Updates the scrollbar to match the size of the canvas
        product_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
            
        # Navigation buttons to go back or save results
        make_navigation(self.show_skin_concerns, "Save results", self.save_results)

    # Where to buy page
    def show_where_to_buy(self, product):
        self.clear_screen()
        self.make_header()

        # Header for where to buy page
        heading = self.make_label("Where to buy", 20)
        heading.pack(pady=10)

        # Add the pink flower to the top right of the page
        flower_image = Image.open("images/pink_flower.png")
        flower_image = resize_decorative_image(flower_image,110,110)
        # Convert the flower image into a format Tkinter can display
        flower_photo = ImageTk.PhotoImage(flower_image)
        # Display the flower near the top right of the page
        flower_label = tk.Label(self.main_frame, image=flower_photo, bg="#FFF4F6")
        flower_label.image = flower_photo # Reference
        flower_label.place(x=980,y=90, anchor="ne")
        # Frame to hold the product image and information
        product_area = tk.Frame(self.main_frame, bg="#FFF4F6", width=1000, height=360)
        product_area.pack(padx=20, pady=10)
        product_area.pack_propagate(False)  # Prevent the frame from resizing to fit the content

        # Product image on the left side
        image_frame = tk.Frame(product_area, bg="#F7BAC9", width=220, height=280)
        image_frame.grid(row=0, column=0, padx=20, pady=10, sticky="n")
        image_frame.grid_propagate(False)  # Prevent the frame from resizing to fit the image
        # Load the product image
        product_image = Image.open(product["image"])
        # Resize the product image to fit
        product_image = product_image.resize((190, 250))
        # Convert the image to a format that Tkinter can use
        product_image = ImageTk.PhotoImage(product_image)
        # Display the product image
        product_image_label = tk.Label(image_frame, image=product_image, bg="#F7EAE6")
        product_image_label.image = product_image  # Keep a reference so the image doesnt disappear
        product_image_label.pack(padx=10, pady=10)

        # Product information on the right side
        # Create a frame for the product information
        information_frame = tk.Frame(product_area, bg="#FFF4F6")
        information_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nw")
        information_frame.grid_propagate(False)

        # Display product name
        product_name = tk.Label(information_frame, text=product["name"], bg="#FFF4F6", fg="#3B2929", font=("Times", 18, "bold"), wraplength=600, justify="left")
        product_name.pack(anchor="w")

        # Display product description
        product_description = tk.Label(information_frame, text=product["description"], bg="#FFF4F6", fg="#3B2929", font=("Times", 16), wraplength=600, justify="left")
        product_description.pack(anchor="w")

        # Display product price
        product_price = tk.Label(information_frame, text="Price: $"+str(product["price"]), bg="#FFF4F6", fg="#3B2929", font=("Times", 16))
        product_price.pack(anchor="w")

        # Display product key ingredients
        product_ingredients = tk.Label(information_frame, text="Key ingredients: " + str(product["key_ingredients"]), bg="#FFF4F6", fg="#3B2929", font=("Times", 14), wraplength=600, justify="left")
        product_ingredients.pack(anchor="w")

        # Where to buy
        # Information about where to buy the product
        instruction_label = tk.Label(information_frame, text="Where to buy:", bg="#FFF4F6", fg="#3B2929", font=("Times", 18, "bold"))
        instruction_label.pack(anchor="w", pady=10)

        # Frame to hold shop logos
        shop_frame = tk.Frame(information_frame, bg="#FFF4F6")
        shop_frame.pack(anchor="w")

        # Display each shop logo and make it clickable to open the shop link
        for shop in product["where_to_buy"]:
            # Create a frame for each shop logo
            logo_box = tk.Frame(shop_frame, bg="#F7BAC9", width=210, height=100)
            logo_box.pack(side=tk.LEFT, padx=10, pady=5)
            logo_box.pack_propagate(False)
            # Load the shop logo image from product_database
            logo_image = Image.open(shop["logo"])
            # Resize the shop logo image to fit
            logo_image = logo_image.resize((180, 70))
            # Convert the image to a format that Tkinter can use
            logo_image = ImageTk.PhotoImage(logo_image)
            # Display the shop logo image
            logo_image_label = tk.Label(logo_box, image=logo_image, bg="#F7EAE6")
            # Keep a reference so the image doesn't disappear
            logo_image_label.image = logo_image
            logo_image_label.pack(expand=True, padx=5, pady=5)
            # Make the shop logo clickable to open the shop link
            logo_image_label.bind("<Button-1>", lambda event, url=shop["link"]: webbrowser.open(url))
            
        # Navigation buttons to go back to results page and home page
        make_navigation(self.show_results, "Home", self.show_home)

    # Save the user's answers and results to a text file
    def save_results(self):
        results_file = open("skincare_results.txt", "w")
        results_file.write("Personalised Skincare Checker Results\n")
        results_file.write("Name: " + self.checker.user_name + "\n")
        results_file.write("Age: " + self.checker.user_age + "\n")
        results_file.write("Skin Type: " + self.checker.selected_skin_type + "\n")
        results_file.write("Skin concerns: " + ", ".join(self.checker.selected_skin_concerns) + "\n")

        results_file.write("Recommended Products:\n")

        for product in self.checker.recommended_products:
            results_file.write("- " + product["name"] + ": " + product["description"] + "\n")
            results_file.write("Price: $" + str(product["price"]) + "\n")
            results_file.write("Key ingredients: " + str(product["key_ingredients"]) + "\n")

        results_file.close()
        messagebox.showinfo("Results saved", "Your results have been saved")
# Function to resize decorative images while keeping the original proportions
def resize_decorative_image(image, max_width, max_height):
    image = image.copy() # Make a copy of the original image so it is not changed
    # Resize the image to fit the given dimensions
    image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS) # A filter used in libraries (Pillow) to resize or scale images
    return image

# Create a consistent button for every page
def make_button(parent, text, command):
    # Create consistent buttons
    button = tk.Label(parent, text=text, bg="#E493A9", fg="#3B2929", font=("Times", 17), padx=25, pady=8)
    button.pack(pady=5)

    # Makes the button clickable and calls the command function when clicked (macOS compatible)
    button.bind("<Button-1>", lambda event: command())
    return button

# Create navigation buttons for every page
def make_navigation(back_command, next_text, next_command):
    # Create navigation buttons
    navigation_frame = tk.Frame(main_frame, bg="#FFF4F6")
    navigation_frame.pack(pady=10)

    back_button = tk.Label(navigation_frame, text="Back", bg="#E493A9", fg="#3B2929", font=("Times", 17), padx=25, pady=8) # Changed back button to a label for consistency with other buttons
    back_button.pack(side=tk.LEFT, padx=5)
    # Makes the back button clickable
    back_button.bind("<Button-1>", lambda event: back_command())

    next_button = tk.Label(navigation_frame, text=next_text, bg="#E493A9", fg="#3B2929", font=("Times", 17), padx=25, pady=8) # Changed next button to a label for consistency with other buttons
    next_button.pack(side=tk.RIGHT, padx=5)
    # Makes the next button clickable
    next_button.bind("<Button-1>", lambda event: next_command())

# Main program
def main():

    # Create the checker object
    checker = SkincareChecker()
    # Create the GUI
    gui = SkincareGUI(checker)
    # Run the program
    gui.window.mainloop()

main()
