import tkinter as tk
from tkinter import messagebox

# List to store cart items
cart = []
pets = [
        {"type": "Dog", "name": "Bulldog", "icon": "🐶", "age": "2", "button": None},
        {"type": "Cat", "name": "Siamese", "icon": "🐱", "age": "3", "button": None},
        {"type": "Rabbit", "name": "Himalayan", "icon": "🐇", "age": "1", "button": None}
    ]

def refresh(self):
    self.destroy()
    self.__init__()


# Global variables for entry widgets
new_pet_name_entry = None
new_pet_age_entry = None
new_pet_type_entry = None

# Function declarations (to be implemented by you)
def add_to_cart(item):
    """Add the selected pet or accessory to the cart."""
    cart.append(item)
    update_cart_count()  # Update the cart count label
    messagebox.showinfo("Added to Cart", f"{item['name']} has been added to your cart!")

def add_pet_to_store():
    global pets
    """Add a new pet to the store inventory."""
    # Use global variables to access entry fields
    pet_name = new_pet_name_entry.get()
    pet_age = new_pet_age_entry.get()
    pet_type = new_pet_type_entry.get()
    pets.append({"type": pet_type, "name": pet_name, "icon": pet_type, "age": "1", "button": None})
    print(pets)
    root.update()
    # Add pet to store inventory (not implemented)
    messagebox.showinfo("Pet Added", f"Added {pet_name} ({pet_type}), Age: {pet_age} years to the store inventory!")

    # Clear fields after adding pet (optional)
    new_pet_name_entry.delete(0, tk.END)
    new_pet_age_entry.delete(0, tk.END)
    new_pet_type_entry.delete(0, tk.END)
    render()


def purchase():
    """Process the cart and display the contents."""
    if len(cart) == 0:
        messagebox.showwarning("Empty Cart", "Your cart is empty!")
    else:
        cart_contents = "\n".join([f"{item['name']} - {item['type']}" for item in cart])
        messagebox.showinfo("Cart Contents", f"Items in your cart:\n{cart_contents}")
        
    # Clear the cart after purchase (optional)
    cart.clear()
    update_cart_count()  # Update the cart count label

def update_cart_count():
    """Update the cart count label to reflect the number of items in the cart."""
    cart_count_label.config(text=f"Items in Cart: {len(cart)}")

"""Render the pet shop GUI after user name is provided."""
# Frame for the pet shop interface
pet_shop_frame = tk.Frame(root)

# Title label
title_label = tk.Label(pet_shop_frame, text="Welcome to the Pet Shop", font=("Arial", 16))
title_label.pack(pady=10)

# Cart count label
global cart_count_label
cart_count_label = tk.Label(pet_shop_frame, text="Items in Cart: 0", font=("Arial", 14))
cart_count_label.pack(pady=5)

# Frame for displaying pets
pet_frame = tk.Frame(pet_shop_frame)
pet_frame.pack(pady=20)

# Label for Pets section
pet_label = tk.Label(pet_frame, text="Pets Available", font=("Arial", 14))
pet_label.grid(row=0, column=0, columnspan=2, pady=10)

# Sample pet icons (buttons for simplicity, can use images in practice)
# Display pet icons and add them to the cart
def render():
    for i, pet in enumerate(pets):
        print(pet)
        if pet['button'] == None: 
            pet_button = tk.Button(pet_frame, text=pet["icon"], font=("Arial", 20), command=lambda p=pet: add_to_cart(p))
            pet_button.grid(row=1, column=i, padx=10, pady=10)
            pet["button"] = pet_button

# Frame for displaying accessories
accessory_frame = tk.Frame(pet_shop_frame)
accessory_frame.pack(pady=20)

# Label for Accessories section
accessory_label = tk.Label(accessory_frame, text="Accessories Available", font=("Arial", 14))
accessory_label.grid(row=0, column=0, columnspan=2, pady=10)

# Sample accessories
accessories = [
    {"name": "Collar", "type": "Accessory", "icon": "📿", "button": None},
    {"name": "Leash", "type": "Accessory", "icon": "🔗", "button": None},
    {"name": "Toy", "type": "Accessory", "icon": "🧸", "button": None}
]

# Display accessory icons and add them to the cart
for i, accessory in enumerate(accessories):
    accessory_button = tk.Button(accessory_frame, text=accessory["icon"], font=("Arial", 20), command=lambda a=accessory: add_to_cart(a))
    accessory_button.grid(row=1, column=i, padx=10, pady=10)
    accessory["button"] = accessory_button

# Frame for adding pets to the store inventory
add_pet_frame = tk.Frame(pet_shop_frame)
add_pet_frame.pack(pady=20)

# Label for adding a pet to the store
add_pet_label = tk.Label(add_pet_frame, text="Add a New Pet to Store Inventory", font=("Arial", 14))
add_pet_label.grid(row=0, column=0, columnspan=2, pady=10)

# Pet Type, Name, and Age Entry Fields for adding to the store inventory
new_pet_type_label = tk.Label(add_pet_frame, text="Pet Type:", font=("Arial", 12))
new_pet_type_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

new_pet_type_entry = tk.Entry(add_pet_frame, font=("Arial", 12))
new_pet_type_entry.grid(row=1, column=1, padx=5, pady=5)

new_pet_name_label = tk.Label(add_pet_frame, text="Pet Name:", font=("Arial", 12))
new_pet_name_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")

new_pet_name_entry = tk.Entry(add_pet_frame, font=("Arial", 12))
new_pet_name_entry.grid(row=2, column=1, padx=5, pady=5)

new_pet_age_label = tk.Label(add_pet_frame, text="Pet Age:", font=("Arial", 12))
new_pet_age_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")

new_pet_age_entry = tk.Entry(add_pet_frame, font=("Arial", 12))
new_pet_age_entry.grid(row=3, column=1, padx=5, pady=5)

# Button to add the pet to the store inventory
add_pet_button = tk.Button(add_pet_frame, text="Add Pet", command=add_pet_to_store)
add_pet_button.grid(row=4, column=0, columnspan=2, pady=10)

# Button to purchase the items in the cart
purchase_button = tk.Button(pet_shop_frame, text="Purchase", font=("Arial", 12), command=purchase)
purchase_button.pack(pady=20)

# Exit button
exit_button = tk.Button(pet_shop_frame, text="Exit", font=("Arial", 12), command=root.quit)
exit_button.pack(pady=20)

# Show the pet shop interface
pet_shop_frame.pack(pady=20)

# Function to handle user login and proceed to pet shop
def show_shop():
    """Show the pet shop interface after user has entered their name."""
    user_name = user_name_entry.get()
    if user_name.strip() == "":
        messagebox.showwarning("Input Error", "Please enter your name!")
    else:
        # Hide login frame and render pet shop interface
        login_frame.pack_forget()
        render()

# Create the main window
root = tk.Tk()
root.title("Pet Shop Store")
root.geometry("800x600")

# Frame for the user's name (Login Screen)
login_frame = tk.Frame(root)
login_frame.pack(pady=100)

# Label for user name entry
user_name_label = tk.Label(login_frame, text="Please Enter Your Name:", font=("Arial", 14))
user_name_label.pack(pady=10)

# User Name Entry Field
user_name_entry = tk.Entry(login_frame, font=("Arial", 12))
user_name_entry.pack(pady=5)

# Button to confirm name and proceed to the shop
confirm_name_button = tk.Button(login_frame, text="Confirm Name", font=("Arial", 12), command=show_shop)
confirm_name_button.pack(pady=20)

# Start the main loop
root.mainloop()
