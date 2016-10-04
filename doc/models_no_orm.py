import mysql.connector

def get_conn():
    host = '127.0.0.1'
    port = 3306
    db = "micblog"
    user = "root"
    passwd = "159357"
    conn = mysql.connector.connect(
            host = host,
            user = user,
            password = passwd,
            db = db,
            port = port)
    return conn

#  ORM
#  与数据库里的表映射类
class User(object):
    def __init__ (self, user_id, user_name, user_passwd):
        self.user_id = user_id
        self.user_name = user_name
        self.user_passwd = user_passwd

    def save(self):
        conn = get_conn()
        cursor = conn.cursor()
        sql = "insert into users(user_id, user_name, user_passwd) values (%s, %s, %s)"
        cursor.execute(sql,(self.user_id, self.user_name, self.user_passwd))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def query_all():
        conn = get_conn()
        cursor = conn.cursor()
        sql = "select * from users"
        cursor.execute(sql)
        raws = cursor.fetchall()
        users=[]
        for r in raws:
            user = User(r[0], r[1], r[2])
            users.append(user)
        conn.commit()
        cursor.close()
        conn.close()
        return users

    def __str__(self):
        return "id:{}\tname:{}\t passwd:{}".format(self.user_id, self.user_name, self.user_passwd)

