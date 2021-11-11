import bt_keywords as kw 
import create_csv_utils_custom_dir as csv_util
import plot_graphs as pg 

from datetime import datetime
import sys
import os

CONNECTIVITY_TESTED = ["3g"]

def main(throttleType, comrade, rootPath):
    currTime = datetime.now()
    csvFilePath = csv_util.createCSVFromJsons(rootPath, currTime, throttleType, comrade)
    for connectivity in CONNECTIVITY_TESTED:
        pg.generatePlots(csvFilePath, rootPath, currTime, connectivity)
    
if __name__ == "__main__":
    if len(sys.argv) > 4 or len(sys.argv) < 3:
        print("There should be at most 4 sys arguments.")
        print("python3 main.py THROTTLE_TYPE COMRADE_NAME PATH")
        print("Where PATH is an OPTIONAL different absolute path to find the results directory")
        sys.exit(1)

    # default root path is the current dir    
    rootPath = os.getcwd()

    throttleType = sys.argv[1]
    comrade = sys.argv[2]

    # sys.argv[3] should be the root path if any
    if len(sys.argv) == 4:
        rootPath = sys.argv[3]
    
    print("absolute path using:", rootPath)

    main(throttleType, comrade, rootPath)