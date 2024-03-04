import mysql.connector
import hashlib

# Constants
SALT = "PasswordSalt"  

sourceHost = "localhost"
sourceUser = "root"
sourcePassword = ""
sourceDatabase = "elearning"

# DATABASE CONNECTION
def connectToDb():

    host = "localhost"
    user = "root"
    dbPass = ""
    database = "omr"

    try:
        # Connect to the MySQL server
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=dbPass,
            database=database
        )

        if connection.is_connected():
            print("Connected to the MySQL server")
            return connection

    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return None

# Establish connection of the firt database
connection = connectToDb()

# Create cursor for the "omr" database
cursor = connection.cursor()

# Connect to source database
sourceConnection = mysql.connector.connect(
    host = sourceHost,
    user = sourceUser,
    password = sourcePassword,
    database = sourceDatabase
)

# Create cursor for source database
source_cursor = sourceConnection.cursor()

# Query data from source table
source_cursor.execute("SELECT * FROM activity")

#Fetch all rows from the source table
rows = source_cursor.fetchall()

for row in rows:
    cursor.execute("INSERT INTO activity VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)

# Commit the transaction
connection.commit()

# Close cursors and connection
cursor.close()
source_cursor.close()
sourceConnection.close()




## USERS

def hash_password(password):
    salted_password = password + SALT
    hashed_password = hashlib.md5(salted_password.encode()).hexdigest()
    return hashed_password

def createUsersTable(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                name TEXT,
                surname TEXT,
                email TEXT NOT NULL,
                password TEXT
            )
        """)
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print("Error:", err)
    else:
        return connection


def initializeUsersTable():
    connection = connectToDb()
    if connection:
        cursor = connection.cursor()
        createUsersTable(connection)
        return connection, cursor
    else:
        print("Failed to initialize users table.")
        return None, None


def register(name, surname, email, password):
    con, cursor = initializeUsersTable()
    try:
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (name, surname, email, password) VALUES (%s, %s, %s, %s)",
                       (name, surname, email, hashed_password))
    except mysql.connector.Error as err:
        print("Error:", err)
        return False
    else:
        con.commit()
        con.close()
        return True

def login(email, password):
    con, cursor = initializeUsersTable()
    try:
        cursor.execute(
            "SELECT email, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user and user[1] == hash_password(password):
            return True
        return False
    except mysql.connector.Error as err:
        print("Error:", err)
        return False
    finally:
        con.close()

def getUserByEmail(email):
    con, cursor = initializeUsersTable()
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
    except mysql.connector.Error as err:
        print("Error:", err)
        return None
    else:
        con.close()
        if not user:
            return None
        else:
            return user


def deleteUserByEmail(email):
    con, cursor = initializeUsersTable()
    try:
        cursor.execute("DELETE FROM users WHERE email = %s", (email,))
        con.commit()
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        con.close()



## OPERATION

def createOperationsTable(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS operations(id TEXT NOT NULL, email TEXT, answerKey TEXT, PRIMARY KEY (id(255)))")
        connection.commit()
        cursor.close()
        print("Operations table created successfully")
    except mysql.connector.Error as err:
        print("Error creating operations table:", err)
    else:
        return connection


def initializeOperationsTable():
    connection = connectToDb()
    if connection:
        cursor = connection.cursor()
        createOperationsTable(connection)
        return connection, cursor
    else:
        print("Failed to initialize operations table.")
        return None, None


def getOperationsByEmail(email):
    con, cursor = initializeOperationsTable()
    try:
        cursor.execute("SELECT * FROM operations WHERE email = %s", (email,))
        operations = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Error:", err)
        return None
    else:
        con.close()
        if not operations:
            return None
        else:
            operations.reverse()
            return operations



def addOperation(id, email, answerKey):
    con, cursor = initializeOperationsTable()
    id = id.split('uploads/')[1]
    try:
        cursor.execute("INSERT INTO operations (id, email, answerKey) VALUES (%s, %s, %s)",
                       (id, email, answerKey))
    except mysql.connector.Error as err:
        print("Error:", err)
        return False
    else:
        con.commit()
        con.close()
        return True


def getOperationById(id):
    con, cursor = initializeOperationsTable()
    try:
        cursor.execute("SELECT * FROM operations WHERE id = %s", (id,))
        record = cursor.fetchone()
    except mysql.connector.Error as err:
        print("Error:", err)
        return None
    else:
        con.close()
        if not record:
            return None
        else:
            return record


def deleteOperation(id):
    con, cursor = initializeOperationsTable()
    try:
        cursor.execute("DELETE FROM operations WHERE id = %s", (id,))
        con.commit()
    except mysql.connector.Error as err:
        print("Error:", err)
        return False
    finally:
        con.close()
        return True


##  RECORDS

def createRecordsTable(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS records(id TEXT, nameImage TEXT, correct INT, wrong INT, empty INT, score REAL, answers TEXT, image TEXT)")
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print("Error:", err)
    else:
        return connection


def initializeRecordsTable():
    connection = connectToDb()
    if connection:
        cursor = connection.cursor()
        createRecordsTable(connection)
        return connection, cursor
    else:
        print("Failed to initialize records table.")
        return None, None


def getRecordsById(id):
    con, cursor = initializeRecordsTable()
    try:
        cursor.execute("SELECT * FROM records WHERE id = %s", (id,))
        records = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Error:", err)
        return None
    else:
        con.close()
        if not records:
            return None
        else:
            return records

def addRecord(id, nameImage, correct, wrong, empty, score, answer, image):
    con, cursor = initializeRecordsTable()
    id = id.split('uploads/')[1]
    try:
        cursor.execute("INSERT INTO records (id, nameImage, correct, wrong, empty, score, answers, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (id, nameImage, correct, wrong, empty, score, answer, image))
    except mysql.connector.Error as err:
        print("Error:", err)
        return False
    else:
        con.commit()
        con.close()
        return True




# Example usage:

##Francis Code

# if connection:
#     # Do something with the connection
#     pass
# else:
#     print("Failed to connect to the database.")