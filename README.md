# Teploměr
![example event parameter](https://github.com/ProstoPetrxd/Teplomer/actions/workflows/pylint.yml/badge.svg) - Program je psán v pythonu na počítač, v githubu se bohužel vyskytují chyby, které ovšem nejsou fatální.

Python program teploměr, který získává data z meteostanice na Gymnáziu ve Dvoře Králové nad Labem
Program nejdříve přečte hodnoty z <b><a href="http://moje.meteo-pocasi.cz/environment/web/me220012/xml/xml.xml?USID=1673&_=1684220025754" target="_blank">XML souboru</a></b>, 
převede je na zpracovatelný text a ten následně zapíše do tabulky na <b><a href="" target="_blank"><a href="https://www.freecodecamp.org/" target="_blank">Google drivu</a></b>
pomocí <b><a href="https://docs.google.com/spreadsheets/d/1IW56MOHPfkZLbOVdcOHwZlVQ1qMjMGtHqwEHfrzlKH8/edit#gid=0" target="_blank">Google Apps Scripts</a></b>. 
Toto se děje každé dvě minuty a každých deset minut se pomocí aplikace Pushover pošle upozornění s momentální naměřenou teplotou. 
