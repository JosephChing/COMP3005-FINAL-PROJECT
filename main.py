import queries
import itertools
from decimal import *

q = queries.Query()

current_user = ''
cart = ['10231203123','57481737129']


def converToArray(tuple):
    l = list(itertools.chain.from_iterable(tuple))
    # l = list(tuple)
    return [str(i) for i in l]


def main():
   
    print("Welcome To The Bookstore\n--------------------------\n")
    login()
        


def addBook():
    print("ADD BOOK FUNCTION. Enter the appropriate information.")
    pubprompt = input("1) Add with publisher in database\n2) Add new publisher")
    if(pubprompt == '1'):
        while(1):
            publisherList = converToArray(q.getPublisherNamesQuery())
            for i in range(1,len(publisherList),1):
                print(f"{i}) {publisherList[i]}")
            pubchoice = input()
            publisher = publisherList[int(pubchoice)-1]
            if(int(pubchoice)<1 or int(pubchoice)>len(publisherList)):
                continue
            else:
                break
        
    elif(pubprompt == '2'):
        print("Please enter Publisher info:")
        publisher = input("Publisher name: ")
        pubadderess = input("Address: ")
        pubemail = input("Email: ")
        pubbank_account = input("Bank Account Transfer Number:")

        phoneNumbers = []
        done = False
        while done == False or len(phoneNumbers) == 0:
            inp = input("Enter a phone number(s). Enter 0 to finish.")
            if inp == "0":
                done = True
                break

            if len(inp) != 0:
                phoneNumbers.append(inp)
        
        q.addPublisherQuery(publisher,pubadderess,pubemail,pubbank_account, phoneNumbers)
    
    print("Enter book information:")
    isbn = input("isbn:")
    name = input("Title:")
    num_of_pages = input("Number of Pages: ")
    price = input("Price: ")
    min_stock = input("Minimum Stock")
    current_stock = -1
    while current_stock < 0:
        try:
            current_stock = int(input("Current Stock (must be 0 or more):"))
        except:
            print("Value not an bigint. Try again.")
            last_month_sales = -1


    last_month_sales = -1
    while last_month_sales < 0:
        try:
            last_month_sales = int(input("Last month sales (must be 0 or more): "))
        except:
            print("Value not an bigint. Try again.")
            last_month_sales = -1

    min_stock = -1
    while min_stock < 0:
        try:
            min_stock = int(input("Last month sales (must be 0 or more): "))
        except:
            print("Value not an bigint. Try again.")
            min_stock = -1


    author = []
    done = False
    while done == False or len(author) == 0:
        inp = input("Enter an author name(s). Enter 0 to finish.")
        if inp == "0":
            done = True
            break

        if len(inp) != 0:
            author.append(inp)
        
    genre = []
    done = False
    while done == False or len(genre) == 0:
        inp = input("Enter a genre(s). Enter 0 to finish.")
        if inp == "0":
            done = True
            break

        if len(inp) != 0:
            genre.append(inp)
    q.addBookQuery(isbn, name, num_of_pages, price, publisher, current_stock,last_month_sales, min_stock, author, genre)

def adminReport():
    
    ordersList = q.getAllOrders()
    ordersTotalSum = 0
    for i in range(0,len(ordersList),1):
        ordersTotalSum+=ordersList[i]['total_sum']

    pubpaymentsList = q.getPublisherPayments()

    try:
        ordersavg = ordersTotalSum/len(ordersList)
    except:
        ordersavg = 0

    print(f" length of publist = {len(pubpaymentsList)} pub payments ---> {pubpaymentsList}")    
    # for x in range(0,len(pubpaymentsList),1):
    #     for j , pu(pubpaymentsList[x])

        
        # pubpaymenttotal += pubpaymentsList[x][1] * pubpaymentsList[x][2] * pubpaymentsList[x][3]

    publishersAndPayments = {}
    for x in pubpaymentsList:
        for j in x:
            print(j)
            # try:
            orderid = j[0]
            quantity = j[1]
            price = j[2]
            royalties = j[3]
            publisher = j[4]

            payment = (price * royalties * quantity)

            print(payment)
            if publisher in publishersAndPayments.keys():
                publishersAndPayments[publisher] = publishersAndPayments[publisher] + payment
            else:
                publishersAndPayments[publisher] = payment

            # except:
            #     print("Error in admin report")

    print(publishersAndPayments)
    receiptString = f"""
--------------------------
BOOK STORE EARNINGS REPORT
--------------------------
REVENUES:

NUMBER OF ORDERS PLACED: {len(ordersList)}
AVERAGE ORDER TOTAL: ${round(ordersavg, 2)}
TOTAL REVENUE FROM ALL ORDERS: ${round(ordersTotalSum, 2)}

EXPENDITURES:
"""
    totalExpenditures = 0
    
    for key, value in publishersAndPayments.items():
        totalExpenditures += float(value)
        receiptString += f"Payment to publisher {key} of ${value}\n"

    
    receiptString + f"Total expenditures: ${round(totalExpenditures,2)}"


    
    print(receiptString)
        

