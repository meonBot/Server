import mysql.connector
import argparse

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="new_password"
)
class Database:
    def __init__(self, name):
        self.db_name=name
        self.mycursor = mydb.cursor()
        self.mycursor.execute("SHOW DATABASES")
        self.exists=False
        for row in self.mycursor:
            if(row[0]==self.db_name):
                print("Ddatabase "+self.db_name+" exists")
                self.exists=True
                self.mycursor.fetchall()
                self.mycursor.execute("USE "+self.db_name)
        self.mycursor.fetchall()
    def createdb(self):
        if(not self.exists):
            self.mycursor.execute("CREATE DATABASE "+self.db_name)
            self.exists=True
            self.mycursor.execute("USE "+self.db_name)
        else:
            print("Database "+self.db_name+" already exists!")
    def createtable(self,table_name):
        self.mycursor.execute("CREATE TABLE "+table_name+"(id INT NOT NULL AUTO_INCREMENT, PRIMARY KEY ( id ));")
        self.mycursor.fetchall()
    def addcolum(self, table_name, colum_name, colum_type):
        self.mycursor.execute("ALTER TABLE "+table_name)
        self.mycursor.fetchall()
        self.mycursor.execute("ALTER TABLE " + table_name + " ADD " + colum_name+ " "+colum_type)
            
class UsersDatabase:
    def __init__(self, db):
        self.db=db
    def createtable(self):
        self.db.createtable("Users")
        self.db.addcolum("Users", "username", "VARCHAR(30)")
    
class MainDatabase:
    def __init__(self, db):
        self.db=db
    def createtable(self):
        self.db.createtable("Main")

class StructureDatbase:
    pass
    
class App:
    def __init__(self, args):
        self.db_name=args["database_name"]
        self.db=Database(self.db_name)
        self.create_tables=args['create_db']
        self.main_db=MainDatabase(self.db)
        self.user_db=UsersDatabase(self.db)
    def createtable(self):
        self.db.createdb()
        self.main_db.createtable()
        self.user_db.createtable()
    def execute(self):
        if(self.create_tables):
            self.createtable()
        
parser = argparse.ArgumentParser(description='Art-classifier server.')
parser.add_argument('--database-name', '-m', required=True, help='Name of main db')
parser.add_argument('--create-db', '-c', type=bool, help='Create database')
app=App(vars(parser.parse_args()))
app.execute()
