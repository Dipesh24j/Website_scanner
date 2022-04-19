#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
import requests
import urlparse

response = requests.get("http://10.0.2.5/mutillidae/index.php?page=dns-lookup.php")
html_code = BeautifulSoup(response.content)

form_list = html_code.findAll("form")
action = form_list[0].get("action")
url = urlparse.urljoin("http://10.0.2.5/mutillidae/index.php?page=dns-lookup.php", action)
print(url)
input_list = html_code.findAll("input")
data_dist = {}
for input in input_list:
    name = input.get("name")
    value = input.get("value")
    if input.get("type") == "text":
        data_dist[name] = "test"
    elif input.get("type") == "submit":
        data_dist[name] = "submit"

submit = requests.post(url, data=data_dist)
print(submit.content)