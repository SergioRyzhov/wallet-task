from enum import Enum


class TransactionType(Enum):
    INCOME = "Income"
    COST = "Cost"


class DataHandle:
    def __init__(self):
        self.data = [{
            "Date": "2024-05-02",
            "Category": TransactionType.COST,
            "Amount": 1500,
            "Description": "Products buying"
        }, {
            "Date": "2024-05-03",
            "Category": TransactionType.INCOME,
            "Amount": 30000,
            "Description": "Salary"
        }]
        self.balance = sum(record["Amount"] for record in self.data)
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

        if new_data:
            updated_data = data.copy()
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


# Example usage:
new_handle = DataHandle()

res = new_handle.add_record({
    "Date": "2024-05-01",
    "Category": TransactionType.COST,
    "Amount": 1000,
    "Description": "Groceries"
})
second_res = new_handle.add_record({
    "Date": "2024-05-05",
    "Category": TransactionType.INCOME,
    "Amount": 2000,
    "Description": "Freelance work"
})

# Search for records with a specific category and amount
search_criteria = {"Category": TransactionType.INCOME, "Amount": 2000}
matching_records = new_handle.search_records(search_criteria)
print("Matching records:", matching_records)
