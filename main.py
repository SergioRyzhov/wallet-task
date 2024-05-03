import argparse
from enum import Enum
import pandas as pd


class TransactionType(Enum):
    """
    Enumeration for categories
    """
    INCOME = "Income"
    COST = "Cost"


class DataManager:
    """
    Class for reading and writing a CSV file
    """
    def __init__(self, filename: str):
        self.filename = filename

    def read_data(self) -> pd.DataFrame:
        """
        Read data from the CSV file
        """
        try:
            data = pd.read_csv(self.filename)
        except FileNotFoundError:
            data = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
        return data

    def write_data(self, data: pd.DataFrame) -> None:
        """
        Write data to the CSV file
        """
        data.to_csv(self.filename, index=False)


class DataHandle:
    """
    Class for managing financial records
    """
    def __init__(self, filename: str):
        self.data_manager = DataManager(filename)
        self.data: pd.DataFrame = self.data_manager.read_data()
        self.balance: int = 0
        self.err_msg: str = ''
        self.status_code: int = 0

    def update_balance_from_data(self) -> None:
        """
        Update the balance
        """
        for index, record in self.data.iterrows():
            if record['Category'] == str(TransactionType.INCOME):
                self.balance += record['Amount']
            else:
                self.balance -= record['Amount']

    def add_record(self, new_data: dict) -> int:
        """
        Add a new record to the data
        """
        is_valid = True
        is_recorded = False

        if new_data:
            if not new_data.get('Date'):
                self.err_msg = 'Date is empty'
                is_valid = False
            if not new_data.get('Category'):
                self.err_msg = 'Category is empty'
                is_valid = False
            elif new_data.get('Category') not in TransactionType.__members__.values():
                self.err_msg = f'Invalid category. Please choose from: {", ".join([t.value for t in TransactionType])}'
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
            new_record = pd.DataFrame([new_data])
            self.data = pd.concat([self.data, new_record], ignore_index=True)
            self.data_manager.write_data(self.data)
            self.balance += new_data["Amount"]
            is_recorded = True

        self.status_code = 201 if is_recorded else 400

        return self.status_code

    def update_record_by_index(self, index: int, new_data: dict) -> int:
        """
        Update the record in the data by index
        """
        is_valid = True
        is_recorded = False

        existing_record = self.data.iloc[index].to_dict()
        updated_data = existing_record.copy()

        if index < 0 or index >= len(self.data):
            self.err_msg = f'Invalid index. Index should be between 0 and {len(self.data) - 1}.'
            is_valid = False
        if not new_data.get('Category'):
            self.err_msg = 'Category is empty'
            is_valid = False
        elif new_data.get('Category') not in TransactionType.__members__.values():
            self.err_msg = f'Invalid category. Please choose from: {", ".join([t.value for t in TransactionType])}'
            is_valid = False
        if type(new_data.get('Amount')) is not int:
            self.err_msg = 'Amount is not int'
            is_valid = False
        if not new_data.get('Description'):
            self.err_msg = 'Description is empty'
            is_valid = False

        if is_valid:
            updated_data.update(new_data)
            self.data.loc[index] = updated_data
            self.data_manager.write_data(self.data)
            self.balance += updated_data["Amount"] - existing_record["Amount"]
            is_recorded = True

        self.status_code = 200 if is_recorded else 400
        return self.status_code

    def show_balance(self) -> int:
        """
        Show current balance on flow
        """
        self.update_balance_from_data()
        return self.balance

    def search_records(self, criteria: dict) -> list:
        """
        Search for records by criteria (ex: "Category" and "Amount")
        """
        filtered_records = self.data.copy()
        for key, value in criteria.items():
            filtered_records = filtered_records[filtered_records[key] == value]
        return filtered_records.to_dict('records')


def main() -> None:
    """
    Main function to execute CLI commands
    """
    parser = argparse.ArgumentParser(description="CLI app for managing financial records.")
    parser.add_argument("command", choices=["add", "balance", "search", "update"], help="Command to execute")

    args = parser.parse_args()

    filename = "financial_records.csv"
    data_handle = DataHandle(filename)

    # command to add a record
    if args.command == "add":
        date = input("Enter Date: ")
        category = input("Enter Category (Income/Cost): ")
        amount = int(input("Enter Amount: "))
        description = input("Enter Description: ")

        try:
            category_enum = TransactionType[category.upper()]
        except KeyError:
            print("Error: Invalid category. Please enter 'Income' or 'Cost'.")
            return

        status_code = data_handle.add_record({
            "Date": date,
            "Category": category_enum,
            "Amount": amount,
            "Description": description
        })

        if status_code == 201:
            print("Record added successfully.")
        else:
            print(f"Error: {data_handle.err_msg} (Status Code: {status_code})")

    # command to watch the balance
    elif args.command == "balance":
        print(f"Current balance: {data_handle.show_balance()}")

    # command to commit the search by "Category" and "Amount"
    elif args.command == "search":
        category = input("Enter Category (Income/Cost): ")
        amount = int(input("Enter Amount: "))

        try:
            category_enum = TransactionType[category.upper()]
        except KeyError:
            print("Error: Invalid category. Please enter 'Income' or 'Cost'.")
            return
        search_criteria = {"Category": str(category_enum), "Amount": amount}
        matching_records = data_handle.search_records(search_criteria)
        print("Matching records:")
        for record in matching_records:
            print(record)

    # command to update record
    elif args.command == "update":
        index = int(input(f"Enter the index of the record to update (count of records: {len(data_handle.data)}): "))
        if index < 0 or index >= len(data_handle.data):
            print(f"Error: Invalid index. Index should be between 0 and {len(data_handle.data) - 1}.")
            return

        print("Enter the new record details:")
        date = input("Enter Date: ")
        category_str = input("Enter Category (Income/Cost): ")
        amount = int(input("Enter Amount: "))
        description = input("Enter Description: ")

        try:
            category_enum = TransactionType[category_str.upper()]
        except KeyError:
            print("Error: Invalid category. Please enter 'Income' or 'Cost'.")
            return

        new_data = {
            "Date": date,
            "Category": category_enum,
            "Amount": amount,
            "Description": description
        }

        status_code = data_handle.update_record_by_index(index, new_data)

        if status_code == 200:
            print("Record updated successfully.")
        else:
            print(f"Error: {data_handle.err_msg} (Status Code: {status_code})")


if __name__ == "__main__":
    main()
