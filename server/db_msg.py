import sqlite3
import calendar
import time
import json

class Msg:

    def __init__(self, uid: int, doc_id: str, role: str, content, create_at: int = 0):
        self.uid = uid
        self.doc_id = doc_id
        self.role = role
        if role == 'chatdoc':
            self.content = content.response
        else:
            self.content = content
        self.create_at = create_at

        ts = calendar.timegm(time.gmtime())
        if self.create_at == 0:
            self.create_at = ts

        self.__conn = sqlite3.connect('database.db')
        self.__cursor = self.__conn.cursor()

    # 将对象插入到数据库中
    def insert(self):
        self.__cursor.execute('INSERT INTO messages (uid, doc_id, role, content, create_at) VALUES (?, ?, ?, ?, ?)',
                              (self.uid, self.doc_id, self.role, self.content, self.create_at))
        self.__conn.commit()

    # 从数据库中删除对象
    def delete(self):
        self.__cursor.execute(
            'DELETE FROM messages WHERE doc_id = ?', (self.doc_id,))
        self.__conn.commit()

    # 从数据库中获取指定doc_id的对象
    @staticmethod
    def get_by_doc_id(doc_id, uid):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute(
            'SELECT uid, doc_id, role, content, create_at FROM messages WHERE doc_id = ? and uid = ?', (doc_id, uid))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        if rows is not None:
            return [{"uid": row[0], "doc_id": row[1], "role": row[2], "content": row[3] if row[2] == 'user' else row[3]} for row in rows]
        else:
            return None
