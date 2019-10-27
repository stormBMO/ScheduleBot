import sqlite3

db_name = "DB/users.db"
us_db_name = "DB/users_schedule.db"

#db_name = "users.db"
#us_db_name = "users_schedule.db"


def get_user_info(id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
    user_info = cursor.fetchone()
    conn.close()
    return user_info[1], user_info[2]


def add_user_to_db(id, name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT rowid FROM users WHERE id = ?", (id,))
    data = cursor.fetchall()
    if len(data) == 0:
        cursor.execute("INSERT INTO users VALUES (?, ?, '', '', '')", (id, name))
        conn.commit()
    conn.close()


def db_update_name(id, name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ? WHERE id = ?", (name, id))
    conn.commit()
    conn.close()


def db_update_schedule(id, schedule):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET schedule = ? WHERE id = ?", (schedule, id))
    conn.commit()
    conn.close()


def db_update_faculty(id, faculty):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET faculty = ? WHERE id = ?", (faculty, id))
    conn.commit()
    conn.close()


def db_check_user(id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT rowid FROM users WHERE id = ?", (id,))
    data = cursor.fetchall()
    res = True
    if len(data) == 0:
        res = False
    conn.close()
    return res


def create_schedule(id):
    conn = sqlite3.connect(us_db_name)
    cursor = conn.cursor()
    name = "schedule_" + str(id)
    cursor.execute("CREATE TABLE IF NOT EXISTS " + name + " (number integer NOT NULL, weekday integer NOT NULL, time text, pair1 text, pair2 text)")
    db_update_schedule(id, name)
    conn.close()