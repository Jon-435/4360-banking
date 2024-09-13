import platform
import getpass

# Python Banking v1.00

# Username Array (Security)
usernames = [
    ["admin", "hackme"], 
    ["jon435", "password"], 
    ["nws", "qwerty"]]
accountBals = [
    ["admin", [["Checking", 0.45], ["Savings", 270.25]]],
    ["jon435", [["Checking", 170.22], ["Savings", 1278.42]]],
    ["nws", [["Checking", 287253.78], ["Savings", 15615615.22]]]
]
cards = [
    ["admin", False, False], 
    ["jon435", True, False], 
    ["nws", False, True]]

hacks = 0 

def check_win():
    os_name = platform.system()
    if os_name == "Windows":
        print("Insecure Operating System (Windows NT) Detected. Please Consider Using Linux or Mac For Enhanced Security.\n")
    else:
        print(f"You are Using {os_name}, a Secure Operating System.\n")

def menu(username):
    print(f"Welcome to Python Bank, {username}. Here is a list of your options: \n1. Access Your Account Balances \n2. Transfer Money Between Accounts \n3. Deposit a check \n4. Manage Your PythonCard Debit Card \n5. Log Out\n")
    selection = input(f"Type your selection: ")
    print("")
    if selection == "1":
        accountBal(username)
    elif selection == "2":
        transferMoney(username)
    elif selection == "3":
        depositCheck(username)
    elif selection == "4":
        cardControl(username)
    elif selection == "5":
        input(f"Have a good day {username}! Press return to securely log out.\n")
        print("")
        main()
    else:
        print("It looks like you typed an invalid input. Try again.\n")
        menu(username)

def getUserAccounts(username):
    for user in accountBals:
        if username == user[0]:
            return user[1]
    print("Error: User account not found.\n")
    return None

def displayBalances(accounts):
    print(f"Accounts and Balances:")
    for account in accounts:
        print(f"{account[0]} Account: ${account[1]:.2f}")
    print("")
        
def accountBal(username):
    accounts = getUserAccounts(username)
    if accounts is not None:
        displayBalances(accounts)
        input("Press return to return to the main menu.\n")
        menu(username)

def getValidAmount(prompt):
    while True:
        try:
            amount = float(input(prompt))
            if amount > 0:
                return amount
            else:
                print("Amount must be greater than zero. Please try again.\n")
        except ValueError:
            print("Invalid amount entered. Please try again.\n")

def getValidAccount(prompt, valid_accounts):
    while True:
        account = input(prompt).capitalize()
        if account in valid_accounts:
            return account
        print(f"Invalid Account selection. Please choose from {valid_accounts}.\n")

def handleMenuReturn(username):
    input("Press return to return to the main menu.\n")
    menu(username)

def transferMoney(username):
    accounts = getUserAccounts(username)
    if accounts is not None:
        displayBalances(accounts)

        from_account = getValidAccount("Which account would you like to transfer FROM? (Checking/Savings): ", ["Checking", "Savings"])
        to_account = "Savings" if from_account == "Checking" else "Checking"
        
        transfer_amount = getValidAmount(f"How much would you like to transfer from {from_account} to {to_account}?: $")

        from_balance = next((account[1] for account in accounts if account[0] == from_account), None)
        to_balance = next((account[1] for account in accounts if account[0] == to_account), None)
        
        if transfer_amount > from_balance:
            print(f"Insufficient funds in {from_account}. Transfer canceled.\n")
            handleMenuReturn(username)
            return
        
        for account in accounts:
            if account[0] == from_account:
                account[1] -= transfer_amount
            if account[0] == to_account:
                account[1] += transfer_amount

        print(f"Successfully transferred ${transfer_amount:.2f} from {from_account} to {to_account}.")
        print(f"New balances: {from_account}: ${from_balance - transfer_amount:.2f}, {to_account}: ${to_balance + transfer_amount:.2f}\n")
        handleMenuReturn(username)

def depositCheck(username):
    accounts = getUserAccounts(username)
    if accounts is not None:
        displayBalances(accounts)
        account_selection = getValidAccount("What account would you like to deposit to? (Checking/Savings) or type M to return to main menu: ", ["Checking", "Savings", "M"])
        if account_selection == 'M':
            menu(username)
            return
        
        sender = input("Who is the sender of the check? ")
        amount = getValidAmount("What is the amount on the check? $ ")

        verify = input(f"To verify, you want to deposit ${amount:.2f} from {sender} to your {account_selection} account? (Y/N): ").lower()
        if verify in ["y", "yes"]:
            for account in accounts:
                if account[0] == account_selection:
                    account[1] += amount
                    print(f"Successfully deposited ${amount:.2f} from {sender} to your {account_selection} account.\n")
                    break
            handleMenuReturn(username)
        else:
            print("Deposit canceled. Returning to the main menu.\n")
            menu(username)

def cardControl(username):
    user_found = False
    for user in cards:
        if username == user[0]:
            user_found = True
            while True:
                print(f"Card Management for {username}:")
                card_status = "Enabled" if user[1] else "Disabled"
                fraud_status = "Flagged for Fraud" if user[2] else "No Fraud Detected"
                print(f"Card Status: {card_status}")
                print(f"Fraud Status: {fraud_status}\n")
                action = input("Would you like to: \n1. Enable/Disable Card \n2. Reset Fraud Status \n3. Return to the main menu \nSelect an option: ")
                print("")

                if action == "1":
                    user[1] = not user[1]
                    print(f"Card is now {'Enabled' if user[1] else 'Disabled'}.\n")
                elif action == "2":
                    user[2] = False
                    print("Fraud status has been reset.\n")
                elif action == "3":
                    handleMenuReturn(username)
                    return
                else:
                    print("Invalid selection. Returning to the main menu.\n")
                    continue
    if not user_found:
        print("Error: User account not found.\n")
        handleMenuReturn(username)

def main():
    global hacks
    print("Welcome to Python Bank: The Bestest and Mostest Secure Bank in Town.\n")
    check_win()

    while hacks < 3:
        input_username = input("To continue, enter your eBanking username: ")
        user_found = False
        for user in usernames:
            if input_username == user[0]:
                user_found = True
                input_password = getpass.getpass(prompt=f"Welcome {input_username}! Please enter your password. Your password is protected by obfuscation: ")
                print("")
                if input_password == user[1]:
                    print("Login successful! Welcome to your account.\n")
                    menu(input_username)
                    return
                else:
                    print("Incorrect password. Access denied.\n")
                    hacks += 1
                    break
        if not user_found:
            print("Username not found. Please try again.\n")
            hacks += 1

    print("You have been banned for hacking. All information on this session has been reported to the FBI and local law enforcement agencies\n")

main()