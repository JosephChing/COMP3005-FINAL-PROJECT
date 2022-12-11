import psycopg2
import queries

databaseName = "bookstoreTest"
databaseUser = 'postgres'
databasePassword = 'Baseball55@'
databaseHost='127.0.0.1'
databasePort= '5432'
#establishing the connection
conn = psycopg2.connect(
   database=databaseName, user=databaseUser, password=databasePassword, host=databaseHost, port= databasePort
)
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

f = open("ddl.sql", "r")

sqlremove = """DROP SCHEMA public CASCADE;
CREATE SCHEMA public;"""
cursor.execute(sqlremove)

sqlfile = f.read()
print(sqlfile)
cursor.execute(sqlfile)

print("Database created successfully........")



#Closing the connection
conn.close()



q = queries.Query()


q.addBillingInfo('9829367583','Sugma','22-11','73 oak st')
q.addBillingInfo('8234234923','Sugon','22-11','73 maple st')
q.addBillingInfo('6243824939','Sugon','22-11','73 maple st')

#addUser(self,username,password,cardnumber,address):
q.addUser('admin','pass','9829367583','77 goober street')
q.addUser('cal','pass','8234234923','22 Goober street')

#addPublisherQuery(self, name, email, address, bank_account_number, phone_numbers):
q.addPublisherQuery('penguin random house','penguin@email.com','99 antarctica ave','837292349',['6178464','9325843'])
q.addPublisherQuery('dk','dk@email.com','333 sweet ave','1829349281' , ['12112','1232365'])
q.addPublisherQuery('simon and goofster','sandg@email.com','7232 america ave','12342893', ['5433543'])
q.addPublisherQuery('harper collins','hc@email.com','729 book st','18234050993', ['2333123','23666'])
q.addPublisherQuery('ottawa publisher','ottawapublisherg@email.com','111 ottawa st','2134752859', ['5455468','546213'])
q.addPublisherQuery('awesome books','awesomebooks@email.com','1 a st','2134122859', ['5455468','546213'])


#def addBookQuery(self, isbn, name, num_of_pages, price, publisher, current_stock, last_month_sales, min_stock, authors, genres):
# addBookQuery(self, isbn, name, num_of_pages, price, publisher, current_stock, last_month_sales, min_stock, authors, genres):
# q.addBookQuery("00000000000", "dog", "11", "0", "a", "0", "0", "0", ["joe", "bob"], ["f", "c", "z"])
q.addBookQuery("10231203123", "Harry potter", "500", "35", "penguin random house", "123", "18", "10", ["JK rowling", "Dogmaster"], ["fantasy", "fiction", "magic"])
q.addBookQuery("18231283291", "The Catcher in the Rye", "364", "30", "dk", "12311", "3", "12", ["JD salinger", "Bobby bill"], ["coming of age", "biograophy"])
q.addBookQuery("57481737129", "Pride and Prejudice", "342", "20", "dk", "11", "10", "14", ["Jane Austen"], ["coming of age", "biograophy"])
q.addBookQuery("93749249271", "The Picture of Dorian Gray", "999", "15", "harper collins", "133", "4", "10", ["Oscar Wilde", "Dorian Gray"], ["fiction", "history", "science"])
q.addBookQuery("12312321313", "War and Peace", "9909", "35", "ottawa publisher", "33", "1", "10", ["Oscar Wilde", "Dorian Gray"], ["fiction", "history", "science"])
q.addBookQuery("56293847182", "Don Quixote", "933", "53", "ottawa publisher", "3", "11", "10", ["Miguel de Cervantes"], ["fiction", "classic"])
q.addBookQuery("29304528573", "The Odyssey", "347", "20", "penguin random house", "33", "132", "10", ["Homer"], ["fiction", "history", "science"])



# def addOrderQuery(self, cardnumber, shipping_address, username, cartIsbns, cartTotal)
q.addOrderQuery("8234234923", "43 Dog Cat Boolevard", "cal", ["18231283291", "93749249271"], 148)
q.addOrderQuery("8234234923", "43 VHS playe Street", "cal", ["12312321313", "57481737129"], 248)
q.addOrderQuery("8234234923", "43 VHS playe Street", "cal", ["12312321313", "10231203123"],288)