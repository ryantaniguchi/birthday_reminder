import sqlite3
import csv

# Function that displays different options related to the database data. It also allows the user
# to enter an option to manipulate and view the data.
def display_menu():
    while True:
        print("************MAIN MENU**************")
        print("""
A: Add Table Entries
B: View Table details
C: View a Customer Entry
D: Delete a Customer Entry
U: Update a Customer Entry
Q: Quit/Log Out
""")
        # Asks the user to choose an option. Converts input to uppercase if not already.
        user_input = input("Please enter your selection: ").upper()
        # Connects to the database.
        database_connection, cursor = connect()
        # If user enters "A", allows them to add a new entry to the table.
        if user_input == "A":
            while True:
                # Allows the user to add an entry via a .csv file or to manually enter the data.
                display_input = input("Are you adding from file or manually? (Type 'Quit' to return to the menu): ").upper()
                # Calls the read_csv function to pull the data from a compatible .csv file.
                if display_input == "FILE":
                    birthday_info = read_csv()
                    if birthday_info != None:
                        # Pulls the database info and uses it to update the database
                        file_addition(birthday_info, database_connection, cursor)
                        break
                    # Prints an error if it can't find the file.
                    else:
                        print("Invalid entry. Only formatted csv files are accepted.")
                # Calls the manually_addition function and allows the user to enter a new entry manually.
                elif display_input == "MANUALLY":
                    manual_addition(database_connection, cursor)
                    break
                # Returns to menu if the user types "QUIT".
                elif display_input == "QUIT":
                    print("Returning to menu.")
                    break
                # Returns an error if any other entry is given.
                else:
                    print("Invalid entry. Valid options are 'File' or 'Manually'.")
        # Calls the display_table function to show the current table.
        elif user_input == "B":
            display_table(database_connection, cursor)
        # Allows the user to search the table for entries, either by name or by birth month.
        elif user_input == "C":
            while True:
                display_input = input("Are you searching by name or by month?: ").upper()
                # Calls the display_name function, allowing the user to search the database by a person's
                # name.
                if display_input == "NAME":
                    display_name(database_connection, cursor)
                    break
                # Calls the display_month function, allowing the user to search the database by a person's
                # birth month.
                elif display_input == "MONTH":
                    display_month(database_connection, cursor)
                    break
                # Returns an error if any other entry is provided.
                else:
                    print("Invalid selection. Please enter 'name' or 'month'.")
        # Allows a user to delete a row in the table based on the entry's name
        elif user_input == "D":
            delete_row(database_connection, cursor)
        # Allows a user to update an entry's birth day, birth month, or interests
        elif user_input == "U":
            manual_update(database_connection, cursor)
        # Allows a user to quit the program.
        elif user_input == "Q":
            print("Exiting the program. Goodbye.")
            disconnect(database_connection)
            return
        # Prints an error message if any other option is selected.
        else:
            print("Invalid entry. Please enter one of the above choices: ")
        # Disconnects from the database.
        disconnect(database_connection)

# A function that reads a .csv file and returns the values it reads
def read_csv():
    # Requests the user provide the name of a .csv file.
    csv_name = input("Please enter the name of the file: ")
    try:        
        # Opens birthday_info.csv file
        with open(csv_name, 'r') as fin:
            dr = csv.DictReader(fin)
            birthday_info = [(i['NAME'], i['DAY'], i['MONTH'], i['INTERESTS']) for i in dr]
            return birthday_info        
    # Prints an error message if it can't find the file in question.
    except FileNotFoundError as error:
        print("Unable to find", csv_name)
        """Maybe change this to allow a return to the main program"""

# Creates the birthday table if it doesn't already exist.
def table_creation(cursor):
    cursor.execute('create table if not exists birthday(name varchar2(10), day int, month varchar2(10), interests varchar2(255));')
    print("\nTable creation is successful.\n")

# Connects to the sqlite3 database and the Python program.
def connect():
    try:
        # Making a connection between sqlite3 database and the Python program
        database_connection = sqlite3.connect('birthday_database.db')
        cursor = database_connection.cursor()

        # If sqlite3 makes a connection with python program then it will print "Connected to SQLite"
        print("Connection to birthday_database is successful.")
        return database_connection, cursor
    # Otherwise it will show errors
    except sqlite3.Error as error:
        print("Failed to connect with the birthday_database database.", error)

# Closes the connection to the sqlite3 database.
def disconnect(database_connection):
    if database_connection:
        # using close() method, we will close the connection
        database_connection.close()
        # After closing connection object, we will print "the sqlite connection is closed"
        print("\nThe connection to birthday_database is closed.\n")
    

