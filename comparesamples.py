from math import *
from statistics import mean
#!/usr/bin/env python
from argparse import ArgumentParser

def comparesamples(samples1, samples2, weights = 1, summary = 'd', analysis = 'x', threshold = 5):
    
    # User specifies an unrecognised analysis method or summary measure
    if summary != 'd' and summary != 'criticality':
        raise Exception('The defined summary does not exist')

    if analysis != 'x' and analysis != 'y':
        raise Exception('The defined analysis does not exist')

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
    # Default case for weights
    if weights == 1:
        w = 1
    # Otherwise recall the function
    else:
        w = data_read(weights)
    
    # Case of two locations with different number of samples or features - count the number of elements in data1 and data2
    count1 = 0
    count2 = 0
    for listElem1 in data1:
        count1 += len(listElem1)
    for listElem2 in data2:
        count2 += len(listElem2)
    if count1 != count2:
        raise Exception('The two locations have different number of samples or features')

    # Case of number of weights not matching the number of features
    number_of_features1 = count1/len(data1)
    number_of_features2 = count2/len(data2)

    if w != 1 and (len(w) != number_of_features1 or len(w) != number_of_features2):
        raise Exception('Number of weights not matching the number of features')

    
    results = []
    for sample in range(len(data1)):
        s = 0
        for feature in range(len(data1)):
            if isnan(data1[sample][feature]) or isnan(data2[sample][feature]):
                data1[sample][feature] = 0
                data2[sample][feature] = 0

            if analysis == 'x':
                    d = data1[sample][feature] - data2[sample][feature]

            if analysis == 'y':
                    d = (data1[sample][feature] - data2[sample][feature])**2

            if w == 1:
                s += w * abs(d)
            else:
                # Case of negative weights
                if w[0][feature] < 0:
                    raise ValueError('You cannot have negative weights')
                else:
                    s += w[0][feature] * abs(d)

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
