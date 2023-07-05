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
    #Добавить админа
    def AddAdmin(self,tgname):
        query = f"INSERT INTO admin (tgname) VALUES('{tgname}')"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
            self.conn.commit()
        except pymysql.Error as e:
            return e
    
    #Удалить админа
    def DeleteAdmin(self,tgname):
        query = f"DELETE FROM admin WHERE tgname='{tgname}'"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
            self.conn.commit()
        except pymysql.Error as e:
            return e
    
    #Получить админа по телеграмм id
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
        
    #Добавить задание
    def NewTask(self,title,body,course,max):
        query = f"INSERT INTO tasks (title, body, course, max) VALUES ('{title}','{body}','{course}','{max}')"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                self.conn.commit()
        except pymysql.Error as e:
            return e
    

    #Удалить задание
    def DeleteTask(self,id):
        query = f"DELETE FROM tasks WHERE id = {id}"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
            self.conn.commit()
        except pymysql.Error as e:
            return e
    

    #Получить список всех заданий
    def GetTasksAll(self):
        query = f"SELECT * FROM tasks ORDER BY course, title"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows, None
        except pymysql.Error as e:
            return None, e
    

    #Получить список всех заданий только определенного курса
    def GetTasksByCourse(self,course):
        query = f"SELECT * FROM tasks WHERE course = '{course}' ORDER BY course, title"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows, None
        except pymysql.Error as e:
            return None, e
        

    #Добавить студента в базу
    def AddStudent(self,name,lastname,group,course,tgname):
        query = f"INSERT INTO students (name, lastname, group_number, course, tgname) VALUES ('{name}','{lastname}','{group}','{course}','{tgname}')"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                self.conn.commit()
        except pymysql.Error as e:
            return e

    #Получить студента по id
    def DeleteStudentById(self,id):
        query = f"DELETE FROM students WHERE id = {id}"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
            self.conn.commit()
        except pymysql.Error as e:
            return e
    

    #Удалить студента по телеграм id
    def DeleteStudentByTgname(self,tgname):
        query = f"DELETE FROM students WHERE tgname = {tgname}"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
            self.conn.commit()
        except pymysql.Error as e:
            return e
    

    #Получить студента по телеграм id
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
    

    #Получить список всех студентов
    def GetStudentsAll(self):
        query = f"SELECT * FROM students ORDER BY course, group_number, name"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows, None
        except pymysql.Error as e:
            return None, e
    
    #Назначить задание на студента. Если кол-во студентов взявших эту задачу >= max, возвращается ошибка. Курс не учитывается
    def AssignTask(self,student_tgname,task_id):
        query1 = f"SELECT max FROM tasks WHERE id = '{task_id}'"
        query2 = f"SELECT Count(*) as cnt FROM taken WHERE task_id = '{task_id}'"

        query = f"INSERT INTO taken (taken.student_id, taken.task_id) VALUES ((SELECT students.id FROM students WHERE students.tgname = '{student_tgname}'),'{task_id}')"
        try:
            with self.conn.cursor() as cursor:

                cursor.execute(query1)
                tas = cursor.fetchall()

                cursor.execute(query2)
                cnt = cursor.fetchall()

                if cnt[0]["cnt"] < tas[0]["max"]:
                    cursor.execute(query)
                    self.conn.commit()
                else:
                    return "the maximum number has been reached"
        except pymysql.Error as e:
            return e
    

    #Удалить назначение задания
    def DeleteAssignment(self, student_tgname,task_id):
        query = f"DELETE FROM taken WHERE (taken.student_id,taken.task_id) = ((SELECT students.id FROM students WHERE students.tgname = '{student_tgname}'),'{task_id}')"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                self.conn.commit()
        except pymysql.Error as e:
            return e
    
    #Получить список всех назначений
    def GetAssignements(self):
        query = f"SELECT * FROM taken"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows, None
        except pymysql.Error as e:
            return None, e
    
    #Получить список назначенных заданий студенту
    def GetMyTasks(self,tgname):
        query = f"SELECT DISTINCT tasks.id, tasks.title, tasks.body, tasks.course, tasks.max FROM tasks JOIN taken ON taken.task_id = tasks.id WHERE taken.student_id = (SELECT students.id FROM students WHERE students.tgname = '{tgname}')"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows, None
        except pymysql.Error as e:
            return None, e

    #Получить список свободных заданий для студента
    def GetFreeTasks(self,tgname):
        query = f"SELECT tasks.id, tasks.title, tasks.body, tasks.course, tasks.max FROM tasks WHERE (SELECT Count(*) FROM taken WHERE taken.task_id = tasks.id) < tasks.max AND tasks.course = (SELECT course FROM students WHERE students.tgname = '{tgname}');"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows, None
        except pymysql.Error as e:
            return None, e
    
    #Выгрузка всей базы
    def GetAllData(self):
        query = f"SELECT students.id, students.name, students.lastname, students.group_number, students.course, students.tgname, taken.task_id, tasks.title, tasks.body, tasks.course as task_course, tasks.max FROM students LEFT JOIN taken ON students.id = taken.student_id LEFT JOIN tasks ON taken.task_id = tasks.id"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows, None
        except pymysql.Error as e:
            return None, e


def TestDataabase():
    mydb = DB("std-mysql",3306,"std_2064_polyquest","qwerty123","std_2064_polyquest")

    e = mydb.AddAdmin("@Semyon981")
    print(e)

    row,e = mydb.GetAdminByTgname("@Semyon981")
    print(row,e)

    e= mydb.DeleteAdmin("@Semyon981")
    print(e)



    e = mydb.NewTask("задание","описание",1,5)
    print(e)

    rows,e = mydb.GetTasksAll()
    print(rows,e)

    rows,e = mydb.GetTasksByCourse(1)
    print(rows,e)

    taskid = rows[len(rows)-1]["id"]


    e = mydb.AddStudent("sema","permogorov","211-722",1,"@Semyon9812")
    print(e)

    row,e = mydb.GetStudentByTgname("@Semyon9812")
    print(row,e)

    rows, e = mydb.GetStudentsAll()
    print(rows,e)


    e = mydb.AssignTask("@Semyon9812",taskid)
    print(e)


    rows,e = mydb.GetAssignements()
    print(rows,e)


    rows,e = mydb.GetMyTasks("@Semyon9812")
    print(rows,e)


    rows,e = mydb.GetFreeTasks("@Semyon9812")
    print(rows,e)


    rows,e = mydb.GetAllData()
    print(rows,e)



    mydb.DeleteAssignment("@Semyon9812",taskid)
    print(e)


    e = mydb.DeleteStudentByTgname("@Semyon9812")
    print(e)


    e = mydb.DeleteTask(taskid)
    print(e)



TestDataabase()