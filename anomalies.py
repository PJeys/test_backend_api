import sqlite3
from datetime import datetime
import time as tm
import collections


def create_connection(db):
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Exception as e:
        print(e)
    return conn

def search_anomalies(conn):
    cur = conn.cursor()
    cur1 = conn.cursor()
    output=[]
    cur.execute('SELECT "Login TS" FROM users_logged_tom_devices')
    rows = cur.fetchall()
    login_times = []
    for row in rows:
        login_times.append(row[0])
    duplicates = [item for item, count in collections.Counter(login_times).items() if count > 1]
    for duplicate in duplicates:
        print(duplicate)
        cur.execute('SELECT "User name", "Device name" FROM users_logged_tom_devices Where "Login TS" =?',(duplicate,))
        rows = cur.fetchall()
        cur1.execute('SELECT "User name", "Country" FROM users_countries_list Where "Login TS" =?',(duplicate.encode("ascii"),))
        rows1 = cur1.fetchall()
        i = 0
        k = 0
        for row in rows:
            output.append({"userName":row[0].encode("ascii"), "device":row[1].encode("ascii"), "loginTime":duplicate.encode("ascii"),"unexpectedLogin":{}})
            if rows1[i][0].encode("ascii") == row[0].encode("ascii"):
                output[k]["unexpectedLogin"]["coutry"] = rows1[i][1].encode("ascii")
                output[k]["unexpectedLogin"]["loginTime"] = duplicate.encode("ascii")
                i=i+1
            else:
                output[i]["unexpectedLogin"]='null'
            k=k+1

    return output

def main():
    database = r"data.db"
    conn = create_connection(database)
    print(search_anomalies(conn))

if __name__ == "__main__":
    main()
