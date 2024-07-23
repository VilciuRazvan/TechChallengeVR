import csv
import os
import random
from glob import glob
from datetime import datetime, timedelta
import sys

HEADER = ['tick', 'date', 'value']

def main():
    filenames = get_pwd_csvs() # get all .csv file names in the current directory
    if (len(filenames) < 1):
        print("No .csv files found in the current working directory.")
        return
    
    if (len(sys.argv) == 1): # no arg provided - parse and predict from all files
        for file in filenames:
            process_file(file)
    
    elif (len(sys.argv) == 2): # another arg provided
        try:
            arg = int(sys.argv[1])
            if (arg == 1): # process only 1 file, as requested in the task
                process_file(filenames[0])
            elif (arg == 2): # process the 2 files, as requested in the task
                for file in filenames[:2]:
                    process_file(file)
            else:
                print("Argument must be 1 or 2")
        except ValueError:
            print("Argument must be an integer")
    else: # 2+ args provided
        print("Invalid use. Please use python main.py [1|2]")        
        
def process_file(file):
    input_data = read_input_csv(file) # read .csv content into a list dict
    output_data = get_predicted_data(input_data) # return the input + predicted values into a list dict
    write_csv(file, output_data)

def get_pwd_csvs():
    filenames = glob("*.csv") # get the .csv filename from the current folder
    return filenames

def write_csv(file, output_data):
    new_file_name = file.replace('.csv', '_predict.csv')
    path = 'predictions/' + new_file_name
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=HEADER)
        writer.writeheader() # add csv headers
        writer.writerows(output_data)    


def read_input_csv(filename):
    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file, fieldnames=HEADER)
        data = [row for row in csv_reader]
    starting_index = random.randint(0, len(data) - 10) # minus 10 to make sure we have at least 10 consecutive data points
    return data[starting_index : starting_index + 10]

# using the algo provided in the pdf
def get_predicted_data(input_data):
    # make an array of stock values only (for ease of use)
    stock_values = [  float(item['value']) for item in input_data]
    n = stock_values[-1] # select newest value

    # first predicted (n+1) data point is same as the 2nd highest value present in the 10 data points
    dup_list = list(set(stock_values)) # remove duplicate stock values
    dup_list.sort(reverse=True) # sort in descending order
    n1 = dup_list[1] # second highest value

    # n+2 data point has half the difference between n and n +1
    n2 = round(min(n, n1) + (abs(n-n1) / 2), 2)

    # n+3 data point has 1/4th the difference between n+1 and n+2
    n3 = round(min(n1, n2) + (abs(n1-n2) / 4), 2)

    output_data = input_data.copy() # create a deep copy in case input data is still needed
    
    predicted_stock_values = [n1, n2, n3]
    predicted_data = [] # create a dict list of the 3 predicted values
    latest_date = datetime.strptime(input_data[-1]['date'], '%d-%m-%Y')    
    for i, value in enumerate(predicted_stock_values, start=1): 
        next_date = latest_date + timedelta(days=i)
        new_entry = {
        'tick': input_data[0]['tick'], # use the stock ticker name from the input
        'date': next_date.strftime('%d-%m-%Y'), # create the following days dates
        'value': value
    }
        predicted_data.append(new_entry)
    output_data.extend(predicted_data)

    return output_data


if __name__ == "__main__":
    main()