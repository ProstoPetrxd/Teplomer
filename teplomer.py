import time
import datetime
import urllib.request
import xml.etree.ElementTree as ET
import http.client
 
class PyMeteo:
    debug = False
    url = None
 
    root = None
    timestamp = None
 
    def __init__(self, url, download_now=False, debug=False):
        self.debug = debug
        self.url = url
 
        if self.debug:
            print(self.url)
 
        if download_now:
            self.download()
 
    def download(self):
        try:
            xmldata = urllib.request.urlopen(self.url, timeout=5).read().decode('utf-8')
        except Exception:
            self.clear_values()
            if self.debug:
                print('Error when downloading data')
            return
 
        if (xmldata.find('status="false"') != -1 or xmldata.find('<login>false</login>') != -1):
            self.clear_values()
            if self.debug:
                print('Bad response')
            return
 
        try:
            self.root = ET.fromstring(xmldata)
            self.timestamp = time.mktime(datetime.datetime.strptime(self.root.attrib['date'] + ' ' + self.root.attrib['time'], '%Y-%m-%d %H:%M:%S').timetuple())
            if self.debug:
                print('Data parsed')
        except Exception:
            self.clear_values()
            if self.debug:
                print('Error when parsing data')
 
    def clear_values(self):
        self.root = None
        self.timestamp = None
 
    def get_value(self, param):
        if self.root is None:
            if self.debug:
                print('No data downloaded')
            return None
 
        value = self.root.find('./input/sensor[type="%s"]/value' % param).text
        if self.debug:
            print('%s: %s' % (param, value))
        if value != 'ERROR':
            return value
        return None
 
    def get_min(self, param):
        if self.root is None:
            if self.debug:
                print('No data downloaded')
            return None
 
        value = self.root.find('./minmax/s[@id="%s"]' % param).attrib['min']
        if self.debug:
            print('%s: %s' % (param, value))
        if value != 'ERROR':
            return value
        return None
 
    def get_max(self, param):
        if self.root is None:
            if self.debug:
                print('No data downloaded')
            return None
 
        value = self.root.find('./minmax/s[@id="%s"]' % param).attrib['max']
        if self.debug:
            print('%s: %s' % (param, value))
        if value != 'ERROR':
            return value
        return None
 
    def get_last_update(self):
        if self.debug:
            print(time.strftime('%c', time.localtime(self.timestamp)))
        return self.timestamp

pocet = 0
while True:
    if __name__ == '__main__':
        sensors = ['temperature', 'temperature_apparent', 'humidity', 'pressure']
        print ("Dvůr Králové nad Labem")
        m = PyMeteo('http://moje.meteo-pocasi.cz/environment/web/me220012/xml/xml.xml?USID=1673&_=1684220025754', debug=True)
        m.download()
        m.get_last_update()
        for sensor in sensors:
            m.get_value(sensor)
        urllib.request.urlopen("https://script.google.com/macros/s/AKfycbwywgTKg7z5HZ20MCVtSzl-UiqNcUcTdc5_4C4Jzc3B03S89ykNE-S7Yt9UcOJT735I1g/exec?value=%s" % m.get_value(sensors[0]))
        
        if(pocet == 5):
            conn = http.client.HTTPSConnection("api.pushover.net:443")
            conn.request("POST", "/1/messages.json",
            urllib.parse.urlencode({
                "token": "a8fafvyjck1k2de5yz3hphcku3i499",
                "html": "1",
                "user": "u586cd4vg7qf4mtgert6buum515t8u",
                "title": "Teplota ve Dvoře: <b>%s°C</b>" % m.get_value(sensors[0]),
                "message": "Rozdíl za posledních deset minut je: <b>%s°C</b>" % (stara_teplota - m.get_value(sensors[0])),
            }), { "Content-type": "application/x-www-form-urlencoded" })
            conn.getresponse()
            print("Zpráva byla odeslána.")
            pocet = 0
            stara_teplota = m.get_value(sensors[0])

    pocet += 1
    time.sleep(118.5)
