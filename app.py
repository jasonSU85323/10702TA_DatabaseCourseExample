import web
import configparser
import pymysql
import os
import json
import time
import sys
import random


urls = (
    '/','index',
    '/Inquire', 'Inquire',
    '/insert', 'insert',
    '/update', 'update',
    '/delete', 'delete',
)

web.config.debug = False
app = web.application(urls, globals())

# Read Configure
conf = configparser.ConfigParser()
conf.read("config.conf")

#Databse definition
# SQLtitle = "MySQL Database"
# address = conf.get(SQLtitle, "address"   )    
# port = int(conf.get(SQLtitle, "port"   ))
# account = conf.get(SQLtitle, "account"     )
# password = conf.get(SQLtitle, "password"   )
# datasheet = conf.get(SQLtitle, "datasheet"   )
SQLtitle = "XMAPP"
address = conf.get(SQLtitle, "address"   )    
port = int(conf.get(SQLtitle, "port"   ))
account = conf.get(SQLtitle, "account"     )
password = conf.get(SQLtitle, "password"   )
datasheet = conf.get(SQLtitle, "datasheet"   )

#Template definition
template = conf.get("Template", "template" )
render = web.template.render(template)

class index:  
    def GET(self):
        return render.Inquire()

class Inquire:
    def __init__(self):  
        #Value definition
        self.mode = []             
        #Databse definition
        self.db = pymysql.connect(host=address, port=port, user=account, passwd=password, db=datasheet, charset='utf8')
        self.cursor = self.db.cursor()
    def GET(self):
        return render.Inquire()        
    def POST(self):
        i = web.input()

        sql =   """
                    SELECT e.e_id, e.name, e.rank,  d.name
                    FROM employee as e JOIN department as d ON e.d_id=d.d_id
                """
        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        for row in data:
            # print(row[5])
            v = {'Eid':row[0], 'Ename':row[1], 'rank':row[2], 'Dname':row[3]}
            # print(v)
            self.mode.append(v)
        self.db.close()
        # print(self.mode)
        web.header('Content-Type', 'application/json')
        return json.dumps(self.mode)

class insert:
    def __init__(self):      
        #Databse definition
        self.db = pymysql.connect(host=address, port=port, user=account, passwd=password, db=datasheet, charset='utf8')
        self.cursor = self.db.cursor()
    def GET(self):
        return render.insert()        
    def POST(self):
        i = web.input()
        Ename = i.Ename
        Dname = i.Dname

        sql1 = "SELECT d_id FROM department WHERE name=\'{}\'".format(Dname)
        self.cursor.execute(sql1)
        data = self.cursor.fetchone()

        sql = "INSERT INTO employee(e_id, name, d_id) VALUES (\'{}\', \'{}\', \'{}\')"\
            .format(str(random.randint(1, 1000)), str(Ename), str(data[0]))
        # print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        self.db.close()        
        return  '''
                    <script language="JavaScript">
                        window.alert('insert OK!!');
                        window.location.href='/';
                    </script>
                '''    

class update:
    def __init__(self):      
        #Databse definition
        self.db = pymysql.connect(host=address, port=port, user=account, passwd=password, db=datasheet, charset='utf8')
        self.cursor = self.db.cursor()     
    def GET(self):
        return render.update()
    def POST(self):
        i = web.input()
        if i.fun=="fun1":
            web.header('Content-Type', 'application/json')
            return self.fun1(i.Eid, i.Ename)
        elif i.fun=="fun2":
            self.fun2(i.tid, i.tname, i.trank, i.td)
            return  "update OK!!"          
  
    def fun1(self, Eid, Ename):
        sql =   """
                    SELECT e.e_id, e.name, e.rank,  d.name
                    FROM employee as e JOIN department as d ON e.d_id=d.d_id
                    WHERE e.e_id=\'{}\' AND e.name=\'{}\'
                """.format(Eid, Ename)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        self.db.close()
        return json.dumps(data)

    def fun2(self, tid, tname, trank, td):
        sql1 = "SELECT d_id FROM department WHERE name=\'{}\'".format(td)
        self.cursor.execute(sql1)
        data = self.cursor.fetchone()

        sql = "UPDATE employee as e SET e.name=\'{}\', e.rank=\'{}\', e.d_id=\'{}\' WHERE e_id=\'{}\'".format(tname, trank, data[0], tid)
        # print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        self.db.close()

class delete:
    def __init__(self):      
        #Databse definition
        self.db = pymysql.connect(host=address, port=port, user=account, passwd=password, db=datasheet, charset='utf8')
        self.cursor = self.db.cursor()
    def GET(self):
        return render.delete()
    def POST(self):
        i = web.input()
        Ename = i.Ename

        sql = "DELETE FROM employee WHERE name=\'{}\'".format(Ename) 
        # print(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            self.db.close()
            return  '''
                        <script language="JavaScript">
                            window.alert('delete OK!!');
                            window.location.href='/';
                        </script>
                    '''                
        except Exception as e:
            return  '''
                        <script language="JavaScript">
                            window.alert('Error {}');
                            window.location.href='/';
                        </script>
                    '''.format(e)                 




if __name__ == "__main__":
    app.run()
