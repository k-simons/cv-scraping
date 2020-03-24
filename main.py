from scrape_runner import ScrapeRunner
from file_writer import FileWriter


def main():
    scrapeWorld()
    scrapeUSA()

def scrapeWorld():
    worldMap = {
        "state": 0,
        "totalCases": 1,
        "newCases": 2,
        "totalDeaths": 3,
        "newDeaths": 4,
        "totalRecovered": 5,
        "activeCases": 6,
    }
    scrapeRunner = ScrapeRunner("https://www.worldometers.info/coronavirus/", "main_table_countries_today", worldMap)
    singleScrape = scrapeRunner.run()
    fileWriter = FileWriter(singleScrape, "world")
    fileWriter.writeFile()

def scrapeUSA():
    USAMap = {
        "state": 0,
        "totalCases": 1,
        "newCases": 2,
        "totalDeaths": 3,
        "newDeaths": 4,
        "activeCases": 5,
    }
    scrapeRunner = ScrapeRunner("https://www.worldometers.info/coronavirus/country/us", "usa_table_countries_today", USAMap)
    singleScrape = scrapeRunner.run()
    fileWriter = FileWriter(singleScrape, "usa")
    fileWriter.writeFile()

if __name__== "__main__":
  main()
