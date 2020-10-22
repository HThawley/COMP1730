"""
Template for the COMP1730/6730 project assignment, S2 2020.
The assignment specification is available on the course web site:
https://cs.anu.edu.au/courses/comp1730/assessment/project/

The assignment is due 25/10/2020 at 11.55 pm, Canberra time.

Collaborators: u6942852, u6942813, u6941278
"""

def analyse(path_to_file):
    """
    Function: 
    Prints sequentially the solution to each question in the assignment for the given data file 
    
    Input:
    Takes one string as an argument, containing the location of a csv data file
    
    Output:
    Prints a line stating the name of the file being analysed
    Prints the first year and month data was taken
    For each year present, even if no data was taken, prints the number of days with an AQI_PM2.5 of 100 or above
    For each month which was the worst for any year, prints the years and the number of years for which it was the worst
    Prints the highest AQI_PM2.5 value(s) present in the given data set, and the date and time they were recorded
    Prints a minimum and maximum estimate of the instantaneous AQI reading at that time
    """
    data = import_and_sort(path_to_file)
    question_1(data)
    question_2(data)
    question_3(data)

def import_and_sort(path_to_file):
    """
    Function: 
    Imports a csv data file, sorts into a list with columns: "year, month, day, hour, AQI_PM2.5"
    with rows in chronological order 
        
    Input:
    Takes one string as an argument, containing the location of a csv data file

    Output:
    Returns a list with each element being a list of integers in the format: "year, month, day, hour, AQI_PM2.5" 
    with rows in chronological order 
    Prints a line stating the name of the file being analysed
    """
    import csv
    with open(path_to_file) as file:
        reader = csv.reader(file)
        next(reader) # Removing column headings line
        raw_data = [row for row in reader]

    data = []
    for row in raw_data:
        if row[17][1] == ':': # Check if the time has a one or two digit hour value and store in time variable
            time = row[17][0]
        else: 
            time = row[17][:2]
        if row[14] == '': # Replace empty readings with a reading of -1 so that all readings have integer values
            row[14] = -1
        
        # Create a row with the year, month, day, time and reading extracted from the row of raw_data 
        new_row = [int(row[2][6:10]), int(row[2][3:5]), int(row[2][0:2]), int(time), int(row[14])] 
        data.append(new_row)
    
    data.sort() # The format of the rows in data means this will sort cronologically
    print()
    print("Analysing data from " + path_to_file +":" + "\n")
    return data

def question_1(data):
    """
    Function: 
    For each year in the data file, the function prints a line stating the number of days with an 
    AQI_PM2.5 of 100 or above. 
    
    Input: 
    Takes a list with each element being a list of integers in the format: "year, month, day, hour, AQI_PM2.5"
    and rows in chronological order 
    
    Output: 
    Prints the first year and month data was taken
    For each year present, even if no data was taken, prints the number of days with an AQI_PM2.5 of 100 or above 
    """
   
    for row in data: # Determine and print the first instance of a non-empty data point
        if row[4] != -1:
            print("No AQI PM2.5 data was taken before " + str(row[1]) + "/" + str(row[0]))
            print()
            break
    
    year = data[0][0] # Define variabe for year initially as the first year in the data set
    month = 0 # Define variables for month and day as 0 initially so that the first entry will not be skipped
    day = 0
    
    count = 0
    for row in data: 
        if row[4] <100: #Ignore rows with AQI PM2.5 less than 100
            pass
        else:
            if row[0] == year: 
                if row[1] == month:
                    if row[2] == day: # Ignore if above 100 AQI PM2.5 already counted on this day
                        pass
                    else: # If reading is on a new day in the month increase the counter and update the current day and month
                        count += 1
                        day = row[2]
                        month = row[1]
                else: # If reading is on a day in a new month increase the counter and update the current day and month
                    count += 1 
                    day = row[2]
                    month = row[1]
            else: # If reading is in a new year print the counter from the previous year, update the year and reset day, month and counter
                print("In " + str(year) + " there were " + str(count) + " days recorded with AQI PM2.5 above 100")
                count = 0 
                year += 1 
                month = 0
                day = 0
    print("In " + str(year) + " there were " + str(count) + " days recorded with AQI PM2.5 above 100" +"\n") # Print counter for final year in data set         
    
