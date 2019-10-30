# encoding: utf-8
import MySQLdb


class MysqldbHelper:
    # 获取数据库连接
    def getCon(self):
        try:
            conn = MySQLdb.connect(host='localhost', user='admin', passwd='admin', db='test', port=3306,
                                   charset='utf8')
            return conn
        except MySQLdb.Error, e:
            print "Mysqldb Error:%s" % e

    # 查询方法，使用con.cursor(MySQLdb.cursors.DictCursor),返回结果为字典
    def select(self, sql):
        try:
            con = self.getCon()
            print con
            cur = con.cursor(MySQLdb.cursors.DictCursor)
            count = cur.execute(sql)
            fc = cur.fetchall()
            return fc
        except MySQLdb.Error, e:
            print "Mysqldb Error:%s" % e
        finally:
            cur.close()
            con.close()

    # 带参数的更新方法
    def updateByParam(self, sql, params):
        try:
            con = self.getCon()
            cur = con.cursor()
            count = cur.execute(sql, params)
            con.commit()
            return count
        except MySQLdb.Error, e:
            con.rollback()
            print "Mysqldb Error:%s" % e
        finally:
            cur.close()
            con.close()

    # 不带参数的更新方法
    def update(self, sql):
        try:
            con = self.getCon()
            cur = con.cursor()
            count = cur.execute(sql)
            con.commit()
            return count
        except MySQLdb.Error, e:
            con.rollback()
            print "Mysqldb Error:%s" % e
        finally:
            cur.close()
            con.close()


if __name__ == "__main__":
    db = MysqldbHelper()


    def get():
        sql = "select * from movie"
        fc = db.select(sql)
        for row in fc:
            print row["title"]


    def ins():
        sql = "insert into movie values(null,'test','test', 'test', 'test', 'test',now())"
        count = db.update(sql)
        print count


    def insparam():
        sql = "insert into movie(`title`, `pic_url`, `target_url`, `introduction`, `download_url`, `create_time`) values(%s,%s,%s,%s, %s,now())"
        params = ('test1','test1', 'test1', 'test1', 'test1')
        count = db.updateByParam(sql, params)
        print count


    def delop():
        sql = "delete from movie where id=4"
        count = db.update(sql)
        print "deleted rows：" + str(count)


    def change():
        sql = "update movie set title='test2' where id=5"
        count = db.update(sql)
        print count

    # get()
    # ins()
    # insparam()
    # delop()
    # change()
