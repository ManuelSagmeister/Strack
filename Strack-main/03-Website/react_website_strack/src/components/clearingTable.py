# Establish connection to MySQL database
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="diplo",
    password="htlDA2022!",
    database="strack"
)

# Create a cursor object
mycursor = mydb.cursor()

# Execute the query
query = "Select count(*) from ranges;"
mycursor.execute(query)

myresult = mycursor.fetchall()
filtered_list = [tup for tup in myresult[0]]


if (filtered_list[0] >= 800):
    queryDelete = "DELETE FROM ranges ORDER BY r_ID LIMIT 500;"
    mycursor.execute(queryDelete)
    mydb.commit()


# Close database connection
mydb.close()