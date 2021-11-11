# TODO(Hannah): calculate lighthouse performance scores
# Get speed index  
# Get Connectivity 
# Separate by connectivity 
# Get lighthouse metrics

import bt_keywords as kw 

import matplotlib.pyplot as plt
import pandas as pd
from csv import reader
import os
import sys

PD_CHUNK_SIZE = 100

MEAN = "mean"
CONNECTIVITY_PROFILE = "profile"
DOM_ELE_MEAN = 'Dom Elements Mean'

STATS_MEAN_DOM_ELE_TO_PLOT = [
    kw.BTJsonArgs.FULLY_LOADED, 
    kw.BTJsonArgs.TTFB,
    kw.BTJsonArgs.LOADED_EVENT_END,
    kw.BTJsonArgs.FIRST_PAINT,
    kw.BTJsonArgs.DOM_COMPLETE,
]

'''
Generate all plots from data given in the csv file. 
The plots can be found in 
    rootDir/kw.EXTRACT_DATA_DIR/CURRTIME/kw.PLOT_DIR/CONNECTIVITY

Returns path to the plotDir.
'''
def generatePlots(csv_file, rootPath, currTime, connectivity):
    if not os.path.isfile(csv_file):
        print(csv_file, "not found.")
        sys.exit(1)
    
    plotDir = os.path.join(rootPath, kw.EXTRACT_DATA_DIR, str(currTime), kw.PLOT_DIR, connectivity)
    if not os.path.exists(plotDir):
        os.makedirs(plotDir)

    for statToPlot in STATS_MEAN_DOM_ELE_TO_PLOT:
        mean_name =  statToPlot + "_" + MEAN
        againstNumDomEle(csv_file, mean_name, plotDir, connectivity)
    
    # lighthouse metrics
    for audit in kw.LighthouseJsonArgs.ADUITS_LIST:
        againstNumDomEle(csv_file, audit + "_" + kw.LighthouseJsonArgs.SCORE, plotDir, connectivity)
        againstNumDomEle(csv_file, audit + "_" + kw.LighthouseJsonArgs.NUMERIC_VALUE, plotDir, connectivity)
    
    # performance
    againstNumDomEle(csv_file, kw.LighthouseJsonArgs.PERFORMANCE_TITLE, plotDir, connectivity)

    print("Plots saved in", plotDir)
    return plotDir

'''
Reads the csv file in chunks.

Yields pandas Dataframes in chunks.
'''
def readFromCsv(csv_file):
    for pdChunk in pd.read_csv(csv_file, chunksize=PD_CHUNK_SIZE):
        yield pdChunk

'''
Plots given http2 data and http3 data in the same graph and saves it to 
the given directory. 

This function uses line graphs but we can do other types of graphs 
after future discussions.

Returns None.
'''
def plotH2H3(h2X, h2Y, h3X, h3Y, x_label, y_label, title, plotDir, plot_type = "plot"):
    if len(h2X) >0:
        h2Unsorted = sorted(zip(*[h2X, h2Y]))
        h2X, h2Y = list(zip(*h2Unsorted))

    if len(h3X)>0:
        h3Unsorted = sorted(zip(*[h3X, h3Y]))
        h3X, h3Y = list(zip(*h3Unsorted))
    
    if plot_type == "scatter":
        plt.scatter(h2X, h2Y, label='HTTP2')
        plt.scatter(h3X, h3Y, label='HTTP3')

    else:
        plt.plot(h2X, h2Y, label='HTTP2')
        plt.plot(h3X, h3Y, label='HTTP3')

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.savefig(os.path.join(plotDir, '{}.png'.format(title)))
    plt.clf()

'''
This function is specifically for the plotting of a particular means value
against the number of DOM elements for both HTTP2 and HTTP3. 
It then calls plotH2H3 to plot both lines in the same graph. 

Returns None. 
'''
def againstNumDomEle(csv_file, y_name, plotDir, connectivity):
    title = '{} - {} vs Dom Elements Mean'.format(connectivity, y_name)
    http2DomEle = []
    h2Stat = []
    http3DomEle = []
    h3Stat = []

    for pd_chunk in readFromCsv(csv_file):
        for i, row in pd_chunk.iterrows():
            if row[CONNECTIVITY_PROFILE] != connectivity:
                continue
            httpversion = row[kw.HAR_HTTP_VERSION_SUB]
            numDomEle = row[kw.BTJsonArgs.DOM_ELEMENTS + "_" + MEAN]
            stat = row[y_name]
            if httpversion == 2:
                http2DomEle.append(numDomEle)
                h2Stat.append(stat)
            else:
                http3DomEle.append(numDomEle)
                h3Stat.append(stat)

    plotH2H3(http2DomEle, h2Stat, http3DomEle, h3Stat, DOM_ELE_MEAN, y_name, title, plotDir)

'''
Based on the lighthouse performance metrics
- First contentful paint: 15%
- Speed Index: 15%
- Largest Contentful Paint: 25%
- Time to Interactive: 15%
- Total Blocking time: 25%
- Cumulative Layout Shift: 5%
'''
def getIndivLighthousePerformance(df_row):
    firstContentfulPaint = ""
    speedIndex = 0
    largestContentfulPaint = ""
    timeToInteractive = 0
    totalBlockingTime = 0
    cumulativeLayoutShift = 0
    
    return 

def plotLighthousePerformace():
    for pd_chunk in readFromCsv(csv_file):
        for i, row in pd_chunk.iterrows():
            httpversion = row[kw.HAR_HTTP_VERSION_SUB]
            numDomEle = row[kw.BTJsonArgs.DOM_ELEMENTS + "_" + MEAN]
            statMean = row[mean_name]
            if httpversion == 2:
                http2DomEle.append(numDomEle)
                h2StatMean.append(statMean)
            else:
                http3DomEle.append(numDomEle)
                h3StatMean.append(statMean)

    plotH2H3(http2DomEle, h2StatMean, http3DomEle, h3StatMean, DOM_ELE_MEAN, mean_name, title, plotDir)

