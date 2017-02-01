#!/usr/bin/python

#   PURPOSE: To extract data from csv files 
#               > BT (<timestamp>_BT)
#               > BT_SCAN (<timestamp>_BT_SCAN)
#               > WIFI (<timestamp>_WIFI)
#   and analyse them to compute the following parameters:
#       > number of devices discovered
#       > time to discover all devices
#       > Number of Scans
#       > Time for one scan

import sys
import csv
import os
import math
import re

####################################################################################
# displays the results in a formatted manner
####################################################################################
def print_results(test_name,trial_no, result):

    print("**************************************************")
    
    try:
        if test_name == "BLUETOOTH":

            print("TEST CARRIED OUT:                    ", test_name)
            print("Trial Number:                        ", trial_no) 
            print("Number of devices discovered:        ", result[0])
            print("Max Time to descover all devices:    ", result[1])
            print("Average Time for one scan:           ", result[2])
            print("Max. scans required:                 ", result[3])

        elif test_name == "WIFI":
            
            print("TEST CARRIED OUT:                    ", test_name)
            print("Trial Number:                        ", trial_no) 
            print("Number of devices discovered:        ", result[0])
            print("Max Time to descover all devices:    ", result[1])

        else:
            raise Exception("Undefined test_name:", test_name)
    except Exception as e:
        print(e.args)

    print("**************************************************")

####################################################################################
# calculations
####################################################################################
def BT(mList, file_name):

    #get start time of trial
    start_time = int(re.search(r"\d+(\.\d+)?", file_name).group(0))

    # Bluetooth Computation
    no_of_dev = len(mList)
    total_time = 0
    acc = 0

    for mac, mac_list in mList.items():
        
        for entry in mac_list:
            diff = int(entry[1]) - int(entry[0])
            acc += diff

        total_time = max(total_time,int(mac_list[0][1]))

    return [no_of_dev, total_time - start_time]

def BT_SCAN(mList, result_array):
    
    avg_scan_time = 0
    max_no_scan = 0
    max_time = int(result_array[1])


    for no, times in mList.items():

        diff = int(times[2]) - int(times[0])
        avg_scan_time = avg_scan_time + diff

        if int(times[0]) <= max_time and int(times[2]) >= max_time:
            max_no_scan = no

    result_array.append(avg_scan_time / len(mList))
    result_array.append(max_no_scan)
    return result_array

def WIFI(mList, file_name):

    #get start time of trial
    start_time = int(re.search(r"\d+(\.\d+)?", file_name).group(0))

    # Wifi Computation
    no_of_dev = len(mList)
    total_time = 0
    acc = 0

    for mac, mac_list in mList.items():
        
        for entry in mac_list:
            diff = int(entry[1]) - int(entry[0])
            acc += diff

        total_time = max(total_time, int(mac_list[0][1]))


    return [no_of_dev, total_time - start_time]

####################################################################################
# open and read appropriate files and convert data into datastructure
####################################################################################

def bluetooth(fList):
    # open csv file for reading
    trial = 1
    result = []
    for file in fList:
        with open(m_path+"\\"+file, newline="") as fp:
            reader = csv.reader(fp)

            # based on the file perform the appropriate calculations
            if file.find("BT_SCAN") != -1 :
        
                scan_dict = dict()
                scan_count = 0
                int_count  = 1
                temp = list()
                for row in reader:

                    if row[0] == "REQUESTED" and int_count == 1 :
                        temp.append(row[1])
                        int_count += 1

                    elif row[0] == "STARTED" and int_count == 2:
                        temp.append(row[1])
                        int_count += 1

                    elif row[0] == "FINISHED" and int_count == 3:
                        temp.append(row[1])
                        scan_dict[scan_count] = temp
                        temp = list()
                        int_count = 1
                        scan_count += 1

                result = BT_SCAN(scan_dict, result)
                print_results("BLUETOOTH", trial, result)
                trial +=1

            else:

                mList = dict()
                for row in reader:
                    if row[0].isdigit():

                        if row[3] in mList.keys():
                            mList[row[3]].append(row)
                        else:
                            mList[row[3]] = list()
                            mList[row[3]].append(row)

                result = BT(mList, file)        

def wifi(fList):

    trial = 1

    for file in fList:
        with open(m_path+"\\"+file, newline="") as fp:
            reader = csv.reader(fp)

            mList = dict()
            for row in reader:
                if row[0].isdigit():

                    if row[3] in mList.keys():
                        mList[row[3]].append(row)
                    else:
                        mList[row[3]] = list()
                        mList[row[3]].append(row)
        
        #calculations
        #print(mList)
        result = WIFI(mList, file)
        print_results("WIFI", trial, result)
        trial +=1


if __name__ == "__main__":

    try:
   
        m_path =sys.argv[1] #'C:\\Users\\sarahcs\\Documents\\College\\TRIAL 2\\Sarah'

        #retrieve all files from a directory
        files = [f for f in os.listdir(m_path) if os.path.isfile(os.path.join(m_path, f))]

        btFiles = []
        wifiFiles = []
        
        for file in files:

            if file.find("BT") != -1 :
                btFiles.append(file)
            elif file.find("WIFI") != -1 :
                wifiFiles.append(file)
            else:
                raise Excpetion("Undefined file name: "+file)
        
        bluetooth(btFiles)
        wifi(wifiFiles)

    except Exception as e:
        print(e.args)

    except FileNotFoundError:
        print("The sepcified path does not exist:", m_path)

            

