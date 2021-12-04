import bt_keywords as kw 

import pandas as pd
import json
import os  
import sys

SKIP_LIGHTHOUSE_METRICS=False

'''
This function retrieves all the results from the custom results 
directory and extracts the fields we deem necessary into a csv file. 
The csv file can be found in 
    rootDir/kw.EXTRACT_DATA_DIR/CURRTIME/kw.CSV_FILE_CURRTIME.csv
The program will quit if no custom directory is found in the 
provided root directory. 

Returns: csv file path. 
'''
def createCSVFromJsons(rootPath, currTime, throttleType, site_list_version, csvDir=None, csvFilePath=None, skipLighthouseMetrics=False):
    global SKIP_LIGHTHOUSE_METRICS
    SKIP_LIGHTHOUSE_METRICS = skipLighthouseMetrics
    resultsDir = os.path.join(rootPath, kw.BT_CUSTOM_DIR, throttleType, site_list_version)
    if not os.path.exists(resultsDir):
        print(resultsDir, "directory not found in root path.")
        sys.exit(1)
    

    if csvFilePath == None:
        includeHeader=True
        if csvDir == None:
            csvDir = os.path.join(rootPath, kw.EXTRACT_DATA_DIR, str(currTime))
        if not os.path.exists(csvDir):
            os.makedirs(csvDir)

        csvFileName = "{}_{}.csv".format(kw.CSV_FILE, currTime)
        csvFilePath = os.path.join(csvDir, csvFileName)

    else:
        includeHeader = False
        if not os.path.isfile(csvFilePath):
            print(csvFilePath, "csv file not found")
            sys.exit(1)

    for httpDirName in kw.HTTP_DIR_LIST:
        httpDir = os.path.join(resultsDir, httpDirName)
        throttleparameters = os.listdir(httpDir)
        for throttleparameter in throttleparameters:
            currDir = os.path.join(httpDir, throttleparameter)
            for BTJsonFile, harPath, lighthousePath in getJsonHarFilePaths(currDir):
                cleanedPdData = getCleanedPandas(
                    BTJsonFile, harPath, lighthousePath, 
                    throttleType, throttleparameter)
                if cleanedPdData is not None:
                    cleanedPdData.to_csv(csvFilePath, mode='a', header=includeHeader)
                    includeHeader = False
    print("Cleaned data written to csv file:", csvFilePath)
    return csvFilePath


'''
Checks if the broswertime program failed for that particular run.
This failure is marked in the JSON file. 

Returns True if failed, otherwise false.
'''
def checkHasFailed(result):
    return result.get(kw.BTJsonArgs.FAILURE, 0)

'''
In the sitespeed-results directory, the conventional path used is:
    CUSTOM_DIR/THROTTLE_TYPE/SITE_LIST_VERSION/HTTP_VERSION/THROTTLE_PARAMS/pages/PAGE_NAME/data
where FILE is either browsertime.pageSummary.json or lighthouse.pageSummary.json
    or browsertime.har.

This function goes through each result and yields the Json and Har file 
paths. 

Yields the absolute browsertime Json, Har file, lighthouse json paths one by one.
''' 
def getJsonHarFilePaths(rootPath):
    pageDir = os.path.join(rootPath, kw.SPEED_IO_PAGE_DIR)
    websitesVisited = os.listdir(pageDir)
    for website in websitesVisited:
        dataPath = os.path.join(pageDir, website, kw.SPEED_IO_DATA_DIR)
        if not os.path.exists(dataPath):
            continue

        BTJsonFilePath = os.path.join(dataPath, kw.SPEED_IO_JSON)
        harFilePath = os.path.join(dataPath, kw.SPEED_IO_HAR)
        lighthouseFilePath = os.path.join(dataPath, kw.SPEED_IO_LIGHTHOUSE)

        if os.path.isfile(BTJsonFilePath) and \
            os.path.isfile(harFilePath) and \
                os.path.isfile(lighthouseFilePath):
            yield BTJsonFilePath, harFilePath, lighthouseFilePath
        else:
            print("ERROR(getJsonHarFilePaths): could not get files", BTJsonFilePath, harFilePath, lighthouseFilePath)

