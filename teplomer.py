"""Program, který pomocí dat z meteostanice na Gymnáziu ve Dvoře Králové vytváří teploměr"""
import xml.etree.ElementTree as ET
import requests
import urllib3


URL = "http://moje.meteo-pocasi.cz/environment/web/me220012/xml/xml.xml?USID=1673&_=1684220025754"
response = requests.get(URL)
with open('feed.xml', 'wb') as file:
    file.write(response.content)
