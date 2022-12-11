# COMP3005-FINAL-PROJECT
The repository for the final project in COMP 3005.


Project by: Callum Hendry(100970932) and Joseph Ching (101185426)

Setup Instructions:

1.Setup a blank Postgresql database. Record the database name, username, password and port

2.Install python package psycopg2 (two possible options)
    $ pip install psycopg2
    $ pip install psycopg2-binary

     https://www.psycopg.org/docs/install.html provides more instructions.

3.Modify the python line in queries.py with the call psycopg2.connect and databaseinitializer.py where the databaseName, databaseUser, databasePassword, databaseHost, databasePort    are declared. Change the parameters appropriately for your database.

4.Run python databaseinitializer.py. This inserts a number of dummy values into the database.

5.Run python main.py

6.When prompted by the login menu you can create a new account as a user. There is an account with username:cal, password:pass, which already has orders and items in the cart. In order to log in as the owner to view the owners functionality, like adding and removing books, report, etc log in with username:admin, password:pass.
