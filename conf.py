import sqlite3





def sql_go(base, parameter):
    db = sqlite3.connect(base)
    sql = db.cursor()

    sql.execute(parameter)
    db.commit()

    
def sql_fe(base, parameter):
    db = sqlite3.connect(base)
    sql = db.cursor()

    sql.execute(parameter).fetchall()

