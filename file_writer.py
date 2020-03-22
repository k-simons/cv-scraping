from single_scrape import SingleScrape

class FileWriter:
    def __init__(self, singleScrape: SingleScrape, tag: str):
        self.singleScrape = singleScrape
        self.tag = tag

    def writeFile(self):
        fileName = self.singleScrape.scrapeTime
        relativePath = "scrapedData/" + self.tag + "/" + fileName
        f = open(relativePath, "w")
        f.write(self.singleScrape.serialize())
        f.close()