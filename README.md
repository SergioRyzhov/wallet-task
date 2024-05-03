# Financial Records Management CLI App

This is a command-line interface (CLI) application for managing your digital wallet. It allows users to add, update, search, and view the balance of their financial transactions.

## Features

- Add new financial operations with details such as date, category (Income/Cost), amount, and description.
- Update existing financial records by index with new details.
- Search for financial records based on category and amount.
- View the current balance calculated from the financial records.

## Installation

1. Clone this repository:

````
git clone https://github.com/SergioRyzhov/wallet-task.git
````

2. Navigate to the project directory (example):
````
cd financial-records-cli
````

3. Install the required dependencies:

````
pip install -r requirements.txt
````

## Usage

To use the CLI app, run the `main.py` script with the desired command:
````
python main.py <command>
````

Replace `<command>` with one of the following options:

- `help`: View all commands to work.
- `add`: Add a new financial record.
- `balance`: View the current balance.
- `search`: Search for financial records.
- `update`: Update an existing financial record.

Follow the prompts to input the required information for each command.

## Example

### Add a new financial record:

````
python main.py add

Enter Date: 2024-05-05
Enter Category (Income/Cost): Income
Enter Amount: 500
Enter Description: Salary
````

### View the current balance:
````
python main.py balance
````

### Search for financial records:

````
python main.py search

Enter Category (Income/Cost): Income
Enter Amount: 500
````

### Update an existing financial record:
````
python main.py update

Enter the index of the record to update (count of records: 3): 1
Enter the new record details:
Enter Date: 2024-05-05
Enter Category (Income/Cost): Cost
Enter Amount: 50
Enter Description: Grocery
````
-------