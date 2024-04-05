from init_db import *

print("Initializing the database...")
db_initialization()

print("Creating tables")
createTables()

print("Creating Triggers")
createTriggers()

print("Inserting data")
insertData()


while True: 
    number = int (input(""" SELECT AN OPTION \n
        1. Find Competition(s) with at least one large proposal for a specified month. \n
        2. Find proposal(s) that request(s) the largest amount of money for a specified area. \n
        3. Find the proposals with largest award amount for a specified submission date. \n
        4. Find average requested/awarded discrepancy for a specified area. \n
        5. Assign reviewers to proposals. \n
        6. Find proposals that have not been reviewed by a specified reviewer. \n
        7. exit \n
    """))

    print("You selected:", number)

    if number == 1:
        month = input("Enter the month: ")
        print("The competitions with at least one large proposal for the month of", month, "are:")
        findLargeApplicationFromMonth(month)

    if number == 2:
        area = input("Enter the area: ")
        print("The proposal(s) that request(s) the largest amount of money for the area of", area, "is:")
        findLargestRequestsFromArea(area)

    if number == 3:
        date = input("Enter the date: ")
        print("The proposals submitted before", date, "that are awarded the largest amount of money  are:")
        findLargestAmountAwardedFromDate(date)

    if number == 4:
        area = input("Enter the area: ")
        print("The average requested/awarded discrepancy for the area of", area, "is:")
        findAwardDiscrepancyFromArea(area)

    if number == 5:
        #while loop for different applications? until exit?
        #get application id (should we show the applications that have not been reviewed yet?)
        #option to see reviewers !(conflicts of interest) with researchers from application id
        #assigning reviewers to application id
        while True:
            application_id = input("Enter the application id: ")
            print("The reviewers that have conflicts of interest with the researchers of the application are:")
            findCOIFreeReviewers(application_id)
            reviewer = input("Enter the reviewer: ")
            assignReviewer(application_id, reviewer)
            if input("Do you want to assign another reviewer? (y/n): ") == "n":
                break
    
    if number == 6:
        reviewer = input("Enter the reviewer: ")
        print("The proposals that have not been reviewed by", reviewer, "are:")
        findNotReviewed(reviewer)

    if number == 7:
        break