def viewAllBooks():
    allbooks = q.getAllBooksQuery()
    print("-------------------------------------\nLIST OF ALL BOOKS IN BOOKSTORE\n-------------------------------------\n")
    for index, book in enumerate(allbooks):
        retbook = q.getBookQuery(book['isbn'])
        retbook = retbook[0]
        author = q.getAuthors(book['isbn'])
        print(f"""{index}\nISBN: {retbook['isbn']}\nBOOK TITLE: {retbook['bookname']}\nAUTHOR: {author}\nNUM OF PAGES: {retbook['num_of_pages']}\nPUBLISHER: {retbook['publisher']}\nCURRENT STOCK: {retbook['current_stock']}\nLAST MONTH SALES: {retbook['last_month_sales']}\n
""")

def removeBook():
    viewAllBooks()
    rembook = input(f"\nEnter ISBN of book you would like to remove(Enter to return to menu):\n")
    q.removeBookQuery(rembook)

def searchBook():
    while(1):
        print("BOOK SEARCH FUNCTION. Enter the appropriate information. \n")
        name = input("Title:")
        author = input("Author:")
        isbn = input("isbn:")
        publisher = input("Publisher:")
        genre = input("Genre:")

        if len(name) == 0:
            name = None
        if len(author) == 0:
            author = None
        if len(isbn) == 0:
            isbn = None
        if len(genre) == 0:
            genre = None
        if len(publisher) == 0:
            publisher = None

        if(name == None and author == None and isbn == None and genre == None and publisher == None):
            print("You must enter at least one search: \n")
        else:
            break


    isbns = q.searchBookQuery(name, author, isbn, genre, publisher)
    if(len(isbns) == 0):
        print("No books found...\n")
        return

    print(f"isbns ---> {isbns}")
    searchList = []
    print("Book(s) found! Printing results...")
    
    for index ,isbnTuple in enumerate(isbns):
        isbn = isbnTuple['isbn']
        book = q.getBookQuery(isbn)
        book = book[0]
        print(f"book   {book}")
        # for index, book in enumerate(bookSearchResults):
        authors = ", ".join(q.getAuthors(isbn))
        genres = ", ".join(q.getGenres(isbn))
        print(f"------------- Result #{index + 1} -------------")
        print(f"{book['bookname']}      By: {authors}      Genres: {genres}")
        print(f"${book['price']}        {book['num_of_pages']} pages      {book['current_stock']} remaining.")
    while(1):    
        print("--------------------------\nOPTIONS\n--------------------------\n")
        print("1)ADD book to cart\n2)Return to search\n3)View Cart\n4)Return to menu")
        searchchoice = input()
        if(searchchoice =='1'):
                try:
                    x = len(isbns)
                except:
                    print("There is no book to add")
                    continue
                print("Enter result number of book you want to add:\n")
                bookchoice = input()
                
                try:
                    bookchoice = int(bookchoice)
                except:
                    continue
                if(bookchoice<1 or bookchoice>int(len(isbns)+1)):
                    continue
                else:
                    cart.append(isbns[bookchoice-1]['isbn'])
                    print("ITEM ADDED")
                    continue
        elif(searchchoice =='2'):
            searchBook()
        elif(searchchoice =='3'):
            viewCart()
        elif(searchchoice == '4'):
            return





def loggedInAdmin():
    while(1):
        global current_user 
        current_user = 'admin'
        print("Admin Menu\n--------------------------\n1)Add New Book\n2)Remove book\n3)View Current Books\n4)Print earnings report\n5)Log out")
        admininput = input()
        if(admininput == '1'):
            addBook()
        elif(admininput == '2'):
            removeBook()
            continue
        elif(admininput == '3'):
            viewAllBooks()
        elif(admininput == '4'):
            adminReport()
        elif(admininput == '5'):
            break


def loggedInUser(username):
    global current_user 
    current_user = f"{username}"
    while(1):
        print("USER MENU\n--------------------------\n1)Search for books\n2)View Cart\n3)View Submitted Orders\n4)Log out\n")
        userinput = input()
        if(userinput == '1'):
            searchBook()
        if(userinput == '2'):
            viewCart()
        if(userinput == '3'):
            viewOrders()
        if(userinput == '4'):
            global cart 
            cart = []
            current_user = ''
            break


def viewOrders():
    global current_user
    orders = q.getOrdersForUser(current_user)
    print(f"--------------------------------------\nPrinting orders for user: {current_user}\n--------------------------------------\n")
    
    # orders = orders[0]
    
    for o in orders:
        try:
            o = o[0]
        except:
            print("Error in getting orders")
        # print(o)
        try:
            print(f"ORDER ID: {o['order_id']}")
            print(f"User Name: {o['username']}")
            print(f"Shipping Address: {o['shipping_address']}")
            print(f"Order Status: {o['order_status']}")
            print(f"Ship Date: {o['ship_date']}")
            print(f"Expected Arrival: {o['expected_arrival']}")
            print("Order contains the following books: ")
            for index, orderisbn in enumerate(o['isbns']):
                # print(orderisbn)
                book = q.getBookQuery(orderisbn)
                # print(book)
                try:
                    # print(book)
                    book = book[0]
                    print(f"    {book['bookname']} ${book['price']}")
                except:
                    print("No books are in your cart right now.")

        
        except:
            print("Error: Order cannot be printed.")
        print("\n\n")

