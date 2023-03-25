from selenium import webdriver
import json
import requests
import re

browser = webdriver.Firefox()
browser.get('https://api.bilibili.com/x/v2/reply?type=1&oid=170007&sort=1&pn=1')

Cookie = browser.get_cookies()
strr = ''
# print(Cookie)
for c in Cookie:
    strr += c['name']
    strr += '='
    strr += c['value']
    strr += ';'
# strr = strr[0:-2]
# print(strr)
headers = {'Cookie': strr}
# print(headers)
r2 = requests.get(headers=headers)
print(r2)