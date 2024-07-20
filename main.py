import csv
import random
from glob import glob
from datetime import datetime, timedelta


''' TODO add exception handling when
    - no file found
    - wrong format
    - more TBD
    - check if input file has at least 10 rows

    - add something interative in the cli like : select file from pwd 1.ASH.csv, 2.NMR.csv and read/predict for that file
'''
def main():
    input_data = read_input_csv(0)
    get_predicted_data(input_data)
    output_data = get_predicted_data(input_data)

# files_count - number of files to read from the pwd (1 or 2)
def read_input_csv(file_number):
    filename = glob("*.csv") # get the .csv filename from the current folder
    with open(filename[file_number], 'r') as file:
        csv_reader = csv.DictReader(file, fieldnames=['tick', 'date', 'value'])
        data = [row for row in csv_reader]
    starting_index = random.randint(0, len(data) - 10) # minus 10 to make sure we have at least 10 consecutive data points
    return data[starting_index : starting_index + 10]

# using the algo provided in the pdf
def get_predicted_data(input_data):
    # make an array of stock values only for easier use
    stock_values = [  float(item['value']) for item in input_data]
    n = stock_values[-1]

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


if __name__ == "__main__":
    main()