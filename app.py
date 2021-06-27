import requests

url = 'http://localhost:5000/api/users/anomalies'
X_API_KEY = "fXMWznr92ceoaS5yp8PjcA"

headers = {
    'X-Api-Key':X_API_KEY
}



def get_request(urllink):
    r = requests.get(urllink, headers=headers)
    return r.json()

def main():
    print(get_request(url))

if __name__ == "__main__":
    main()
