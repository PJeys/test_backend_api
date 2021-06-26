import sqlite3
from datetime import datetime



def create_connection(db):
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Exception as e:
        print(e)
    return conn

def select_all_registrations_by_month(conn, *some_date):
    cur = conn.cursor()
    if some_date:
        current_year = str(some_date[0])[:4]
        datetime_object = datetime.strptime(str(some_date[0])[4:], "%m")
        curr_month = datetime_object.strftime('%B')
    else:
        current_year = datetime.now().strftime('%Y')
        curr_month = datetime.now().strftime('%B')
    cur.execute('SELECT "Number of Users" FROM user_registration_month WHERE Month=?',(curr_month,))
    rows = cur.fetchall()
    total_users = rows[0][0]
    output = {"year": current_year, "month": curr_month, "registeredUsers": total_users,"registeredDevices":[]}
    cur.execute('SELECT "Device type", "Number of users" FROM user_registration_device WHERE Month=?',(curr_month,))
    rows = cur.fetchall()
    for row in rows:
        device_dict = {"type":row[0],"value":row[1]}
        output["registeredDevices"].append(device_dict)
    return(output)
def main():
    database = r"data.db"
    conn = create_connection(database)
    print(select_all_registrations_by_month(conn,202101))

if __name__ == "__main__":
    main()
