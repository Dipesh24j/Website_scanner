#!/usr/bin/env python

import requests, re, urlparse


def response(url):
    try:
        return requests.get(url)
    except requests.exceptions.SSLError:
        pass

target1 = "http://davjind.net.in/"
link_list = []


def craw(target):
    result = response(target)
    links = re.findall('(?:href=")(.*?)(?:")', result.content)
    for element in links:
        element = urlparse.urljoin(target, element)
        if "#" in element:
            element =element.split("#")[0]
        if target in element and element not in link_list:
            print(element)
            link_list.append(element)
            craw(element)


craw(target1)
