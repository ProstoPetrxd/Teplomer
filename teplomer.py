import requests
import urllib3
import xml.etree.ElementTree as ET

url = "http://moje.meteo-pocasi.cz/environment/web/me220012/xml/xml.xml?USID=1673&_=1684220025754"
response = requests.get(url)
with open('feed.xml', 'wb') as file:
    file.write(response.content)
