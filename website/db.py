import pyodbc

connectionString = f'DRIVER={{SQL Server}};SERVER=SHADAN\SQLEXPRESS;DATABASE=UserNew;'
conn = pyodbc.connect(connectionString)

cursor = conn.cursor()
cursor.execute("SELECT * FROM UsersList")

for row in cursor.fetchall():
    print (row)