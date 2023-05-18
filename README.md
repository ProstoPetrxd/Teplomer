# Teploměr
![example event parameter](https://github.com/ProstoPetrxd/Teplomer/actions/workflows/pylint.yml/badge.svg) - Program je psán v pythonu na počítač, v githubu se bohužel vyskytují chyby, které ovšem nejsou fatální.

Python program teploměr, který získává data z meteostanice na Gymnáziu ve Dvoře Králové nad Labem
Program nejdříve přečte hodnoty z XML souboru ("http://moje.meteo-pocasi.cz/environment/web/me220012/xml/xml.xml?USID=1673&_=1684220025754") , převede je na zpracovatelný text a ten následně zapíše to tabulky na <b>Google drivu</b> ("https://docs.google.com/spreadsheets/d/1IW56MOHPfkZLbOVdcOHwZlVQ1qMjMGtHqwEHfrzlKH8/edit#gid=0")<br> pomocí <b>Google Apps Scripts</b> ("https://script.google.com/home/projects/1toAQ6DrrOEdmX3YBgh3j0tDDZqbMweVSt0bsPVZ875BEaDtpOoFnvYvK/edit"). Toto se děje každé dvě minuty a každých deset minut se pomocí aplikace Pushover pošle upozornění s momentální naměřenou teplotou. 
