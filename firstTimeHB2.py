import requests
import datetime
import time
from bs4 import BeautifulSoup

start_time = time.time()

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
        for text in links:
            if text not in existing:
                print(text)
                f.write(text + " | " + dateAnnouced + "\n")
except FileNotFoundError:
    with open(fname, "w", encoding="utf-8") as f:
        for text in links:
            print(text)
            f.write(text+"\n")

end_time = time.time()
print(f"Execution time: {end_time - start_time:.2f} seconds")