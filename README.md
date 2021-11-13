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
