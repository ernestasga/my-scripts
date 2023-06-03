# Python scripts
My python scripts 
## WI-FI Grabber

Grab saved wi-fi passwords on Windows and Linux systems. **Need root permissions for Linux**.

Windows part loops through saved wlan profiles
>netsh wlan show profiles

Linux searches for files in
>/etc/NetworkManager/system-connections/

### Usage
> python wifi-grabber.py [-h] [-o OUTFILE] [-q] [-n]

Written in Python 3.9

## Scraper
Scrape websites and output results to .xlsx files

### Usage
> pip install -r requirements.txt

> python scraper.py [-h] [-o OUTFILE]

### Supported sites:
* [x] Autogidas.lt
* [x] Autoplius.lt
* [x] Skelbiu.lt

Written in Python 3.9

## Translations
Translate texts for CakePHP from excel files

## Medias Hardlink
Hardlink downloaded media (Movies or TV Shows) for self hosted media server