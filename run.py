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
    # The user inputs the data for the sales.
    data_str = input("Input sales data:")
    # The data is split into a list.
    sales_data = data_str.split(",")
    validate_data(sales_data)


def validate_data(values):
    try:
        if len(values) != 6: # The user must enter 6 values.
            raise ValueError(f"There must be 6 values, you entered {len(values)} values.")
    except ValueError as e: #e means error.
        print(f"Invalid data: {e}, please try again.\n")
        return

get_sales_data()