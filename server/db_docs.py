import sqlite3
import calendar
import time

class Docs:
    
    def __init__(self, uid: int, doc_id: str, doc_name: str, doc_type: str, size : int = 0, state : int = 0, create_at: int = 0, update_at: int = 0, id : int = 0):
        self.uid = uid
        self.doc_id = doc_id
        self.doc_name = doc_name
        self.doc_type = doc_type
        self.state = state
        self.size = size
        self.create_at = create_at
        self.update_at = update_at

        ts = calendar.timegm(time.gmtime())
        if self.create_at == 0:
            self.create_at = ts
        if self.update_at == 0:
            self.update_at = ts

        self.__conn = sqlite3.connect('database.db')
        self.__cursor = self.__conn.cursor()

    # 将对象插入到数据库中
    def insert(self):
        docs = self.get_by_doc_id(self.doc_id)
        if docs != None :
            return
        print('size', self.size)
        self.__cursor.execute('INSERT INTO docs (uid, doc_id, doc_name, doc_type, size, state, create_at, update_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (self.uid, self.doc_id, self.doc_name, self.doc_type, self.size, self.state, self.create_at, self.update_at))
        self.__conn.commit()

    # 从数据库中删除对象
    def delete(self):
        self.__cursor.execute('DELETE FROM docs WHERE doc_id = ?', (self.doc_id,))
        self.__conn.commit()

    # 更新对象在数据库中的信息
    def update(self):
        self.__cursor.execute('UPDATE docs SET uid = ?, doc_name = ?, doc_type = ?, size = ?, state = ?, create_at = ?, update_at = ? WHERE doc_id = ?',
                    (self.uid, self.doc_name, self.doc_type, self.size, self.state, self.create_at, self.update_at, self.doc_id))
        self.__conn.commit()

    # 从数据库中获取所有对象
    @staticmethod
    def get_all():
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('SELECT id,uid,doc_id,doc_name,doc_type,size,state FROM docs')
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [{"id": row[0], "uid": row[1], "doc_id": row[2], "doc_name": row[3], "doc_type": row[4], "size": row[5], "state": row[6]} for row in rows]

    # 从数据库中获取指定doc_id的对象
    @staticmethod
    def get_by_doc_id(doc_id):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('SELECT id,uid,doc_id,doc_name,doc_type,size,state FROM docs WHERE doc_id = ?', (doc_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row is not None:
            return {"id": row[0], "uid": row[1], "doc_id": row[2], "doc_name": row[3], "doc_type": row[4],"size": row[5], "state": row[6]}
        else:
            return None

    @staticmethod
    def del_by_doc_id(doc_id):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('DELETE FROM docs WHERE doc_id = ?', (doc_id,))
        cur.close()
        conn.commit()
        conn.close()

    def __str__(self):
        return f"Doc(uid={self.uid}, doc_id='{self.doc_id}', doc_name='{self.doc_name}', doc_type='{self.doc_type}', state={self.state}, create_at={self.create_at}, update_at={self.update_at})"
