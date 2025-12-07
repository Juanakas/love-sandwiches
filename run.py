import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    while True:
        # The user inputs the data for the sales.
        data_str = input("Input sales data:")
        # The data is split into a list.
        sales_data = data_str.split(",")
        # Checks the data (list object) is the length of 6.
        if validate_data(sales_data):
            print("Data is correct!")
            break
    return


# Values is a list object.
def validate_data(values):
    try:
        [int(value) for value in values] # Tries to convert each value in the list to an integer.
        if len(values) != 6: # If the length of the list is DIFFERENT than 6.
            raise ValueError(f"There must be 6 values, you entered {len(values)} values.")
    except ValueError as e: #e means error.
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True

data = get_sales_data()