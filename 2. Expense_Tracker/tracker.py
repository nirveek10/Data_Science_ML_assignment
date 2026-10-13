"""Classes for the Expense Tracker.
Expense  -> one spending record
Tracker  -> stores expenses in a CSV file and analyses them with pandas
"""
import csv
import os

import matplotlib.pyplot as plt
import pandas as pd

CSV_FILE = "expenses.csv"
FIELDS = ["date", "category", "description", "amount"]


class Expense:
    def __init__(self, date, category, description, amount):
        self.date = date                  # string, format YYYY-MM-DD
        self.category = category
        self.description = description
        self.amount = float(amount)

    def to_dict(self):
        return {
            "date": self.date,
            "category": self.category,
            "description": self.description,
            "amount": self.amount,
        }


class Tracker:
    def __init__(self, filename=CSV_FILE):
        self.filename = filename
        self.expenses = []
        self.load()

    # ---------- storage ----------
    def load(self):
        """Read existing expenses from the CSV (if the file exists)."""
        if not os.path.exists(self.filename):
            return
        with open(self.filename, newline="") as f:
            for row in csv.DictReader(f):
                self.expenses.append(
                    Expense(row["date"], row["category"], row["description"], row["amount"])
                )

    def add_expense(self, expense):
        """Add to the list and append one row to the CSV."""
        self.expenses.append(expense)
        file_is_new = not os.path.exists(self.filename)
        with open(self.filename, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            if file_is_new:
                writer.writeheader()
            writer.writerow(expense.to_dict())

    # ---------- analysis (pandas) ----------
    def to_dataframe(self):
        df = pd.DataFrame([e.to_dict() for e in self.expenses], columns=FIELDS)
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.to_period("M").astype(str)
        return df

    def summary_by_category(self):
        df = self.to_dataframe()
        return df.groupby("category")["amount"].sum().sort_values(ascending=False)

    def summary_by_month(self):
        df = self.to_dataframe()
        return df.groupby("month")["amount"].sum()

    def category_by_month(self):
        """Table with months as rows and categories as columns."""
        df = self.to_dataframe()
        return df.pivot_table(
            index="month", columns="category", values="amount", aggfunc="sum", fill_value=0
        )

    # ---------- chart ----------
    def plot_category_pie(self, save_path="outputs/category_pie.png"):
        totals = self.summary_by_category()
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.figure(figsize=(6, 6))
        plt.pie(totals, labels=totals.index, autopct="%1.1f%%", startangle=90)
        plt.title("Spending by Category")
        plt.savefig(save_path)
        print(f"Chart saved to {save_path}")
        plt.show()
