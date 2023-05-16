"""Program, který pomocí dat z meteostanice na Gymnáziu ve Dvoře Králové vytváří teploměr."""
import xml.etree.ElementTree as ET
from urllib.request import urlopen

URL = "http://moje.meteo-pocasi.cz/environment/web/me220012/xml/xml.xml?USID=1673&_=1684220025754"

xml = open("file.xml", "r+")
xml.write(urlopen(URL).read().decode('utf-8'))
xml.close()

mytree = ET.parse('file.xml')
myroot = mytree.getroot()
