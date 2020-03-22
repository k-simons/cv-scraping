from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import urllib.request

def main():
    page = urllib.request.urlopen("https://www.worldometers.info/coronavirus/country/us")
    soup = BeautifulSoup(page, 'html.parser')
    usaTable = soup.find("table", {"id": "usa_table_countries_today"})
    tableBody = usaTable.find('tbody')
    tableRows = tableBody.find_all('tr')
    while len(tableRows) < 20:
        print(len(tableRows))
        time.sleep(1)
        tableBody = usaTable.find('tbody')
        tableRows = tableBody.find_all('tr')
    rowResults = []
    for tableRow in tableRows:
        rowResult = singleRowToRowResult(tableRow)
        rowResults.append(rowResult)
    singleStateScrape = SingleStateScrape(rowResults)
    f = open("demofile3.txt", "w")
    f.write(singleStateScrape.serialize())
    f.close()


def singleRowToRowResult(singleTr):
    tds = singleTr.find_all('td')
    state = tds[0]
    totalCases = tds[1]
    newCases = tds[2]
    totalDeaths = tds[3]
    newDeaths = tds[4]
    totalRecovered = tds[5]
    activeCases = tds[6]
    stateString = getText(state)
    totalCases = toInt(totalCases)
    newCases = toIntNoPlus(newCases)
    totalDeaths = toInt(totalDeaths)
    newDeaths = toIntNoPlus(newDeaths)
    totalRecovered = toInt(totalRecovered)
    activeCases = toInt(activeCases)
    return RowResult(stateString, totalCases, newCases, totalDeaths, newDeaths, totalRecovered, activeCases)

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

class SingleStateScrape:
    def __init__(self, rowResults):
        self.rowResults = rowResults
        self.scrapeTime = datetime.utcnow().strftime("%m/%d/%Y,%H:%M:%S")

    def serialize(self):
        result = {}
        json_string = [ob.serialize() for ob in self.rowResults]
        result["rowResults"] = json_string
        result["scrapeTime"] = self.scrapeTime
        return json.dumps(result)

class RowResult:
    def __init__(self, state, total, newCases, totalDeaths, newDeaths, totalRecovered, activeCases):
        self.state = state
        self.total = total
        self.newCases = newCases
        self.totalDeaths = totalDeaths
        self.newDeaths = newDeaths
        self.totalRecovered = totalRecovered
        self.activeCases = activeCases

    def serialize(self):
        return self.__dict__


if __name__== "__main__":
  main()