'''
A session is considered to have used HTTP3 if at least one of the HTTP response messages
in the HAR file indicates that it used HTTP3. Otherwise it is HTTP2.

Returns the HTTP Version 2 or 3, the number of http2 responses and the number of http3 responses
'''
def getHTTPVersion(harFile):
    with open(harFile, 'r') as hf:
        harData = json.loads(hf.read())
    numHTTP2Responses = 0 
    numHTTP3Responses = 0 
    
    for entry in harData[kw.HAR_ROOT][kw.HAR_ENTRIES]:
        response = entry.get(kw.HAR_HTTP_RESPONSE)
        
        h3 = kw.SITESPEED_HTTP_VERSION_3 
        if response is not None:
            if response.get(kw.HAR_HTTP_VERSION_SUB) == h3:
                numHTTP3Responses +=1
                
            else:
                numHTTP2Responses +=1
    if numHTTP3Responses > 0 :
        httpVersion = 3
    else:
        httpVersion = 2

    return httpVersion, numHTTP2Responses, numHTTP3Responses


'''
Inserts all wanted data from a given subJson into a given dictionary extractedData.
The keys of the wanted data has to be listed in wantedKeyList.
The jsonFile is only needed when printing an error message.

Returns None
'''
def getSubJsonInfo(extractedData, subJson, wantedKeyList, jsonFile = None):
    for jsonKey in wantedKeyList:
        try:
            stat = subJson.get(jsonKey)
            if(type(stat) == dict):
                for key, val in stat.items():
                    new_title = jsonKey + "_" + key
                    extractedData[new_title] = val
            else:
                extractedData[jsonKey] = stat
        except:
            print("Could not get", jsonKey, "in", jsonFile)

'''
Only get statistics wanted fromt he given subJson into a given dictionary extractedData.
The keys of the wanted data has to be listed in wantedKeyList.
The jsonFile is only needed when printing an error message.

Returns None
'''
def getSatsSubJsonInfo(extractedData, subJson, wantedKeyList, jsonFile = None):
    for jsonKey in wantedKeyList:
        try:
            stat = subJson.get(jsonKey)
            if(type(stat) == dict):
                for statWanted in kw.BTJsonArgs.STATS_WANTED:
                    val = stat.get(statWanted, None)
                    new_title = jsonKey + "_" + statWanted
                    extractedData[new_title] = val
            else:
                for statWanted in kw.BTJsonArgs.STATS_WANTED:
                    new_title = jsonKey + "_" + statWanted
                    extractedData[new_title] = None
                extractedData[jsonKey + "_" + kw.BTJsonArgs.MEAN] = stat
                
        except:
            print("Could not get", jsonKey, "in", jsonFile)

