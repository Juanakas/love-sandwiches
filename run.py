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
    pprint(stock)
    stock_row = stock[-1]
    print(stock_row)
    


def main():

    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)

main()
