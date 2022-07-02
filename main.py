loop = True

# overall user balance
currentBalance = 0.0

# Keeps track of the current index for the following lists
currentDateIndex = 0

# Stores the dates in anytime the ATM is interacted with
ListOfDates = []

# Stores all the balance changes that have occurred
balanceHistory = []

# Stores all the transactions that have occurred as strings
transactionTypeHistory = []


def Date_Input():
    while True:
        try:
            userDate = int(input("Please enter the date in the format, MDD or MMDD: "))
        except ValueError:
            print("Please enter a numerical value for the date.")
            continue
        if len(str(userDate).strip()) == 3:
            month = str(userDate)[:1]
            day = str(userDate)[1:]

            FullDate = month + day

            month = int(month)
            day = int(day)

            if Valid_Date(month, day):
                return FullDate
            print("The date provided does not exist, please try again.\n")

        elif len(str(userDate).strip()) == 4:
            month = str(userDate)[:2]
            day = str(userDate)[2:]

            FullDate = month + day

            month = int(month)
            day = int(day)

            if Valid_Date(month, day):
                return FullDate
            print("The date provided does not exist, please try again.\n")

        else:
            print("Invalid date, please try again.")


def Valid_Date(month, day):
    # List of the days of the year for each month starting at index 1
    daysOfTheYear = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return 1 <= day <= daysOfTheYear[month]


def DatesInList(ListOfDates):
    global currentDateIndex
    #
    ListOfDates.insert(currentDateIndex, Date_Input())
    return ListOfDates


def deposit():
    DatesInList(ListOfDates)
    global currentBalance
    global currentDateIndex

    print("Please enter the amount you would like to deposit in dollars then cents: \n")
    while True:
        while True:
            try:
                dollars = int(input("dollars: "))
                cents = int(input("cents: "))
                amount = str(dollars) + "." + str(cents)
                break
            except ValueError:
                print("Please enter a numerical value.")
        userResponse = input(
            f"You have entered, ${dollars}.{cents}, is this correct?\nPress (Y) for yes, or (N) for no: \n").upper()
        if userResponse == "Y":
            currentBalance = currentBalance + float(amount)
            balanceHistory.insert(currentDateIndex, currentBalance)
            transactionTypeHistory.insert(currentDateIndex, "Deposit")
            currentDateIndex = currentDateIndex + 1
            break
        elif userResponse == "N":
            continue
        else:
            print("Invalid option, please try again")


def withdrawal():
    DatesInList(ListOfDates)
    global currentBalance
    global currentDateIndex

    print("Please enter the amount you would like to withdrawal in dollars then cents: \n")
    while True:
        dollars = int(input("dollars: "))
        cents = int(input("cents: "))
        amount = str(dollars) + "." + str(cents)
        userResponse = input(
            f"You have entered, ${dollars}.{cents}, is this correct?\nPress (Y) for yes, or (N) for no: \n").upper()
        if userResponse == "Y":
            if float(amount) < currentBalance:
                currentBalance = currentBalance - float(amount)
                balanceHistory.insert(currentDateIndex, currentBalance)
                transactionTypeHistory.insert(currentDateIndex, "Withdrawal")
                currentDateIndex = currentDateIndex + 1
                break
            print("Cannot withdrawal more than your current balance.")
        elif userResponse == "N":
            continue
        else:
            print("Invalid option, please try again.")


def Balance_Inquiry():
    global currentDateIndex
    DatesInList(ListOfDates)
    balanceHistory.insert(currentDateIndex, "-----")
    transactionTypeHistory.insert(currentDateIndex, "Balance inquiry")
    currentDateIndex = currentDateIndex + 1
    print(f"Current balance: ${currentBalance}")


