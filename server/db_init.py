import sqlite3
import os

os.remove("database.db")

table_docs  = """
create table if not exists docs
(
    id        integer primary key autoincrement,
    uid       integer default 0  not null,
    doc_id    text    default '' not null unique,
    doc_name  text    default '' not null,
    doc_type  text    default '' not null,
    state     integer default 0  not null, -- 1 解析文本成功, 2 构建所有成功
    size      integer default 0  not null,
    create_at integer default 0  not null,
    update_at integer default 0  not null
);
"""

table_msg = """
create table if not exists messages
(
    id        integer primary key autoincrement,
    uid       integer default 0  not null,
    doc_id    text    default '' not null,
    role      text    default '' not null,
    content   text    default '' not null,
    create_at integer            not null
);
"""

con = sqlite3.connect("database.db")

cur = con.cursor()

cur.execute(table_docs)
cur.execute(table_msg)

res = cur.execute("SELECT name FROM sqlite_master")

result = res.fetchall()

print(result)