# A function that takes in the info from a .csv file and adds it to a SQLite database
def file_addition(birthday_info, database_connection, cursor):
    # Checks how many tables there are with the specified name.
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='birthday' ''')

    # If the count is 0, then calls the table_creation function to create the table.
    if cursor.fetchone()[0]==0 : {
        table_creation(cursor)
    }

    # Insert data into birthday table
    cursor.executemany(
        "insert into birthday (name, day, month, interests) VALUES (?, ?, ?, ?);", birthday_info)

    # Prints the current table.
    display_table(database_connection, cursor)

    # Commit work and close connection
    database_connection.commit()
    cursor.close()

# Function to allow a user to manually add an entry to the table.
def manual_addition(database_connection, cursor):
    # Create birthday table using 10 characters for name and an integer for day, 10 characters for month, and 255 characters for 
    # interests.
    cursor.execute('create table if not exists birthday(name varchar2(10), day int, month varchar2(10), interests varchar2(255));')
    print("\nTable creation is successful.\n")

    # Insert data into birthday table based on user input
    name_input = input("Please enter the person's name: ")
    day_input = input("Please enter the day the person was born on: ")
    month_input = input("Please enter the person's birth month: ")
    interests_input = input("Please enter some of the person's interests: ")

    # Insert data into birthday table
    cursor.execute(
        "insert into birthday (name, day, month, interests) VALUES (?, ?, ?, ?)", (name_input, day_input, month_input, interests_input))

    # Prints the current state of the table.
    display_table(database_connection, cursor,)

    # Commit work and close connection
    database_connection.commit()
    cursor.close()

# Function to display entries based on their month.
def display_month(database_connection, cursor):
    try:
        # Asks the user to provide the name of the person they are querying.
        query = input("Please enter the name of the month you are querying: ")

        # Creates variable of the select statement used to pull the requested data.
        select_query = 'select * FROM birthday where MONTH = ?'

        # Prints the information for the specified name.
        for i in cursor.execute(select_query, (query, )):
            print(i)

        # Commit work and close connection
        database_connection.commit()
        cursor.close()
    # Returns an error if the table has not been created.
    except Exception as error:
        print("\nUnable to locate table. Please add an entry to create the table.")

# Function to display an entry based on their name.
def display_name(database_connection, cursor):
    try:
        # Asks the user to provide the name of the person they are querying.
        query = input("Please enter the name of the person you are querying: ")

        # Creates variable of the select statement used to pull the requested data.
        select_query = 'select * FROM birthday where NAME = ?'

        # Prints the information for the specified name.
        for i in cursor.execute(select_query, (query, )):
            print(i)

        # Commit work and close connection
        database_connection.commit()
        cursor.close()
    # Returns an error if the table has not been created.
    except Exception as error:
        print("\nUnable to locate table. Please add an entry to create the table.")


# Function to display the table.
def display_table(database_connection, cursor):

    try:
        # Count how many rows are in the table
        cursor.execute('select count(*) from birthday;')
        number_of_rows = cursor.fetchone()[0]

        # Select all the data from the table so it can be printed in order of month
        cursor.execute('select * from birthday order by MONTH;')

        # Print the number of rows in the table.
        print("\nThere are", number_of_rows, "individuals in this table.")

        # Print the table
        for i in cursor.fetchall():
            print(i)

        # Commit work and close connection
        database_connection.commit()
        cursor.close()
    # Returns an error if the table has not been created.
    except Exception as error:
        print("\nUnable to locate table. Please add an entry to create the table.")


# Function to delete the specified row.
def delete_row(database_connection, cursor):
    try:
        # Query to delete all data where ship_id = 2
        name = input("Please enter the name of the person being deleted: ")
        sql_update_query  = """DELETE from birthday where NAME=?"""
        cursor.execute(sql_update_query, (name,))
        print("Specified indvidual has been deleted.")

        # display row by row
        display_table(database_connection, cursor)
    # Returns an error if the table has not been created.
    except Exception as error:
        print("\nUnable to locate table. Please add an entry to create the table.")

# Function to manually add a new row to the table.
def manual_update(database_connection, cursor):
    try:
        # Select the row to update based on name, and update the specified fields.
        name = input("Please enter the name of the person being updated: ")
        # While loop prompts for the field to be updated, and the new info to be updated
        while True:
            field = input("Please enter the field that is being updated: ").upper()
            update = input("Please enter the new value you would like entered: ")
            # Updates the day of the month the person was born on then breaks the loop
            if field == "DAY":
                sql_update_query  = """UPDATE birthday set DAY = ? where NAME = ?"""
                cursor.execute(sql_update_query, (update, name))
                print(name, "has been updated.")
                break
            # Updates the month the person was born on then breaks the loop
            elif field == "MONTH":
                sql_update_query  = """UPDATE birthday set MONTH = ? where NAME = ?"""
                cursor.execute(sql_update_query, (update, name))
                print(name, "has been updated.")
                break
            # Updates the intersts of the person
            elif field == "INTERESTS":
                sql_update_query  = """UPDATE birthday set INTERESTS = ? where NAME = ?"""
                cursor.execute(sql_update_query, (update, name))
                print(name, "has been updated.")
                break
            # Provides error message if the correct field is not entered. Loops to ask for the
            # field once more.
            else:
                print("Invalid field. Valid entries are 'day', 'month', or 'interests'.")

        # display row by row
        display_table(database_connection, cursor)
    # Returns an error if the table has not been created.
    except Exception as error:
        print("\nUnable to locate table. Please add an entry to create the table.")

# Main function, calls the display_menu function.
def main():
    display_menu()


# Run the main function only if it is being run from this file
if __name__ == "__main__":
    main()