def Largest_Chance():
    global currentDateIndex
    DatesInList(ListOfDates)
    balanceHistory.insert(currentDateIndex, "-----")
    transactionTypeHistory.insert(currentDateIndex, "Largest change")
    currentDateIndex = currentDateIndex + 1
    largestChange = 0
    largestChangeIndex = [0, 0]
    pointingIndex = 1
    listOfDatesCopy = ListOfDates.copy()

    for balanceUpdate in range(len(balanceHistory)):
        # Following statement checks the value at index balanceUpdate is a float, and if the value at the next index is also a float
        '''
        print(f"Type for balanceHistory at index balanceUpdate: {type(balanceHistory[balanceUpdate])}")
        print(f"Type for balanceHistory at index pointingIndex: {type(balanceHistory[pointingIndex])}")
        '''
        if balanceUpdate == len(balanceHistory) or pointingIndex == len(balanceHistory):
            break
        while not isinstance(balanceHistory[balanceUpdate], float):
            if balanceUpdate == len(balanceHistory) - 1:
                break
            balanceUpdate = balanceUpdate + 1
        while not isinstance(balanceHistory[pointingIndex], float):
            if pointingIndex == len(balanceHistory) - 1:
                break
            pointingIndex = pointingIndex + 1
        if isinstance(balanceHistory[balanceUpdate], float) and isinstance(balanceHistory[pointingIndex], float):
            # If the difference between both indexes are larger than largestChance, update largestChange and store both indexes
            if abs(balanceHistory[pointingIndex] - balanceHistory[balanceUpdate]) > largestChange:
                largestChange = abs(balanceHistory[pointingIndex] - balanceHistory[balanceUpdate])
                largestChangeIndex.pop()
                largestChangeIndex.pop()
                largestChangeIndex.append(balanceHistory.index(balanceHistory[balanceUpdate]))
                largestChangeIndex.append(balanceHistory.index(balanceHistory[pointingIndex]))
                pointingIndex = pointingIndex + 1
        else:
            pointingIndex = pointingIndex + 1

    localMonth, localDay = "", ""

    print("Date\t\tTransaction\t\t\tAmount\n========== 	=============	    ========")
    for index in range(len(largestChangeIndex)):
        strIndex = str(largestChangeIndex[index])
        if len(strIndex) == 3:
            localMonth = strIndex[:1]
            localDay = strIndex[1:]
        elif len(strIndex) == 4:
            localMonth = strIndex[:2]
            localDay = strIndex[2:]

        balanceIndex = listOfDatesCopy.index(largestChangeIndex[index])

        if transactionTypeHistory[largestChangeIndex.index(strIndex)] == "Deposit":
            print(f"{localMonth}/{localDay}/2022\t{transactionTypeHistory[index]}\t\t\t\t{balanceHistory[balanceIndex]}")
        elif transactionTypeHistory[largestChangeIndex.index(strIndex)] == "Withdrawal":
            print(f"{localMonth}/{localDay}/2022\t{transactionTypeHistory[index]}\t\t{balanceHistory[balanceIndex]}")

        largestChangeIndex.insert(index, "---")
        largestChangeIndex.pop(index)
        listOfDatesCopy.insert(index, "---")
        listOfDatesCopy.pop(index+1)


def Display_all_transactions():
    loopingIndex = 0
    global currentDateIndex

    DatesInList(ListOfDates)
    balanceHistory.insert(currentDateIndex, "-----")
    transactionTypeHistory.insert(currentDateIndex, "All transactions")
    currentDateIndex = currentDateIndex + 1

    print("Date\t\tTransaction\t\t\tAmount\n========== 	=============	    ========")
    for date in ListOfDates:
        localMonth, localDay = "", ""
        dateString = str(date)
        if len(dateString.strip()) == 3:
            localMonth = dateString[:1]
            localDay = dateString[1:]
        elif len(str(date).strip()) == 4:
            localMonth = dateString[:2]
            localDay = dateString[2:]

        # formatting the displayed transactions according to the transaction type
        if transactionTypeHistory[loopingIndex] == "Deposit":
            print(
                f"{localMonth}/{localDay}/2022\t{transactionTypeHistory[loopingIndex]}\t\t\t\t{balanceHistory[loopingIndex]}")
        elif transactionTypeHistory[loopingIndex] == "Withdrawal":
            print(
                f"{localMonth}/{localDay}/2022\t{transactionTypeHistory[loopingIndex]}\t\t\t{balanceHistory[loopingIndex]}")
        elif transactionTypeHistory[loopingIndex] == "Balance inquiry":
            print(
                f"{localMonth}/{localDay}/2022\t{transactionTypeHistory[loopingIndex]}\t\t{balanceHistory[loopingIndex]}")
        elif transactionTypeHistory[loopingIndex] == "Largest change":
            print(
                f"{localMonth}/{localDay}/2022\t{transactionTypeHistory[loopingIndex]}\t{balanceHistory[loopingIndex]}")
        elif transactionTypeHistory[loopingIndex] == "All transactions":
            print(
                f"{localMonth}/{localDay}/2022\t{transactionTypeHistory[loopingIndex]}\t{balanceHistory[loopingIndex]}")
        elif transactionTypeHistory[loopingIndex] == "Day\'s transactions":
            print(
                f"{localMonth}/{localDay}/2022\t{transactionTypeHistory[loopingIndex]}\t{balanceHistory[loopingIndex]}")
        loopingIndex = loopingIndex + 1


