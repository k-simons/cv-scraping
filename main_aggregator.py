from os import listdir
from os.path import isfile, join
import json
from functools import cmp_to_key
from datetime import datetime



scrapedDataPrefix = "./scrapedData/"
aggregatedDataPrefix = "./aggregatedData/"

def main():
    writeAggregatedFile("usa")
    writeAggregatedFile("world")

def writeAggregatedFile(subDir: str):
    finalMap = createFinalMap2(subDir)
    finalJSONMap = json.dumps(finalMap)
    mypath = aggregatedDataPrefix + subDir +  "/data.json"
    f = open(mypath, "w")
    f.write(finalJSONMap)
    f.close()

def createFinalMap2(subDir: str):
    mypath = scrapedDataPrefix + subDir
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    allDatas = []
    for fileName in onlyfiles:
        fullFileName = mypath + "/" + fileName
        with open(fullFileName) as json_file:
            data = json.load(json_file)
            allDatas.append(data)
    sortedArray = sorted(allDatas, key=lambda x: datetime.strptime(x['scrapeTime'], "%m:%d:%Y,%H:%M:%S"))
    finalMap = {}
    for i in range(len(sortedArray) - 1):
        firstDay = sortedArray[i]
        secondDay = sortedArray[i + 1]
        firstDayDatetimeObject =  dataToDatetimeObject(firstDay)
        secondDayDatetimeObject =  dataToDatetimeObject(secondDay)
        firstDayDateString = firstDayDatetimeObject.date().strftime("%m/%d/%Y")
        secondDayDateString = secondDayDatetimeObject.date().strftime("%m/%d/%Y")
        if firstDayDateString != secondDayDateString:
            smoothed = smoothOut(firstDay, secondDay)
            finalMap[firstDayDateString] = smoothed

    return finalMap

def smoothOut(firstDay, secondDay):
    w1, w2 = getWeights(firstDay, secondDay)
    newResults = []
    for item in firstDay["rowResults"]:
        for item2 in secondDay["rowResults"]:
            if item["state"] == item2["state"]:
                combine = {
                    "state": item["state"],
                }
                for k in item.keys():
                    if k == "state":
                        continue
                    valueFromItem1 = item[k]
                    valueFromItem2 = item2[k]
                    newValue = round((valueFromItem1 * w1) + (valueFromItem2 * w2))
                    combine[k] = newValue
                newResults.append(combine)

    return newResults

def getWeights(firstDay, second):
    firstDataTimeObject = dataToDatetimeObject(firstDay)
    secondDataTimeObject = dataToDatetimeObject(second)
    if firstDataTimeObject.hour == 23:
        return 1, 0
    return (firstDataTimeObject.hour/24), (secondDataTimeObject.hour/24)

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

def dataToDatetimeObject(data) -> datetime :
    scrapeTime = data["scrapeTime"]
    datetime_object = datetime.strptime(scrapeTime, "%m:%d:%Y,%H:%M:%S")
    return datetime_object

if __name__== "__main__":
  main()
