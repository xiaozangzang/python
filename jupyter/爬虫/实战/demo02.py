#将文件中数据读出来解析并写入对应数据库
import pymysql
import random

createuserid = random.randint(6,829)
bankuai_id = random.randint(5,14)
zhutiid = random.randint(1,23)
		
#读取文件数据，写入数据库
def save_user(conn):
	#创建游标
	cursor = conn.cursor()
	usernames = read_file()
	while len(usernames) > 0:
		username = usernames.pop()
		print(username)
		effect_row = cursor.execute('insert into jbbs_user(name,loginname,pwd,img,createtime,zhuceip,loginip,flag,jifen,onlinetime)' 
			+'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
			,(username,username,'4QrcOUm6Wau+VuBX8g+IPg==','touxiang.jpg','2018-05-24 15:22:26','192.168.43.192','192.168.43.192','1','0','0'))	
		# 提交
		conn.commit()
	cursor.close()
	
def read_user_file():
	file = open('用户.txt','r',encoding = 'utf-8')
	all_data = file.readlines()
	#将所有用户名放入集合中
	usernames = set()
	for row in all_data:
		username = row.split(':')[0]
		usernames.add(username)
	return usernames

	#保存帖子
def save_tiezi(conn,zhuti,name):
	#创建游标
	cursor = conn.cursor()
	#将帖子保存至数据库
	effect_row = cursor.execute('insert into jbbs_tiezi(name,contenthtml,contenttxt,createtime,createuserid,bankuai_id,zhutiid,findcount,huifuid)' 
		+'values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		,(zhuti,'<p>'+name+'</p>',name,'2018-05-24 15:22:26',str(createuserid),str(bankuai_id),str(zhutiid),'0','0'))
	conn.commit()
	cursor.close()
	
def read_tiezi_file():
	file = open('帖子的内容.txt','r',encoding = 'utf-8')
	all_data = file.readlines()
	return all_data	
		
	
def save_huifu(conn,huifu,tiezi_id,orderby):
	#创建游标
	cursor = conn.cursor()
	#将帖子保存至数据库
	effect_row = cursor.execute('insert into jbbs_huifu(tieziid,contenthtml,contenttxt,createtime,createuserid,isdel,orderby)' 
		+'values(%s,%s,%s,%s,%s,%s,%s)'
		,(tiezi_id,'<p>'+huifu+'</p>',huifu,'2018-05-24 15:22:26',str(createuserid),'0',orderby))
	conn.commit()
	cursor.close()

	
# 获取帖子id	
def get_tiezi_id(conn,name):
	cursor = conn.cursor()
	print(name)
	#获取该帖子的ID
	effect = cursor.execute("SELECT id FROM jbbs_tiezi WHERE name = '" + name +"'")
	row = cursor.fetchone()
	return row
	
#将帖子写入数据库
def save(conn):
	rows = read_tiezi_file()
	while len(rows) > 0:
		zhuti = ''
		name = ''
		tiezi_id = ''
		if rows[0] == '******主题***********'+'\n':
			zhuti = rows[1]
			name = rows[3]
			save_tiezi(conn,zhuti,name)
			del rows[0]
			del rows[0]
			del rows[0]
			del rows[0]
			tiezi_id = get_tiezi_id(conn,name)
			print(tiezi_id)
			orderby = 0
			#将回复保存至数据库
			while rows[0] != '******主题***********'+'\n':
				orderby += 1
				huifu = rows[0].split(':')[1]
				save_huifu(conn,huifu,tiezi_id,orderby)
				del rows[0]
	
def getConn():
	# 创建连接
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='bbs', charset='utf8')
	return conn
	
def close(conn):
	# 关闭连接
	conn.close()
	
if __name__ == '__main__':
	conn = getConn()
	#将用户名写入数据库
	#save_user(conn)
	#read_file()
	#将帖子写入数据库
	save(conn)
	
	#关闭连接
	close(conn)
