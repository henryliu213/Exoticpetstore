import pymysql
db = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'dr4g0n123!')
    #database = 'petshop')
#password = 'MyNewPass'

cursor = db.cursor()



cursor.execute("Drop database petshop")
# cursor.execute("Show databases")
# clist = [i for i in cursor.fetchall()] 
# print(clist)

cursor.execute("CREATE DATABASE if not exists petshop ")
cursor.execute("Show databases")
clist = [i for i in cursor.fetchall()] 
# print(clist)

dbpets = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'dr4g0n123!',
    database = 'petshop')

#ALL CODE FOR MAKING TABLES HERE 
STORECAPACITY = 10

curpets = dbpets.cursor()
curpets.execute("CREATE TABLE if not exists customers (cid int not null auto_increment, name varchar(255) not null unique, primary key (cid))")
curpets.execute("CREATE TABLE if not exists pets (pid int not null auto_increment, name varchar(255) not null, type varchar(255), age int check(age >= 0), primary key (pid))")
curpets.execute("CREATE TABLE if not exists orders (oid int not null auto_increment, odate DATE, primary key (oid))")
curpets.execute("CREATE TABLE if not exists accessories (aid int not null auto_increment, name varchar(255), primary key (aid))")
curpets.execute("CREATE TABLE if not exists contains (oid int, aid int unique, pid int unique, foreign key(oid) references orders(oid) on delete cascade, foreign key(aid) references accessories(aid) on delete cascade, foreign key(pid) references pets(pid) on delete cascade)")
curpets.execute("CREATE TABLE if not exists places (cid int, oid int, Foreign key(cid) references customers (cid) on delete cascade, foreign key(oid) references orders(oid) on delete cascade)")
curpets.execute("""Create trigger if not exists atcapacity
                    before insert on pets 
                for each row 
                Begin 
                    if (select count(*) from pets p where p.pid not in (select pid from contains)) >= %s  
                    then signal sqlstate '45000'
                    set message_text = "store too small";
                    end if;
                end;""", STORECAPACITY)

curpets.execute("""Create procedure if not exists getOrderInfo(in soid int)
                begin
                    select a.name as info, count(a.aid) as count from contains C, accessories A where C.aid = A.aid and C.oid = soid group by a.name 
                    Union 
                    select p.type as info, count(p.pid) as count from pets P, contains C where  C.pid = p.pid and C.oid = soid group by p.type;
                end
""")

curpets.executemany(" insert into pets (name, type, age) values (%s,%s,%s)", 
                [('zoe','zebra',4),
                ('samantha','snake',2),
                ('fred', 'frog', 1),
                ('laika', 'dog', 0),
                ('lucy', 'dog', 2),
                ('finnegan', 'dog', 11),
                ('oreo', 'cat', 5),
                ('tom', 'cat', 0),
                ('mousy', 'mouse', 0),
                ('lia', 'lion', 1)])

# curpets.executemany("insert into pets (name, type, age) values (%s,%s,%s)", 
#                 [('zoe','zebra',4),
#                 ('samantha','snake',2),
#                 ('fred', 'frog', 1),
#                 ('laika', 'dog', 0),
#                 ('lucy', 'dog', 2)])
# curpets.executemany("insert into accessories (name) values (%s)", 
#                     [("food"),
#                      ("food"),
#                      ("leash"),
#                      ("leash"),
#                      ("leash"),
#                      ("collar")])


curpets.execute("select * from pets")
clist = [i for i in curpets.fetchall()] 
print("\nPets: ")
print(clist)
curpets.execute("select * from accessories")
clist = [i for i in curpets.fetchall()] 
print("\nAccessories: ")
print(clist)
curpets.execute("select * from orders")
clist = [i for i in curpets.fetchall()] 
print("\nOrders: ")
print(clist)
curpets.execute("select * from places")
clist = [i for i in curpets.fetchall()] 
print("\nPlaces: ")
print(clist)
curpets.execute("select * from contains")
clist = [i for i in curpets.fetchall()] 
print("\nContains: ")
print(clist)
curpets.execute("select * from customers")
clist = [i for i in curpets.fetchall()] 
print("\nCustomers: ")
print(clist)




# curpets.callproc("getOrderInfo", (1,))
# clist = [i for i in curpets.fetchall()] 
# print("\nOrder 1: ")
# print(clist)



dbpets.commit()
dbpets.close()

#DELETE BELOW WHEN DONE, KEEP commit and close though.  

# cursor.execute("Drop database petshop")
# cursor.execute("Show databases")
# clist = [i for i in cursor.fetchall()] 
# print(clist)
db.commit()
db.close()






#cursor.execute("ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass';")
