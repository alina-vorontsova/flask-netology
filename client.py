import requests 

data = requests.post('http://127.0.0.1:5000/users/', json={'email': 'email1@flask.com', 'password': '123456789'})
print(data.status_code)
print(data.text)