from enum import Enum


class TransactionType(Enum):
    INCOME = "Income"
    COST = "Cost"


class DataHandle:
    def __init__(self, initial_amount: int = 0):
        self.data = []
        self.err_msg = ''
        self.status_code = 0
        self.initial_amount = initial_amount

        if initial_amount:
            self.add_record({
                "Date": "Initial",
                "Category": TransactionType.INCOME.value,
                "Amount": initial_amount,
                "Description": "Initial amount"
            })

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

        if self.data[-1] == new_data:
            is_recorded = True

        self.status_code = 201 if is_recorded else 400

        return self.status_code

    def update_record(self, data: dict, new_data: dict) -> int:
        is_valid = True
        is_recorded = False

        if new_data:
            updated_data = data.copy()  # Initialize updated_data with a copy of data
            for key, val in data.items():
                if key == 'Amount' and type(new_data.get(key)) is not int:
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
            self.data.append(updated_data)  # Append the updated data

        if self.data[-1] == updated_data:
            is_recorded = True
        self.status_code = 200 if is_recorded else 400
        return self.status_code


# Example usage:
new_handle = DataHandle(initial_amount=5000)

res = new_handle.add_record({
    "Date": "2024-05-02",
    "Category": TransactionType.COST.value,
    "Amount": 1500,
    "Description": "Products buying"
})
second_res = new_handle.add_record({
    "Date": "2024-05-03",
    "Category": TransactionType.INCOME.value,
    "Amount": 30000,
    "Description": "Salary"
})

upd_res = new_handle.update_record({
    "Date": "2024-05-02",
    "Category": TransactionType.COST.value,
    "Amount": 1500,
    "Description": "Products buying"
}, {
    "Amount": 2000
})

print(res)
print(second_res)
print(upd_res)
print(new_handle.err_msg)
print(new_handle.data)
