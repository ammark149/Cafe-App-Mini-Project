#!/usr/bin/env python3
"""Mini project CLI: cafe menu and basket management"""
import os
import json
from secrets import choice
import utils


########### MAIN APPLICATION ############

class CafeApp:

   
    #Initializes the CafeApp with empty lists for products, couriers, and orders
    def __init__(self):
        self.products = []
        self.couriers = []
        self.orders = []
        self.menus = {}
        self.inventory = []
        self.main_menu = None
        self.product_menu = None    
        self.courier_menu = None
        self.basket_menu = None
        self.product_edit_menu = None   
        self.order_management_menu = None
        self.order_edit_menu = None

    def run(self):
        # Importing csv files and menu json
        self.products = utils.load_data('./csv/products.csv')
        self.couriers = utils.load_data('./csv/couriers.csv')
        self.orders = utils.load_data('./csv/orders.csv')
        self.inventory = utils.load_data('./csv/inventory.csv')
        menus_data = utils.load_json('./menu/Menus.json')

        for name_id, menu_dict in menus_data.items():
            self.menus[name_id] = Menu(menu_dict, name=menu_dict.get('title', name_id)) 

        # Initialize Child Menus
        self.main_menu = MainMenu(self.menus['MainMenu'].menu_dict, name=self.menus['MainMenu'].name, app=self)
        self.product_menu = ProductMenu(self.menus['ProductMenu'].menu_dict, name=self.menus['ProductMenu'].name, app=self)
        self.courier_menu = CourierMenu(self.menus['CourierMenu'].menu_dict, name=self.menus['CourierMenu'].name, app=self)
        self.order_management_menu = OrderManagementMenu(self.menus['OrderManagementMenu'].menu_dict, name=self.menus['OrderManagementMenu'].name, app=self)
        self.order_edit_menu = Menu(self.menus['OrderEditMenu'].menu_dict, name=self.menus['OrderEditMenu'].name, app=self)

        while True:
            self.main_menu.handle()
            break
        ## TO DO - Save chnages to products and couriers back to csv files when exiting
        utils.save_data('./csv/products.csv', self.products)
        utils.save_data('./csv/couriers.csv', self.couriers)
        utils.save_data('./csv/orders.csv', self.orders)
        utils.save_data('./csv/inventory.csv', self.inventory)
        print("Data saved. Goodbye!")
        
     


############### MENU #################
class Menu:
    def __init__(self, menu_dict=None, name=None, app=None):
          
        self.name = name
        self.menu_dict = menu_dict or {}
        self.title = self.menu_dict.get("title", "Menu")
        self.app = app

    def __str__(self):
        result = "" 
        for key, value in self.menu_dict.items():
            result += f"Menu Key: {key} | Menu Value: {value}\n"
        
        return result.strip() # .strip() removes the very last extra newline

    def display(self):
        print(f"\n{self.title}")
        for key in self.menu_dict.keys():
            if key != "title":
                print(f"{key} - {self.menu_dict[key]}")
            else:
                continue
    
    def get_choice(self):
        valid_options = {k for k in self.menu_dict.keys() if k != "title"}
        
        while True:
            choice = input("Select option: ").strip()
            if choice in valid_options:
                return choice
            
            print(f"Invalid choice. Enter one of: {', '.join(sorted(valid_options, key=int))}")
            self.display()
    
    def get_valid_index(self, max_index, prompt="Select index: "):
        while True:
            try:
                index = int(input(prompt))
                if 0 <= index < max_index:
                    return index
                print(f"Invalid index. Enter a number between 0 and {max_index - 1}.")
            except ValueError:
                print("Please enter a valid number.")

    def handle(self, name=None):
        while True:
            self.display()
            choice = self.get_choice()
            if choice == "0":
                return
            self.route(choice)
    
    def route(self, choice):
        print(f"Selected option {choice} - {self.menu_dict.get(choice, 'Unknown Option')}")

class MainMenu(Menu):
    pass
    def handle(self, name=None):
    #     pass
        while True:
            self.display()
            choice = self.get_choice()
            if choice == "0":
                return
            self.route(choice)

    def route(self, choice):
            if choice == "1":
                self.app.product_menu.handle(self.app)
            elif choice == "2":
                self.app.courier_menu.handle(self.app)
            elif choice == "3":
                self.app.order_management_menu.handle(self.app)

