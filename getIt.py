from scrape_runner import ScrapeRunner
from file_writer import FileWriter


def main():
    scrapeWorld()
    scrapeUSA()

def scrapeWorld():
    scrapeRunner = ScrapeRunner("https://www.worldometers.info/coronavirus/", "main_table_countries_today")
    singleScrape = scrapeRunner.run()
    fileWriter = FileWriter(singleScrape, "world")
    fileWriter.writeFile()

def scrapeUSA():
    scrapeRunner = ScrapeRunner("https://www.worldometers.info/coronavirus/country/us", "usa_table_countries_today")
    singleScrape = scrapeRunner.run()
    fileWriter = FileWriter(singleScrape, "usa")
    fileWriter.writeFile()

if __name__== "__main__":
  main()
