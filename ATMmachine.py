#Default_password:1234
import json
import datetime

def load_pin():
    """Loads the PIN from a file or returns a default PIN."""
    try:
        with open('pin.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return "1234"  # Default PIN if file doesn't exist

def load_account_data():
    """Loads account data (balance and transaction history) from a JSON file.

    Returns:
        tuple: A tuple containing the balance and transaction history.
    """
    try:
        with open('account_data.json', 'r') as f:
            data = json.load(f)
            return data['balance'], data['transaction_history']
    except FileNotFoundError:
        return 5000, []  # Default balance and empty transaction history

def save_account_data(balance, transaction_history):
    """Saves account data to a JSON file.

    Args:
        balance (float): The account balance.
        transaction_history (list): The transaction history.
    """
    data = {'balance': balance, 'transaction_history': transaction_history}
    try:
        with open('account_data.json', 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Error saving account data: {e}")

def save_pin(pin):
    """Saves the new PIN to a file."""
    try:
        with open('pin.txt', 'w') as f:
            f.write(pin)
    except Exception as e:
        print(f"Error saving PIN: {e}")

class ATM:
    """Represents an ATM machine with basic functionalities."""

    def __init__(self, pin, balance=0):
        """Initializes an ATM instance with a PIN and optional balance.

        Args:
            pin (str): The user's PIN.
            balance (float, optional): The initial account balance. Defaults to 0.
        """
        self.pin = pin  # Stores the user's PIN
        self.balance = balance  # Stores the account balance
        self.transaction_history = []  # Stores transaction history

    def check_balance(self):
        """Checks the current account balance and returns a formatted string."""
        return f"Your current balance is: Rs.{self.balance}"

    def withdraw(self, amount):
        """Withdraws cash from the account if sufficient funds.

        Args:
            amount (float): The amount to withdraw.

        Returns:
            str: A message indicating success or insufficient funds.
        """
        if amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"Withdrawal of Rs.{amount} on {datetime.datetime.now()}")
            return f"Withdrawal successful. New balance: Rs.{self.balance}"
        else:
            return "Insufficient funds."

    def deposit(self, amount):
        """Deposits cash into the account.

        Args:
            amount (float): The amount to deposit.
        """
        self.balance += amount
        self.transaction_history.append(f"Deposit of Rs.{amount} on {datetime.datetime.now()}")
        return f"Deposit successful. New balance: Rs.{self.balance}"

    def change_pin(self, old_pin, new_pin):
        """Changes the ATM PIN if the old PIN is correct.

        Args:
            old_pin (str): The current PIN.
            new_pin (str): The new PIN.

        Returns:
            str: A message indicating success or incorrect old PIN.
        """
        if old_pin == self.pin:
            self.pin = new_pin
            save_pin(new_pin)  # Save the new PIN to the file
            return "PIN changed successfully."
        else:
            return "Incorrect old PIN."

    def check_transaction_history(self):
        """Displays the transaction history."""
        if not self.transaction_history:
            return "No transaction history available."
        else:
            return "\n".join(self.transaction_history)

def main():
    """Main function to simulate ATM operations."""
    balance, transaction_history = load_account_data()  # Load account data
    account = ATM(load_pin(), balance)  # Create ATM instance with loaded data
    account.transaction_history = transaction_history  # Set transaction history

    while True:
        pin = input("Enter your PIN: ")
        if pin == account.pin:
            # Display ATM menu and handle user choices
            print("\nATM Menu")
            print("1. Check Balance")
            print("2. Withdraw Cash")
            print("3. Deposit Cash")
            print("4. Change PIN")
            print("5. Check Transaction History")
            print("6. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                print(account.check_balance())
            elif choice == "2":
                amount = int(input("Enter withdrawal amount: "))
                print(account.withdraw(amount))
            elif choice == "3":
                amount = int(input("Enter deposit amount: "))
                print(account.deposit(amount))
            elif choice == "4":
                old_pin = input("Enter old PIN: ")
                new_pin = input("Enter new PIN: ")
                print(account.change_pin(old_pin, new_pin))
            elif choice == "5":
                print(account.check_transaction_history())
            elif choice == "6":
                print("Thank you for using the ATM.")
                save_account_data(account.balance, account.transaction_history)  # Save account data before exiting
                break
            else:
                print("Invalid choice.")
        else:
            print("Incorrect PIN.")

if __name__ == "__main__":
    main()


