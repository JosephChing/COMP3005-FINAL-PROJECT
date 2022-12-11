-- These queries are implemented in our python file. Variables are python variables
-- concatenated with the rest of the sql command.
-- These queries are not meant to be run without the appropriate variables inserted.
-- The variables use python string concatenation syntax.
-- Look at the queries.py for the appropriate queeries


-- NOTE THAT MOST IF NOT ALL INSERT QUERIES ARE PERFORMED USING A FUNCTION
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

-- This generates the appropriate sql for an inseriton.

-- getAllBooksQuery() 
SELECT isbn
FROM books

-- removeBookQuery(self,isbn)

DELETE FROM book_authors WHERE isbn = '{isbn}';
DELETE FROM book_genres WHERE isbn = '{isbn}';
DELETE FROM order_contains WHERE book_isbn = '{isbn}';
DELETE FROM books WHERE isbn = '{isbn}';

-- searchBookQuery(self, name, author, isbn, genre, publisherName)
-- Look at they python funciton for more information.
-- Some parameters are excluded if a None value is given for any attribute.
SELECT b.isbn
FROM books as b
WHERE b.bookname = '{name}' AND ba.author = '{author}' 
AND b.isbn = '{isbn}' AND b.genre = 'genre'
AND b.publisher = 'publisherName'



-- getBookQuery(self, isbn)
-- This gets a book based on isbn
SELECT * from books
WHERE isbn = '{isbn}'


--   def getUnpaidOrdersQuery(self):
-- this gets all orders that have not been paid yet. 
SELECT isbn
FROM order
WHERE publisher_paid = false

-- getAuthors(self,isbn), get the authors of a book by isbn.
SELECT author FROM book_authors
WHERE isbn = '{isbn}'

-- getGenres(self, isbn), get the genres of a book  by isbn.
SELECT genre FROM book_genres
WHERE isbn = '{isbn}'


--def getPublisherPayments(self):
-- this is used to return the relevent information regarding the royalites paid to the publisher from each order      
SELECT o.order_id, oc.quantity,b.price, b.pub_royalties, b.publisher
FROM orders as o
INNER JOIN order_contains as oc
ON o.order_id = oc.order_id
INNER JOIN books as b
ON b.isbn = oc.book_isbn
WHERE o.order_id = '{order['order_id']}'



--def addOrderQuery(self, cardnumber, shipping_address, username, cartIsbns, cartTotal):
-- This inserts an order into the order table. The appropriate strings are inserted in python.
sql = f'''INSERT INTO orders 
VALUES ('{order_id}', '{cardnumber}', '{shipping_address}', '{username}', '{ship_date}' ,'{expected_arrival}', '{order_status}', FALSE, {cartTotal})'''


--     def getOrderInfo(self, orderId):
-- return the order information based on orderid

SELECT * FROM orders AS o INNER JOIN order_contains AS oc ON oc.order_id = o.order_id WHERE o.order_id = '{orderId}'


-- getPublisherPayments(self)
-- gets al values required for publisher payments
SELECT o.order_id, oc.quantity,b.price, b.pub_royalties, b.publisher
FROM orders as o
INNER JOIN order_contains as oc
ON o.order_id = oc.order_id
INNER JOIN books as b
ON b.isbn = oc.book_isbn
WHERE o.order_id = '{order['order_id']}'

-- getAllOrders(self)
-- all orders
SELECT * from orders

-- get order for user by name
SELECT order_id from placed_orders WHERE username = '{username}'

--query to find user and verify password
SELECT username 
FROM users 
WHERE username = '{username}' 
AND password = '{password}'
       
--query to select all the info about the user
SELECT * 
FROM users 
WHERE username = '{username}