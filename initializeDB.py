import pymysql
db = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'MyNewPass')
    #database = 'petshop')

cursor = db.cursor()
cursor.execute("CREATE DATABASE petshop")
cursor.execute("Show databases")
clist = [i for i in cursor.fetchall()] 
print(clist)

dbpets = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'MyNewPass',
    database = 'petshop')

#ALL CODE FOR MAKING TABLES HERE 


curpets = dbpets.cursor()
curpets.execute("CREATE TABLE places (cid int, oid int)")
curpets.execute("show tables")
clist = [i for i in curpets.fetchall()] 
print(clist)
dbpets.commit()
dbpets.close()

#DELETE BELOW WHEN DONE, KEEP commit and close though.  

cursor.execute("Drop database petshop")
cursor.execute("Show databases")
clist = [i for i in cursor.fetchall()] 
print(clist)
db.commit()
db.close()





#cursor.execute("ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass';")
