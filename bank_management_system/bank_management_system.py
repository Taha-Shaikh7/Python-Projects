from pathlib import Path
from datetime import datetime
import uuid

try:
    import pandas as pd
except ImportError:
    print("Pandas is required. Install it with: pip install pandas")
    raise SystemExit(1)


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "bank_data"
ACCOUNTS_FILE = DATA_DIR / "accounts.csv"
TRANSACTIONS_FILE = DATA_DIR / "transactions.csv"

ACCOUNT_COLUMNS = [
    "account_number",
    "name",
    "account_type",
    "balance",
    "created_at",
    "status",
]

TRANSACTION_COLUMNS = [
    "transaction_id",
    "date",
    "account_number",
    "transaction_type",
    "amount",
    "balance_after",
    "details",
]

START_ACCOUNT_NUMBER = 1001


def setup_files():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not ACCOUNTS_FILE.exists():
        pd.DataFrame(columns=ACCOUNT_COLUMNS).to_csv(ACCOUNTS_FILE, index=False)

    if not TRANSACTIONS_FILE.exists():
        pd.DataFrame(columns=TRANSACTION_COLUMNS).to_csv(
            TRANSACTIONS_FILE, index=False
        )


def load_accounts():
    accounts = pd.read_csv(ACCOUNTS_FILE)

    for column in ACCOUNT_COLUMNS:
        if column not in accounts.columns:
            accounts[column] = ""

    accounts = accounts[ACCOUNT_COLUMNS]
    accounts["account_number"] = pd.to_numeric(
        accounts["account_number"], errors="coerce"
    )
    accounts = accounts.dropna(subset=["account_number"])
    accounts["account_number"] = accounts["account_number"].astype(int)
    accounts["balance"] = pd.to_numeric(accounts["balance"], errors="coerce").fillna(0)
    accounts["status"] = accounts["status"].fillna("Active")
    return accounts


def save_accounts(accounts):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    accounts = accounts.copy()
    accounts["account_number"] = pd.to_numeric(
        accounts["account_number"], errors="coerce"
    )
    accounts = accounts.dropna(subset=["account_number"])
    accounts["account_number"] = accounts["account_number"].astype(int)
    accounts["balance"] = pd.to_numeric(accounts["balance"], errors="coerce").fillna(0)
    accounts[ACCOUNT_COLUMNS].to_csv(ACCOUNTS_FILE, index=False)


def load_transactions():
    return pd.read_csv(TRANSACTIONS_FILE)


def save_transactions(transactions):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    transactions.to_csv(TRANSACTIONS_FILE, index=False)


def now_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def make_transaction_id():
    return str(uuid.uuid4())[:8].upper()


def next_account_number(accounts):
    account_numbers = pd.to_numeric(accounts["account_number"], errors="coerce")
    account_numbers = account_numbers.dropna()

    if account_numbers.empty:
        return START_ACCOUNT_NUMBER

    return int(account_numbers.max()) + 1


def get_active_account_index(accounts, account_number):
    matches = accounts[
        (accounts["account_number"] == account_number)
        & (accounts["status"].astype(str).str.lower() == "active")
    ]

    if matches.empty:
        return None

    return matches.index[0]


def add_transaction(account_number, transaction_type, amount, balance_after, details):
    transactions = load_transactions()

    new_transaction = {
        "transaction_id": make_transaction_id(),
        "date": now_text(),
        "account_number": account_number,
        "transaction_type": transaction_type,
        "amount": round(float(amount), 2),
        "balance_after": round(float(balance_after), 2),
        "details": details,
    }

    transactions = pd.concat(
        [transactions, pd.DataFrame([new_transaction])], ignore_index=True
    )
    save_transactions(transactions)


def read_positive_amount(prompt):
    while True:
        try:
            amount = float(input(prompt))
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Please enter a valid number.")


def read_account_number(prompt="Enter account number: "):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid account number.")


def create_account():
    accounts = load_accounts()

    name = input("Enter customer name: ").strip()
    if not name:
        print("Customer name cannot be empty.")
        return

    account_type = input("Enter account type (Savings/Current): ").strip().title()
    if not account_type:
        account_type = "Savings"

    while True:
        try:
            opening_balance = float(input("Enter opening balance: "))
            if opening_balance < 0:
                print("Opening balance cannot be negative.")
                continue
            opening_balance = round(opening_balance, 2)
            break
        except ValueError:
            print("Please enter a valid amount.")

    account_number = next_account_number(accounts)

    new_account = {
        "account_number": account_number,
        "name": name,
        "account_type": account_type,
        "balance": opening_balance,
        "created_at": now_text(),
        "status": "Active",
    }

    accounts = pd.concat([accounts, pd.DataFrame([new_account])], ignore_index=True)
    save_accounts(accounts)

    add_transaction(
        account_number,
        "OPENING",
        opening_balance,
        opening_balance,
        "Account opened",
    )

    print(f"Account created successfully. Account number: {account_number}")
    print(f"Accounts CSV updated: {ACCOUNTS_FILE}")


