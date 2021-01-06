from math import *
from statistics import mean
#!/usr/bin/env python
from argparse import ArgumentParser

def comparesamples(samples1, samples2, weights = 1, summary = 'd', analysis = 'x', threshold = 5):
    
    # Function reading the .csv files (samples and weights data) and prepare data for the analyses
    def data_read (file):
        with open (file) as file:
            lines = file.readlines()
            data_storage_name =[]
            for line in lines:
                row = []
                for string in line.split(','):
                    row.append(float(string.strip()))
                data_storage_name.append(row)
        return data_storage_name
    
    # Recall the function
    data1 = data_read(samples1)
    data2 = data_read(samples2)
    if weights == 1:
        w = 1
    else:
        w = data_read(weights)
    
    results = []
    for value in range(len(data1)):
        s = 0
        for element in range(len(data1)):
            if isnan(data1[value][element]) or isnan(data2[value][element]):
                data1[value][element] = 0
                data2[value][element] = 0

                if analysis == 'x':
                    d = data1[value][element] - data2[value][element]

                if analysis == 'y':
                    d = (data1[value][element] - data2[value][element])**2

                if w == 1:
                    s += w * abs(d)
                else:
                    s += w[0][element] * abs(d)

        if analysis == 'x':          
            results.append(s)
        if analysis == 'y':
            discr = sqrt(s)
            results.append(round(discr,2))
                
# Criticality - number of elements in the sample difference vector exceeding a threshold value 
    critical = 0
    for result in results:
        if result > threshold:
            critical += 1
    
    # d-index - average of sample difference vector across sample pairs
    d_index = mean(results)
    
    if summary == 'criticality':
        return(print("criticality:", critical, "results above", threshold))
    if summary == 'd':
        return(print("d-index:", d_index))

# Command-line interface
if __name__ == "__main__":
    parser = ArgumentParser(description="Compute criticality and d-index of samples of two different locations")
    parser.add_argument('--summary', '-s', help = 'Desired output: criticality or d-index', default='d')
    parser.add_argument('--analysis','-a', help = 'Chosen Algorithm (X o Y)',default='x')
    parser.add_argument('--threshold','-t', help = 'Chosen threshold for criticality calculation', default = 5)
    parser.add_argument('--weights', '-w', help = 'Weights of the different properties', default = 1)
    parser.add_argument('samples1', help = 'Data related to the samples of the first location', default = 'samples1.csv')
    parser.add_argument('samples2', help = 'Data related to the samples of the second location', default = 'samples2.csv')
    arguments= parser.parse_args()
    
    final = comparesamples(arguments.samples1, arguments.samples2, 
      arguments.weights, arguments.summary, arguments.analysis, arguments.threshold)
    
    print(final)