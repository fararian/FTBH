import requests
from bs4 import BeautifulSoup


headings = requests.get("https://www.fairfaxcounty.gov/housing/homeownership/FirstTimeHomebuyers")
headings.raise_for_status()
htmlTags = BeautifulSoup(headings.content, "html.parser")
links = [title.get_text(strip=True) for title in htmlTags.find_all("h2")]

for link in links:
    print(link)