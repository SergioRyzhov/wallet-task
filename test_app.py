import unittest
from main import DataHandle, TransactionType


class TestFinancialRecordsApp(unittest.TestCase):
    def setUp(self):
        self.data_handle = DataHandle("test_financial_records.csv")

    def test_add_record(self):
        initial_balance = self.data_handle.show_balance()
        new_record_data = {
            "Date": "2024-05-05",
            "Category": TransactionType.INCOME,
            "Amount": 500,
            "Description": "Salary"
        }
        status_code = self.data_handle.add_record(new_record_data)
        self.assertEqual(status_code, 201)
        self.assertEqual(self.data_handle.show_balance(), initial_balance + 500)

    def test_update_record(self):
        initial_balance = self.data_handle.show_balance()
        index = 0  # Index of the record to update
        updated_record_data = {
            "Date": "2024-05-05",
            "Category": TransactionType.COST,
            "Amount": 50,
            "Description": "Groceries"
        }
        status_code = self.data_handle.update_record_by_index(index, updated_record_data)
        self.assertEqual(status_code, 200)
        self.assertEqual(self.data_handle.show_balance(), initial_balance - 450)  # initial amount was 500

    def test_search_records(self):
        search_criteria = {"Category": str(TransactionType.INCOME), "Amount": 500}
        matching_records = self.data_handle.search_records(search_criteria)
        self.assertTrue(matching_records)  # should found records by search criteria
