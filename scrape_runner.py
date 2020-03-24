import urllib.request
from typing import Dict
from bs4 import BeautifulSoup
from row_result import RowResult
from single_scrape import SingleScrape
import ssl


class ScrapeRunner:
    def __init__(self, url: str, tableName: str, tdMap: Dict[str, int]):
        self.url = url
        self.tableName = tableName
        self.tdMap = tdMap

    def run(self) -> SingleScrape:
        context = ssl._create_unverified_context()
        page = urllib.request.urlopen(self.url, context=context)
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
        stateString = self.getTextFromTD(tds, "state")
        totalCasesString = self.getTextFromTD(tds, "totalCases")
        newCasesString = self.getTextFromTD(tds, "newCases")
        totalDeathsString = self.getTextFromTD(tds, "totalDeaths")
        newDeathsString = self.getTextFromTD(tds, "newDeaths")
        totalRecoveredString = self.getTextFromTD(tds, "totalRecovered")
        activeCasesString = self.getTextFromTD(tds, "activeCases")
        totalCases = self.strToInt(totalCasesString)
        newCases = self.toIntNoPlus(newCasesString)
        totalDeaths = self.strToInt(totalDeathsString)
        newDeaths = self.toIntNoPlus(newDeathsString)
        totalRecovered = self.strToInt(totalRecoveredString)
        activeCases = self.strToInt(activeCasesString)
        return RowResult(stateString, totalCases, newCases, totalDeaths, newDeaths, totalRecovered, activeCases)

    def getTextFromTD(self, tds, key: str) -> str:
        if key not in self.tdMap:
            return ""
        td = tds[self.tdMap[key]]
        return self.getText(td)


    def toIntNoPlus(self, strAsInput: str) -> int:
        noPlus = self.removeChar(strAsInput, "+")
        return self.strToInt(noPlus)

    def strToInt(self, strAsInput: str) -> int:
        if strAsInput == "":
            return 0
        return int(strAsInput.replace(',', ''))

    def removeChar(self, strAsInput: str, charToRemove: str) -> str:
        return strAsInput.replace(charToRemove, "")

    def getText(self, singleTD) -> str:
        rawText = singleTD.text
        return rawText.strip()
