# Establish connection to MySQL database
import mysql.connector
import re

mydb = mysql.connector.connect(
    host="localhost",
    user="ESP32",
    password="esp32io.com",
    database="strack"
)

# Create a cursor object
mycursor = mydb.cursor()

# Execute the query
query = "Select count(*) from ranges;"
mycursor.execute(query)

myresult = mycursor.fetchall()
filtered_list = [tup for tup in myresult[0]]
print(filtered_list[0])

if (filtered_list[0] > 500):
    queryDelete = "DELETE FROM ranges ORDER BY r_ID LIMIT 500;"
    mycursor.execute(queryDelete)
    mydb.commit()
    print("gelöscht")


# Close database connection
mydb.close()
