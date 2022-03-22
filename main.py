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

    def addrow(self, table_name, columes, values):
        if (len(columes)<=0):
            return
        print("INSERT INTO " +table_name+ " (" + (",".join(columes)) + ") VALUES (" + "'" +("','".join(values)) +"')")
        self.mycursor.execute("INSERT INTO " +table_name+ " (" + (",".join(columes)) + ") VALUES (" + "'" +("','".join(values)) +"')")
        self.mycursor.execute("ALTER TABLE "+table_name)
        for row in self.mycursor:
            print(row[0])
        print("Done!")

class User:
    password_hash=None
    username=None
    def __init__(self):
        pass

class UsersDatabase:
    def __init__(self, db):
        self.db=db

    def createtable(self):
        self.db.createtable("Users")
        self.db.addcolum("Users", "username", "VARCHAR(50)")
        self.db.addcolum("Users", "password_hash", "VARCHAR(32)")

    def adduser(self, user):
        self.db.addrow("Users", ["username", "password_hash"], [user.username, user.password_hash])

class MainDatabase:
    def __init__(self, db):
        self.db=db
    def createtable(self):
        self.db.createtable("Main")

class StructureDatbase:
    pass

class App:
    def __init__(self, args):
        print(args)
        self.db_name=args["database_name"]
        self.db=Database(self.db_name)
        self.create_tables=args['create_db']
        self.main_db=MainDatabase(self.db)
        self.user_db=UsersDatabase(self.db)
        self.add_user=False
        if(args["add_user"]):
            self.add_user=True
            self.new_user=User()
            self.new_user.username=args["add_user"][0]
            self.new_user.password_hash=args["add_user"][1]

    def add_user(self, username, user_password_hash):
        self.last_new_user=User()
        self.last_new_user.username=username
        self.last_new_user.password_hash=user_password_hash

    def createtable(self):
        self.db.createdb()
        self.main_db.createtable()
        self.user_db.createtable()

    def execute(self):
        if(self.create_tables):
            self.createtable()
        if(self.add_user):
            self.user_db.adduser(self.new_user)    

parser = argparse.ArgumentParser(description='Art-classifier server.')
parser.add_argument('--database-name', '-m', required=True, help='Name of main db')
parser.add_argument('--create-db', '-c', help='Create database', action='store_true')
parser.add_argument('--add-user', '-a', nargs=2, metavar=('user_name', 'password_hash'), help='Manually add user')
app=App(vars(parser.parse_args()))
app.execute()
