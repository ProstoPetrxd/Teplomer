"""Program, který pomocí dat z meteostanice na Gymnáziu ve Dvoře Králové vytváří teploměr."""
import xml.etree.ElementTree as ET

URL = "http://moje.meteo-pocasi.cz/environment/web/me220012/xml/xml.xml?USID=1673&_=1684220025754"

mytree = ET.parse(URL)
myroot = mytree.getroot()
