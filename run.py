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
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers seperated
    by commas. The loop will repeatedly request data until it is valid.
    """
    while True: # Asks for the users data that then converts the string of data from the user into a list of values 
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, seperated by commas.")
        print("Example: 10,20,30,40,50,60\n") # \n Creates a new line in the terminal when the code is exicuted

        data_str = input("Enter your data here:\n")

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


# def update_sales_worksheet(data):
#     """
#     Update sales worksheet, add new row with the list data provided.
#     """
#     print("Updating sales worksheet...\n")
#     sales_worksheet = SHEET.worksheet("sales") # Using the SHEET variable to use the GSPEAD library; Using the GSPEAD worksheet() method to access the sales worksheet
#     sales_worksheet.append_row(data) # The .append_row() method adds a new row to the end of our data in the worksheet selected
#     print("Sales worksheet updated successfully.\n")


# def update_suplus_worksheet(data):
#     """
#     Update surplus worksheet, add new row with the list data provided.
#     """
#     print("Updating surplus worksheet...\n")
#     surplus_worksheet = SHEET.worksheet("surplus") 
#     surplus_worksheet.append_row(data)
#     print("Surplus worksheet updated successfully.\n")


def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into the worksheet.
    Update the relevant worksheet with the data provided.
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus inidcates extra made when stock was sold out
    """
    print("Calculating surplus date...\n")
    stock = SHEET.worksheet("stock").get_all_values() # Using the get_all_values() GSPREAD method to fetch all of the calls from the stock worksheet
    stock_row = stock[-1] # Fetches the last row of data in the stock worksheet (indexing[-1])
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row): # The zip() method is used to iterate through two list at the same time
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def get_last_5_entries_sales():
    """
    Collects collumns of data from sales worksheet, collecting
    the last 5 entries from each sandwich and returns the data
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns


def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%.
    """
    print("calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    
    return new_stock_data


def main():
    """
    Run all program functions.
    Common practise to wrap the main function calls of a program 
    within a function called 'main'.
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data] # Converts values into integers; The results from the list comprehension are assigned to the variable sales_data
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")

print("Welcome to Love Sandwiches Data Automation\n")
main()
