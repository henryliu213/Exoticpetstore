import tkinter as tk
from tkinter import messagebox
import pymysql
dbpets = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'MyNewPass',
    database = 'petshop')
curpets = dbpets.cursor()

class PetStoreGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pet Store")
        self.cart = []
        self.available_pets = ['Dog', 'Cat', 'Bird', 'Fish'] #TODO Change to get from db
        self.available_accessories = ['Collar', 'Leash', 'Bed', 'Food', 'Toy'] #TODO Get from db
        self.user_name = ""
        self.orders =[] #GET FROM DB SHOULD BE A FUNCTIOn 

        # Start with the user name input screen
        self.name_screen()

    def name_screen(self):
        """Display a screen to enter the user's name."""
        self.clear_window()
        
        label = tk.Label(self.root, text="Please enter your name:")
        label.pack(pady=10)

        self.name_entry = tk.Entry(self.root, width=30)
        self.name_entry.pack(pady=10)

        submit_button = tk.Button(self.root, text="Submit", command=self.set_user_name)
        submit_button.pack(pady=10)

    def set_user_name(self):
        """Set the user's name and transition to the store screen."""
        self.user_name = self.name_entry.get()
        if not self.user_name:
            messagebox.showerror("Error", "Please enter a name.")
            return
        #TODO Set user in db if not in db.


        self.store_screen()

    # def welcome_screen(self): 
    #     """Display a welcome screen and move to the main store interface."""
    #     self.clear_window()

    #     welcome_label = tk.Label(self.root, text=f"Welcome, {self.user_name}!", font=("Arial", 16))
    #     welcome_label.pack(pady=20)

    #     browse_button = tk.Button(self.root, text="Browse Pets and Accessories", command=self.store_screen)
    #     browse_button.pack(pady=10)

    def store_screen(self):
        """Display the pet store interface with pets and accessories."""
        self.clear_window()

        # Display available pets
        pet_label = tk.Label(self.root, text="Available Pets:", font=("Arial", 14))
        pet_label.pack(pady=10)

        for pet in self.available_pets:
            pet_button = tk.Button(self.root, text=pet, command=lambda pet=pet: self.add_to_cart(pet))
            pet_button.pack(pady=5)

        # Display available accessories
        accessory_label = tk.Label(self.root, text="Available Accessories:", font=("Arial", 14))
        accessory_label.pack(pady=10)

        for accessory in self.available_accessories:
            accessory_button = tk.Button(self.root, text=accessory, command=lambda accessory=accessory: self.add_to_cart(accessory))
            accessory_button.pack(pady=5)

        # View Cart Button
        view_cart_button = tk.Button(self.root, text="View Cart", command=self.view_cart)
        view_cart_button.pack(pady=10)

        # Add Pet Button
        add_pet_button = tk.Button(self.root, text="Add a New Pet", command=self.add_pet)
        add_pet_button.pack(pady=10)

        # Purchase Button
        purchase_button = tk.Button(self.root, text="Purchase Items", command=self.purchase_items)
        purchase_button.pack(pady=10)

    def add_pet(self):
        """Allow the user to add a new pet to the pet store."""
        self.clear_window()
        
        pet_type_label = tk.Label(self.root, text="Enter pet type (e.g., Dog, Cat):")
        pet_type_label.pack(pady=5)
        
        pet_type_entry = tk.Entry(self.root, width=30)
        pet_type_entry.pack(pady=5)
        
        pet_name_label = tk.Label(self.root, text="Enter pet name:")
        pet_name_label.pack(pady=5)
        
        pet_name_entry = tk.Entry(self.root, width=30)
        pet_name_entry.pack(pady=5)
        
        pet_age_label = tk.Label(self.root, text="Enter pet age:")
        pet_age_label.pack(pady=5)
        
        pet_age_entry = tk.Entry(self.root, width=30)
        pet_age_entry.pack(pady=5)
        
        def submit_new_pet():
            pet_type = pet_type_entry.get()
            pet_name = pet_name_entry.get()
            pet_age = pet_age_entry.get()

            if pet_type and pet_name and pet_age:
                new_pet = {'type': pet_type, 'name': pet_name, 'age': pet_age}
                #TODO ADD TO DB 
                self.available_pets.append(new_pet['type']) #THIS SHOULD BE REPLACED BY GETTING FROM DB, WE CAN CREATE A FUNC
                messagebox.showinfo("Success", f"{pet_name} the {pet_type} has been added!")
                self.store_screen()
            else:
                messagebox.showerror("Error", "All fields must be filled in.")
        
        submit_button = tk.Button(self.root, text="Add Pet", command=submit_new_pet)
        submit_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Back to Store", command=self.store_screen)
        back_button.pack(pady=10)

    def add_to_cart(self, item):
        """Add a pet or accessory to the cart."""
        self.cart.append(item)
        messagebox.showinfo("Added to Cart", f"{item} has been added to your cart.")

    def view_cart(self):
        """Display the current contents of the cart."""
        self.clear_window()

        cart_label = tk.Label(self.root, text="Your Cart", font=("Arial", 14))
        cart_label.pack(pady=10)

        if self.cart:
            for item in self.cart:
                item_label = tk.Label(self.root, text=f"- {item}")
                item_label.pack(pady=5)
        else:
            empty_label = tk.Label(self.root, text="Your cart is empty.")
            empty_label.pack(pady=10)

        back_button = tk.Button(self.root, text="Back to Store", command=self.store_screen)
        back_button.pack(pady=10)

    def purchase_items(self):
        """Simulate purchasing items from the cart."""
        if self.cart:
            cart_contents = "\n".join(self.cart)
            messagebox.showinfo("Purchase Complete", f"Thank you for your purchase!\n\n{cart_contents}")
            self.cart.clear()  # Empty the cart after purchase
            #TODO UPDATE ORDERS, NEED TRANSACTION, 
                        #Create order, add contains for each item in cart, and places TRANSACTION!!!
        else:
            messagebox.showerror("Error", "Your cart is empty! Add some items first.")
    
    #TODO
    def order_screen(self): 
        """Display a order screen"""
        self.clear_window()

        welcome_label = tk.Label(self.root, text=f"Orders for , {self.user_name}!", font=("Arial", 16))
        welcome_label.pack(pady=20) 
        

        browse_button = tk.Button(self.root, text="Browse Pets and Accessories", command=self.store_screen)
        browse_button.pack(pady=10)



    def clear_window(self):
        """Clear the current window."""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PetStoreGUI(root)
    root.mainloop()
