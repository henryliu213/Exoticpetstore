import tkinter as tk
from tkinter import messagebox
import pymysql

class PetOrderingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pet Ordering System")
        self.root.geometry("800x600")

        # Database Connection Setup
        self.dbpets = pymysql.connect(
            host='localhost',
            user='root',
            password='MyNewPass',
            database='petshop'
        )
        self.curpets = self.dbpets.cursor()

        # Header Section
        self.header_frame = tk.Frame(self.root, bg="lightblue", height=80)
        self.header_frame.pack(fill="x")
        self.header_label = tk.Label(self.header_frame, text="Welcome to Pet Ordering System", font=("Arial", 24), bg="lightblue")
        self.header_label.pack(pady=20)

        # Main Content Area to Display Pet Listings and Forms
        self.content_frame = tk.Frame(self.root, bg="white")
        self.content_frame.pack(fill="both", expand=True)

        self.pet_info_label = tk.Label(self.content_frame, text="Select a category to view pets", font=("Arial", 18), bg="white")
        self.pet_info_label.pack(pady=20)

        # Category Buttons - Allow the user to choose the pet type
        self.category_frame = tk.Frame(self.content_frame, bg="white")
        self.category_frame.pack(pady=20)

        self.dogs_button = tk.Button(self.category_frame, text="Dogs", width=20, command=lambda: self.show_pets("Dog"))
        self.dogs_button.pack(side="left", padx=5)

        self.cats_button = tk.Button(self.category_frame, text="Cats", width=20, command=lambda: self.show_pets("Cat"))
        self.cats_button.pack(side="left", padx=5)

        self.birds_button = tk.Button(self.category_frame, text="Birds", width=20, command=lambda: self.show_pets("Bird"))
        self.birds_button.pack(side="left", padx=5)

        self.fish_button = tk.Button(self.category_frame, text="Fish", width=20, command=lambda: self.show_pets("Fish"))
        self.fish_button.pack(side="left", padx=5)

        self.small_animals_button = tk.Button(self.category_frame, text="Others", width=20, command=lambda: self.show_pets("Small Animal"))
        self.small_animals_button.pack(side="left", padx=5)

        # Listbox for displaying selected pets
        self.pet_listbox = tk.Listbox(self.content_frame, width=50, height=10, font=("Arial", 14))
        self.pet_listbox.pack(pady=20)

        # Order Button (appears when a pet is selected)
        self.order_button = tk.Button(self.content_frame, text="Order Pet", width=20, state="disabled", command=self.order_pet)
        self.order_button.pack(pady=10)

        # Insert Pet Section
        self.insert_pet_label = tk.Label(self.content_frame, text="Insert a New Pet", font=("Arial", 18), bg="white")
        self.insert_pet_label.pack(pady=10)

        # Entry fields for inserting new pet
        self.pet_name_label = tk.Label(self.content_frame, text="Pet Name:", font=("Arial", 14), bg="white")
        self.pet_name_label.pack(pady=5)
        self.pet_name_entry = tk.Entry(self.content_frame, font=("Arial", 14))
        self.pet_name_entry.pack(pady=5)

        self.pet_type_label = tk.Label(self.content_frame, text="Pet Type (Species):", font=("Arial", 14), bg="white")
        self.pet_type_label.pack(pady=5)
        self.pet_type_entry = tk.Entry(self.content_frame, font=("Arial", 14))
        self.pet_type_entry.pack(pady=5)

        self.pet_age_label = tk.Label(self.content_frame, text="Pet Age:", font=("Arial", 14), bg="white")
        self.pet_age_label.pack(pady=5)
        self.pet_age_entry = tk.Entry(self.content_frame, font=("Arial", 14))
        self.pet_age_entry.pack(pady=5)

        # Insert Pet Button
        self.insert_pet_button = tk.Button(self.content_frame, text="Insert Pet", width=20, command=self.insert_pet)
        self.insert_pet_button.pack(pady=10)

        # Insert Customer Section
        self.insert_customer_label = tk.Label(self.content_frame, text="Insert a New Customer", font=("Arial", 18), bg="white")
        self.insert_customer_label.pack(pady=10)

        # Entry fields for inserting new customer
        self.customer_name_label = tk.Label(self.content_frame, text="Customer Name:", font=("Arial", 14), bg="white")
        self.customer_name_label.pack(pady=5)
        self.customer_name_entry = tk.Entry(self.content_frame, font=("Arial", 14))
        self.customer_name_entry.pack(pady=5)

        # Insert Customer Button
        self.insert_customer_button = tk.Button(self.content_frame, text="Insert Customer", width=20, command=self.insert_customer)
        self.insert_customer_button.pack(pady=10)

        # Insert Order Section
        self.insert_order_label = tk.Label(self.content_frame, text="Insert an Order", font=("Arial", 18), bg="white")
        self.insert_order_label.pack(pady=10)

        # Insert Order Button
        self.insert_order_button = tk.Button(self.content_frame, text="Insert Order", width=20, command=self.insert_order)
        self.insert_order_button.pack(pady=10)

        # Insert Accessories Section
        self.insert_accessory_label = tk.Label(self.content_frame, text="Insert an Accessory", font=("Arial", 18), bg="white")
        self.insert_accessory_label.pack(pady=10)

        # Entry fields for inserting new accessory
        self.accessory_name_label = tk.Label(self.content_frame, text="Accessory Name:", font=("Arial", 14), bg="white")
        self.accessory_name_label.pack(pady=5)
        self.accessory_name_entry = tk.Entry(self.content_frame, font=("Arial", 14))
        self.accessory_name_entry.pack(pady=5)

        # Insert Accessory Button
        self.insert_accessory_button = tk.Button(self.content_frame, text="Insert Accessory", width=20, command=self.insert_accessory)
        self.insert_accessory_button.pack(pady=10)

    def insert_pet(self):
        # Get data from the input fields
        pet_name = self.pet_name_entry.get().strip()
        pet_type = self.pet_type_entry.get().strip()
        pet_age = self.pet_age_entry.get().strip()

        # Validate the input
        if not pet_name or not pet_type or not pet_age:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            pet_age = int(pet_age)
            if pet_age < 0:
                raise ValueError("Age cannot be negative.")
        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid age: {ve}")
            return

        # Insert the pet into the database
        try:
            self.curpets.execute("INSERT INTO pets (name, type, age) VALUES (%s, %s, %s)", (pet_name, pet_type, pet_age))
            self.dbpets.commit()
            messagebox.showinfo("Success", f"{pet_name} has been added successfully!")
            
            # Clear the entry fields after successful insertion
            self.pet_name_entry.delete(0, tk.END)
            self.pet_type_entry.delete(0, tk.END)
            self.pet_age_entry.delete(0, tk.END)
        except pymysql.MySQLError as e:
            messagebox.showerror("Error", f"Failed to insert pet: {e}")

    def insert_customer(self):
        customer_name = self.customer_name_entry.get().strip()

        if not customer_name:
            messagebox.showerror("Error", "Please enter a customer name.")
            return

        try:
            self.curpets.execute("INSERT INTO customers (name) VALUES (%s)", (customer_name,))
            self.dbpets.commit()
            messagebox.showinfo("Success", f"Customer {customer_name} added successfully!")
            self.customer_name_entry.delete(0, tk.END)
        except pymysql.MySQLError as e:
            messagebox.showerror("Error", f"Failed to insert customer: {e}")

    def insert_order(self):
        # Create an order
        try:
            self.curpets.execute("INSERT INTO orders (odate) VALUES (CURDATE())")
            self.dbpets.commit()
            messagebox.showinfo("Success", "Order placed successfully!")
        except pymysql.MySQLError as e:
            messagebox.showerror("Error", f"Failed to place order: {e}")

    def insert_accessory(self):
        accessory_name = self.accessory_name_entry.get().strip()

        if not accessory_name:
            messagebox.showerror("Error", "Please enter an accessory name.")
            return

        try:
            self.curpets.execute("INSERT INTO accessories (name) VALUES (%s)", (accessory_name,))
            self.dbpets.commit()
            messagebox.showinfo("Success", f"Accessory {accessory_name} added successfully!")
            self.accessory_name_entry.delete(0, tk.END)
        except pymysql.MySQLError as e:
            messagebox.showerror("Error", f"Failed to insert accessory: {e}")

    def show_pets(self, pet_type):
        # Fetch pets of the selected type from the database
        self.curpets.execute("SELECT * FROM pets WHERE type = %s", (pet_type,))
        pets = self.curpets.fetchall()

        # Clear existing list
        self.pet_listbox.delete(0, tk.END)

        # Add new pet items
        if pets:
            for pet in pets:
                self.pet_listbox.insert(tk.END, f"{pet[1]} - Age: {pet[3]}")  # Name and Age
            self.order_button.config(state="normal")
        else:
            self.pet_info_label.config(text=f"No pets available in {pet_type} category.")

    def order_pet(self):
        selected_pet_index = self.pet_listbox.curselection()

        if selected_pet_index:
            selected_pet = self.pet_listbox.get(selected_pet_index)
            pet_name = selected_pet.split(" - ")[0]
            self.place_order(pet_name)
        else:
            messagebox.showerror("Error", "Please select a pet to order.")

    def place_order(self, pet_name):
        # Record the order in the 'orders' table
        self.curpets.execute("INSERT INTO orders (odate) VALUES (CURDATE())")
        order_id = self.curpets.lastrowid

        # Get the pet id
        self.curpets.execute("SELECT pid FROM pets WHERE name = %s", (pet_name,))
        pet = self.curpets.fetchone()
        if pet:
            pet_id = pet[0]
            self.curpets.execute("INSERT INTO contains (oid, pid) VALUES (%s, %s)", (order_id, pet_id))
            self.dbpets.commit()

            messagebox.showinfo("Order Confirmation", f"You have successfully ordered a {pet_name}!")
        else:
            messagebox.showerror("Error", "Pet not found in the database.")

# Main program execution
if __name__ == "__main__":
    root = tk.Tk()
    app = PetOrderingApp(root)
    root.mainloop()