########## Product Menu ###########
class ProductMenu(Menu):
    def handle(self, app_instance=None):
        while True:
            self.display()
            choice = self.get_choice()

            if choice == "0":
                break
            elif choice == "1":
                self._view_products(app_instance)
            elif choice == "2":
                self._create_product(app_instance)
            elif choice == "3":
                self._update_product(app_instance)
            elif choice == "4":
                self._delete_product(app_instance)
            elif choice == "5":                          # NEW
                self._view_inventory(app_instance)       # NEW
            elif choice == "6":                          # NEW
                self._update_stock(app_instance)         # NEW

    def _view_products(self, app_instance):
        if not app_instance.products:
            print("No products found.")
            return
        print("\n--- Products ---")
        for i, product in enumerate(app_instance.products):
            print(f"  [{i}] {product['name']}")

    def _create_product(self, app_instance):
        name = input("Enter new product name: ").strip()
        if name:
            app_instance.products.append({"name": name})
            print(f"'{name}' added.")
        else:
            print("Product name cannot be empty.")

    def _update_product(self, app_instance):
        self._view_products(app_instance)
        if not app_instance.products:
            return
        index = self.get_valid_index(len(app_instance.products), "Enter index of product to update: ")
        new_name = input("Enter new product name: ").strip()
        if new_name:
            app_instance.products[index]['name'] = new_name
            print(f"Product updated to '{new_name}'.")
        else:
            print("Name cannot be empty.")

    def _delete_product(self, app_instance):
        self._view_products(app_instance)
        if not app_instance.products:
            return
        index = self.get_valid_index(len(app_instance.products), "Enter index of product to delete: ")
        removed = app_instance.products.pop(index)
        print(f"'{removed['name']}' deleted.")

    def _view_inventory(self, app_instance):       # NEW
        if not app_instance.inventory:
            print("No inventory found.")
            return
        print(f"\n{'ID':<5} {'Name':<25} {'Price':<8} {'Sold':<8} {'Stock':<8}")
        print("-" * 55)
        for item in app_instance.inventory:
            print(f"  {item['id']:<5} {item['name']:<25} £{float(item['price']):<7.2f} {item['sold']:<8} {item['total_stock']:<8}")

    def _update_stock(self, app_instance):          #NEW
        self._view_inventory(app_instance)
        if not app_instance.inventory:
            return
        index = self.get_valid_index(len(app_instance.inventory), "Enter index of item to update stock: ")
        new_stock = input(f"Enter new stock level for '{app_instance.inventory[index]['name']}': ").strip()
        if new_stock.isdigit():
            app_instance.inventory[index]['total_stock'] = new_stock
            print("Stock updated.")
        else:
            print("Please enter a valid number.")

######## Courier Menu ###########
class CourierMenu(Menu):
    def handle(self, app_instance=None):
        while True:
            self.display()
            choice = self.get_choice()

            if choice == "0":
                break
            elif choice == "1":
                self._view_couriers(app_instance)
            elif choice == "2":
                self._add_courier(app_instance)
            elif choice == "3":
                self._update_existing_courier(app_instance)
            elif choice == "4":
                self._delete_courier(app_instance)

    def _view_couriers(self, app_instance):
        if not app_instance.couriers:
            print("No couriers found.")
            return

        print(f"\n{'ID':<3} | {'Name':<20} | {'Phone':<15}")
        print("-" * 45)
        for i, courier in enumerate(app_instance.couriers):
            print(
                f"[{i}] {courier.get('name',''):<20} | {courier.get('phone',''):<15}"
            )

    def _add_courier(self, app_instance):
        name = input("Enter courier name: ").strip()
        phone = input("Enter courier phone number: ").strip()
        if name:
            app_instance.couriers.append({
                "name": name,
                "phone": phone
            })
            print(f"Courier '{name}' added.")
        else:
            print("Name cannot be empty.")

    def _update_existing_courier(self, app_instance):
        self._view_couriers(app_instance)
        if not app_instance.couriers:
            return

        index = self.get_valid_index(len(app_instance.couriers), "Enter courier index to update: ")
        courier = app_instance.couriers[index]

        new_name = input(f"Enter new courier name (leave blank to keep '{courier.get('name','')}'): ").strip()
        new_phone = input(f"Enter new courier phone (leave blank to keep '{courier.get('phone','')}'): ").strip()

        if new_name:
            courier['name'] = new_name
        if new_phone:
            courier['phone'] = new_phone

        print(f"Courier updated: {courier.get('name')} | {courier.get('phone','')}.")

    def _delete_courier(self, app_instance):
        self._view_couriers(app_instance)
        if not app_instance.couriers:
            return

        index = self.get_valid_index(len(app_instance.couriers), "Enter courier index to delete: ")
        removed = app_instance.couriers.pop(index)
        print(f"Courier '{removed.get('name','')}' deleted.")

