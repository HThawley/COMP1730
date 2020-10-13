"""
Template for the COMP1730/6730 project assignment, S2 2020.
The assignment specification is available on the course web site:
https://cs.anu.edu.au/courses/comp1730/assessment/project/

The assignment is due 25/10/2020 at 11.55 pm, Canberra time.

Collaborators: u6942813, u(HARRY), u(PANDA)
"""

def analyse(path_to_file):
    ''' plz add a docstring
    ''' 
    
    # Import data from csv file
    import csv

    with open(path_to_file) as file:
        reader = csv.reader(file)
        next(reader)
        raw_data = [row for row in reader]

    # Reduce the raw data rows down to the format: [year, month, day, time, AQI_PM2.5]
    # This enables chronological sorting with the .sort() method
    data = []
    for row in raw_data:
        new_row = [row[2][6:10], row[2][3:5], row[2][0:2], row[17], row[14]]
        data.append(new_row)

    data.sort()
    
    #Print answers to questions
    Question_1(data)



def Question_1(data):
    ''' plz add a docstring
    '''

    year = int(data[0][0])
    month = 0
    day = 0
    count = 0

    for row in data: 
        if row[4] == '' or int(row[4]) <100:
            pass
        else:
            if int(row[0]) == year:
                if int(row[1]) == month:
                    if int(row[2]) == day:
                        pass
                    else:
                        count += 1
                        day = int(row[2])
                        month = int(row[1])
                else:
                    count +=1 
                    day = int(row[2])
                    month = int(row[1])
            else:
                print("In " + str(year) + " there were " + str(count) + " days with PM2.5 above 100")
                count = 0 
                day = 0
                month = 0
                year += 1
    print("In " + str(year) + " there were " + str(count) + " days with PM2.5 above 100")

