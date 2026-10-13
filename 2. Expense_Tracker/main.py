"""Expense Tracker - command-line menu."""
from datetime import datetime

from tracker import Expense, Tracker


def read_date():
    while True:
        text = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
        if text == "":
            return datetime.today().strftime("%Y-%m-%d")
        try:
            datetime.strptime(text, "%Y-%m-%d")
            return text
        except ValueError:
            print("Invalid date. Use the format YYYY-MM-DD.")


def read_amount():
    while True:
        try:
            amount = float(input("Amount: "))
            if amount > 0:
                return amount
            print("Amount must be greater than 0.")
        except ValueError:
            print("Please enter a number.")


def add_expense(tracker):
    date = read_date()
    category = input("Category (Food, Transport, Bills...): ").strip().title()
    description = input("Description: ").strip()
    if not category:
        print("Category cannot be empty.")
        return
    tracker.add_expense(Expense(date, category, description, read_amount()))
    print("Expense added.")


def view_all(tracker):
    if not tracker.expenses:
        print("No expenses recorded yet.")
        return
    print(tracker.to_dataframe()[["date", "category", "description", "amount"]]
          .to_string(index=False))


def main():
    tracker = Tracker()
    while True:
        print("\n=== Expense Tracker ===")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Summary by category")
        print("4. Summary by month")
        print("5. Category x month table")
        print("6. Pie chart of spending")
        print("7. Exit")
        choice = input("Choose (1-7): ").strip()

        if choice == "1":
            add_expense(tracker)
        elif choice in ("2", "3", "4", "5", "6") and not tracker.expenses:
            print("No expenses recorded yet. Add some first.")
        elif choice == "2":
            view_all(tracker)
        elif choice == "3":
            print("\nTotal spent per category:")
            print(tracker.summary_by_category().round(2))
        elif choice == "4":
            print("\nTotal spent per month:")
            print(tracker.summary_by_month().round(2))
        elif choice == "5":
            print(tracker.category_by_month().round(2))
        elif choice == "6":
            tracker.plot_category_pie()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
