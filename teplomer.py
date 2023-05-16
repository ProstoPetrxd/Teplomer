"""Program, který vypisuje data o počasí z meteostanice ve Dvoře Králové nad Labem na Gymnáziu"""
import time
import datetime
import urllib.request
import xml.etree.ElementTree as ET

URL = "http://moje.meteo-pocasi.cz/environment/web/me220012/xml/xml.xml?USID=1673&_=1684220025754"
class PyMeteo:
"""Class pro přečtení dat z meteostanice"""
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
            self.timestamp = time.mktime
            (datetime.datetime.strptime(self.root.attrib['date'] + ' ' +
                                        self.root.attrib['time'], '%Y-%m-%d %H:%M:%S').timetuple())
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
if __name__ == '__main__':
    sensors = ['temperature', 'temperature_apparent', 'humidity', 'pressure']
    print ("Dvůr Králové nad Labem")
    m = PyMeteo(URL, debug=True)
    m.download()
    m.get_last_update()
    for sensor in sensors:
        m.get_value(sensor)
