import requests
from BeautifulSoup import BeautifulSoup
import urlparse
import re


class Scan:
    def __init__(self, url1, list):
        self.url = url1
        self.link_list = []
        self.session = requests.session()
        self.ignore_list = list

    def crawl(self, url=None):
        if url is None:
            url = self.url
        result = self.session.get(url)
        links = re.findall('(?:href=")(.*?)(?:")', result.content)
        for element in links:
            element = urlparse.urljoin(url, element)
            if "#" in element:
                element = element.split("#")[0]
            if url in element and element not in self.link_list and element not in self.ignore_list:
                print(element)
                self.link_list.append(element)
                self.crawl(element)

    def xss_form(self, form, url):
        script = "<sCriPt>alert('Test');</ScrIpt>"
        response = self.form_submit(form, url, script)
        try:
            if script in response.content:
                print("\n\n***XSS Found in Link:" + url)
                print (form)

        except AttributeError:
            pass

    def xss_link(self, url):
        script = "<sCriPt>alert('Test');</ScrIpt>"
        url.replace("=", "=" + script)
        response = self.session.get(url)
        try:
            if script in response.content:
                print("\n\nXSS Found in " + url)
        except AttributeError:
            pass

    def start(self):
        for link in self.link_list:
            print("Testing for form in " + link)
            form = self.extract_forms(link)
            self.xss_form(form, link)


        if "=" in link:
                print ("Testing for Link " + link)
                self.xss_link(link)

    def extract_forms(self, url):
        response = self.session.get(url)
        html_code = BeautifulSoup(response.content)
        form_list = html_code.findAll("form")
        return form_list

    def form_submit(self, form, url, value):
        for html_code in form:
            action = html_code.get("action")
            method = html_code.get("method")
            url = urlparse.urljoin(url, action)
            input_list = html_code.findAll("input")
            data_dist = {}
            for input in input_list:
                name = input.get("name")
                if input.get("type") == "text":
                    data_dist[name] = value
                elif input.get("type") == "submit":
                    data_dist[name] = "submit"
            if method == "post":
                return self.session.post(url, data=data_dist)
            return self.session.post(url, params=data_dist)


#main code start here
login_data = {"username": "admin", "password": "password", "Login": "submit"}
target_url = "http://10.0.2.5/mutillidae/"
list = ["http://10.0.2.5/dvwa/logout.php"]

scan = Scan(target_url, list)
scan.session.post("http://10.0.2.5/dvwa/login.php", data=login_data)


#this is not working its only show testing on link name and doesnt find the vulnerability
scan.crawl()
scan.start()


# scan.crawl()
# url_list = scan.link_list
# for url in url_list:
#     form = scan.extract_forms(url)
#     scan.xss_form(form, url)
