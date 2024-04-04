from init_db import *

print("Initializing the database...")
db_initialization()

print("Creating tables")
createTables()

print("Creating Triggers")
createTriggers()

print("Inserting data")
insertData()


number = 0
print(""" SELECT AN OPTION \n
      1. Find Competition(s) with at least one large proposal for a specified month. \n
      2. Find proposal(s) that request(s) the largest amount of money for a specified area. \n
      3. Find the proposals submitted before that date that are awarded the largest amount of money for a specified date. \n
      4. Find average requested/awarded discrepancy for a specified area. \n
      5. Assign reviewers to proposals. \n
      6. Find proposals that have not been reviewed by a specified reviewer. \n
""")

def store_number():
    try:
        number = float(input("Enter a number: ")) 
        return number
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return None

# Example usage:
number = store_number()
if number is not None:
    print("You entered:", number)

