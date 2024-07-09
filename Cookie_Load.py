from selenium import webdriver
import http.cookiejar
import json
import time

driver = webdriver.Chrome()
filename = 'cookies.json'
cookie_jar = http.cookiejar.CookieJar()

with open(filename, 'r') as f:
    cookies_list = json.load(f)
for cookie_data in cookies_list:
    cookie = http.cookiejar.Cookie(
        name=cookie_data['name'],
        value=cookie_data['value'],
        domain=cookie_data['domain'],
        path=cookie_data['path'],
        expires=cookie_data['expires'],
        secure=cookie_data['secure'],
    )
    cookie_jar.set_cookie(cookie)
for cookie in cookie_jar:
    try:
        driver.add_cookie({
            'name': cookie.name,
            'value': cookie.value,
            'domain': cookie.domain,
            'path': cookie.path,
            'secure': cookie.secure,
            'expirys': cookie.expires,
        })
    except Exception as e:
        print(f"Error adding cookie {cookie.name,cookie.domain}: {str(e)}")
        
print(f"Cookies loaded from {filename}")

for cookie in cookie_jar:
    driver.add_cookie({
        'name': cookie.name,
        'value': cookie.value,
        'domain': cookie.domain,
        'path': cookie.path,
        'secure': cookie.secure,
        'expiry': cookie.expires,
    })
print(f"Cookies loaded and added to WebDriver session from {filename}")
driver.get('https://mail.google.com/mail/u/0/#inbox')
time.sleep(5)
driver.quit()
