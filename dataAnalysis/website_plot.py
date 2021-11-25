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

    if website != 'average' and website != "weighted_average":
        #select according to the stated x_label
        selected_df = data.loc[data['url']==website]

        for index,row in selected_df.iterrows():
            http_v = int(row['httpVersion'])
            x_val = row[x_label].replace("%",'')
            x_val = x_val.replace("ms",'')
            x_val = x_val.replace("Mbps",'')
            if x_label == 'throttleparameter':

                if metric == 'packetLoss':
                    
                    x_value = x_val * 100
                else:
                    x_value = round(float(x_val),5)
            else:
                x_value = round(float(x_val),5)
            #split into the http2 and http3
            if http_v == 2:
                http2_x.append(x_value)
                http2_y.append(row[y_input])
                
            if http_v == 3:
                http3_x.append(x_value)
                http3_y.append(row[y_input])


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

    elif website == 'average':
        urls = [
            "https://www.facebook.com/",
            "https://www.instagram.com/",
            "https://www.glassdoor.com/",
            "https://www.canva.com/",
            "https://www.youtube.com/",
            "https://www.google.com/",
        ]
        averageByMetricDictHTTP2 = {}
        averageByMetricDictHTTP3 = {}

        for index,row in data.iterrows():
            if(row["url"] not in urls):
                continue
            http_v = int(row['httpVersion'])
            x_val = row[x_label].replace("%",'')
            x_val = x_val.replace("ms",'')
            x_val = x_val.replace("Mbps",'')

            if x_label == 'throttleparameter':
                if metric == 'packetLoss':
                    
                    x_value = x_val * 100
                else:
                    x_value = round(float(x_val),5)
            else:
                x_value = round(float(x_val),5)

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
    else:
        urls = [
            "https://www.facebook.com/",
            "https://www.instagram.com/",
            "https://www.glassdoor.com/",
            "https://www.canva.com/",
            "https://www.youtube.com/",
            "https://www.google.com/",
        ]
        segmented_data = {} #key: throttle param, val = {url: [[stat, http2type, http3 fraction]]}

        for index,row in data.iterrows():
            if(row["url"] not in urls):
                continue
            http_v = int(row['httpVersion'])
            x_val = row[x_label].replace("%",'')
            x_val = x_val.replace("ms",'')
            x_val = x_val.replace("Mbps",'')

            if x_label == 'throttleparameter':
                if metric == 'packetLoss':
                    
                    x_value = x_val * 100
                else:
                    x_value = round(float(x_val),5)
            else:
                x_value = round(float(x_val),5)
        
            segmented_data[x_value] = segmented_data.get(x_value, {})
            data = segmented_data[x_value].get(row['url'], [])
            
            if http_v == 2:
                data.append((row[y_input], http_v, None))

            elif http_v == 3:
                http3_response_fraction = float(row["num_http3_responses"])/ (float(row["num_http3_responses"]) + float(row["num_http2_responses"]))
                data.append((row[y_input], http_v, http3_response_fraction))
            
            segmented_data[x_value][row['url']] = data

        print(segmented_data)
        x_keys = sorted(segmented_data.keys())  # Keys for HTTP2 and 3 are the same

        for key in x_keys:
            http2_x_ls.append(key)
            http3_x_ls.append(key)
            # get all weighted average

            http2_http3_values = segmented_data[key]
            total_fraction = 0
            url_weights = {}
            for url in http2_http3_values:
                for index in http2_http3_values[url]:
                    # for _, version, fraction in index:
                    if index[1]==3:
                        url_weights[url] = index[2]
                        total_fraction+=index[2]
            
            http3_average_score = 0 
            http2_average_score = 0
            for url in http2_http3_values:
                for index in http2_http3_values[url]:
                        stat = index[0]
                        if index[1]==3:
                            http3_average_score += stat* (url_weights[url])/len(http2_http3_values)

                        else:
                            http2_average_score += stat* (url_weights[url])/len(http2_http3_values)

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
        filein = "delay_cleaned_data_with_num_requests.csv"
    if metric == "packetLoss":
        filein = "packetLoss_cleaned_data_with_num_requests.csv"
    if metric == "bandwidth":
        filein = "bandwidth_cleaned_data_with_num_requests.csv"
    
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
