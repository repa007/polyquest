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
    def AddAdmin(self,chatid):
        query = f"INSERT INTO admin (chatid) VALUES('{chatid}')"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
            self.conn.commit()
        except pymysql.Error as e:
            return e
    
    #Удалить админа
    def DeleteAdmin(self,chatid):
        query = f"DELETE FROM admin WHERE chatid='{chatid}'"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
            self.conn.commit()
        except pymysql.Error as e:
            return e
    
    #Получить админа по chatid
    def GetAdminByChatid(self,chatid):
        query = f"SELECT * FROM admin WHERE chatid='{chatid}'"
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
    def AddStudent(self,name,lastname,group,course,chatid):
        query = f"INSERT INTO students (name, lastname, group_number, course, chatid) VALUES ('{name}','{lastname}','{group}','{course}','{chatid}')"
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
    

    #Удалить студента по chatid
    def DeleteStudentByChatid(self,chatid):
        query = f"DELETE FROM students WHERE chatid = {chatid}"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
            self.conn.commit()
        except pymysql.Error as e:
            return e
    

    #Получить студента по chatid
    def GetStudentByChatid(self,chatid):
        query = f"SELECT * FROM students WHERE chatid='{chatid}'"
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
    def AssignTask(self,chatid,task_id):
        query1 = f"SELECT max FROM tasks WHERE id = '{task_id}'"
        query2 = f"SELECT Count(*) as cnt FROM taken WHERE task_id = '{task_id}'"

        query = f"INSERT INTO taken (taken.student_id, taken.task_id) VALUES ((SELECT students.id FROM students WHERE students.chatid = '{chatid}'),'{task_id}')"
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
    def DeleteAssignment(self, chatid,task_id):
        query = f"DELETE FROM taken WHERE (taken.student_id,taken.task_id) = ((SELECT students.id FROM students WHERE students.chatid = '{chatid}'),'{task_id}')"
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
    def GetMyTasks(self,chatid):
        query = f"SELECT DISTINCT tasks.id, tasks.title, tasks.body, tasks.course, tasks.max FROM tasks JOIN taken ON taken.task_id = tasks.id WHERE taken.student_id = (SELECT students.id FROM students WHERE students.chatid = '{chatid}')"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows, None
        except pymysql.Error as e:
            return None, e

    #Получить список свободных заданий для студента
    def GetFreeTasks(self,chatid):
        query = f"SELECT tasks.id, tasks.title, tasks.body, tasks.course, tasks.max FROM tasks WHERE (SELECT Count(*) FROM taken WHERE taken.task_id = tasks.id) < tasks.max AND tasks.course = (SELECT course FROM students WHERE students.chatid = '{chatid}');"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows, None
        except pymysql.Error as e:
            return None, e

    #Вернуть текст задания по id задания
    def GetBodyOfTask(self,taskid):
        query = f"SELECT tasks.id, tasks.title, tasks.body, tasks.course, tasks.max FROM tasks WHERE tasks.id = {taskid}"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows, None
        except pymysql.Error as e:
            return None, e


    #Выгрузка всей базы
    def GetAllData(self):
        query = f"SELECT students.id, students.name, students.lastname, students.group_number, students.course, students.chatid, taken.task_id, tasks.title, tasks.body, tasks.course as task_course, tasks.max FROM students LEFT JOIN taken ON students.id = taken.student_id LEFT JOIN tasks ON taken.task_id = tasks.id"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return rows, None
        except pymysql.Error as e:
            return None, e


