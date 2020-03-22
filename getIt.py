from bs4 import BeautifulSoup
import urllib.request

page = urllib.request.urlopen("https://www.worldometers.info/coronavirus/country/us/#nav-yesterday")
soup = BeautifulSoup(page, 'html.parser')
a = soup.find("table", {"id": "usa_table_countries_today"})
c = a.find('tbody')
tr = c.find_all('tr')
singleTr = tr[0]
print(singleTr)
# print(soup.prettify())