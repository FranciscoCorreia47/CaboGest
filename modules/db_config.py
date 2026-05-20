import mysql.connector

connection = mysql.connector.connect(
        host="localhost",
        user="cabogest",
        password="c4b0_g3st#",
        database="cabogest_db"
    )

cursor = connection.cursor()