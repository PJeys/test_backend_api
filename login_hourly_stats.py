import sqlite3
from datetime import datetime
import time as tm

def create_connection(db):
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Exception as e:
        print(e)
    return conn

def login_hourly_stats(conn, *time):
    cur = conn.cursor()
    output = []
    if time:
        if time[0].get('startTime') and time[0].get('endTime'):
            startTime = time[0].get('startTime')
            startDate = startTime.split('T')[0]
            startHour = startTime.split('T')[1]
            endTime = time[0].get('endTime')
            endDate = endTime.split('T')[0]
            endHour = endTime.split('T')[1]
            cur.execute('SELECT "Date", "Hour", "Total session duration for hour (in minutes)", "Total session duration accumulated"  FROM total_session_duration Where DATE(Date) >=?',(startDate,))
            rows = cur.fetchall()
            for row in rows:
                if row[0] == startDate and row[1]>=int(startHour[:2]):
                    output.append({"date":row[0], "hour":row[1], "concurrentSessions":[], "totalTimeForHour":row[2], "qumulativeForHour":row[3]})
                if row[0]>startDate:
                    output.append({"date":row[0], "hour":row[1], "concurrentSessions":[], "totalTimeForHour":row[2], "qumulativeForHour":row[3]})
                if row[0] == endDate and str(row[1]) == endHour[1]:
                    break
            new_date = startDate + ' ' +tm.strftime('%H:%M:%S', tm.gmtime(int(startHour[:2])*3600))
            cur.execute('SELECT "Maximum concurent sessions","Hour" FROM login_sessions_for_hour WHERE Hour>=?',(new_date,))
            rows = cur.fetchall()
            new_end_date = endDate + ' ' +tm.strftime('%H:%M:%S', tm.gmtime(int(endHour[:2])*3600)) + ' '
            i = 0
            for row in rows:
                output[i]["concurrentSessions"] = row[0]
                if str(row[1]) == str(new_end_date):
                    break
                i=i+1
        elif time[0].get('startTime'):
            startTime = time[0].get('startTime')
            startDate = startTime.split('T')[0]
            startHour = startTime.split('T')[1]
            cur.execute('SELECT "Date", "Hour", "Total session duration for hour (in minutes)", "Total session duration accumulated"  FROM total_session_duration Where DATE(Date) >=?',(startDate,))
            rows = cur.fetchall()
            for row in rows:
                if row[0] == startDate and row[1]>=int(startHour[:2]):
                    output.append({"date":row[0], "hour":row[1], "concurrentSessions":[], "totalTimeForHour":row[2], "qumulativeForHour":row[3]})
                if row[0]>startDate:
                    output.append({"date":row[0], "hour":row[1], "concurrentSessions":[], "totalTimeForHour":row[2], "qumulativeForHour":row[3]})
            new_date = startDate + ' ' +tm.strftime('%H:%M:%S', tm.gmtime(int(startHour[:2])*3600))
            cur.execute('SELECT "Maximum concurent sessions" FROM login_sessions_for_hour WHERE Hour>=?',(new_date,))
            rows = cur.fetchall()
            i = 0
            for row in rows:
                output[i]["concurrentSessions"] = row[0]
                i=i+1
        elif time[0].get('endTime'):
            endTime = time[0].get('endTime')
            endDate = endTime.split('T')[0]
            endHour = endTime.split('T')[1]
            cur.execute('SELECT "Date", "Hour", "Total session duration for hour (in minutes)", "Total session duration accumulated"  FROM total_session_duration Where Date BETWEEN DATE(Date) AND DATE(?)',(endDate,))
            rows = cur.fetchall()
            for row in rows:
                if row[0] == endDate and row[1]<=int(endHour[:2]):
                    output.append({"date":row[0], "hour":row[1], "concurrentSessions":[], "totalTimeForHour":row[2], "qumulativeForHour":row[3]})
                if row[0]<endDate:
                    output.append({"date":row[0], "hour":row[1], "concurrentSessions":[], "totalTimeForHour":row[2], "qumulativeForHour":row[3]})
            new_date = endDate + ' ' +tm.strftime('%H:%M:%S', tm.gmtime(int(endHour[:2])*3600+3600))
            cur.execute('SELECT "Maximum concurent sessions", "Hour" FROM login_sessions_for_hour WHERE Hour BETWEEN DATE(Hour) AND (?)',(new_date,))
            rows = cur.fetchall()
            i = 0
            for row in rows:
                output[i]["concurrentSessions"] = row[0]
                i=i+1
    else:
        cur.execute('SELECT "Date", "Hour", "Total session duration for hour (in minutes)", "Total session duration accumulated"  FROM total_session_duration')
        rows = cur.fetchall()
        for row in rows:
            output.append({"date":row[0], "hour":row[1], "concurrentSessions":[], "totalTimeForHour":row[2], "qumulativeForHour":row[3]})
        cur.execute('SELECT "Maximum concurent sessions" FROM login_sessions_for_hour')
        rows = cur.fetchall()
        i = 0
        for row in rows:
            output[i]["concurrentSessions"] = row[0]
            i = i + 1
    return output

def main():
    database = r"data.db"
    conn = create_connection(database)
    print(login_hourly_stats(conn,{'startTime':'2021-05-31T23:00:00','endTime':'2021-06-01T04:00:00'}))

if __name__ == "__main__":
    main()
