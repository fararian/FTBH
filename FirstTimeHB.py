import requests
import hashlib
from pymsgbox import *
from bs4 import BeautifulSoup

fthb = requests.get("https://www.fairfaxcounty.gov/housing/homeownership/FirstTimeHomebuyers")


if fthb.status_code == 200:
    soup = BeautifulSoup(fthb.text, "html.parser")
    raw_text = soup.get_text(separator=" ", strip=True)
    new_hash = hashlib.sha1()
    new_hash.update(raw_text.encode("utf-8"))
    print('new hash', new_hash.hexdigest())

    with open("fthbhash.txt") as currentHash:
        fileHash = currentHash.read()
        print('old hash', fileHash)

        if fileHash == new_hash.hexdigest():
            message = alert(text='No new listing', title='FTBH listing', button='OK')
        else:
            message = alert(text='New listing available', title='FTHB listing', button='OK')
            with open("fthbhash.txt", "w") as currentHash:
                soup = BeautifulSoup(fthb.text, "html.parser")
                raw_text = soup.get_text(separator=" ", strip=True)
                new_hash = hashlib.sha1()
                new_hash.update(raw_text.encode("utf-8"))
                hash_Value = new_hash.hexdigest()
                currentHash.write(hash_Value)
                currentHash.close()
else:
    print("connection error")