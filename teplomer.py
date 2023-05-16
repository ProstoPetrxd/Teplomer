"""Program, který pomocí dat z meteostanice na Gymnáziu ve Dvoře Králové vytváří teploměr."""
import xml.etree.ElementTree as ET
import Requests


URL = "http://moje.meteo-pocasi.cz/environment/web/me220012/xml/xml.xml?USID=1673&_=1684220025754"
response = Requests.get(URL)
with open('feed.xml', 'wb') as file:
    file.write(response.content)

mytree = ET.parse(URL)
myroot = mytree.getroot()