def deposit_money():
    accounts = load_accounts()
    account_number = read_account_number()
    index = get_active_account_index(accounts, account_number)

    if index is None:
        print("Active account not found.")
        return

    amount = read_positive_amount("Enter deposit amount: ")
    current_balance = float(accounts.loc[index, "balance"])
    accounts.loc[index, "balance"] = round(current_balance + amount, 2)
    new_balance = accounts.loc[index, "balance"]
    save_accounts(accounts)

    add_transaction(account_number, "DEPOSIT", amount, new_balance, "Cash deposit")
    print(f"Deposit successful. New balance: {new_balance:.2f}")


def withdraw_money():
    accounts = load_accounts()
    account_number = read_account_number()
    index = get_active_account_index(accounts, account_number)

    if index is None:
        print("Active account not found.")
        return

    amount = read_positive_amount("Enter withdrawal amount: ")
    current_balance = float(accounts.loc[index, "balance"])

    if amount > current_balance:
        print("Insufficient balance.")
        return

    accounts.loc[index, "balance"] = round(current_balance - amount, 2)
    new_balance = accounts.loc[index, "balance"]
    save_accounts(accounts)

    add_transaction(account_number, "WITHDRAWAL", amount, new_balance, "Cash withdrawal")
    print(f"Withdrawal successful. New balance: {new_balance:.2f}")


def transfer_money():
    accounts = load_accounts()
    sender_account = read_account_number("Enter sender account number: ")
    receiver_account = read_account_number("Enter receiver account number: ")

    if sender_account == receiver_account:
        print("Sender and receiver accounts cannot be the same.")
        return

    sender_index = get_active_account_index(accounts, sender_account)
    receiver_index = get_active_account_index(accounts, receiver_account)

    if sender_index is None:
        print("Sender active account not found.")
        return

    if receiver_index is None:
        print("Receiver active account not found.")
        return

    amount = read_positive_amount("Enter transfer amount: ")
    sender_balance = float(accounts.loc[sender_index, "balance"])

    if amount > sender_balance:
        print("Insufficient balance in sender account.")
        return

    accounts.loc[sender_index, "balance"] = round(sender_balance - amount, 2)
    accounts.loc[receiver_index, "balance"] = round(
        float(accounts.loc[receiver_index, "balance"]) + amount, 2
    )

    sender_new_balance = accounts.loc[sender_index, "balance"]
    receiver_new_balance = accounts.loc[receiver_index, "balance"]
    save_accounts(accounts)

    add_transaction(
        sender_account,
        "TRANSFER_OUT",
        amount,
        sender_new_balance,
        f"Transfer to account {receiver_account}",
    )
    add_transaction(
        receiver_account,
        "TRANSFER_IN",
        amount,
        receiver_new_balance,
        f"Transfer from account {sender_account}",
    )

    print("Transfer successful.")
    print(f"Sender new balance: {sender_new_balance:.2f}")
    print(f"Receiver new balance: {receiver_new_balance:.2f}")


def check_balance():
    accounts = load_accounts()
    account_number = read_account_number()
    index = get_active_account_index(accounts, account_number)

    if index is None:
        print("Active account not found.")
        return

    account = accounts.loc[index]
    print("\nAccount Details")
    print(f"Account Number: {account['account_number']}")
    print(f"Name: {account['name']}")
    print(f"Account Type: {account['account_type']}")
    print(f"Balance: {float(account['balance']):.2f}")


def view_transaction_history():
    transactions = load_transactions()
    account_number = read_account_number()

    account_transactions = transactions[
        transactions["account_number"] == account_number
    ].copy()

    if account_transactions.empty:
        print("No transactions found for this account.")
        return

    print("\nTransaction History")
    print(account_transactions.to_string(index=False))


def list_accounts():
    accounts = load_accounts()
    active_accounts = accounts[accounts["status"].astype(str).str.lower() == "active"]

    if active_accounts.empty:
        print("No active accounts found.")
        return

    print("\nActive Accounts")
    print(
        active_accounts[
            ["account_number", "name", "account_type", "balance", "created_at"]
        ].to_string(index=False)
    )


def close_account():
    accounts = load_accounts()
    account_number = read_account_number()
    index = get_active_account_index(accounts, account_number)

    if index is None:
        print("Active account not found.")
        return

    balance = float(accounts.loc[index, "balance"])
    if balance != 0:
        print("Account can only be closed when balance is zero.")
        return

    accounts.loc[index, "status"] = "Closed"
    save_accounts(accounts)
    add_transaction(account_number, "CLOSE", 0, 0, "Account closed")
    print("Account closed successfully.")


def show_menu():
    print("\n===== Bank Management System =====")
    print("1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Check Balance")
    print("5. Transfer Money")
    print("6. View Transaction History")
    print("7. List Active Accounts")
    print("8. Close Account")
    print("0. Exit")


def main():
    setup_files()

    menu_actions = {
        "1": create_account,
        "2": deposit_money,
        "3": withdraw_money,
        "4": check_balance,
        "5": transfer_money,
        "6": view_transaction_history,
        "7": list_accounts,
        "8": close_account,
    }

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Thank you for using the Bank Management System.")
            break

        action = menu_actions.get(choice)
        if action is None:
            print("Invalid choice. Please try again.")
        else:
            action()


if __name__ == "__main__":
    main()
