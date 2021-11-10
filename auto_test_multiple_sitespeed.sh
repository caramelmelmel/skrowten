#!/bin/bash
echo 'Stopping Docker networks'
docker network rm 3g
docker network rm 3gslow

echo 'Starting Docker networks'
docker network create --driver bridge --subnet=192.168.33.0/24 --gateway=192.168.33.10 --opt "com.docker.network.bridge.name"="docker1" 3g
tc qdisc add dev docker1 root handle 1: htb default 12
tc class add dev docker1 parent 1:1 classid 1:12 htb rate 1.6mbit ceil 1.6mbit
tc qdisc add dev docker1 parent 1:12 netem delay 150ms

docker network create --driver bridge --subnet=192.168.36.0/24 --gateway=192.168.36.10 --opt "com.docker.network.bridge.name"="docker4" 3gslow
tc qdisc add dev docker4 root handle 1: htb default 12
tc class add dev docker4 parent 1:1 classid 1:12 htb rate 0.4mbit ceil 0.4mbit
tc qdisc add dev docker4 parent 1:12 netem delay 200ms

echo 'Browsertime Running 3g and 3g slow'
http3WebsitesFile="./testing_sites.txt"

counter=1

while IFS= read -r site
do
	echo "--------- $site ------------"
	docker run --rm -v "$(pwd):/sitespeed.io" sitespeedio/sitespeed.io:11.0.0-plus1 --network=3g -c 3g --iterations 3 --prettyPrint true --cacheClearRaw true --preURL https://www.lazada.sg/ $site --plugins.add analysisstorer --plugins.add /lighthouse

	echo "-----Done $counter 3g HTTP2-----"

	docker run --rm -v "$(pwd):/sitespeed.io" sitespeedio/sitespeed.io:11.0.0-plus1 --network=3gslow -c 3gslow --iterations 3 --prettyPrint true --cacheClearRaw true --preURL https://www.lazada.sg/ $site --plugins.add analysisstorer --plugins.add /lighthouse

	echo "-----Done $counter 3gslow HTTP2-----"

	
	docker run --rm -u $USER -v "$(pwd):/sitespeed.io" sitespeedio/sitespeed.io:20.5.0-plus1 --network=3g -c 3g --iterations 3 --prettyPrint true --cacheClearRaw true --preURL https://www.lazada.sg/ $site --plugins.add analysisstorer --plugins.add /lighthouse


	echo "-----Done $counter 3g HTTP3-----"

	docker run --rm -u $USER -v "$(pwd):/sitespeed.io" sitespeedio/sitespeed.io:20.5.0-plus1 --network=3gslow -c 3gslow --iterations 3 --prettyPrint true --cacheClearRaw true --preURL https://www.lazada.sg/ $site --plugins.add analysisstorer --plugins.add /lighthouse

	echo "-----Done $counter 3gslow HTTP3-----"

	((counter=counter+1))

done < "$http3WebsitesFile"


echo '-----FINISHED-----'


