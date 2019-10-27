import sqlite3


def get_user_info(id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
    user_info = cursor.fetchone()
    conn.close()
    return (user_info[1], user_info[2])


def add_user_to_db(id, name):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT rowid FROM users WHERE id = ?", (id,))
    data = cursor.fetchall()
    if len(data) == 0:
        cursor.execute("INSERT INTO users VALUES (?, ?, '', '', '')", (id, name))
        conn.commit()
    conn.close()


def db_update_name(id, name):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ? WHERE id = ?", (name, id))
    conn.commit()


def db_update_faculty(id, faculty):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET faculty = ? WHERE id = ?", (faculty, id))
    conn.commit()


def db_check_user(id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT rowid FROM users WHERE id = ?", (id,))
    data = cursor.fetchall()
    res = True
    if len(data) == 0:
        res = False
    conn.close()
    return res