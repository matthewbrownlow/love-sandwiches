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


def get_sales_data(): # This function checks for errors. If there are no errors, it will return True, and the "data is valid" print statement should appear, and the while loop is stopped with the break keyword. If our validate_data function encounters an error, it will print the error message to the terminal and return False. So the while loop will repeat it's request for data until the data provided is valid
    """
    Get sales figures input from the user.
    """
    while True: # Asks for the users data that then converts the string of data from the user into a list of values 
        print("Please enter sales data from th last market.")
        print("Data should be six numbers, seperated by commas.")
        print("Example: 10,20,30,40,50,60\n") # \n Creates a new line in the terminal when the code is exicuted

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")

        if validate_data(sales_data): # Calls the validate data function, passing it the sales_data list
            print("Data is valid!")
            break
    
    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    print(values)
    try:
        [int(value) for value in values] # Convertes each value in the values list into an integer
        if len(values) != 6: # Checks if our values list has exactly 6 values inside it
            raise ValueError(f"Exactly 6 values required, you provided {len(values)}")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True




data = get_sales_data()
