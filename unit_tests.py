import unittest
from app import get_request
import requests

X_API_KEY = "fXMWznr92ceoaS5yp8PjcA"
url = 'http://localhost:5000/api/users/anomalies'
database = r"data.db"

headers = {
    'X-Api-Key':X_API_KEY
}


class TestApiRequests(unittest.TestCase):
    def test_API_KEY(self):
        r = requests.get(url, headers={'X-Api-Key':'fXMWznr92ceoaS5yp8PjcA'})
        self.assertEqual(str(r), '<Response [200]>')
        r1 = requests.get(url, headers={'X-Api-Key':'fXMWznr92ceoaS5yp8PjA'})
        self.assertEqual(r1.json(), 'status code 403')
        r2 = requests.get(url)
        self.assertEqual(r2.json(), 'status code 401')

    def test_anomalies(self):
        r = requests.get(url, headers=headers)
        self.assertEqual(r.json(), [{'device': "John's Tablet", 'loginTime': '2021-07-01 17:35:18', 'unexpectedLogin': {'coutry': 'Poland', 'loginTime': '2021-07-01 17:35:18'}, 'userName': 'John Smith'}, {'device': "Kate's Laptop", 'loginTime': '2021-07-01 17:35:18', 'unexpectedLogin': 'null', 'userName': 'Kate Olsen'}, {'device': "Kate's Mobile Phone", 'loginTime': '2021-07-01 17:35:18', 'unexpectedLogin': {}, 'userName': 'Kate Olsen'}, {'device': "Jerry's Tablet", 'loginTime': '2021-07-01 17:35:18', 'unexpectedLogin': {'coutry': 'Germany', 'loginTime': '2021-07-01 17:35:18'}, 'userName': 'Jerry Tron'}])

    def test_registration_dynamics(self):
        url = 'http://localhost:5000/api/registration/bymonth'
        r = requests.get(url, headers=headers)
        self.assertEqual(r.json(),{'month': 'June', 'registeredDevices': [{'type': 'Laptop', 'value': 33}, {'type': 'Mobile phone', 'value': 16}, {'type': 'Tablet', 'value': 5}], 'registeredUsers': 54, 'year': '2021'})

    def test_login_stats(self):
        url = 'http://localhost:5000/api/sessions/byhour'
        r = requests.get(url, headers=headers)
        self.assertEqual(r.json(),[{'concurrentSessions': 6, 'date': '2021-05-31', 'hour': 22, 'qumulativeForHour': 14421, 'totalTimeForHour': 321}, {'concurrentSessions': 4, 'date': '2021-05-31', 'hour': 23, 'qumulativeForHour': 14721, 'totalTimeForHour': 300}, {'concurrentSessions': 3, 'date': '2021-06-01', 'hour': 0, 'qumulativeForHour': 200, 'totalTimeForHour': 200}, {'concurrentSessions': 1, 'date': '2021-06-01', 'hour': 1, 'qumulativeForHour': 430, 'totalTimeForHour': 230}, {'concurrentSessions': 0, 'date': '2021-06-01', 'hour': 2, 'qumulativeForHour': 830, 'totalTimeForHour': 400}, {'concurrentSessions': 5, 'date': '2021-06-01', 'hour': 3, 'qumulativeForHour': 955, 'totalTimeForHour': 125}, {'concurrentSessions': 11, 'date': '2021-06-01', 'hour': 4, 'qumulativeForHour': 1300, 'totalTimeForHour': 345}, {'concurrentSessions': 9, 'date': '2021-06-01', 'hour': 5, 'qumulativeForHour': 1500, 'totalTimeForHour': 200}, {'concurrentSessions': 15, 'date': '2021-06-01', 'hour': 6, 'qumulativeForHour': 1600, 'totalTimeForHour': 100}, {'concurrentSessions': 22, 'date': '2021-06-01', 'hour': 7, 'qumulativeForHour': 1900, 'totalTimeForHour': 300}, {'concurrentSessions': 36, 'date': '2021-06-01', 'hour': 8, 'qumulativeForHour': 2900, 'totalTimeForHour': 1000}, {'concurrentSessions': 56, 'date': '2021-06-01', 'hour': 9, 'qumulativeForHour': 3800, 'totalTimeForHour': 700}])

if __name__ == "__main__":
    unittest.main()
