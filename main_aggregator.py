from os import listdir
from os.path import isfile, join
import json
from datetime import datetime



scrapedDataPrefix = "./scrapedData/"
aggregatedDataPrefix = "./aggregatedData/"

def main():
    writeAggregatedFile("usa")
    writeAggregatedFile("world")

def writeAggregatedFile(subDir: str):
    finalMap = createFinalMap(subDir)
    finalJSONMap = json.dumps(finalMap)
    mypath = aggregatedDataPrefix + subDir +  "/data.json"
    f = open(mypath, "w")
    f.write(finalJSONMap)
    f.close()

def createFinalMap(subDir: str):
    mypath = scrapedDataPrefix + subDir
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    scrapesPerData = {}
    for fileName in onlyfiles:
        fullFileName = mypath + "/" + fileName
        with open(fullFileName) as json_file:
            data = json.load(json_file)
            newDateTimeObject = dataToDatetimeObject(data)
            dateString = newDateTimeObject.date().strftime("%m/%d/%Y")
            if dateString not in scrapesPerData:
                scrapesPerData[dateString] = data
            exisingDateTimeObject = dataToDatetimeObject(scrapesPerData[dateString])
            if newDateTimeObject > exisingDateTimeObject:
                scrapesPerData[dateString] = data
    finalMap = {}
    for key in scrapesPerData:
        finalMap[key] = scrapesPerData[key]["rowResults"]
    return finalMap


def dataToDatetimeObject(data):
    scrapeTime = data["scrapeTime"]
    datetime_object = datetime.strptime(scrapeTime, "%m:%d:%Y,%H:%M:%S")
    return datetime_object

if __name__== "__main__":
  main()
