#!/bin/bash

# NOTE: The txt files used to read the URLs for testing MUST have an empty line at the end, otherwise the bash script will fail to read the final line and we'll have one less website tested

# NOTE: This file is different from auto_test_multiple_sitespeed.sh in the fact that it only tests for variations in delay. Moreover, it only tests for testing_sites3.

# Constants
browsertimeVersion="20.5.0-plus1"
preURL="https://www.lazada.sg/"

delayTestingFolder="delayRunResults"
baseTestingFolder="BrowserTimeResults"
networkImpairmentFolder=""
outputFolderHTTP2="HTTP2_testing"
outputFolderHTTP3="HTTP3_testing"

# Get User Name for Directory (everyone will be running as root)
read -p "Enter name (1 word): " userName

# Network Impairment
networkImpairment="delay"

echo $networkImpairment
echo "-------------------------"

# Testing_sites txt file
testingSiteTxtName="testing_sites3"
testingSite="./$testingSiteTxtName.txt"

echo $testingSiteTxtName
echo $testingSite
echo "-------------------------"

# Number of times to run all the websites
read -p "Number of Repetitions (integer>0): " numRepetitions
echo $numRepetitions repetitions
echo "-------------------------"

# Counters
repetitionCounter=1

while [ $repetitionCounter -le $numRepetitions ]  # while repetitionCounter <= numRepetitions
do
	userDir=$userName"_"$repetitionCounter
	
	# Prepare Network Impairment variables for start of for loop
	networkImpairmentAmount=0
	delayIntervalSize=200  # 0ms to 1000ms
	noOfIntervals=6  # 6 
	iterations=3  # Number of repeated trials ran for each website in every run
	
	# Counters
	intervalCounter=1
	
	echo "----Starting New Repetition" $userDir "-----"
	
	while [ $intervalCounter -le $noOfIntervals ]  # while intervalCounter <= noOfIntervals
	do
		echo 'Stopping Docker networks'
		docker network rm 3g

		# Setup docker bridge with specified network impairment, prepare networkImpairmentFolder, increment networkImpairmentAmount for next run

		echo Starting Docker network with $networkImpairmentAmount ms delay
		docker network create --driver bridge --subnet=192.168.33.0/24 --gateway=192.168.33.10 --opt "com.docker.network.bridge.name"="docker1" 3g
		tc qdisc add dev docker1 root netem delay $networkImpairmentAmount'ms'

		networkImpairmentFolder="$networkImpairmentAmount"ms
		((networkImpairmentAmount+=delayIntervalSize))  # Prepare network impairment value for NEXT RUN


		# Begin Browsertime testing with network impaired bridge over all websites in txt file, for HTTP2 and HTTP3, with $iterations each
		siteCounter=1

		while IFS= read -r site
		do
			echo "--------- $site ------------"
			docker run --rm -v "$(pwd):/sitespeed.io" sitespeedio/sitespeed.io:$browsertimeVersion \
				--network=3g -c 3g -n $iterations --video false --visualMetrics false --prettyPrint true --cacheClearRaw true \
				--preURL $preURL --outputFolder "$delayTestingFolder/$userDir/$baseTestingFolder/$networkImpairment/$testingSiteTxtName/$outputFolderHTTP2/$networkImpairmentFolder" $site \
				--plugins.add analysisstorer --plugins.add /lighthouse --lighthouse.iterations=$iterations --chrome.args="--disable-quic"

			echo "----- Done Site $siteCounter ($site) HTTP2 with $networkImpairmentFolder $networkImpairment -----"
			docker run --rm -v "$(pwd):/sitespeed.io" sitespeedio/sitespeed.io:$browsertimeVersion \
				--network=3g -c 3g -n $iterations --video false --visualMetrics false --prettyPrint true --cacheClearRaw true \
				--preURL $preURL --outputFolder "$delayTestingFolder/$userDir/$baseTestingFolder/$networkImpairment/$testingSiteTxtName/$outputFolderHTTP3/$networkImpairmentFolder" $site \
				--plugins.add analysisstorer --plugins.add /lighthouse --lighthouse.iterations=$iterations

			echo "----- Done Site $siteCounter ($site) HTTP3 $networkImpairmentFolder $networkImpairment -----"

			((siteCounter=siteCounter+1))

		done < "$testingSite"

		((intervalCounter++))
	done
	
	((repetitionCounter++))
done