def completeOrder():
    global current_user
    global cart
    print("Completing order...")
    print('1) Checkout using existing payment information and shipping information.')
    print('2) Provide new existing payment information and shipping information for this order.')
    
    inputValid = False
    while (not inputValid):
        value = input("Enter your selection: ")
        if (value == "1"):
            user = q.getAllUserInfo(current_user)
            if(len(user ) < 1):
                raise(f"User with username {current_user} does not have an entry in the user table. ")

            inputValid = True
            existingCardNumber = user[0]['cardnumber']
            existingShippingAddress = user[0]['address']
            cartTotal = 0


            for ibsn in cart:
                book = q.getBookQuery(ibsn)
                for b in book:
                    cartTotal = cartTotal + b['price']
                
            q.addOrderQuery(existingCardNumber, existingShippingAddress, current_user, cart,cartTotal)
            
            cart.clear()
            print("ORDER PLACED")
        if (value == "2"):
            inputValid = True
            cardNumber = addBillingInfo()
            cartTotal = 0
            for ibsn in cart:
                book = q.getBookQuery(ibsn)
                for b in book:
                    cartTotal = cartTotal + b['price']


            newShippingAddress = input("Enter a new shipping address: ")
            q.addOrderQuery(cardNumber, newShippingAddress, current_user, cart,cartTotal)
            
            cart.clear()

            print("ORDER PLACED: ")


def viewCart():
    while(1):
        print("SHOPPING CART\n-------------------------")
        if(len(cart)<1):
            print("Your cart is empty\n")
            return
        # for x in range(1,len(cart)+1,1):
        #     book = q.getBookQuery(cart[x-1])
        #     print(f"{x}) ISBN: {book[0]['isbn']} TITLE: {book[0]['bookname']} PRICE: ${book[0]['price']}")
        for index, cartIsbn in enumerate(cart):
            book = q.getBookQuery(cartIsbn)
            try:
                book = book[0]
                print(f"{index}) ISBN: {book['isbn']} TITLE: {book['bookname']} PRICE: ${book['price']}")
            except:
                print("No books are in your cart right now.")
 
        userinput = input(f"\n---------------------\nOptions\n---------------------\n1)Complete Order\n2)Remove Item\n3)Return to search\n4)Return to menu")
        if(userinput == '1'):
            completeOrder()
        elif(userinput == '2'):
            while(1):
                print(f"Please enter list number of book you want removed\n")
                removeinput = input()
                try:
                    numberInput = int(removeinput)
                except:
                    continue
                if(numberInput<0 or numberInput>len(cart)):
                    continue
                else:
                    cart.remove(cart[numberInput])
                    break
        elif(userinput == '3'):
            searchBook()
        elif(userinput == '4'):
            return



#returns 1 if user wants to use the same billing info as their user account
# returns 0 if user adds new billing info and adds new billing info into database       
def addBillingInfo():
    while(1):
        print("Please enter billing info:\n")
        cardnumber = input("Cardnumber\n")
        if(cardnumber==''):
            continue
        cardname = input("Card Holder name:\n")
        if(cardname==''):
            continue
        cardexpdate = input("Card expiration date(ex: 12-68):\n")
        if(cardexpdate==''or len(cardexpdate)!=5 ):
            print("Incorrect date format")
            continue
        cardaddress = input("Enter your Billing address (street,city,postal code): ")
        if(cardaddress==''):
            continue
        q.addBillingInfo(cardnumber,cardname,cardexpdate,cardaddress)
        return cardnumber



#def completeOrder():



    
def login():
    while(1):
        print(f"--------------------------\nLOGIN MENU\n--------------------------\n")
        loginInput = input("1)Login\n2)Create new user\n3)exit\n")
        if(loginInput == '1'):
            usernameInput = input("Username:").replace(" ","")
            passwordInput = input("Password:").replace(" ","")
            loginReturn = q.loginQuery(usernameInput,passwordInput) 
            if(loginReturn =='admin'):
                loggedInAdmin()
            elif(loginReturn == 0):
                print("Invalid Credentials, Try Again")
                continue
            else:
                loggedInUser(usernameInput)

        if(loginInput == '2'):
            print("Create a User: ")
            cardNumber = addBillingInfo()
            usernameInput = input("New Username:").replace(" ","")
            passwordInput = input("New Password:").replace(" ","")
            addressInput = input("Enter your address: ")
            q.addUser(usernameInput,passwordInput,cardNumber,addressInput)


        if(loginInput == '3'):
            print("Goodbye!")
            return


main()
