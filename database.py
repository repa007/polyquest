import pymysql

class DB:

    def __init__(self, host, port, user, password, db_name):
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

    def AddAdmin(self,tgname):
        query = f"INSERT INTO admin (tgname) VALUES('{tgname}')"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
            self.conn.commit()
        except pymysql.Error as e:
            return e
        
    def DeleteAdmin(self,tgname):
        query = f"DELETE FROM admin WHERE tgname='{tgname}'"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
            self.conn.commit()
        except pymysql.Error as e:
            return e
        
    def GetAdminByTgname(self,tgname):
        query = f"SELECT * FROM admin WHERE tgname='{tgname}'"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                if len(rows) < 1:
                    return None, "not found"
                if len(rows) > 1:
                    return rows, "dublicate"
                return rows[0], None
        except pymysql.Error as e:
            return None, e
        
    
    def NewTask(self,title,body,course,max):
        query = f"INSERT INTO tasks (title, body, course, max) VALUES ('{title}','{body}','{course}','{max}')"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                self.conn.commit()
        except pymysql.Error as e:
            return e
        
    def DeleteTask(self,id):
        query = f"DELETE FROM tasks WHERE id = {id}"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
            self.conn.commit()
        except pymysql.Error as e:
            return e
        
    def GetTasksAll(self):
        query = f"SELECT * FROM tasks ORDER BY course, title"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows, None
        except pymysql.Error as e:
            return None, e
        
    def GetTasksByCourse(self,course):
        query = f"SELECT * FROM tasks ORDER BY course, title WHERE course = '{course}'"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows, None
        except pymysql.Error as e:
            return None, e
    
    def AddStudent(self,name,lastname,group,course,tgname):
        query = f"INSERT INTO students (name,lastname,group,course,tgname) VALUES ('{name}','{lastname}','{group}','{course}','{tgname}')"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                self.conn.commit()
        except pymysql.Error as e:
            return e
    
    def DeleteStudent(self,id):
        query = f"DELETE FROM students WHERE id = {id}"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
            self.conn.commit()
        except pymysql.Error as e:
            return e
    
    def GetStudentByTgname(self,tgname):
        query = f"SELECT * FROM students WHERE tgname='{tgname}'"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                if len(rows) < 1:
                    return None, "not found"
                if len(rows) > 1:
                    return rows, "dublicate"
                return rows[0], None
        except pymysql.Error as e:
            return None, e
        
    def GetStudentsAll(self):
        query = f"SELECT * FROM students ORDER BY course, group, name"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows, None
        except pymysql.Error as e:
            return None, e
    

mydb = DB("std-mysql",3306,"std_2064_polyquest","qwerty123","std_2064_polyquest")

e = mydb.AddAdmin("@Semyon981")
print(e)

row,e = mydb.GetAdminByTgname("@Semyon981")
print(row,e)

e= mydb.DeleteAdmin("@Semyon981")
print(e)



