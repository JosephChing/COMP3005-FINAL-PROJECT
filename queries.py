import psycopg2
import psycopg2.extras
import random
import uuid
import datetime



class Query():
    def __init__(self):
        self.conn = psycopg2.connect(database="bookstoreTest", user='postgres', password='Baseball55@', host='127.0.0.1', port= '5432')
        self.conn.autocommit = True
        self.cursor =  self.conn.cursor()

    def getAllBooksQuery(self):
        sql = '''
            SELECT isbn
            FROM books 
            '''  
        self.cursor.execute(sql)
        returnArray = []
        for tuple in self.cursor.fetchall():
            # tuple looks something like -> [('10231203123',)]
            # returnArray.append(tuple)
            returnArray.append( {'isbn': tuple[0]} ) 
        return returnArray
    
    def removeBookQuery(self,isbn):
        sql1=f'''DELETE FROM 
        
        '''
        
        sql = f'''
            DELETE FROM book_authors WHERE isbn = '{isbn}';
            DELETE FROM book_genres WHERE isbn = '{isbn}';
            DELETE FROM order_contains WHERE book_isbn = '{isbn}';
            DELETE FROM books WHERE isbn = '{isbn}';
        '''
        #print(f"sql   {sql}")
        self.cursor.execute(sql)



    def searchBookQuery(self, name, author, isbn, genre, publisherName):
        sql = '''
        SELECT b.isbn
        FROM books as b
        '''
        whereConditions = [] # in the format of 'name=joe author=bob
        if(name != None):
            whereConditions.append("b.bookname = '" + name + "'")
        if(author!= None):
            # Perform inner join
            sql += '''
            INNER JOIN book_authors AS ba
            ON b.isbn = ba.isbn
            '''
            whereConditions.append("ba.author = '" + author + "'")
        if(isbn!= None):
            whereConditions.append("b.isbn = '" + isbn + "'")
        if(genre!= None):
            sql += '''
            INNER JOIN book_genres AS bg
            ON b.isbn = bg.isbn
            '''
            whereConditions.append("bg.genre = '" + genre + "'")
        if(publisherName!=None):
            whereConditions.append("b.publisher = '" + publisherName + "'")

        whereConditions = " AND ".join(whereConditions)
        sql += "WHERE " + whereConditions

        self.cursor.execute(sql)

        returnArray = []
        for tuple in self.cursor.fetchall():
            # tuple looks something like -> [('10231203123',)]
            # returnArray.append(tuple)
            returnArray.append( {'isbn': tuple[0]} ) 
        print(returnArray)
        return returnArray

    def getBookQuery(self, isbn):
        sql = f'''
        SELECT * from books
        WHERE isbn = '{isbn}'
        '''
        self.cursor.execute(sql)
        

        returnArray = []
        for tuple in self.cursor.fetchall():
            row = {
                'isbn': tuple[0],
                'bookname': tuple[1],
                'num_of_pages': tuple[2],
                'price': tuple[3],
                'publisher': tuple[4],
                'pub_royalties': tuple[5],
                'current_stock': tuple[6],
                'min_books': tuple[7],
                'last_month_sales': tuple[8],
            }
            returnArray.append(row)
        return returnArray

    #returns ['joe', 'bob']
    def getAuthors(self,isbn):
        sql = f'''
        SELECT author FROM book_authors
        WHERE isbn = '{isbn}'
        '''
        self.cursor.execute(sql)
        returnArray = []
        for tuple in self.cursor.fetchall():
            returnArray.append(tuple[0])
        return returnArray

    #returns ['violence', 'fantasy']
    def getGenres(self, isbn):
        sql = f'''
        SELECT genre FROM book_genres
        WHERE isbn = '{isbn}'
        '''
        self.cursor.execute(sql)
        returnArray = []
        for tuple in self.cursor.fetchall():
            returnArray.append(tuple[0])
        return returnArray


    def addOrderQuery(self, cardnumber, shipping_address, username, cartIsbns, cartTotal):
        # In the format of 2022-03-2
        start = datetime.date(2022,12, 1)
        end = datetime.date(2023, 12, 31)
        random_ship_date = start + datetime.timedelta(days=random.randint(0, (end - start).days))
        random_expected_arrival_date = random_ship_date + datetime.timedelta(days=7)
        ship_date = (random_ship_date).strftime('%Y-%m-%d')
        expected_arrival = (random_expected_arrival_date).strftime('%Y-%m-%d')


        order_id = str(uuid.uuid1())
        order_status = "placed"
        sql = f'''INSERT INTO orders 
        VALUES ('{order_id}', '{cardnumber}', '{shipping_address}', '{username}', '{ship_date}' ,'{expected_arrival}', '{order_status}', FALSE, {cartTotal})'''

        # print(f"DEBUG MESSAGE: {sql}")
        self.cursor.execute(sql)
        # order_id varchar UNIQUE,
        # cardnumber bigint NOT NULL,
        # shipping_address varchar NOT NULL,
        # username varchar NOT NULL,
        # ship_date date NOT NULL,
        # expected_arrival date NOT NULL,
        # order_status varchar NOT NULL,
        # publisher_paid boolean NOT NULL,
        # total_sum float NOT NULL,

        sql = self.insertIntoSql("placed_orders", [order_id, username])
        self.cursor.execute(sql)

        
        orderIsbnQuantity = {} #format of 'isbn':count
        for isbn in cartIsbns:
            if isbn not in orderIsbnQuantity:
                orderIsbnQuantity[isbn] = 1
            else:
                orderIsbnQuantity[isbn] = orderIsbnQuantity[isbn] + 1
        #print(orderIsbnQuantity)
        for isbn in orderIsbnQuantity:
            sql = self.insertIntoSql('order_contains', [str(order_id), isbn, orderIsbnQuantity[isbn]])
            #print(sql)
            self.cursor.execute(sql)

    def getOrderInfo(self, orderId):
        sql=f"""
        SELECT * FROM orders AS o INNER JOIN order_contains AS oc ON oc.order_id = o.order_id WHERE o.order_id = '{orderId}'
        
        """
        self.cursor.execute(sql)
        order = self.cursor.fetchall()
        #print(order)
        array = []
       
        try:
            t = order[0]
            d = {
                'order_id' : t[0],
                'cardnumber' : t[1],
                'shipping_address' : t[2],
                'username' : t[3],
                'ship_date' : t[4],
                'expected_arrival' : t[5],
                'order_status' : t[6],
                'publisher_paid' : t[7],
                'total_sum' : t[8],
            }
        except:
            print("rrererer")
        isbnarray = []
        for tuple in order:
            isbnarray.append(tuple[10])
        d['isbns'] = isbnarray
        array.append(d)
        return array

    
    def getPublisherPayments(self):
        orderList = self.getAllOrders()
        retList = []
        
        for order in orderList:
            print(f"orderid--->{order['order_id']}")
            sql = f"""
            SELECT o.order_id, oc.quantity,b.price, b.pub_royalties, b.publisher
            FROM orders as o
            INNER JOIN order_contains as oc
            ON o.order_id = oc.order_id
            INNER JOIN books as b
            ON b.isbn = oc.book_isbn
            WHERE o.order_id = '{order['order_id']}'
            """
            self.cursor.execute(sql)
            retList.append(self.cursor.fetchall())
            
        # print(f"retVal --> {retList}")
        return retList

    def getAllOrders(self):
        sql= '''
        SELECT * from orders
        '''
        self.cursor.execute(sql)
        
        array = []
        for t in self.cursor.fetchall():
            d = {
                'order_id' : t[0],
                'cardnumber' : t[1],
                'shipping_address' : t[2],
                'username' : t[3],
                'ship_date' : t[4],
                'expected_arrival' : t[5],
                'order_status' : t[6],
                'publisher_paid' : t[7],
                'total_sum' : t[8],
            }
            array.append(d)
        #print(array)
        return array

    def getOrdersForUser(self, username):
        sql= f'''
        SELECT order_id from placed_orders WHERE username = '{username}'
        '''
        self.cursor.execute(sql)
        
        orders = []
        for orderIDTuple in self.cursor.fetchall():
            orders.append(self.getOrderInfo(orderIDTuple[0]))

        return orders
    
    def addBookQuery(self, isbn, name, num_of_pages, price, publisher, current_stock, last_month_sales, min_stock, authors, genres):

        sql = self.insertIntoSql("books", [isbn, name, num_of_pages, price, publisher, random.uniform(0.05, 0.20), current_stock, last_month_sales, min_stock] )
        self.cursor.execute(sql)
       
        # add to the books_genres table

        for a in authors:
            sql = '''
            INSERT INTO book_authors (isbn, author)
            VALUES (
            '''
            sql+= isbn + ",'" + a  + "');"
            self.cursor.execute(sql)

        for g in genres:
            sql = '''
            INSERT INTO book_genres (isbn, genre)
            VALUES (
            '''
            sql+= isbn + ",'" + g + "');"
            self.cursor.execute(sql)

    def addPublisherQuery(self, name, email, address, bank_account_number, phone_numbers):
        sql = '''
        INSERT INTO publisher
        VALUES (
        '''
        values = (f"'{name}', '{address}', '{email}', {bank_account_number}")
        sql += values + ");"
        self.cursor.execute(sql)


        for number in phone_numbers:
            sql = '''
            INSERT INTO publisher_phone_numbers
            VALUES (
            '''
            values = (f"'{name}', '{number}'")
            sql += values + ");"
            self.cursor.execute(sql)
    
    def getPublisherNamesQuery(self):
        sql = '''
        SELECT name
        FROM publisher
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getUnpaidOrdersQuery(self):
        sql = '''
        SELECT isbn
        FROM order
        WHERE publisher_paid = false
        '''

        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getAllUserInfo(self,username):
        sql = (f"SELECT * FROM users WHERE username = '{username}'")
        self.cursor.execute(sql)
        array = []
        #print(sql)
        
        for tuple in self.cursor.fetchall():
            d = {
                'username': tuple[0],
                'password': tuple[1],
                'cardnumber': tuple[2],
                'address': tuple[3]
            }
            array.append(d)

        #print(array)
        return array




#         CREATE TABLE users(
# 	username varchar UNIQUE,
# 	password varchar NOT NULL,
# 	cardnumber bigint NOT NULL,
# 	address varchar NOT NULL,
# 	PRIMARY KEY(username)
# );

       
    def getUser(self, username):
        sql = (f"SELECT username FROM users WHERE username = '{username}'")
        self.cursor.execute(sql)
        usernamesql = self.cursor.fetchall()
        if(len(usernamesql)>0):
            return 0
        else:
            return 1
    
    def addUser(self,username,password,cardnumber,address):
        sql = self.insertIntoSql('users', [username,password,cardnumber,address])
        self.cursor.execute(sql)
    
    
    def addBillingInfo(self, cardnumber, cardholder_name, exp_date, address):
        sql = self.insertIntoSql("billing_info", [cardnumber, cardholder_name, exp_date, address] )
        self.cursor.execute(sql)
        return cardnumber


    def loginQuery(self,username, password):
        sql = (f"SELECT username FROM users WHERE username = '{username}' AND password = '{password}'")
        self.cursor.execute(sql)
        usernamesql = self.cursor.fetchall()
        if(len(usernamesql)==1):
            if(username == 'admin'):
                return 'admin'
            else:
                return username
        else:
            return 0
       
    def insertIntoSql(self, into, values):
        if isinstance(into, str) == False:
            raise ValueError('into is not a string.')

        sql = (f"INSERT INTO {into} VALUES(")


        add = []
        for v in values:
            if isinstance(v, str):
                add.append("'" + v + "'")
            else:
                add.append(str(v))

        sql += ", ".join(add) + ");"
        return sql
        
    def selectSql(self, table, columns, where_clause=None):
        sql = "SELECT " + ", ".join(columns) + " FROM " + table
        if where_clause:
            sql += " WHERE " + where_clause
        return sql



# sql function
