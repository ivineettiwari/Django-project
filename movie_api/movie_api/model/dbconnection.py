import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="vineet@123",
  database="movie"
)

mycursor = mydb.cursor()

def mysql_select(query, val = None):
    try:
        mycursor.execute(query, val)
        myresult = mycursor.fetchall()
        return myresult
    except Exception as e:
        raise Exception(e)
    
def mysql_insert(query, val):
    try:
        mycursor.execute(query, val)
        mydb.commit()
        resp = str(mycursor.rowcount) + " record inserted."
        return resp 
    except Exception as e:
        raise Exception(e)
    

def mysql_update(query):
    try:
        mycursor.execute(query)
        mydb.commit()
        return str(mycursor.rowcount) + " record(s) affected"
    except Exception as e:
        raise Exception(e)