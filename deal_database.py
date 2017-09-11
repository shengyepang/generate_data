import MySQLdb
conn= MySQLdb.Connect(host='localhost', user='root', passwd='931011', db='backup', charset='utf8mb4')
cur=conn.cursor()
insert_temp= 'insert into temp1 select DISTINCT  ApiID from apicate where CateID in (select ID from category where Amount <870)'
delete_api= 'delete from apibasic where ID in (select id from temp1)'
delete_cate= 'delete from category where Amount <870'
cur.execute(insert_temp)
cur.execute(delete_api)
cur.execute(delete_cate)
conn.close()