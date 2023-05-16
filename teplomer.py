from urllib import request
remote_url = 'http://moje.meteo-pocasi.cz/environment/web/me220012/xml/xml.xml?USID=1673&_=1684220025754'
local_file = 'data.txt'
request.urlretrieve(remote_url, local_file)
