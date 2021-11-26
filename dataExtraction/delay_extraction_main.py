'''
This file is specifically for the collection of data used in 
our runs varying DELAY parameters for test_sites3.txt.

It will recursively look through all directories in delayRunResults. 
'''

import bt_keywords as kw 
import create_csv_utils_custom_dir as csv_util

from datetime import datetime
import sys
import os

DELAY = "delay"
DELAY_RESULTS_DIR = "delayRunResults"
SITE_LIST_VERSION = "testing_sites3"


def main(rootPath):
    currTime = datetime.now() 

    # Get all the directories
    full_delay_results_dir = os.path.join(rootPath, DELAY_RESULTS_DIR)
    all_user_files = os.listdir(full_delay_results_dir)

    csvFilePath = None
    for user_file in all_user_files:
        user_file_path = os.path.join(full_delay_results_dir, user_file)
        print("Extracting data from", user_file_path)
        csvFilePath = csv_util.createCSVFromJsons(user_file_path, currTime, DELAY, SITE_LIST_VERSION, rootPath, csvFilePath, True)
    
    print("-----------DONE-------------")

    
if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("There should be at most 2 sys arguments.")
        print("python3 delay_extraction_main.py PATH")
        print()
        print("Where PATH is an OPTIONAL different absolute path to find the results directory")
        sys.exit(1)

    # default root path is the current dir    
    rootPath = os.getcwd()

    # sys.argv[1] should be the root path if any
    if len(sys.argv) == 4:
        rootPath = sys.argv[1]

    # confirm params
    print()
    print("absolute path using:", rootPath)

    main(rootPath)