import random
import datetime
import json
import os

# transaction array ug file nga isave pero json instead sa txt para naay structure hihi
transactions = []
transactions_file = 'transactions.json'

# para di na libog and dali ra ma read sa system so nag gamit tag class nga Transaction
class Transaction:
    def __init__(self, car, name, number, serial_num, warranty=30):
        self.car = car
        self.name = name
        self.number = number
        self.serial_num = serial_num
        self.warranty = warranty
        self.date_of_transaction = datetime.datetime.now().isoformat() #naka iso format para well strcutured and dili tong awat sa txt nga basta basta lang

    def __str__(self):
        return f"Car: {self.car}, Name: {self.name}, Number: {self.number}, Serial Number: {self.serial_num}, " \
               f"Warranty: {self.warranty} days, Date of Transaction: {self.date_of_transaction}" #inani lang ni sya pero naka iso man so naka new line ni siya every category pag abot sa json file

# mao ning i open nimo ang file para maka write, read, or append 
def load_transactions():
    if os.path.exists(transactions_file):
        try:
            with open(transactions_file, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error reading the file: {e}")
            return []
    return []

# diri ni siya mag save to json file, as you can see anka structure kay perfectionist ko
def save_transactions():
    with open(transactions_file, 'w') as file:
        transactions_data = [{
            'car': transaction.car,
            'name': transaction.name,
            'number': transaction.number,
            'serial_num': transaction.serial_num,
            'warranty': transaction.warranty,
            'date_of_transaction': transaction.date_of_transaction
        } for transaction in transactions]
        json.dump(transactions_data, file, indent=4)

# function for choice nga mag purchase ug car
def purchase_car():
    print("\n========== MissyuBibi Car Dealership ==========")
    print("Choose a car to purchase:")
    print("1. MissyuBibi GT400")
    print("2. MissyuBibi Alpha 6000")
    print("3. MissyuBibi 2nd Gen Alpha 6000")
    print("4. MissyuBibi 'NHIA' Limited Edition")
    print("5. Cancel Purchase")
    print("================================================")

    car_choice = input("Enter car number (1-5): ")

    # kay number raman akong gusto i input, need i if else statement para mag matter sa number choice ang mugawas nga ngalan instead of car 1 and car 2
    if car_choice == '1':
        car_name = "MissyuBibi GT400"
    elif car_choice == '2':
        car_name = "MissyuBibi Alpha 6000"
    elif car_choice == '3':
        car_name = "MissyuBibi 2nd Gen Alpha 6000"
    elif car_choice == '4':
        car_name = "MissyuBibi 'NHIA' Limited Edition"
    elif car_choice == '5':
        return # Cancel then mubalik sa main menu
    else:
        print("Invalid choice. Please select a number between 1 and 5.")
        return purchase_car()

    # user info kay syempre need ang ngalan ug contact in case ma identity theft para pud dali ra mahibal an ug naka palit baka saamo in case mag pa warranty ka or refund
    name = input("Enter your name: ")
    number = input("Enter your contact number: ")
    serial_num = random.randint(100000, 999999)  # naka generate random serial number ex. 11033232 (awat anang barcode)

    # i append ni siya sa array nga transaction ug sa json file
    transaction = Transaction(car_name, name, number, serial_num)
    transactions.append(transaction)
    
    save_transactions()  # Save the transaction to a file

    # i display ang transaction nga success
    print(f"\nTransaction Successful:")
    print(f"Car: {transaction.car}")
    print(f"Name: {transaction.name}")
    print(f"Contact No.: {transaction.number}")
    print(f"Serial Number: {transaction.serial_num}")
    print(f"Warranty: {transaction.warranty} days")
    print(f"Transaction Date: {transaction.date_of_transaction}")

# View all transactions
def view_all_transactions():
    if not transactions:
        print("No transactions found.")
    else:
        sort_choice = input("Sort by name or number? (Enter 'name' or 'number'): ").lower()
        if sort_choice == 'name':
            transactions.sort(key=lambda t: t.name) #naka sort by name bali name, car, and serial ra mugawas
        elif sort_choice == 'number':
            transactions.sort(key=lambda t: t.number) #contact number, car, ug serial ra mugawas
        else:
            print("Invalid choice.")
            return

        for transaction in transactions:
            print(transaction)

# Search transactions by name, number, or serial number
def search_receipt():
    print("\n========== Search Transactions ==========")
    print("Search by:")
    print("1. Name")
    print("2. Number")
    print("3. Serial Number")
    choice_customer = input("Enter choice (1-3): ")

    if choice_customer == '1':
        search_name = input("Enter name: ")
        found = False
        for transaction in transactions:
            if search_name.lower() == transaction.name.lower():
                print(transaction)
                found = True
        if not found:
            print("Name not found.")
    elif choice_customer == '2':
        search_number = input("Enter contact number: ")
        found = False
        for transaction in transactions:
            if search_number == transaction.number:
                print(transaction)
                found = True
        if not found:
            print("Contact number not found.")
    elif choice_customer == '3':
        search_serial = input("Enter serial number: ")
        found = False
        for transaction in transactions:
            if str(search_serial) == str(transaction.serial_num):
                print(transaction)
                found = True
        if not found:
            print("Serial number not found.")
    else:
        print("Invalid choice.")

# Available refunds based sa warranty, if 1-30 pa then ma warrant. pero ug 0 na then dili na
def available_refund():
    if not transactions:
        print("No transactions found.")
        return

    for transaction in transactions:
        if transaction.warranty > 1 and transaction.warranty <= 30:
            print(f"Car {transaction.car} with Serial Number {transaction.serial_num} can still be refunded.")
        else:
            print(f"Car {transaction.car} with Serial Number {transaction.serial_num} warranty has ended, cannot be refunded.")

# Clear all transactions
def clear_transactions():
    if transactions:
        transactions.clear()
        save_transactions()
        print("All transactions cleared.")
    else:
        print("No transactions to clear.")

#main function bali main menu or dashboard
def main():
    global transactions
    transactions = load_transactions()  # Load existing transactions from file

    while True:
        print("\n========== MissyuBibi Car Dealership =============")
        print("1. Purchase Car")
        print("2. View All Transactions")
        print("3. Search Transaction")
        print("4. Available Refunds")
        print("5. Save Transactions to File")
        print("6. Clear All Transactions")
        print("7. Exit")
        print("==================================================")

        choice = input("Enter choice (1-7): ")

        if choice == '1':
            purchase_car()
        elif choice == '2':
            view_all_transactions()
        elif choice == '3':
            search_receipt()
        elif choice == '4':
            available_refund()
        elif choice == '5':
            save_transactions()
            print("Transactions saved to file.")
        elif choice == '6':
            clear_transactions()
        elif choice == '7':
            print("Exiting MissyuBibi Car Dealership...")
            break
        else:
            print("Invalid choice. Please try again.")

#para mu run ang main function
if __name__ == "__main__":
    main()
