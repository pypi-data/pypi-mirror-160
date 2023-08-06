import sys
import numpy as np 
import matplotlib.pyplot as plt
import json

def Graph(filePath, shifted, displayAllYears):

    # Opening JSON file
    with open(filePath) as json_file:
        data = json.load(json_file)
    
    fileName = data[0]['subjectCourse']

    offering = {}
    Spring = []
    Summer = []
    Fall = []
    SpringMax = []
    SummerMax = []
    FallMax = []

    year = ['2007', '2008', '2009', '2010', 
            '2011', '2012', '2013', 
            '2014', '2015', '2016', 
            '2017', '2018', '2019', 
            '2020', '2021', '2022']

    # Display all years
    for yr in year:
        offering[yr] = {'summer': [0,0], 'fall': [0,0], 'spring': [0,0]}

    for term in data:
        # Spring
        if term['term'][-2:] == '01':
            if shifted:
                # adjusting spring offering back to correct year
                adjustedYear = str(int(term['term'][0:4]) - 1)
                offering[adjustedYear]['spring'][0] += term['enrollment']
                offering[adjustedYear]['spring'][1] += (term['maximumEnrollment'] - term['enrollment'])
            else:
                offering[term['term'][0:4]]['spring'][0] += term['enrollment']
                offering[term['term'][0:4]]['spring'][1] += (term['maximumEnrollment'] - term['enrollment'])

        # Summer
        if term['term'][-2:] == '05':
            if shifted:
                # adjusting spring offering back to correct year
                adjustedYear = str(int(term['term'][0:4]) - 1)
                offering[adjustedYear]['summer'][0] += term['enrollment']
                offering[adjustedYear]['summer'][1] += (term['maximumEnrollment'] - term['enrollment'])
            else:
                offering[term['term'][0:4]]['summer'][0] += term['enrollment']
                offering[term['term'][0:4]]['summer'][1] += (term['maximumEnrollment'] - term['enrollment'])

        # Fall
        if term['term'][-2:] == '09':
            offering[term['term'][0:4]]['fall'][0] += term['enrollment']
            offering[term['term'][0:4]]['fall'][1] += (term['maximumEnrollment'] - term['enrollment'])
    
    for item in offering:
        if displayAllYears:
            Summer.append(offering[item]['summer'][0])
            Fall.append(offering[item]['fall'][0])
            Spring.append(offering[item]['spring'][0])

            SummerMax.append(offering[item]['summer'][1])
            FallMax.append(offering[item]['fall'][1])
            SpringMax.append(offering[item]['spring'][1])
        else:
            if(offering[item]['summer'][0] == 0 and offering[item]['fall'][0] == 0 and offering[item]['spring'][0] == 0):
                year.remove(item)
            else:
                Summer.append(offering[item]['summer'][0])
                Fall.append(offering[item]['fall'][0])
                Spring.append(offering[item]['spring'][0])

                SummerMax.append(offering[item]['summer'][1])
                FallMax.append(offering[item]['fall'][1])
                SpringMax.append(offering[item]['spring'][1])
    

    # Graph stuff
    x_axis = np.arange(len(year))

    # Multi bar Chart
    plt.bar(x_axis +0.20, Summer, width = 0.2, label = 'Summer')
    plt.bar(x_axis +0.20, SummerMax, width = 0.2, bottom = Summer, color = '0.75')

    plt.bar(x_axis +0.20 * 2, Fall, width = 0.2, label = 'Fall')
    plt.bar(x_axis +0.20 * 2, FallMax, width = 0.2, bottom = Fall, color = '0.50')

    plt.bar(x_axis +0.20 * 3, Spring, width = 0.2, label = 'Spring')
    plt.bar(x_axis +0.20 * 3, SpringMax, width = 0.2, bottom = Spring, color = '0.75')


    # Xticks
    plt.xticks(x_axis, year)
    
    # Labels
    plt.xlabel("Year")
    plt.ylabel("# Students Enrolled")
    plt.title(fileName)

    plt.legend()
    plt.plot()
    plt.xticks(rotation = 90)
    plt.savefig('images/' + str(fileName + "_bar"))
    # plt.show()
    plt.clf()
    plt.close()

def main():
    shifted = False
    displayAllYears = False

    for arg in sys.argv:
        if arg == '-s':
            shifted = True
        if arg == '-f':
            displayAllYears = True
    
    print("Graphing " + sys.argv[1])
    Graph(sys.argv[1], shifted, displayAllYears)