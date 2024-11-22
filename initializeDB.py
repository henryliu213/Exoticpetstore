import pymysql
db = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'MyNewPass')
    #database = 'petshop')


cursor = db.cursor()
# cursor.execute("Drop database petshop")
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
    password = 'MyNewPass',
    database = 'petshop')

#ALL CODE FOR MAKING TABLES HERE 
STORECAPACITY = 10

curpets = dbpets.cursor()
curpets.execute("CREATE TABLE if not exists customers (cid int not null auto_increment, name varchar(255) not null, primary key (cid))")
curpets.execute("CREATE TABLE if not exists pets (pid int not null auto_increment, name varchar(255) not null, type varchar(255), age int check(age >= 0), primary key (pid))")
curpets.execute("CREATE TABLE if not exists orders (oid int not null auto_increment, odate DATE, primary key (oid))")
curpets.execute("CREATE TABLE if not exists accessories (aid int not null auto_increment, name varchar(255), primary key (aid))")
curpets.execute("CREATE TABLE if not exists contains (oid int, aid int, pid int, foreign key(oid) references orders(oid) on delete cascade, foreign key(aid) references accessories(aid) on delete cascade, foreign key(pid) references pets(pid) on delete cascade)")
curpets.execute("CREATE TABLE if not exists places (cid int, oid int, Foreign key(cid) references customers (cid) on delete cascade, foreign key(oid) references orders(oid) on delete cascade)")
curpets.execute("""Create trigger if not exists atcapacity
                    before insert on pets 
                for each row 
                Begin 
                    if (select count(*) from pets p) >= %s  
                    then signal sqlstate '45000'
                    set message_text = "store too small";
                    end if;
                end;""", STORECAPACITY)

curpets.execute("""Create procedure if not exists getOrderInfo(in soid int)
                begin
                    select a.name as info, count(a.aid) as count from orders O, accessories A where O.oid = soid and O.aid = A.aid group by a.name 
                    Union 
                    select p.type as info, count(p.pid) as count from orders O, pets P where O.oid = soid and o.pid = p.pid group by p.type;
                end
""")

n = 'po'
t = 'panda'
a = 55
curpets.execute(" insert into pets (name, type, age) values ('fred','zebra', 2),(%s,%s,%s)", (n,t,a))

curpets.execute("select * from pets")
clist = [i for i in curpets.fetchall()] 
print(clist)
dbpets.commit()
dbpets.close()

#DELETE BELOW WHEN DONE, KEEP commit and close though.  

cursor.execute("Drop database petshop")
cursor.execute("Show databases")
clist = [i for i in cursor.fetchall()] 
# print(clist)
db.commit()
db.close()





#cursor.execute("ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass';")
