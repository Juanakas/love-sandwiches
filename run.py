import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data(): # FUNCTION 1.  Get sales data from the User.

    while True:
        # The user inputs the data for the sales.
        data_str = input("Input sales data:")
        # The data is split into a list.
        sales_data = data_str.split(",")
        # Checks the data (list object) is the length of 6.
        if validate_data(sales_data):
            print("Data is correct!")
            print(sales_data)
            break
    
    return sales_data

def validate_data(values): # FUNCTION 2.  Validate the data provided by the User. Values is a list object.

    try:
        [int(value) for value in values] # Tries to convert each value in the list to an integer.
        if len(values) != 6: # If the length of the list is DIFFERENT than 6.
            raise ValueError(f"There must be 6 values, you entered {len(values)} values.")
    except ValueError as e: #e means error.
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True

def update_worksheet(data, worksheet):
    """"
    Receives a list of integers to be inserted into a worksheet.
    Update the relevant worksheet with the data provided.
    """
    while True:
        match worksheet:
            case "sales":
                sales_worksheet = SHEET.worksheet('sales')
                sales_worksheet.append_row(data)
                break
            case "surplus":
                surplus_worksheet = SHEET.worksheet('surplus')
                surplus_worksheet.append_row(data)
                break
            case _:
                print(f"worksheet {worksheet} is incorrect. Please choose sales or suprplus worksheet.\n")
                continue


def update_sales_worksheet(data): # FUNCTION 3.  Update sales worksheet in the Google Sheet.
    """
   Update sales worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")

def calculate_surplus_data(sales_row): # FUNCTION 4. Calculate surplus data.

    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    stock_row = [int(x) for x in stock_row]
    print(f"stock_row: {stock_row}")
    print(f"sales_row: {sales_row}")
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus_data.append(stock - sales)
    print(f"Surplus_sandwiches: {surplus_data}")
    return surplus_data
    

def update_surplus_worksheet(surplus_data): # FUNCTION 5. Update the Surplus worksheet by adding one more row.

    surplus_worksheet = SHEET.worksheet('surplus')
    surplus_worksheet.append_row(surplus_data)
    print("Surplus worksheet updated successfully.\n")
    print(f"Surplus row added: {surplus_data}")


"""
def calculate_avg_sales_last_5_days(sandwich_name): # FUNCTION 6. Function needs to retrieve last 5 days sales numbers for a given sandwich and, calculate average.

   sales = SHEET.worksheet('sales').get_all_values()
   # Find the row that starts with sandwich_name
   for row in sales:
       if row[0] == sandwich_name:
           # Extract the last 5 values from that list.
           last_5_values = row[-5:]
           # Convert to integers
           last_5_values = [int(value) for value in last_5_values]

    # Calculate average
    return sum(last_5_values) / len(last_5_values)
"""

def get_last_5_entries_sales():
    """
    Collects columns of data from Sales worksheet.
    Collecting the last 5 entries for each sandwich column and returns the data as a list of lists.
    """
    sales = SHEET.worksheet('sales')
    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns

def calculate_stock_data(data):
    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data







def main():

    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")

    surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data,"stock")
    


main()

