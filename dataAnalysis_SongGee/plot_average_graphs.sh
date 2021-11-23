for metric in delay packetLoss bandwidth; do
    for yaxis in $(seq 1 8); do
        python3 website_plot.py -m $metric -w 11 -yaxis $yaxis -xaxis "throttleparameter"
    done
done