####### Order Management Menu ##########
class OrderManagementMenu(Menu):
    def handle(self, app_instance=None):
        while True:
            self.display()
            choice = self.get_choice()

            if choice == "0":
                break
            elif choice == "1": #View orders
                self.view_orders(app_instance)
            elif choice == "2": #Create Orders
                self.create_order(app_instance)
            elif choice == "3": #Update Existing Orders' status
                self.update_order_status(app_instance)
            elif choice == "4": #Edit Orders
                self.edit_order(app_instance)
            elif choice == "5": #Delete Orders
                self.delete_order(app_instance)

    # Choice 1 Viewing Orders
    def view_orders(self, app_instance):
        print("\n--- Current Orders ---")
        if not app_instance.orders:
            print("No orders found.")
            return
            
        for i, order in enumerate(app_instance.orders):
            print(f"[{i}] Customer: {order['customer_name']}")
            print(f"    Address: {order['customer_address']}")
            print(f"    Phone: {order['customer_phone']}")
            print(f"    Courier Index: {order['courier']}")
            print(f"    Status: {order['status']}")
            print(f"    Items: {order['items']}\n")

    #Choice 2 Creating Orders
    def create_order(self, app_instance):
        print("\n--- Create New Order ---")
        cust_name = input("Customer Name: ")
        cust_address = input("Customer Address: ")
        cust_phone = input("Customer Phone: ")
    
        #Print products with index
        print("\nAvailable Products:")
        for i, prod in enumerate(app_instance.products):
            print(f"[{i}] {prod['name']}")
        items = input("Enter product indexes (e.g. 1,2,5): ")

        #Print couriers with index
        if not app_instance.couriers:
            print("No couriers available. Add a courier first.")
            return
        print("\nAvailable Couriers:")
        for i, cour in enumerate(app_instance.couriers):
            print(f"[{i}] {cour['name']}")
        courier_idx = self.get_valid_index(len(app_instance.couriers), "Select courier index: ")

        #Create dictionary and append
        new_order = {
            "customer_name": cust_name,
            "customer_address": cust_address,
            "customer_phone": cust_phone,
            "courier": courier_idx,
            "status": "preparing",
            "items": items
        }
        app_instance.orders.append(new_order)
        print("Order created successfully!")

    #Choice 3 Updating Order Status
    def update_order_status(self, app_instance):
        if not app_instance.orders:
            print("No orders available.")
            return

        for i, order in enumerate(app_instance.orders):
            print(f"[{i}] {order['customer_name']} - {order['status']}")
        
        order_idx = self.get_valid_index(len(app_instance.orders), "Select order index to update: ")
        
        #Shows status for orders
        statuses = ["preparing", "ready", "out for delivery", "delivered"]
        for i, stat in enumerate(statuses):
            print(f"[{i}] {stat}")
        
        stat_idx = self.get_valid_index(len(statuses), "Select new status index: ")
        app_instance.orders[order_idx]['status'] = statuses[stat_idx]
        print("Status updated!")
    
    #Choice 4 Editing Orders
    def edit_order(self, app_instance):
        if not app_instance.orders:
            print("No orders available.")
            return

        for i, order in enumerate(app_instance.orders):
            print(f"[{i}] {order['customer_name']}")

        #Fail safe to return to menu
        user_input = input("Select order index to edit (or press Enter to cancel): ").strip()
        if user_input == "":
            print("Edit cancelled. Returning to Orders Menu.")
            return
        
        try:
            order_idx = int(user_input)
            if order_idx < 0 or order_idx >= len(app_instance.orders):
                print("Invalid index.")
                return
        except ValueError:
            print("Invalid input.")
        
        selected_order = app_instance.orders[order_idx]

        while True:
            app_instance.order_edit_menu.display()
            choice = app_instance.order_edit_menu.get_choice()

            if choice == "0":
                break
            elif choice == "1":
                selected_order['customer_name'] = input("Enter new name: ")
            elif choice == "2":
                selected_order['customer_address'] = input("Enter new address: ")
            elif choice == "3":
                selected_order['customer_phone'] = input("Enter new phone: ")
            elif choice == "4":
                statuses = ["preparing", "ready", "out for delivery", "delivered"]
                for i, stat in enumerate(statuses):
                    print(f"[{i}] {stat}")
                stat_idx = self.get_valid_index(len(statuses), "Select status index: ")
                selected_order['status'] = statuses[stat_idx]
        print("Order updated!")
    
    #Choice 5 Deleting Orders
    def delete_order(self, app_instance):
        print("\n--- Delete Order ---")
        
        if not app_instance.orders:
            print("No orders to delete.")
            return

        for i, order in enumerate(app_instance.orders):
            print(f"[{i}] {order['customer_name']} - {order['status']}")

        user_input = input("\nEnter order index to delete (or press Enter to cancel): ").strip()
        
        #Failsafe to return to main menu
        if user_input == "":
            print("Deletion cancelled. Returning to Orders Menu.")
            return
        try:
            order_idx = int(user_input)
            if order_idx < 0 or order_idx >= len(app_instance.orders):
                print("Invalid index choice. Returning to menu.")
                return
        except ValueError:
            print("Invalid input choice. Returning to menu.")
            return

        deleted_order = app_instance.orders.pop(order_idx)
        print(f"Successfully deleted order for: {deleted_order['customer_name']}")


# ################# MAIN APPLICATION LOOP #################

 
 
 
if __name__ == "__main__":
    app = CafeApp()
    app.run()