'''
Validates if the browsertime session was completed succesfully
and extracts data from the browsertime json file.

Returns True, if the session completed successfully, otherwise, False.
'''
def getBTJsonInfo(extractedData, BTJsonFile):
    with open(BTJsonFile) as file:
        data = json.load(file)
    if type(data) == list:
        data = data[0]
    
    # Validate if page fetch was a success
    if checkHasFailed(data):
        print(BTJsonFile, "was marked as failed.")
        return False

    # Get websites and timing
    infoSubJson = data[kw.BTJsonArgs.INFO]
    getSubJsonInfo(extractedData, infoSubJson, kw.BTJsonArgs.INFO_LIST, BTJsonFile)

    # Get info.connectivity sub json
    infoConnectivity = infoSubJson[kw.BTJsonArgs.CONNECTIVITY]
    extractedData[kw.BTJsonArgs.PROFILE] = infoConnectivity[kw.BTJsonArgs.PROFILE]

    stats = data[kw.BTJsonArgs.STATISTICS]
    
    # Get statistic.coach.coachAdvice.advice.info sub json
    statsCoachAdviceInfo = stats[kw.BTJsonArgs.STAT_COACH][kw.BTJsonArgs.STAT_COACH_ADVICE] \
        [kw.BTJsonArgs.STAT_COACH_ADVICE_ADVICE]\
        [kw.BTJsonArgs.STAT_COACH_ADVICE_ADVICE_INFO]
    getSatsSubJsonInfo(extractedData, statsCoachAdviceInfo, kw.BTJsonArgs.STATS_COACH_ADVICE_INFO_LIST, BTJsonFile)


    # Get statistic.timing sub json
    statsTiming = stats[kw.BTJsonArgs.STAT_TIMINGS]
    getSatsSubJsonInfo(extractedData, statsTiming, kw.BTJsonArgs.STATS_TIMING_LIST, BTJsonFile)
    
    # Get statistic.timing.navigationTiming sub json
    statsTimingNav = statsTiming[kw.BTJsonArgs.NAV_TIMING]
    getSatsSubJsonInfo(extractedData, statsTimingNav, kw.BTJsonArgs.STATS_NAV_TIMING_LIST, BTJsonFile)
    return True

'''
Extracts data from the lighthouse json file if available

'''
def getLighthouseInfo(extractedData, lighthouseFilePath):
    with open(lighthouseFilePath) as file:
        data = json.load(file)

    # get perfoamce score
    performance = data
    for key in kw.LighthouseJsonArgs.GET_SCORE_LIST:
        performance = performance[key]
    if kw.LighthouseJsonArgs.SCORE in performance:
        extractedData[kw.LighthouseJsonArgs.PERFORMANCE_TITLE] = performance[kw.LighthouseJsonArgs.SCORE]
    else:
        for performance_stat in kw.LighthouseJsonArgs.PERFORMANCE_STAT_KEYS:
            extractedData[kw.LighthouseJsonArgs.PERFORMANCE_TITLE+"_"+performance_stat] = performance[performance_stat]


    # get audit scores
    audits = data.get(kw.LighthouseJsonArgs.AUDITS, None)
    if audits !=None:
        for audit in kw.LighthouseJsonArgs.ADUITS_LIST:
            auditJson = audits.get(audit, None)
            if auditJson is None:
                if not SKIP_LIGHTHOUSE_METRICS:
                    extractedData[audit] = None
            else:
                if auditJson["scoreDisplayMode"] == "error":
                    print("Lighthouse faced error for:", lighthouseFilePath)
                    return

                extractedData[audit + "_" + kw.LighthouseJsonArgs.SCORE] = auditJson[kw.LighthouseJsonArgs.SCORE]
                extractedData[audit + "_" + kw.LighthouseJsonArgs.NUMERIC_VALUE] = auditJson[kw.LighthouseJsonArgs.NUMERIC_VALUE]

'''
This function extracts the necessary data from the Json and Har files 
and puts them into a pandas dataframe.

Returns a pandas dataframe. 
'''
def getCleanedPandas(BTJsonFile, harFile, lighthouseFilePath, throttleType, throttleparameter):
    extractedData = {}
    
    # Get Browsertime Info
    validated = getBTJsonInfo(extractedData, BTJsonFile)

    if not validated:
        return None

    extractedData["throttleType"] = throttleType
    extractedData["throttleparameter"] = throttleparameter

    # Get HTTP version
    httpVersion, numHTTP2Responses, numHTTP3Responses = getHTTPVersion(harFile)
    extractedData[kw.HAR_HTTP_VERSION_SUB] = httpVersion
    extractedData[kw.NUM_HTTP2_REPONSES] = numHTTP2Responses
    extractedData[kw.NUM_HTTP3_REPONSES] = numHTTP3Responses

    # Get Lighthouse Info
    getLighthouseInfo(extractedData, lighthouseFilePath)

    df = pd.DataFrame(extractedData, index=[0])
    # print (df)
    return df