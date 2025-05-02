
import mysql.connector

# Connects to MySQL
db = mysql.connector.connect(
    #host="localhost",
    user="root",
    password="Yamilette2010#",
    database= "elite102bankingsystem"
)
cursor = db.cursor()

# Helps to get account
def get_account(acc_number, pin):
    cursor.execute("SELECT * FROM accounts WHERE account_number = %s AND pin = %s", (acc_number, pin))
    row = cursor.fetchone()
    if row:
        return {
            'account_number': row[0],
            'name': row[1],
            'pin': row[2],
            'balance': row[3]
        }
    return None


# Allows for User to View their Balance
def view_balance():
    acc = input("Account Num: ")
    pin = input("PIN: ")
    account = get_account(acc, pin)
    if account:
        print(f"Balance: ${account['balance']:.2f}")
    else:
        print("\nAccount not found.")
    print("-------------------------------")

# Enables Desposits or Withdrawals
def transaction():
    acc = input("Account Num: ")
    pin = input("PIN: ")
    account = get_account(acc, pin)
    if not account:
        print("\nInvalid account or PIN.")
        print("-------------------------------")
        return

    action = input("Type 'deposit' or 'withdraw': ").lower()
    try:
        amount = float(input("Amount: "))
        if amount <= 0:
            raise ValueError
    except:
        print("\nInvalid amount.")
        print("-------------------------------")
        return

    if action == 'withdraw':
        if amount > account['balance']:
            print("Not enough funds.")
            print("-------------------------------")   
            return
        account['balance'] -= amount
    elif action == 'deposit':
        account['balance'] += amount
    else:
        print("\nInvalid transaction type.")
        print("-------------------------------")
        return

    cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s",
                   (account['balance'], account['account_number']))
    db.commit()
    print("\nTransaction successful!")
    print("-------------------------------")    

# Allows the user to Register an Account
def register():
    acc = input("New Account Num: ")

    # Check if account already exists
    cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (acc,))
    cursor.fetchall()  # clears the unread result

    name = input("Name: ")
    pin = input("Choose a 4-digit PIN: ")

    try:
        balance = float(input("Initial deposit: "))
    except:
        print("\nInvalid amount.")
        print("-------------------------------")
        return

    cursor.execute("INSERT INTO accounts (account_number, account_name, pin, balance) VALUES (%s, %s, %s, %s)",
                   (acc, name, pin, balance))
    db.commit()
    print("\nAccount registered!")
    print("-------------------------------")


# Deletes an Account
def delete_account():
    acc, pin = input("Account Num: "), input("PIN: ")
    if get_account(acc, pin):
        cursor.execute("DELETE FROM accounts WHERE account_number = %s", (acc,))
        db.commit()
        print("\nAccount deleted.")
        print("-------------------------------")
    else:
        print("\nAccount not found.")
        print("-------------------------------")

# Updates any User Info that may be Requested
def update_account():
    acc = input("Account Num: ")
    pin = input("PIN: ")
    account = get_account(acc, pin)
    if not account:
        print("\nInvalid account.")
        print("-------------------------------")
        return

    print("What would you like to update?")
    print("1. Name\n2. PIN")
    choice = input("Choice: ")
    if choice == '1':
        new_name = input("Enter new name: ")
        cursor.execute("UPDATE accounts SET account_name = %s WHERE account_number = %s", (new_name, acc))
    elif choice == '2':
        new_pin = input("Enter new PIN: ")
        cursor.execute("UPDATE accounts SET pin = %s WHERE account_number = %s", (new_pin, acc))
    else:
        print("\nInvalid choice.")
        return

    db.commit()
    print("\nUpdate successful.")
    print("-------------------------------")
# Close the database connection when done

# Menu System
def menu():
    while True:
        print("\n//// Elite 102 Banking System ////")
        print("1. View Balance")
        print("2. Deposit/Withdraw")
        print("3. Register New Account")
        print("4. Delete Account")
        print("5. Update Account Info")
        print("6. Exit")
        choice = input("\nSelect an option (1–6): \n")

        if choice == '1':
            view_balance()
        elif choice == '2':
            transaction()
        elif choice == '3':
            register()
        elif choice == '4':
            delete_account()
        elif choice == '5':
            update_account()
        elif choice == '6':
            print("\nThank you for using our Elite Banking Program.")
            print("Have a great day!")
            print("-------------------------------")
            break
        else:
            print("\nInvalid choice. Try again.")

# Run the menu
menu()