def question_2(data):
    """
    Function: 
    For each month, prints the number of years and the years within which that 
    month had the highest number of days with AQI_PM2.5 greater than or equal to 33
    
    Input: 
    Takes a list with each element being a list of integers in the format: "year, month, day, hour, AQI_PM2.5"
    and rows in chronological order 
    
    Output: 
    For each month which was the worst for any year, prints the years and the number of years for which it was the worst
    """
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August','September', 'October', 'November', 'December', ]
    i=0

    years = [] 
    while data[0][0] + i <= data[-1][0]: #Defines a list containing a list for each year present. Each secondary list contains an integer for each month
        years.append([0,0,0,0,0,0,0,0,0,0,0,0])
        i += 1


    day = 0 
    month = 0 #Define initial conditions for following loop 
    for row in data: 
        if row[4] < 33: #Ignore rows with an AQI below 33 
            pass
        else: 
            if row[2] == day: 
                if row[1] != month: #If the current day is the same as the day of the most recently counted entry but the month has changed, update day and month values
                    month = row[1]
                    day = row[2] 
                    years[row[0] - data[0][0]][row[1] - 1] += 1 #Adds one to an integer in the appropriate indicies of the list 'years'
            else: 
                day = row[2]
                month = row[1]
                years[row[0] - data[0][0]][row[1] - 1] += 1

    for i, year in enumerate(years): 
        if max(year)==0: #no data taken
            x=[]
        else: 
            x = [i for i, j in enumerate(year) if j == max(year)]
        years[i] = x

    dictionary = {}

    for month in months: 
        dictionary[month] = []
        for i, year in enumerate(years):
            for month_ in year: 
                if month_ == months.index(month):
                    dictionary[month].append(data[0][0]+i)

    for month in months:
        x = dictionary.get(month)
        if x != []: 
            print(month + " was the worst or equal worst month in " + str(len(x)) + " year(s): "+ str(x)[1:-1])
    print()
    
    
    for i, year in enumerate(years):
        if len(year) == 0:
            print("No days with AQI PM2.5 below 'good' were recorded in " + str(data[0][0] + i))
        elif len(year) > 1: 
            statement = ''
            for x in year: 
                statement = statement + months[x] + ", "
            print("In " + str(data[0][0] + i) + " the months: " + str(statement) + "were the equal worst")
            
