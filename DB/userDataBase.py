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

def db_get_all_schedule(id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT schedule FROM users WHERE id = ?", (id,))
    user_schedule_name = cursor.fetchone()[0]
    conn = sqlite3.connect(us_db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT pair1, pair2 FROM " + user_schedule_name + " WHERE pair1 IS NOT NULL")
    user_info = cursor.fetchall()
    conn.close()
    return user_info


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
    cursor.execute("CREATE TABLE IF NOT EXISTS " + name
                   + " (weekday integer NOT NULL, number integer NOT NULL, time text, pair1 text, pair2 text, flag integer NOT NULL)")
    db_update_schedule(id, name)
    cursor.execute("SELECT rowid FROM " + name)
    data = cursor.fetchall()
    if len(data) == 0:
        for i in range(6):
            for j in range(8):
                cursor.execute("INSERT INTO " + name + " VALUES (?, ?, '', '', '', 0)", (i + 1, j + 1))
                conn.commit()
    conn.close()


def add_weekday_flag(id, weekday):
    conn = sqlite3.connect(us_db_name)
    cursor = conn.cursor()
    name = "schedule_" + str(id)
    cursor.execute("UPDATE " + name + " SET flag = 0 WHERE flag = -1")
    cursor.execute("UPDATE " + name + " SET flag = -1 WHERE weekday = ?", (weekday,))
    conn.commit()
    conn.close()


def add_number_flag(id, number):
    conn = sqlite3.connect(us_db_name)
    cursor = conn.cursor()
    name = "schedule_" + str(id)
    cursor.execute("UPDATE " + name + " SET flag = 0 WHERE number != ? AND flag = -1", (number,))
    conn.commit()
    conn.close()


def add_pair_flag(id, pair_num):
    conn = sqlite3.connect(us_db_name)
    cursor = conn.cursor()
    name = "schedule_" + str(id)
    cursor.execute("UPDATE " + name + " SET pair1 = '' WHERE pair1 = 'null_pair'")
    cursor.execute("UPDATE " + name + " SET pair2 = '' WHERE pair2 = 'null_pair'")
    if pair_num != 2:
        cursor.execute("UPDATE " + name + " SET pair1 = 'null_pair' WHERE flag = -1")
    if pair_num != 1:
        cursor.execute("UPDATE " + name + " SET pair2 = 'null_pair' WHERE flag = -1")
    conn.commit()
    conn.close()


def schedule_add_pair(id, pair):
    conn = sqlite3.connect(us_db_name)
    cursor = conn.cursor()
    name = "schedule_" + str(id)
    cursor.execute("UPDATE " + name + " SET pair1 = ? WHERE pair1 = 'null_pair'", (pair,))
    cursor.execute("UPDATE " + name + " SET pair2 = ? WHERE pair2 = 'null_pair'", (pair,))
    conn.commit()
    conn.close()

def db_update_time(id, time):
    conn = sqlite3.connect(us_db_name)
    cursor = conn.cursor()
    name = "schedule_" + str(id)
    cursor.execute("UPDATE " + name + " SET time = ? WHERE id = ?", (time, id))
    conn.commit()
    conn.close()