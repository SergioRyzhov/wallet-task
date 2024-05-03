import argparse
from enum import Enum


class TransactionType(Enum):
    INCOME = "Income"
    COST = "Cost"


class DataHandle:
    def __init__(self):
        self.data = []
        self.balance = 0
        self.err_msg = ''
        self.status_code = 0

    def add_record(self, new_data: dict) -> int:
        is_valid = True
        is_recorded = False

        if new_data:
            if not new_data.get('Date'):
                self.err_msg = 'Date is empty'
                is_valid = False
            if not new_data.get('Category'):
                self.err_msg = 'Category is empty'
                is_valid = False
            if not new_data.get('Amount'):
                self.err_msg = 'Amount is empty'
                is_valid = False
            if type(new_data.get('Amount')) is not int:
                self.err_msg = 'Amount is not int'
                is_valid = False
            if not new_data.get('Description'):
                self.err_msg = 'Description is empty'
                is_valid = False

        if is_valid:
            self.data.append(new_data)
            self.balance += new_data["Amount"]
            is_recorded = True

        self.status_code = 201 if is_recorded else 400

        return self.status_code

    def update_record(self, data: dict, new_data: dict) -> int:
        is_valid = True
        is_recorded = False
        updated_data = data.copy()

        if new_data:
            for key, val in data.items():
                if key == 'Amount' and type(new_data[key]) is not int:
                    self.err_msg = 'Amount is not int'
                    is_valid = False
                    break
                try:
                    updated_data[key] = new_data[key]
                except KeyError:
                    continue

        if is_valid:
            try:
                self.data.remove(data)
            except ValueError:
                self.status_code = 404
                self.err_msg = "Record doesn't exist"
            self.data.append(updated_data)
            self.balance += updated_data["Amount"] - data["Amount"]
            is_recorded = True

        self.status_code = 200 if is_recorded else 400
        return self.status_code

    def show_balance(self):
        return self.balance

    def search_records(self, criteria: dict) -> list:
        filtered_records = list(
            filter(lambda record: all(record.get(key) == value for key, value in criteria.items()), self.data))
        return filtered_records


def main():
    parser = argparse.ArgumentParser(description="CLI app for managing financial records.")
    parser.add_argument("command", choices=["add", "balance", "search"], help="Command to execute")

    args = parser.parse_args()

    data_handle = DataHandle()

    if args.command == "add":
        date = input("Enter Date: ")
        category = input("Enter Category (Income/Cost): ")
        amount = int(input("Enter Amount: "))
        description = input("Enter Description: ")

        status_code = data_handle.add_record({
            "Date": date,
            "Category": TransactionType[category.upper()],
            "Amount": amount,
            "Description": description
        })

        if status_code == 201:
            print("Record added successfully.")
        else:
            print(f"Error: {data_handle.err_msg}")

    elif args.command == "balance":
        print(f"Current balance: {data_handle.show_balance()}")

    elif args.command == "search":
        category = input("Enter Category (Income/Cost): ")
        amount = int(input("Enter Amount: "))
        search_criteria = {"Category": TransactionType[category.upper()], "Amount": amount}
        matching_records = data_handle.search_records(search_criteria)
        print("Matching records:")
        for record in matching_records:
            print(record)


if __name__ == "__main__":
    main()