def question_3(data):
    """
    Function: 
    Prints the highest AQI_PM2.5 value(s) present in the given data set, and the date and time they were recorded
    Prints a minimum and maximum estimate of the instantaneous AQI reading at that time
    
    Input: 
    Takes a list with each element being a list of integers in the format: "year, month, day, hour, AQI_PM2.5"
    and rows in chronological order 
    
    Output: 
    Prints the highest AQI_PM2.5 value(s) present in the given data set, and the date and time they were recorded
    Prints a minimum and maximum estimate of the instantaneous AQI reading at that time
    """
    maximum = [[0,0]] #defines a list used to store the maximum AQI value(s) and its index(es)
    for i, row in enumerate(data): #searches the data for the highest AQI value and updates the content of the list maximum 
        if row[4] > maximum[0][0]:
            maximum = [[row[4],i]] 
        elif row[4] == maximum[0][0]:
            maximum.append([row[4],i])
                         
    if len(maximum) == 1: #Allows processing of multiple maxima 
        print("\nThe highest AQI PM2.5 in the data is " + str(maximum[0][0]) + " recorded on " + str(data[maximum[0][1]][2]) + "/" + str(data[maximum[0][1]][1]) + '/' + str(data[maximum[0][1]][0]) + " at " + str(data[maximum[0][1]][3]) +":00")   
    elif len(maximum) > 1: 
        print("\nThe equal highest AQI PM2.5 in the data is " + str(maximum[0][0]) + " recorded on", end = '')
        for entry in maximum: 
            print(' ' + str(data[entry[1]][2]) + '/' + str(data[entry[1]][1]) + '/' + str(data[entry[1]][0]) + " at " + str(data[entry[1]][3]) + ":00,", end = '')
              
    
    for entry in maximum:
        prev_time_window = data[entry[1]-25:entry[1]+1]  #defines a subset of the main data, and reverses it to simplifiy computation
        prev_time_window.reverse()
        
        i = 0
        for measurement in prev_time_window: 
            if i + 1 >= len(prev_time_window):
                break #Prevents index error
            if prev_time_window[i][4] == -1: #finds times at which no data was taken and approximates a reading through linear interpolation
                prev_time_window[i][4] = interpolate([prev_time_window[i+1][3],prev_time_window[i-1][3]],[prev_time_window[i+1][4],prev_time_window[i-1][4]],prev_time_window[i][3])    
                
            if prev_time_window[i][3]-prev_time_window[i+1][3] == 1 or prev_time_window[i][3] - prev_time_window[i+1][3] == -23: #Checks there are no missing measurements 
                pass 
            #In the case of missing data entry, the following elif statements run    
            elif prev_time_window[i][2] != prev_time_window[i+1][2]: #Checks if the day has changed, adds an entry with an approximated reading
                prev_time_window.insert(i+1, [prev_time_window[i+1][0],prev_time_window[i+1][1],prev_time_window[i+1][2],prev_time_window[i+1][3]+1, (prev_time_window[i][4]+prev_time_window[i+1][4])//2])
                if prev_time_window[i+1][3] == 24: #updates time into preferred format 
                    prev_time_window[i+1][3] = 0 
                    
            elif prev_time_window[i][3] - prev_time_window[i+1][3] != 1: #If the day has not changed, adds an entry with an approximated reading 
                prev_time_window.insert(i+1, [prev_time_window[i+1][0],prev_time_window[i+1][1],prev_time_window[i+1][2],prev_time_window[i+1][3]+1, (prev_time_window[i][4]+prev_time_window[i+1][4])//2])
            i += 1


        #Estimates minimum actual reading by finding a maximum value for the average of the prior 23 hours of readings. The minimum raises the maximum 23-hour average by the smallest amount to reach the measured 24-hour average 
        #The maximum average for the prior 23 hours is calculated by assuming the oldest actual reading is 0 
        est_min = 24*prev_time_window[0][4] - 23*prev_time_window[1][4]
    
        #Estimates maximum actual reading by finding a minimum value for the average of the prior 23 hours of readings. The maximum raises the minimum 23-hour average by the smallest amount to reach the measured 24-hour average
        #The minimum average for the prior 23 hours is caluclated by finding the minimum actual measurement of each reading in the 23-hour average via the method above
        min_prev_23hour_avg = 0 
        i = 24 
        while i > 0 :
            min_prev_23hour_avg +=(24*prev_time_window[i][4]-23*prev_time_window[i+1][4])//23
            i -= 1
        est_max = 23*min_prev_23hour_avg -24*prev_time_window[0][4] 
    
        print("Estimated instantaneous reading at " + str(data[entry[1]][2]) + '/' + str(data[entry[1]][1]) + '/' + str(data[entry[1]][0]) + " at " + str(data[entry[1]][3]) + ":00: \nmin = " +str(est_min)+", max = "+str(est_max)) 
         
def interpolate(x, y, x_test):
    '''    
    Function:
    Performs linnear interpolation to determine a y value at x_test given a series of
    corrasponding x and y values within which x_test is located
        
    Input: 
    This functions takes two sequences with purely numerical members,
    and a test point as arguments.
    The first sequence represents the x values of a function and should 
    be in increasing order with no repeated elements. 
    The second sequence represents the corresponding y values, such that 
    x[i] is correctly paired with y[i]. 
    Linear interpolation is performed at the test point. 
        
    Output: 
    The function outputs one float which is the linear interpolation 
    of the test point.
    If the test point is outside of the range of x_values, the function 
    will return none.
        
    Details: 
    The function first checks that x_test is in the range of x, then 
    whether x_test is a member of x. If x is a memeber of x, it returns 
    the corresponding member of y. 
    Then the function finds the largest member of x below, and the
    smallest value above x_test. It finds the corresponding y values, 
    and determines the equation of the line through these two points. 
    Then it finds the y value of x_test on this line. 
    '''
    range_x = max(x) - min(x)
    difference_below = range_x 
    for x_values in x:
        if x_values == x_test: 
             return y[x.index(x_test)]
        elif x_values < x_test and x_test - x_values <= difference_below:
            difference_below = x_test - x_values
            x_below = x_values
        elif x_values > x_test:
            x_above = x_values
            break

    y_below = y[x.index(x_below)]
    y_above = y[x.index(x_above)]
    
    gradient = (y_above - y_below)/(x_above - x_below)
    intercept = y_below - gradient*x_below
    y_test = x_test * gradient + intercept

    return y_test

if __name__ == '__main__':
    # test on data from the Civic monitoring station
    analyse('aqi_data_civic.csv')

    # test on data from the Florey monitoring station
    analyse('aqi_data_florey.csv')

    # test on data from the Monash monitoring station
    analyse('aqi_data_monash.csv')
    
