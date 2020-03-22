import urllib.request
from bs4 import BeautifulSoup
from row_result import RowResult
from single_scrape import SingleScrape
import json
from datetime import datetime

class ScrapeRunner:
    def __init__(self, url: str, tableName: str):
        self.url = url
        self.tableName = tableName

    def run(self) -> SingleScrape:
        page = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(page, 'html.parser')
        usaTable = soup.find("table", {"id": self.tableName})
        tableBody = usaTable.find('tbody')
        tableRows = tableBody.find_all('tr')
        rowResults = []
        for tableRow in tableRows:
            rowResult = self.singleRowToRowResult(tableRow)
            rowResults.append(rowResult)
        return SingleScrape(rowResults)

    def singleRowToRowResult(self, singleTr):
        tds = singleTr.find_all('td')
        state = tds[0]
        totalCases = tds[1]
        newCases = tds[2]
        totalDeaths = tds[3]
        newDeaths = tds[4]
        totalRecovered = tds[5]
        activeCases = tds[6]
        stateString = self.getText(state)
        totalCases = self.toInt(totalCases)
        newCases = self.toIntNoPlus(newCases)
        totalDeaths = self.toInt(totalDeaths)
        newDeaths = self.toIntNoPlus(newDeaths)
        totalRecovered = self.toInt(totalRecovered)
        activeCases = self.toInt(activeCases)
        return RowResult(stateString, totalCases, newCases, totalDeaths, newDeaths, totalRecovered, activeCases)

    def toIntNoPlus(self, singleTD):
        strAsInput = self.getText(singleTD)
        noPlus = self.removeChar(strAsInput, "+")
        return self.strToInt(noPlus)

    def toInt(self, singleTD):
        strAsInput = self.getText(singleTD)
        return self.strToInt(strAsInput)

    def strToInt(self, strAsInput):
        if strAsInput == "":
            return 0
        return int(strAsInput.replace(',', ''))

    def removeChar(self, strAsInput, charToRemove):
        return strAsInput.replace(charToRemove, "")

    def getText(self, singleTD):
        rawText = singleTD.text
        return rawText.strip()
