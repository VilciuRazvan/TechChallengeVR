# TechChallenge

# How to run
Clone the repo to your local device, then open up a terminal in the directory of the project. In there you should also have the desired .csv files (you can copy them from the LSE/NYSE/NASDAQ directories). You can then execute the script using the following commands:
- python main.py` this will attempt to read, predict and write the output .csv files in the /predictions directory. Note that this does not take into account the number of .csv files in the pwd. For that you can use:
- `python main.py 1` - which will only process one file
- `python main.py 2` - which will process two files, as stated in the Tech Challenge Data & Inputs.


All other uses will result in an error message to be displayed and the script to exit.

# Details
The two functions requested in the pdf are as follows:
- `read_input_csv(filename)` which reads a file and returns 10 random datapoints from that specific file
- `get_predicted_data(input_data)` which will attempt to predict the next 3 stock values based on the algorithm provided in the document
 ```
• first predicted (n+1) data point is same as the 2nd highest value present in the 10 data points
• n+2 data point has half the difference between n and n +1
• n+3 data point has 1/4th the difference between n+1 and n+2
 ```

Besides that there are 4 other functions meant to increase readability and maintainability of the code.
- `get_pwd_csvs()` - which returns the file names of all the .csv files in the directory of the main.py file (if there are any)
- `write_csv(file, output_data)` - writes a .csv file containing the initial values and the next 3 predicted values in the /predictions folder
- `process_file(file)` - reads the input .csv file, predicts the next values and writes to an output .csv file
- `main()` - entry point of the script