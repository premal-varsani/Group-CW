from math import *
import numpy as np
import yaml
from argparse import ArgumentParser


def load_file(path):

    if len(path) != 2:
        raise ValueError('Incorrect number of input files')

    res = []
    for p in path:
        with open(p) as file:
            lines = file.readlines()
            data = []
            for line in lines:
                row = []
                for n in line.split(','):
                    row.append(float(n.strip()))
                data.append(row)
        res.append(data)

    if len(np.asarray(res)[0]) != len(np.asarray(res)[1]):
        raise ValueError('The two locations have different sample numbers')
    if len(np.asarray(res)[0][0]) != len(np.asarray(res)[1][1]):
        raise ValueError('The two locations have different sample features')
 
    return np.asarray(res)

def load_weight(path):
    with open(path) as filew:
        linew = filew.read()
        w = []
        for n in linew.split(','):
            w.append(float(n.strip()))
    return w

def analyse(input_data, weight_data, analysis = 'x', summary = 'd', cri = '5'):
    
    if len(weight_data) != input_data.shape[2]:
        raise ValueError('The weight input doesnt match feature length')
    if not all(i >= 0 for i in weight_data):
        raise ValueError('One of the weights is negative')
    if len(input_data) != 2:
        raise ValueError('Incorrect number of input files')

    if analysis == "x":
        d = analysis_x(input_data, weight_data)

    elif analysis == "y":
        d = analysis_y(input_data, weight_data)

    
    if summary == 'criticality':
        res = summary_cri(input_data=d, cri=cri)

    elif summary == 'd':
        res = summary_d(input_data=d)

    return res

def analysis_x(input_data, weight_data):

    if len(weight_data) != input_data.shape[2]:
        raise ValueError('The weight input doesnt match feature length')
    if not all(i >= 0 for i in weight_data):
        raise ValueError('One of the weights is negative')
    if len(input_data) != 2:
        raise ValueError('Incorrect number of input files')

    res = weight_data * np.abs(input_data[0] - input_data[1])
    res = np.nansum(res, axis=1)
    return res

def analysis_y(input_data, weight_data):


    if len(weight_data) != input_data.shape[2]:
        raise ValueError('The weight input doesnt match feature length')
    if not all(i >= 0 for i in weight_data):
        raise ValueError('One of the weights is negative')
    if len(input_data) != 2:
        raise ValueError('Incorrect number of input files')
    if len(input_data[0]) != len(input_data[1]):
        raise ValueError('The two locations have ahve different sample numbers')   

    res = weight_data * (input_data[0] - input_data[1])**2
    res = np.nansum(res, axis=1)
    res = np.sqrt(res)
    return res

def summary_cri(input_data, cri):
    res = np.sum(input_data > cri)
    print("criticality:", res, "results above", cri)
    return res

def summary_d(input_data):
    res = np.average(input_data)
    print("d-index:", res)
    return  res

def YAML_Read(path):
    with open(path) as yaml_file:
        my_data = yaml.safe_load(yaml_file)
    #print(my_data)
    return my_data

def process():

    parser = ArgumentParser(description="comparesamples <sample file 1> <sample file 2> \
        [--summary <measure>] \
        [--analysis <algorithm>] [--weights <weights file>]")
    parser.add_argument('--analysis', help="analysis input should be x or y", type=str)
    parser.add_argument('--summary', help="summary input should be either d or criticality", type=str)
    parser.add_argument('--weights', help="file path of weights", type=str)
    parser.add_argument('--criticality', help = "critical cut off", type = int)
    parser.add_argument('--config', help = 'YAML file input')
    parser.add_argument('--file1', help="file path of data1")
    parser.add_argument('--file2', help="file path of data2")
    arguments= parser.parse_args()
    
    if arguments.analysis != None:
        analysis = arguments.analysis
    else:
        analysis = 'x'

    if arguments.summary !=None:
        summary = arguments.summary
    else: 
        summary = 'd'
        
    if arguments.criticality != None:
        cri = arguments.criticality
    else:
        cri = 5

    if arguments.config != None:
        #print(arguments.config)
        YAML = YAML_Read(arguments.config)
        #print(YAML)
        for i in YAML.keys():
            analyse(load_file([YAML[i]['samples'][0], YAML[i]['samples'][1]]),load_weight(YAML[i]['weights']), YAML[i]['algorithm'],YAML[i]['summary'],cri)
    else:
        load_file([arguments.file1, arguments.file2])
        load_weight(arguments.weights)
        analyse(load_file([arguments.file1, arguments.file2]),load_weight(arguments.weights), analysis,summary,cri)



    #print([arguments.file1, arguments.file2])
    #message = analyse(input_data=[arguments.file1, arguments.file2], weight_data=arguments.weights,
                    #analysis=arguments.analysis, summary=arguments.summary)
    #print(message)

if __name__ == "__main__":
    process()

