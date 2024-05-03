import unittest
from main import DataHandle, TransactionType


class TestFinancialRecordsApp(unittest.TestCase):
    def setUp(self):
        self.data_handle = DataHandle("test_financial_records.csv")
        self.first_record_data = {
            "Date": "2024-05-05",
            "Category": TransactionType.INCOME,
            "Amount": 500,
            "Description": "Salary"
        }
        self.updated_record_data = {
            "Date": "2024-05-05",
            "Category": TransactionType.COST,
            "Amount": 50,
            "Description": "Groceries"
        }

    def test_add_record(self):
        initial_balance = self.data_handle.show_balance()
        status_code = self.data_handle.add_record(self.first_record_data)
        self.assertEqual(status_code, 201)
        self.assertEqual(self.data_handle.show_balance(), initial_balance + 500)

    def test_update_record(self):
        initial_balance = self.data_handle.show_balance()
        index = 0  # Index of the record to update
        status_code = self.data_handle.update_record_by_index(index, self.updated_record_data)
        self.assertEqual(status_code, 200)
        self.assertEqual(self.data_handle.show_balance(), initial_balance - 450)  # initial amount was 500, update 50

    def test_search_records(self):
        search_criteria = {"Category": str(TransactionType.INCOME), "Date": "2024-05-05", "Amount": 500}
        matching_records = self.data_handle.search_records(search_criteria)
        self.assertTrue(matching_records)  # should found records by search criteria


class TestFinancialRecordsIncomeCosts(unittest.TestCase):
    def setUp(self):
        self.csv_file = "test_se_financial_records.csv"

        # Write test data directly to CSV file
        with open(self.csv_file, "w") as f:
            f.write("Date,Category,Amount,Description\n")
            f.write("2024-05-05,TransactionType.INCOME,500,Salary\n")
            f.write("2024-05-10,TransactionType.INCOME,200,Bonus\n")
            f.write("2024-05-15,TransactionType.COST,100,Groceries\n")
            f.write("2024-05-20,TransactionType.COST,50,Utilities\n")

        self.data_handle = DataHandle(self.csv_file)

    def test_show_income_records(self):
        income_records = self.data_handle.show_records(TransactionType.INCOME)
        expected_income_records = [
            {"Date": "2024-05-05", "Category": str(TransactionType.INCOME), "Amount": 500, "Description": "Salary"},
            {"Date": "2024-05-10", "Category": str(TransactionType.INCOME), "Amount": 200, "Description": "Bonus"}
        ]

        # Convert TransactionType enum values to strings for comparison
        income_records_str = [{k: str(v) if k == 'Category' else v for k, v in record.items()} for record in
                              income_records]

        self.assertEqual(income_records_str, expected_income_records)

    def test_show_cost_records(self):
        cost_records = self.data_handle.show_records(TransactionType.COST)
        expected_cost_records = [
            {"Date": "2024-05-15", "Category": str(TransactionType.COST), "Amount": 100, "Description": "Groceries"},
            {"Date": "2024-05-20", "Category": str(TransactionType.COST), "Amount": 50, "Description": "Utilities"}
        ]

        # Convert TransactionType enum values to strings for comparison
        cost_records_str = [{k: str(v) if k == 'Category' else v for k, v in record.items()} for record in cost_records]

        self.assertEqual(cost_records_str, expected_cost_records)
