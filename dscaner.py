import vun_scan

login_data = {"username": "admin", "password": "password", "Login": "submit"}
target_url = "http://10.0.2.5/dvwa/"
list = ["http://10.0.2.5/dvwa/logout.php"]

scan = vun_scan.Scan(target_url, list)
scan.session.post("http://10.0.2.5/dvwa/login.php", data=login_data)
# scan.crawl()
# scan.start()
form = scan.extract_forms("http://10.0.2.5/dvwa/vulnerabilities/xss_r/")
print(scan.xss_form(form, "http://10.0.2.5/dvwa/vulnerabilities/xss_r/"))
