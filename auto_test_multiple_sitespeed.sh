#!/bin/bash

# Constants
browsertimeVersion="20.5.0-plus1"

outputFolderHTTP2="HTTP2_testing"
outputFolderHTTP3="HTTP3_testing"
preURL="https://www.lazada.sg/"

# User Select for Network Impairment and testing_sites txt files
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

testingSiteChoices='./testing_sites1.txt ./testing_sites2.txt'
testingSite=''
PS3='Select which testing_sites file to use (Input number from 1 to 2): '
select _ in $testingSiteChoices
do
	testingSite=$_
	break
done

echo $testingSite
echo "-------------------------"


# Prepare Network Impairment variables for start of for loop
networkImpairmentAmount=0
delayIntervalSize=100  # 0ms to 1000ms
bandwidthIntervalSize=80  # 0Mbps to 1000Mbps
packetLossIntervalSize=0.15  # 0% to 1.5%
noOfIntervals=11  # 11
iterations=3  # Number of repeated trials ran for each website in every run

# Counters
intervalCounter=1

while [ $intervalCounter -le $noOfIntervals ]  # while intervalCounter <= noOfIntervals
do

	siteCounter=1

	echo 'Stopping Docker networks'
	docker network rm 3g

	# Setup docker bridge with specified network impairment
	case $networkImpairment in

		delay)
			echo Starting Docker network with $networkImpairmentAmount ms delay
			docker network create --driver bridge --subnet=192.168.33.0/24 --gateway=192.168.33.10 --opt "com.docker.network.bridge.name"="docker1" 3g
			tc qdisc add dev docker1 root netem delay $networkImpairmentAmount'ms'
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
			((networkImpairmentAmount+=bandwidthIntervalSize))  # Prepare network impairment value for NEXT RUN
			;;

		packetLoss)
			echo Starting Docker network with $networkImpairmentAmount% packet loss
			docker network create --driver bridge --subnet=192.168.33.0/24 --gateway=192.168.33.10 --opt "com.docker.network.bridge.name"="docker1" 3g
			tc qdisc add dev docker1 root netem loss 0$networkImpairmentAmount%  # 0 in front otherwise 
			networkImpairmentAmount=`echo $networkImpairmentAmount + $packetLossIntervalSize | bc`  # Prepare network impairment value for NEXT RUN, use pipe to BC for floating point addition
			;;

	esac

	((intervalCounter++))
done

# echo 'Stopping Docker networks'
# docker network rm 3g

# echo 'Starting Docker networks'
# docker network create --driver bridge --subnet=192.168.33.0/24 --gateway=192.168.33.10 --opt "com.docker.network.bridge.name"="docker1" 3g
# tc qdisc add dev docker1 root handle 1: htb default 12
# tc class add dev docker1 parent 1:1 classid 1:12 htb rate 1.6mbit ceil 1.6mbit
# tc qdisc add dev docker1 parent 1:12 netem delay 150ms

# # echo 'Browsertime Running 3g and 3g slow'

# while IFS= read -r site
# do
# 	echo "--------- $site ------------"
# 	docker run --rm -v "$(pwd):/sitespeed.io" sitespeedio/sitespeed.io:$browsertimeVersion \
# 		--network=3g -c 3g --iterations $iterations --video false --visualMetrics false --prettyPrint true --cacheClearRaw true \
# 		--preURL $preURL --outputFolder "$outputFolderHTTP2" $site --plugins.add analysisstorer --plugins.add /lighthouse --chrome.args="--disable-quic"

# 	echo "----- Done Site $siteCounter ($site) HTTP2 -----"

# 	docker run --rm -v "$(pwd):/sitespeed.io" sitespeedio/sitespeed.io:$browsertimeVersion \
# 		--network=3g -c 3g --iterations $iterations --video false --visualMetrics false --prettyPrint true --cacheClearRaw true \
# 		--preURL $preURL --outputFolder "$outputFolderHTTP3" $site --plugins.add analysisstorer --plugins.add /lighthouse

# 	echo "----- Done Site $siteCounter ($site) HTTP3 -----"

# 	((siteCounter=siteCounter+1))

# done < "$http3WebsitesFile"


# echo '-----FINISHED-----'


