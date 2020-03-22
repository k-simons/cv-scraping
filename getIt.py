from bs4 import BeautifulSoup
import urllib.request

def main():
    page = urllib.request.urlopen("https://www.worldometers.info/coronavirus/country/us/#nav-yesterday")
    soup = BeautifulSoup(page, 'html.parser')
    a = soup.find("table", {"id": "usa_table_countries_today"})
    c = a.find('tbody')
    trs = c.find_all('tr')
    singleTr = trs[0]
    singleThing(singleTr)
# print(soup.prettify())


def singleThing(singleTr):
    tds = singleTr.find_all('td')
    state = tds[0]
    totalCases = tds[1]
    newCases = tds[2]
    totalDeaths = tds[3]
    newDeaths = tds[4]
    totalRecovered = tds[5]
    activeCases = tds[6]
    stateString = getText(state)
    print(stateString)
    totalCases = toInt(totalCases)
    print(totalCases)
    newCases = toIntNoPlus(newCases)
    print(newCases)
    totalDeaths = toInt(totalDeaths)
    print(totalDeaths)
    newDeaths = toIntNoPlus(newDeaths)
    print(newDeaths)
    totalRecovered = toInt(totalRecovered)
    print(totalRecovered)
    activeCases = toInt(activeCases)
    print(activeCases)

def toIntNoPlus(singleTD):
    strAsInput = getText(singleTD)
    noPlus = removeChar(strAsInput, "+")
    return strToInt(noPlus)

def toInt(singleTD):
    strAsInput = getText(singleTD)
    return strToInt(strAsInput)

def strToInt(strAsInput):
    if strAsInput == "":
        return 0
    return int(strAsInput.replace(',', ''))

def removeChar(strAsInput, charToRemove):
    return strAsInput.replace(charToRemove, "")

def getText(singleTD):
    rawText = singleTD.text
    return rawText.strip()

class RowResult:
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart

if __name__== "__main__":
  main()
