import bt_keywords as kw 
import create_csv_utils_custom_dir as csv_util

from datetime import datetime
import sys
import os

PACKET_LOSS = "packetLoss"
BANDWIDTH = "bandwidth"
DELAY = "delay"

THROTTLE_TYPE_LIST = [
    PACKET_LOSS,
    BANDWIDTH,
    DELAY,
]

TEST_SITE_DIR = "testing_sites"

def getThrottleChoicePrompt():
    throttlePrompt = "Invalid throttle type, enter 0-{} ".format(len(THROTTLE_TYPE_LIST)-1) + \
        "to choose a valid throttle type.\n"
    for i, choice in enumerate(THROTTLE_TYPE_LIST):
        throttlePrompt +="{}) {}\n".format(i, choice)
    return throttlePrompt


def main(throttleType, site_list_version_num, rootPath):
    currTime = datetime.now()
    site_list_version = TEST_SITE_DIR + str(site_list_version_num) 
    csvFilePath = csv_util.createCSVFromJsons(rootPath, currTime, throttleType, site_list_version)
    
if __name__ == "__main__":
    if len(sys.argv) > 4 or len(sys.argv) < 3:
        print("There should be at most 4 sys arguments.")
        print("python3 main.py THROTTLE_TYPE SITELIST_NUM PATH")
        print()
        print("Where THROTTLE_TYPE is either {}, {} or {}".format(PACKET_LOSS, BANDWIDTH, DELAY))
        print("Where PATH is an OPTIONAL different absolute path to find the results directory")
        sys.exit(1)

    # default root path is the current dir    
    rootPath = os.getcwd()

    # check valid throttle type
    throttleType = sys.argv[1]
    while throttleType not in THROTTLE_TYPE_LIST:
        try:
            throttleTypeIndex = int(input(getThrottleChoicePrompt()))
            throttleType = THROTTLE_TYPE_LIST[throttleTypeIndex]
        except:
            pass

    # check valid site list version num
    if not sys.argv[2].isnumeric():
        site_list_version_num = -1
    else:
        site_list_version_num = int(sys.argv[2])
    while site_list_version_num != 1 and site_list_version_num !=2:
        site_list_version_num = int(input("Please enter either 1 or 2 for the testing site list version num. " +\
         "1 corresponds to {0}1 and 2 corresponds to {0}2: ".format(TEST_SITE_DIR)))

    # sys.argv[3] should be the root path if any
    if len(sys.argv) == 4:
        rootPath = sys.argv[3]

    # confirm params
    print()
    print("Throttle Type:", throttleType)
    print("Site List Version Num:", site_list_version_num)
    print("absolute path using:", rootPath)

    main(throttleType, site_list_version_num, rootPath)