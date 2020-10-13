def import_and_sort(path_to_file):
    import csv
    with open(path_to_file) as file:
        reader = csv.reader(file)
        next(reader)
        raw_data = [row for row in reader]

    data = []

    for row in raw_data:
        if row[17][1] == ':':
            time = row[17][0]
        else: 
            time = row[17][:2]
        if row[14] == '':
            row[14] = 0 
        new_row = [int(row[2][6:10]), int(row[2][3:5]), int(row[2][0:2]), int(time), int(row[14])]
        data.append(new_row)
    data.sort() 
    return data

def question_1(data):
    
    year = data[0][0]
    month = 0
    day = 0
    count = 0
   
    for row in data: 
        if row[4] <100:
            pass
        else:
            if row[0] == year:
                if row[1] == month:
                    if row[2] == day:
                        pass
                    else:
                        count += 1
                        day = row[2]
                        month = row[1]
                else:
                    count +=1 
                    day = row[2]
                    month = row[1]
            else:
                print("In " + str(year) + " there were " + str(count) + " days with AQI PM2.5 above 100")
                count = 0 
                year += 1 
                month = 0
                day=0
    print("In " + str(year) + " there were " + str(count) + " days with AQI PM2.5 above 100")             
    print( )
    
def question_2(data):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August','September', 'October', 'November', 'December', ]
    yearly_count=  []
    first_year = data[0][0]
    day = 0 
    month = 0 

    while first_year <= data[-1][0]:
        yearly_count.append([0,0,0,0,0,0,0,0,0,0,0,0])
        first_year +=1

    for row in data: 
        if row[4] < 33:
            pass
        else: 
            index_0 = row[0] - data[0][0]
            index_1 = row[1] - 1 
            if row[2] == day:
                if row[1] != month:
                    month = row[1]
                    day = row[2]
                    yearly_count[index_0][index_1] += 1
            else: 
                day = row[2]
                month = row[1]
                yearly_count[index_0][index_1] += 1

    k=0
    for year in yearly_count: 
        x = [i for i, j in enumerate(year) if j == max(year)]
        if len(x) == 12: #If all months had same count i.e. no data taken
            x = []
        yearly_count[k] = x    
        k+=1

    final_countdown = {}

    for month in months: 
        final_countdown[month] = []
        for i, year in enumerate(yearly_count):
            for mon in year: 
                if mon == months.index(month):
                    final_countdown[month].append(data[0][0]+i)

    for month in months:
        x = final_countdown.get(month)
        if x != []: 
            print(month + " was the worst or equal worst month in " + str(len(x)) + " year(s): "+ str(x)[1:-1])
    print( )
    
    i = 0 
    for year in yearly_count: 
        if len(year) == 0: 
            print("No AQI PM2.5 data was taken in " + str(data[0][0] + i))
        elif len(year) > 1: 
            statement = ''
            for x in year: 
                statement = statement + months[x] + ", "
            print("In " + str(data[0][0] + i) + " the months: " + str(statement) + " were the equal worst")
        i+=1
        
def analyse(path_to_file):
    data = import_and_sort(path_to_file)
    question_1(data)
    question_2(data)
    
analyse("aqi_data_florey.csv")
