#!/bin/bash

# NOTE: The txt files used to read the URLs for testing MUST have an empty line at the end, otherwise the bash script will fail to read the final line and we'll have one less website tested

# Constants
browsertimeVersion="20.5.0-plus1"
preURL="https://www.lazada.sg/"

baseTestingFolder="BrowserTimeResults"
networkImpairmentFolder=""
outputFolderHTTP2="HTTP2_testing"
outputFolderHTTP3="HTTP3_testing"

# User Select for Network Impairment
networkImpairmentChoices='delay bandwidth packetLoss'  # Bash script array
networkImpairment=''
PS3='Select Network Impairment (Input number from 1 to 3): '
select _ in $networkImpairmentChoices
do
	networkImpairment=$_
	break
done

echo $networkImpairment
echo "-------------------------"

# User Select for testing_sites txt files
testingSiteChoices='testing_sites1 testing_sites2'
testingSite=''
testingSiteTxtName=''
PS3='Select which testing_sites file to use (Input number from 1 to 2): '
select _ in $testingSiteChoices
do
	testingSiteTxtName=$_
	testingSite="./$testingSiteTxtName.txt"
	break
done

echo $testingSiteTxtName
echo $testingSite
echo "-------------------------"


# Prepare Network Impairment variables for start of for loop
networkImpairmentAmount=0
delayIntervalSize=100  # 0ms to 1000ms
bandwidthIntervalSize=80  # 0Mbps to 1000Mbps
packetLossIntervalSize=0.15  # 0% to 1.5%
noOfIntervals=2  # 11
iterations=1  # Number of repeated trials ran for each website in every run

# Counters
intervalCounter=1

while [ $intervalCounter -le $noOfIntervals ]  # while intervalCounter <= noOfIntervals
do

	echo 'Stopping Docker networks'
	docker network rm 3g

	# Setup docker bridge with specified network impairment, prepare networkImpairmentFolder, increment networkImpairmentAmount for next run
	case $networkImpairment in

		delay)
			echo Starting Docker network with $networkImpairmentAmount ms delay
			docker network create --driver bridge --subnet=192.168.33.0/24 --gateway=192.168.33.10 --opt "com.docker.network.bridge.name"="docker1" 3g
			tc qdisc add dev docker1 root netem delay $networkImpairmentAmount'ms'

			networkImpairmentFolder="$networkImpairmentAmount"ms
			((networkImpairmentAmount+=delayIntervalSize))  # Prepare network impairment value for NEXT RUN
			;;

		bandwidth)
			# For bandwidth, since 0Mbps totally makes no sense, we skip it and continue with the other 10 iterations
			if [ $networkImpairmentAmount == '0' ]
			then
				echo Skipping bandwidth impairment of 0Mbps
				((intervalCounter++))
				((networkImpairmentAmount+=bandwidthIntervalSize))
				continue
			fi

			echo Starting Docker network with $networkImpairmentAmount Mbps bandwidth limit
			echo $(($networkImpairmentAmount*8))mbit
			docker network create --driver bridge --subnet=192.168.33.0/24 --gateway=192.168.33.10 --opt "com.docker.network.bridge.name"="docker1" 3g
			tc qdisc add dev docker1 root handle 1: htb default 12
			tc class add dev docker1 parent 1:1 classid 1:12 htb rate $(($networkImpairmentAmount*8))mbit ceil $(($networkImpairmentAmount*8))mbit

			networkImpairmentFolder="$networkImpairmentAmount"Mbps
			((networkImpairmentAmount+=bandwidthIntervalSize))  # Prepare network impairment value for NEXT RUN
			;;

		packetLoss)
			echo Starting Docker network with $networkImpairmentAmount% packet loss
			docker network create --driver bridge --subnet=192.168.33.0/24 --gateway=192.168.33.10 --opt "com.docker.network.bridge.name"="docker1" 3g
			tc qdisc add dev docker1 root netem loss 0$networkImpairmentAmount%  # 0 in front otherwise 

			networkImpairmentFolder="$networkImpairmentAmount"%
			networkImpairmentAmount=`echo $networkImpairmentAmount + $packetLossIntervalSize | bc`  # Prepare network impairment value for NEXT RUN, use pipe to BC for floating point addition
			;;

	esac

	# Begin Browsertime testing with network impaired bridge over all websites in txt file, for HTTP2 and HTTP3, with $iterations each
	siteCounter=1

	while IFS= read -r site
	do
		echo "--------- $site ------------"
		docker run --rm -v "$(pwd):/sitespeed.io" sitespeedio/sitespeed.io:$browsertimeVersion \
			--network=3g -c 3g -n $iterations --video false --visualMetrics false --prettyPrint true --cacheClearRaw true \
			--preURL $preURL --outputFolder "$baseTestingFolder/$networkImpairment/$testingSiteTxtName/$outputFolderHTTP2/$networkImpairmentFolder" $site \
			--plugins.add analysisstorer --plugins.add /lighthouse --chrome.args="--disable-quic"

		echo "----- Done Site $siteCounter ($site) HTTP2 with $networkImpairmentFolder $networkImpairment -----"
		docker run --rm -v "$(pwd):/sitespeed.io" sitespeedio/sitespeed.io:$browsertimeVersion \
			--network=3g -c 3g -n $iterations --video false --visualMetrics false --prettyPrint true --cacheClearRaw true \
			--preURL $preURL --outputFolder "$baseTestingFolder/$networkImpairment/$testingSiteTxtName/$outputFolderHTTP3/$networkImpairmentFolder" $site \
			--plugins.add analysisstorer --plugins.add /lighthouse

		echo "----- Done Site $siteCounter ($site) HTTP3 $networkImpairmentFolder $networkImpairment -----"

		((siteCounter=siteCounter+1))

	done < "$testingSite"

	((intervalCounter++))
done
