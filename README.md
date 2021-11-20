# skrowten

## Configs

Some important variables currently set in the script:

| Variable                | Current Value | Remarks                                                                                      |
| ----------------------- | ------------- | -------------------------------------------------------------------------------------------- |
| networkImpairmentAmount | 0             | starting value for network impairment                                                        |
| delayIntervalSize       | 100           | 100ms per interval, from 0ms to 1000ms                                                       |
| bandwidthIntervalSize   | 80            | 80Mbps per interval, from 80Mbps to 1000Mbps (0Mbps is excluded in the script for bandwidth) |
| packetLossIntervalSize  | 0.15          | 0.15% per interval, from 0% to 1.5%                                                          |
| noOfIntervals           | 11            | Decides how many network impairments we test, starting interval is from 0                    |
| iterations              | 3             | How many repeated runs are done per website test                                             |

## Running the Script

You can run the script with this command (sudo needed for tc command in script):

```
sudo ./auto_test_multiple_sitespeed.sh
```

You will then be prompted to choose the Network Impairment you want to run the tests on, as well as which txt file you want to use. You can refer to the assignments below

| Person                        | Delay  | Packet Loss | Bandwidth |
| ----------------------------- | ------ | ----------- | --------- |
| Person 1 (testing_sites1.txt) | Melody | Song Gee    | Hannah    |
| Person 2 (testing_sites2.txt) | Jerome | Marcus      | Jun Wei   |

## Uploading Files

You don't need to worry about uploading excess files, as Hannah has configured the gitignore to exclude unnecessary files and only include those we need. You can run the script, and the files will be saved in a folder unique to your assigned configuration, which you can upload in a commit. If you choose the right config, your files should not conflict or overwrite someone else's.

That's all, have fun running the script :D
<br/>
<br/>
<br/>

## Data Analysis

1. Get into the directory else the csv file not found error is thrown even if you use dataAnalysis/{file_name}

```
cd ${PWD}/skrowten/dataAnalysis
```

2. You should be able to see a few files that are needed for this script to run:
```
bandwidth.csv
delay.csv
packet_loss.csv
```
If anyone of the above stated files are missing,
run 
<br/>

On Mac/Linux:
```
python3 split_metric.py
```
On Windows:
```
python split_metric.py
```

3. The script works on the following flags READ CAREFULLY:
<br/>
<br/>
a. `-m` which means that you can input the metric that you are looking out for 
The only valid arguments are `delay`, `packetLoss` and `bandwidth`. Key in the EXACT syntax so that no exceptions are raised.
<br/>
<br/>
b. `-w` write the name of the website not the domain. The only valid arguments are `facebook`, `vk`,`instagram`,`whatsapp`, `canva`, `glassdoor`, any website name in the excel sheet works.
<br/>
<br/>
c. `-yaxis` write the name of the y axis that you would like to label.

d. `-xaxis` write the name of any of the column headers in the excel sheet.

An example of how to call the script would be the following:
```
python3 website_plot.py -m "delay" -w "facebook" -yaxis "lighthouse performance" -xaxis "throttleparameter"







