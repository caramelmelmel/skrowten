#file related
import csv
import argparse
from posixpath import split
import sys
import os

#plot related
import matplotlib.pyplot as plt
import seaborn as sb 
import pandas as pd

#constants related
from helper_ls import metric_ls_input
from constant_mapper import input_mapper_y, input_mapper_y_label, website_mapper

#plot two lines at once
def plot_http_ver_comparison(http2_x_ls, http2_y_ls, http3_x_ls, http3_y_ls,fig_file_p):
    print(http2_x_ls)
    print(http2_y_ls)
    print(http3_x_ls)
    print(http3_y_ls)
    plt.scatter(http2_x_ls,http2_y_ls,label='HTTP 2',c='#FF0000',alpha=0.8)
    plt.scatter(http3_x_ls,http3_y_ls,label='HTTP 3',c='#FFA500',alpha=0.5,s=15**2)
    plt.legend()
    #save into a dir 
    plt.savefig(fig_file_p)

#to split for example the Mbps
def split_throttleparams(str_input,file_name):
    if file_name == "delay.csv":
        return str_input.split('ms')
    if file_name == 'bandwidth.csv':
        return str_input.split('Mbps')


#plot based on the http version
def plot_graphs(metric,filein,website,x_label,y_input):
    #open the file in 
    data = pd.read_csv(filein)

    #read header and check if in header
    if x_label not in data.columns:
        raise ValueError("The stated label is not valid")

    http2_x = []
    http3_x = []
    http2_y = []
    http3_y = []

    http2_x_ls = []
    http2_y_ls = []
    http3_x_ls = []
    http3_y_ls = []

    if website != 'average':
        #select according to the stated x_label
        selected_df = data.loc[data['url']==website]

        for index,row in selected_df.iterrows():
            http_v = int(row['httpVersion'])
            if x_label == 'throttleparameter':
                if metric == 'packetLoss':
                    x_value = float(row[x_label]) * 100
                else:
                    x_value = round(float(split_throttleparams(row[x_label],filein)[0]),5)
            else:
                x_value = round(float(row[x_label]),5)

            #split into the http2 and http3
            if http_v == 2:
                http2_x.append(x_value)
                http2_y.append(row[y_input])
                
            if http_v == 3:
                http3_x.append(x_value)
                http3_y.append(row[y_input])

        print(len(http2_x))
        print(len(http2_y)) 
        print(http2_x)
        print(http2_y)
        print(http3_x)
        print(http3_y)

        http2_x = {i: http2_x[i] for i in range(0, len(http2_x))}
        http2_y = {i: http2_y[i] for i in range(0, len(http2_y))}
        http3_x = {i: http3_x[i] for i in range(0, len(http3_x))}
        http3_y = {i: http3_y[i] for i in range(0, len(http3_y))}

        #get a tuple
        http2_x = sorted(http2_x.items(), key=lambda x: x[1])
        http3_x = sorted(http3_x.items(), key=lambda x: x[1])

        for i in http2_x:
            http2_x_ls.append(i[1])
            http2_y_ls.append(http2_y[i[0]])
        
        for i in http3_x:
            http3_x_ls.append(i[1])
            http3_y_ls.append(http3_y[i[0]])

    else:
        averageByMetricDictHTTP2 = {}
        averageByMetricDictHTTP3 = {}

        for index,row in data.iterrows():
            http_v = int(row['httpVersion'])

            if x_label == 'throttleparameter':
                if metric == 'packetLoss':
                    x_value = float(row[x_label]) * 100
                else:
                    x_value = round(float(split_throttleparams(row[x_label],filein)[0]),5)
            else:
                x_value = round(float(row[x_label]),5)

            if http_v == 2:
                if x_value not in averageByMetricDictHTTP2:
                    averageByMetricDictHTTP2[x_value] = [row[y_input]]
                else:
                    averageByMetricDictHTTP2[x_value] = averageByMetricDictHTTP2[x_value] + [row[y_input]]
            elif http_v == 3:
                if x_value not in averageByMetricDictHTTP3:
                    averageByMetricDictHTTP3[x_value] = [row[y_input]]
                else:
                    averageByMetricDictHTTP3[x_value] = averageByMetricDictHTTP3[x_value] + [row[y_input]]
            
        print(averageByMetricDictHTTP2)
        print(averageByMetricDictHTTP3)

        x_keys = sorted(averageByMetricDictHTTP2.keys())  # Keys for HTTP2 and 3 are the same

        for key in x_keys:
            http2_x_ls.append(key)
            http3_x_ls.append(key)

            # Compute Avg
            http2_results_list = averageByMetricDictHTTP2[key]
            http3_results_list = averageByMetricDictHTTP3[key]
            http2_average_score = sum(http2_results_list) / len(http2_results_list)
            http3_average_score = sum(http3_results_list) / len(http3_results_list)

            http2_y_ls.append(http2_average_score)
            http3_y_ls.append(http3_average_score)

    
    save_file = f"results_graphs/{website}/{y_input}_{metric}.png"
    #realised
    plot_http_ver_comparison(http2_x_ls,http2_y_ls,http3_x_ls,http3_y_ls,save_file)


if __name__ == "__main__":

    #add arguments to parse into the script
    parser = argparse.ArgumentParser()
    parser.add_argument("-m",dest="metric",help="metric")
    parser.add_argument("-w",dest="website",help="website name (enter all in small caps)",type=int)
    parser.add_argument("-yaxis",dest="y_label",help="y axis label",type=int)
    parser.add_argument("-xaxis",dest="x_label", help="x axis label")
    args = parser.parse_args()


    website = website_mapper[args.website]
    print(f"You have entered the website as {website}")
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
    
    #manage directories here
    if os.path.isdir('results_graphs') == False:
        print('making the results_graph directory')
        os.makedirs('results_graphs')
    
    if os.path.isdir('results_graphs/'+website) == False:
        print(f"making the directory for {website}")
        os.makedirs(f'results_graphs/{website}')
    
    #label axis
    #Plot title here refers to that of the website
    plt.xlabel(args.x_label)
    plt.ylabel(input_mapper_y_label[args.y_label])
    plt.title(website + " "+metric)

    plot_graphs(metric, filein,website,args.x_label,input_mapper_y[args.y_label])
