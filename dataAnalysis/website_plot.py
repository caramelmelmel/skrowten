#file related
import csv
import argparse
import sys
import os

#plot related
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np 
import pandas as pd

#constants related
from helper_ls import metric_ls_input

#plot two lines at once
def plot_http_ver_comparison(http2_x_ls, http2_y_ls, http3_x_ls, http3_y_ls):
    plt.plot(http2_x_ls,http2_y_ls,label='HTTP 2')
    plt.plot(http3_x_ls,http3_y_ls,label='HTTP 3')
    plt.legend()
    plt.show()

#to split for example the Mbps
def split_params(str_input,split_param):
    return str_input.split(split_param)


def plot_graphs(filein,website,x_label):
    
    #open the file in 
    data = pd.read_csv(filein)

    #read header and check if in header
    if x_label not in data.columns:
        raise ValueError("The stated label is not valid")
    
    #select according to the stated x_label
    selected_df = data.loc[data['url']==website]

    for index,row in selected_df.iterrows():
        http_v = int(row['httpVersion'])
        if x_label == 'throttleparameter':
            x_value = int(split_params(row['throttleparameter'],'Mbps'))
        else:
            x_value = float(row[x_label])
        
        http2_x = []
        http3_x = []

        #split into the http2 and http3
        if http_v == 2:
            http2_x.append(x_value)
        if http_v == 3:
            http3_x.append(x_value)

        #TODO add the y plots here for what you would like to plot
        #add the plots for http2 and 3 and then call the
        #plot_http_ver_comparison(http2_x_ls, http2_y_ls, http3_x_ls, http3_y_ls)
        #for analysis

    #TODO settle the file out here
    #make the dirs here


if __name__ == "__main__":

    #add arguments to parse into the script
    parser = argparse.ArgumentParser()
    parser.add_argument("-m",dest="metric",help="metric")
    parser.add_argument("-w",dest="website",help="website name (enter all in small caps)")
    parser.add_argument("-yaxis",dest="y_label",help="y axis label")
    parser.add_argument("-xaxis",dest="x_label", help="x axis label")
    args = parser.parse_args()


    website = "https://www." + args.website + ".com/"
    print(f"You have entered the website as {args.website}")
    metric = args.metric

    if (metric == None or args.website==None or args.y_label==None or args.x_label == None):
        raise ValueError("Please enter in all the flags as stated in the readme")
    
    if metric not in metric_ls_input:
        raise ValueError("Please enter either delay, packetLoss or bandwidth as the metric")

    if metric == "delay":
        filein = "delay.csv"
    if metric == "packetLoss":
        filein = "packet_loss.csv"
    if metric == "bandwidth":
        filein = "bandwidth.csv"
    
    #label axis
    #Plot title here refers to that of the website
    plt.xlabel(args.x_label)
    plt.ylabel(args.y_label)
    plt.title(args.website + " "+metric)
    plot_graphs(filein,website,args.x_label)

    

    

    
    

    