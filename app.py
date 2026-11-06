"""A small command-line expense tracker that stores entries in a CSV file."""

import argparse
import csv
from datetime import date
from pathlib import Path

DATA_FILE = Path("expenses.csv")
FIELDS = ["date", "category", "description", "amount"]


def load_expenses():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def add_expense(category, description, amount):
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    new_file = not DATA_FILE.exists()
    with DATA_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerow({
            "date": date.today().isoformat(),
            "category": category,
            "description": description,
            "amount": f"{amount:.2f}",
        })
    print("Expense saved.")


def list_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    for item in expenses:
        print(
            f'{item["date"]} | {item["category"]} | '
            f'{item["description"]} | ₹{float(item["amount"]):.2f}'
        )


def show_summary():
    totals = {}
    for item in load_expenses():
        category = item["category"]
        totals[category] = totals.get(category, 0) + float(item["amount"])

    if not totals:
        print("No expenses to summarize.")
        return

    print("Spending by category:")
    for category, total in sorted(totals.items()):
        print(f"{category}: ₹{total:.2f}")


def main():
    parser = argparse.ArgumentParser(description="Track personal expenses.")
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="Record an expense")
    add.add_argument("category")
    add.add_argument("description")
    add.add_argument("amount", type=float)

    commands.add_parser("list", help="List recorded expenses")
    commands.add_parser("summary", help="Show totals by category")

    args = parser.parse_args()
    if args.command == "add":
        try:
            add_expense(args.category, args.description, args.amount)
        except ValueError as error:
            parser.error(str(error))
    elif args.command == "list":
        list_expenses()
    elif args.command == "summary":
        show_summary()


if __name__ == "__main__":
    main()
