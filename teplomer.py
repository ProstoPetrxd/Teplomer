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
        if value != 'ERROR':
            return value
        return None
 
    def get_last_update(self):
        if self.debug:
            print(time.strftime('%c', time.localtime(self.timestamp)))
        return self.timestamp

nova_teplota = 0.0
stara_teplota = 0.0
rozdil_teplot = 0.0
pocet = 0
celkova_teplota = 0.0
maximalni_teplota = 0.0
minimalni_teplota = 100.0

# Zacyklení programu do nekonečna
while True:

    # Zjištění aktuálního času
    t = datetime.datetime.now()

    # Vymazání dat z tabulky každý den o půlnoci.
    if((t.hour == 0) and (t.minute == 0)):
        urllib.request.urlopen("https://script.google.com/macros/s/AKfycbx8dInME9tlD57F9EjqsVx0RMmk5p4XEpGsS6hv11ggZ6jfNNxRrGLi3uXQwC3h1DG3/exec")
    
    if __name__ == '__main__':

        # Zapnutí programu, pokud uběhly dvě minuty
        if((((t.minute%2) == 0) or (t.minute == 0)) and (t.second == 0)):

            # Získáni hodnot
            sensors = ['temperature']
            m = PyMeteo('http://moje.meteo-pocasi.cz/environment/web/me220012/xml/xml.xml?USID=1673&_=1684220025754', debug=True)
            m.download()
            nova_teplota = m.get_value(sensors[0])

            # Kontrolní vypsání aktuálních hodnot.
            if(t.hour < 10):
                print("0%s:%s - Teplota: %s°C" % (t.hour, t.minute, nova_teplota))
            elif(t.hour < 10 and t.minute < 10):
                print("0%s:0%s - Teplota: %s°C" % (t.hour, t.minute, nova_teplota))
            elif(t.minute < 10):
                print("%s:0%s - Teplota: %s°C" % (t.hour, t.minute, nova_teplota))
            else:
                print("%s:%s - Teplota: %s°C" % (t.hour, t.minute, nova_teplota))

            # Zjištění, není-li hodnota neplatná (Bez tohoto by se program jednou za čas vypl, protože naměřil chybnou hodnotu.)
            if (nova_teplota != None):

                # Přidání naměřené hodnoty do průměru
                celkova_teplota += float(nova_teplota)
                pocet += 1

                # Případný zápis nové maximální hodnoty
                if(float(nova_teplota) > float(maximalni_teplota)):
                    maximalni_teplota = float(nova_teplota)

                # Případný zápis nové minimální hodnoty
                if(float(nova_teplota) < float(minimalni_teplota)):
                    minimalni_teplota = float(nova_teplota)

                # Zapsání aktuální teploty do Google Sheets tabulky
                urllib.request.urlopen("https://script.google.com/macros/s/AKfycbwywgTKg7z5HZ20MCVtSzl-UiqNcUcTdc5_4C4Jzc3B03S89ykNE-S7Yt9UcOJT735I1g/exec?value=%s" % nova_teplota)

                # Program bude odesílat upozornění pouze mezi 7:00 a 22:00
                if((t.hour >= 7) and (t.hour <= 22)):

                    # Pokud je celá hodina, spustit proces pro odeslání notifikace.
                    if((t.minute == 0) and (t.second == 0)):

                        # Zjistit teplotu minulou hodinu pro porovnání
                        with open('teplota.txt', 'r') as f:
                            stara_teplota = f.read()
                            f.close()

                        # Vypočítání rozílů teplot mezi hodinami
                        rozdil_teplot = float(nova_teplota) - float(stara_teplota)

                        # Vypočítání průměrné teloty za poslední hodinu a její zaokrouhlení
                        prumerna_teplota = celkova_teplota/pocet
                        prumerna_teplota = round(prumerna_teplota, 1)

                        # Odeslání upozornění na telefon
                        conn = http.client.HTTPSConnection("api.pushover.net:443")
                        conn.request("POST", "/1/messages.json",
                        urllib.parse.urlencode({
                            "token": "a8fafvyjck1k2de5yz3hphcku3i499",
                            "html": "1",
                            "user": "u586cd4vg7qf4mtgert6buum515t8u",
                            "title": "Teplota ve Dvoře: %s°C" % nova_teplota,
                            "message": "Rozdíl teplot za uplynulou hodinu: <b>%s°C</b>\
                            <br>Průměrná teplota: <b>%s°C</b>\
                            <br>Minimální teplota: <b>%s°C</b>\
                            <br>Maximální teplota: <b>%s°C</b>"\
                            % (round(rozdil_teplot, 1), prumerna_teplota, round(minimalni_teplota, 1), round(maximalni_teplota, 1)),
                        }), { "Content-type": "application/x-www-form-urlencoded" })
                        conn.getresponse()
                        print("Zpráva byla odeslána.")

                        # Zapsat aktuální teplotu pro porovnání příští hodinu
                        with open('teplota.txt', 'w') as f:
                            stara_teplota = f.write(nova_teplota)
                            f.close()

                        # Nastavení proměnných na základní hodnoty
                        celkova_teplota = 0.0
                        maximalni_teplota = 0.0
                        minimalni_teplota = 100.0
                        
    # Počkat 1 sekundu, aby se odeslal jen jeden záznam.
    time.sleep(1)
