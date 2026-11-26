import requests
import datetime
import time
from pymsgbox import *
from bs4 import BeautifulSoup

r = requests.get("https://www.fairfaxcounty.gov/housing/homeownership/FirstTimeHomebuyers")
r.raise_for_status()
soup = BeautifulSoup(r.content, "html.parser")
links = [h.get_text(strip=True) for h in soup.find_all("h2")]

listingDate = datetime.datetime.now()
dateAnnouced = str(listingDate.strftime("%x"))

fname = "output.txt"  # correct filename
try:
    with open(fname, "r+", encoding="utf-8") as f:
        existing = f.read()
        f.seek(0, 2)  # move to end for appending
        for newLisitng in links:
            if newLisitng not in existing:
                # print(newLisitng)
                f.write(newLisitng + " | " + dateAnnouced + "\n")
                message = alert(text=newLisitng, title='FTHB listing', button='OK')

except FileNotFoundError:
    with open(fname, "w", encoding="utf-8") as f:
        for newLisitng in links:
            # print(newLisitng)
            f.write(newLisitng+"\n")