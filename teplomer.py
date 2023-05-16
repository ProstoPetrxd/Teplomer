from urllib import request
URL = 'http://moje.meteo-pocasi.cz/environment/web/me220012/xml/xml.xml?USID=1673&_=1684220025754'
SOUBOR = 'data.txt'
request.urlretrieve(URL, SOUBOR)