def Display_day_transactions():
    global currentDateIndex, userDate
    DatesInList(ListOfDates)
    balanceHistory.insert(currentDateIndex, "-----")
    transactionTypeHistory.insert(currentDateIndex, "Day's transactions")
    currentDateIndex = currentDateIndex + 1
    while True:
        try:
            userDate = input("Please enter the date to see all transactions that occurred on that day: ")
        except ValueError:
            print("Please enter a numerical value for the date.")

        if len(userDate) == 3:
            userMonth = userDate[:1]
            userDay = userDate[1:]

            userMonth = int(userMonth)
            userDay = int(userDay)

            if Valid_Date(userMonth, userDay):
                break
            print("That date does not exist, please try again.")
        elif len(userDate) == 4:
            userMonth = userDate[:2]
            userDay = userDate[2:]
            userMonth = int(userMonth)
            userDay = int(userDay)

            if Valid_Date(userMonth, userDay):
                break
            print("That date does not exist, please try again.")
        else:
            print("Please enter a valid date")

    dateIndexes = [i for i, date in enumerate(ListOfDates) if date == userDate]

    print("Date\t\tTransaction\t\t\tAmount\n========== 	=============	    ========")
    for dateIndex in dateIndexes:
        if transactionTypeHistory[dateIndex] == "Deposit":
            print(f"{userMonth}/{userDay}/2022\t{transactionTypeHistory[dateIndex]}\t\t\t\t{balanceHistory[dateIndex]}")
        elif transactionTypeHistory[dateIndex] == "Withdrawal":
            print(f"{userMonth}/{userDay}/2022\t{transactionTypeHistory[dateIndex]}\t\t\t{balanceHistory[dateIndex]}")
        elif transactionTypeHistory[dateIndex] == "Balance inquiry":
            print(f"{userMonth}/{userDay}/2022\t{transactionTypeHistory[dateIndex]}\t\t{balanceHistory[dateIndex]}")
        elif transactionTypeHistory[dateIndex] == "Largest change":
            print(f"{userMonth}/{userDay}/2022\t{transactionTypeHistory[dateIndex]}\t{balanceHistory[dateIndex]}")
        elif transactionTypeHistory[dateIndex] == "All transactions":
            print(f"{userMonth}/{userDay}/2022\t{transactionTypeHistory[dateIndex]}\t{balanceHistory[dateIndex]}")
        elif transactionTypeHistory[dateIndex] == "Day\'s transactions":
            print(f"{userMonth}/{userDay}/2022\t{transactionTypeHistory[dateIndex]}\t{balanceHistory[dateIndex]}")


while loop:
    # A dictionary of the choices available to the user
    userChoice = {
        1: deposit,
        2: withdrawal,
        3: Balance_Inquiry,
        4: Largest_Chance,
        5: Display_all_transactions,
        6: Display_day_transactions
    }
    print("\nWelcome to the ATM. Please select which option you would like to perform:\n1. Deposit"
          "\n2. Withdrawal\n3. Balance Inquiry\n4. Display when the largest change in balance occurred"
          "\n5. Display all transactions\n6. Display all transactions that took place on a certain day"
          "\n7. Exit\n")

    # Checking to see if the user's selection is valid (both an integer
    # and is an option)
    while True:
        userOptions = int(input())
        if 1 <= userOptions <= 7:
            if userOptions == 7:
                loop = not loop
                break
            userChoice[userOptions]()
            break
        else:
            print("Selection outside of range, please try again.")
