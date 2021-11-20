#This file splits the cleaned_data.csv into three different files:
# 1. bandwidth.csv 
# 2. delay.csv
# 3. packet_loss.csv
import csv

#input
filein = open('cleaned_data.csv',mode='r')

#output
file_delay = open('delay.csv','w')
file_packet_loss = open('packet_loss.csv','w')
file_bandwidth = open('bandwidth.csv','w')

#split the delimeter
reader = csv.reader(filein)

#read each row and column 28 as the metric

#header lines
header = next(reader)
files_list = [file_delay,file_packet_loss,file_bandwidth]

for file in files_list:
    writer = csv.writer(file)
    writer.writerow(header)

print('written header to all files')

for row in reader:

    if row[28] == 'bandwidth':
        writer = csv.writer(file_bandwidth)
    elif row[28] == 'delay':
        writer = csv.writer(file_delay)
    elif row[28] == 'packetLoss':
        writer = csv.writer(file_packet_loss)
    
    writer.writerow(row)

print('completed segmentation')
filein.close()
file_bandwidth.close()
file_delay.close()
file_packet_loss.close()
    
    
    
    
