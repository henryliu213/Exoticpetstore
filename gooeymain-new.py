import tkinter as tk
from tkinter import messagebox, ttk
import pymysql

# Database connection
dbpets = pymysql.connect(
    host='localhost',
    user='root',
    password='MyNewPass',
    database='petshop'
)
curpets = dbpets.cursor()


def get_available_pets():
    curpets.execute("select distinct p.type FROM pets p where p.pid not in (select c.pid from contains c where c.pid is not null)") # comment out distinct
    return [(i[0], 1) for i in curpets.fetchall()]


def get_available_accs():
    curpets.execute("select distinct a.name from accessories a where a.aid NOT IN (select c.aid from contains c where c.aid is not null)")
    return [(i[0], 0) for i in curpets.fetchall()]


class PetStoreGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pet Store")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Initialize data
        self.cart = []
        #self.available_pets = ['Dog', 'Cat', 'Bird', 'Fish'] #TODO Change to get from db SHOULD BE DONE
        self.available_pets = get_available_pets()
        # print("self available pets is : ")
        # print(self.available_pets)
        #self.available_accessories = ['Collar', 'Leash', 'Bed', 'Food', 'Toy'] #TODO Get from db SHOULD BE DONE
        self.available_accessories = get_available_accs()
        # print("self. availabel access is : ")
        # print(self.available_accessories)
        self.user_name = ""

        # Display the name input screen
        self.name_screen()

    def name_screen(self):
        """Display a screen to enter the user's name."""
        self.clear_window()

        label = tk.Label(self.root, text="Welcome to the Pet Store!", font=("Arial", 20, "bold"))
        label.pack(pady=20)

        name_label = tk.Label(self.root, text="Please enter your name:", font=("Arial", 14))
        name_label.pack(pady=10)

        self.name_entry = tk.Entry(self.root, width=30, font=("Arial", 14))
        self.name_entry.pack(pady=10)

        submit_button = tk.Button(self.root, text="Submit", font=("Arial", 14),
                                  bg="#4CAF50", fg="white", command=self.set_user_name)
        submit_button.pack(pady=20)

    def set_user_name(self):
        """Set the user's name and transition to the store screen."""
        self.user_name = self.name_entry.get().strip()
        if not self.user_name:
            messagebox.showerror("Error", "Please enter a valid name.")
            return
        
        #TODO Set user in db if not in db, should work bc name is a unique value
        try:
            curpets.execute("insert into customers (name) values (%s)", (self.user_name,))
            dbpets.commit()
        except:
            dbpets.rollback()

        self.store_screen()

    def store_screen(self):
        """Display the pet store interface with available items."""
        self.clear_window()

        title_label = tk.Label(self.root, text=f"Welcome, {self.user_name}!", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        # Pets Section
        pets_frame = tk.Frame(self.root, padx=10, pady=10)
        pets_frame.pack(pady=10)
        pets_label = tk.Label(pets_frame, text="Available Pets", font=("Arial", 16, "bold"))
        pets_label.pack()

        for pet in self.available_pets:
            pet_button = tk.Button(pets_frame, text=pet[0].capitalize(), font=("Arial", 12), bg="#ADD8E6",
                                    command=lambda pet=pet: self.add_to_cart(pet))
            pet_button.pack(pady=5)

        # Accessories Section
        accs_frame = tk.Frame(self.root, padx=10, pady=10)
        accs_frame.pack(pady=10)
        accs_label = tk.Label(accs_frame, text="Available Accessories", font=("Arial", 16, "bold"))
        accs_label.pack()

        for acc in self.available_accessories:
            acc_button = tk.Button(accs_frame, text=acc[0].capitalize(), font=("Arial", 12), bg="#F5F5DC",
                                    command=lambda acc=acc: self.add_to_cart(acc))
            acc_button.pack(pady=5)

        # Cart and Actions Section
        actions_frame = tk.Frame(self.root)
        actions_frame.pack(pady=20)

        view_cart_button = tk.Button(actions_frame, text="View Cart", font=("Arial", 14),
                                     bg="#FFD700", command=self.view_cart)
        view_cart_button.grid(row=0, column=0, padx=10)

        purchase_button = tk.Button(actions_frame, text="Purchase Items", font=("Arial", 14),
                                     bg="#4CAF50", fg="white", command=self.purchase_items)
        purchase_button.grid(row=0, column=1, padx=10)

        view_orders_button = tk.Button(actions_frame, text="View Orders", font=("Arial", 14),
                                        bg="#87CEEB", command=self.view_orders)
        view_orders_button.grid(row=0, column=2, padx=10)

    def view_cart(self):
        """Display the current contents of the cart."""
        self.clear_window()

        cart_label = tk.Label(self.root, text="Your Cart", font=("Arial", 18, "bold"))
        cart_label.pack(pady=20)

        if self.cart:
            for item in self.cart:
                # Create a frame for each cart item with a "Remove" button
                item_frame = tk.Frame(self.root, pady=5)
                item_frame.pack()

                item_label = tk.Label(item_frame, text=f"{item[0].capitalize()} - {'Pet' if item[1] == 1 else 'Accessory'}",
                                      font=("Arial", 14))
                item_label.pack(side="left", padx=10)

                remove_button = tk.Button(item_frame, text="Remove", font=("Arial", 12),
                                          bg="#FF6347", fg="white",
                                          command=lambda item=item: self.remove_from_cart(item))
                remove_button.pack(side="right", padx=10)
        else:
            empty_label = tk.Label(self.root, text="Your cart is empty.", font=("Arial", 14), fg="red")
            empty_label.pack(pady=20)

        # Back button
        back_button = tk.Button(self.root, text="Back to Store", font=("Arial", 14),
                                bg="gray", fg="white", command=self.store_screen)
        back_button.pack(pady=20)

    def remove_from_cart(self, item):
        """Remove an item from the cart."""
        if item in self.cart:
            self.cart.remove(item)
            messagebox.showinfo("Removed from Cart", f"{item[0].capitalize()} has been removed from your cart!")
            self.view_cart()  # Refresh the cart view
        else:
            messagebox.showerror("Error", "Item not found in the cart.")

    def add_to_cart(self, item):
        """Add a pet or accessory to the cart."""
        self.cart.append(item)
        messagebox.showinfo("Added to Cart", f"{item[0].capitalize()} has been added to your cart!")

    def purchase_items(self):
        """Simulate purchasing items."""
        if not self.cart:
            messagebox.showerror("Error", "Your cart is empty! Add some items first.")
            return

        try:
            curpets.execute("INSERT INTO orders (odate) VALUES (CURRENT_DATE())")
            oid = curpets.lastrowid

            curpets.execute("SELECT cid FROM customers WHERE name = %s", (self.user_name,))
            cid = curpets.fetchone()[0]

            curpets.execute("INSERT INTO places (cid, oid) VALUES (%s, %s)", (cid, oid))

            for item in self.cart:
                if item[1] == 1:  # Pet
                    curpets.execute("SELECT pid FROM pets WHERE type = %s AND pid NOT IN (SELECT pid FROM contains) LIMIT 1", (item[0],))
                    pid = curpets.fetchone()[0]
                    curpets.execute("INSERT INTO contains (oid, pid) VALUES (%s, %s)", (oid, pid))
                else:  # Accessory
                    curpets.execute("SELECT aid FROM accessories WHERE name = %s AND aid NOT IN (SELECT aid FROM contains) LIMIT 1", (item[0],))
                    aid = curpets.fetchone()[0]
                    curpets.execute("INSERT INTO contains (oid, aid) VALUES (%s, %s)", (oid, aid))

            dbpets.commit()
            messagebox.showinfo("Success", "Your purchase was successful!")
        except Exception as e:
            dbpets.rollback()
            messagebox.showerror("Error", f"Failed to complete purchase: {e}")
        finally:
            self.cart.clear()
            self.store_screen()

    def view_orders(self):
        """Display user's orders."""
        self.clear_window()

        orders_label = tk.Label(self.root, text="Your Orders", font=("Arial", 18, "bold"))
        orders_label.pack(pady=20)

        curpets.execute(
            "SELECT o.oid FROM orders o JOIN places p ON o.oid = p.oid JOIN customers c ON p.cid = c.cid WHERE c.name = %s",
            (self.user_name,)
        )
        orders = curpets.fetchall()

        if orders:
            for oid in orders:
                order_button = tk.Button(
                    self.root,
                    text=f"Order #{oid[0]}",
                    font=("Arial", 14),
                    bg="#87CEEB",
                    command=lambda oid=oid[0]: self.show_order_details(oid)
                )
                order_button.pack(pady=5)
        else:
            no_orders_label = tk.Label(self.root, text="No orders found.", font=("Arial", 14), fg="red")
            no_orders_label.pack(pady=20)

        back_button = tk.Button(
            self.root,
            text="Back to Store",
            font=("Arial", 14),
            bg="gray",
            fg="white",
            command=self.store_screen
        )
        back_button.pack(pady=20)

    def show_order_details(self, orderid):
        """Display details of a specific order and provide a cancel option."""
        self.clear_window()

        title_label = tk.Label(self.root, text=f"Order #{orderid} Details", font=("Arial", 18, "bold"))
        title_label.pack(pady=20)

        curpets.callproc("getOrderInfo", (orderid,))
        details = curpets.fetchall()

        for detail in details:
            item_label = tk.Label(
                self.root,
                text=f"{detail[0]} - Count: {detail[1]}",
                font=("Arial", 14)
            )
            item_label.pack(pady=5)

        cancel_button = tk.Button(
            self.root,
            text="Cancel Order",
            font=("Arial", 14),
            bg="#FF6347",
            fg="white",
            command=lambda: self.cancel_order(orderid)
        )
        cancel_button.pack(pady=10)

        back_button = tk.Button(
            self.root,
            text="Back to Orders",
            font=("Arial", 14),
            bg="gray",
            fg="white",
            command=self.view_orders
        )
        back_button.pack(pady=20)

    def cancel_order(self, orderid):
        """Cancel the specified order."""
        try:
            curpets.execute("DELETE FROM orders WHERE oid = %s", (orderid,))
            dbpets.commit()
            messagebox.showinfo("Success", f"Order #{orderid} has been cancelled.")
            self.view_orders()
        except:
            dbpets.rollback()
            messagebox.showerror("Error", "Failed to cancel order.")

    def clear_window(self):
        """Clear the current window."""
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PetStoreGUI(root)
    root.mainloop()
