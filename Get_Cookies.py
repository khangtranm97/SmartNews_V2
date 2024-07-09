from selenium import webdriver
import json
import time
import browser_cookie3
import http.cookiejar

cookie_jar = http.cookiejar.CookieJar()
chrome_cookies = browser_cookie3.chrome()
cookies_list = []

for cookie in chrome_cookies:
        if cookie.domain ==".google.com":
            cookie_dict = {
        'name': cookie.name,
        'value': cookie.value,
        'domain': cookie.domain,
        'path': cookie.path,
        'secure': cookie.secure,
        'expires': cookie.expires,
        'http_only': cookie.has_nonstandard_attr('HttpOnly')  # Check if cookie has HttpOnly attribute
    }
            cookies_list.append(cookie_dict)
filename = 'cookies.json'

with open(filename, 'w') as f:
    json.dump(cookies_list, f, indent=4)
print('Cookie stored')