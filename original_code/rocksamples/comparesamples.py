from math import *
import numpy as np
import yaml
from argparse import ArgumentParser

# t test
def load_file(path):
    """ 
    Open .csv files holding samples' data and put them into two arrays.

    Parameters
    ----------
    path: list of strings
         Files location, such as new_samples/file1.csv or /Users/home/sam/backup/samples/file2.csv
    
    Returns
    -------
    res: list of arrays
         An appropriate of list of N-by-M arrays, where N is the number of samples and M is the number of features

    Raises
    ------
    ValueError
         If the arrays have different number of rows

    ValueError
         If the arrays have different number of columns
    """
    if len(path) != 2:
        raise ValueError('The input path should be file1_path, file2_path')
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
    """ 
    Open .csv file holding weights of different features and put them into an array.

    Parameters
    ----------
    path: str
         File location, such as new_samples/my_weights.csv
    
    Returns
    -------
    w: array
         An appropriate 1-by-M array, where M is the number of features
    """
    with open(path) as filew:
        linew = filew.read()
        w = []
        for n in linew.split(','):
            w.append(float(n.strip()))
    return np.asarray(w)

def analyse(input_data, weight_data, analysis = 'x', summary = 'd', cri = 5):
    """ 
    Generate d-index or criticality according to the chosen analysis method, Algorithm X or Y.

    Parameters
    ----------
    input_data: list of arrays
         An appropriate of list of N-by-M arrays, where N is the number of samples and M is the number of features
         
    weight_data: array
         An appropriate 1-by-M array, where M is the number of features

    analysis: str, optional
         Chosen analysis method, 'x' stands for Algorithm X and 'y' stands for Algorithm Y

    summary: str, optional
         The quantity to be computed, 'd' stands for d-index 'criticality' stands for criticality

    cri: int or float, optional
         Chosen threshold value for criticality

    Returns
    -------
    res: int or float
         Chosen quantity computed according to the chosen Algorithm
    """
    check_input(input_data, weight_data, analysis, summary, cri)

    if analysis == "x":
        d = analysis_x(input_data, weight_data)

    elif analysis == "y":
        d = analysis_y(input_data, weight_data)

    
    if summary == 'criticality':
        res = summary_cri(input_data=d, cri=cri)

    elif summary == 'd':
        res = summary_d(input_data=d)

    return res

def check_input(input_data=[], weight_data=[], analysis=[], summary=[], cri=[]):
    """ 
    Check if all the input files (samples' and weights) and the other parameters(cri, analysis and summary)
     are valid and raise appropriate errors if they are not.

    Parameters
    ----------
    input_data: list of arrays
         An appropriate of list of N-by-M arrays, where N is the number of samples and M is the number of features
         
    weight_data: array
         An appropriate 1-by-M array, where M is the number of features

    analysis: str, optional
         Chosen analysis method, 'x' stands for Algorithm X and 'y' stands for Algorithm Y

    summary: str, optional
         The quantity to be computed, 'd' stands for d-index 'criticality' stands for criticality

    cri: int or float, optional
         Chosen threshold value for criticality

    Returns
    -------
    logical: boolean
         True if the input files are all valid

    Raises
    ------
    ValueError
         If the input files (samples' files) are not 2
    
    ValueError
         If a weight value is negative
    
    ValueError
         If the number of weights does not match the number of features of the samples
    
    ValueError
         If weights' data are not int or float

    ValueError
         If the threshold value is not an int or a float
    
    ValueError
         If the specified analysis is different from 'x' and 'y'
    
    ValueError
         If the specified summary is different from 'd' and 'criticality' 
    """
    if len(input_data) != 2:
        raise ValueError('Incorrect number of input files')

    if isinstance(weight_data, int) or isinstance(weight_data, float):
        if weight_data < 0:
            raise ValueError('weights should be all positive')
    elif isinstance(weight_data, np.ndarray):
        if not all(i >= 0 for i in weight_data):
            raise ValueError('weights should be all positive')
        if len(weight_data) != input_data.shape[2]:
            raise ValueError('weight input doesnt match feature length')
    else:
        raise ValueError('Weights should be either an int(float) or list of int(float)')
    

    if isinstance(cri, int) or isinstance(cri, float):
        pass
    else:
        raise ValueError('cri option should be either int or float number')
    
    if analysis != 'x' and analysis != 'y':
        raise ValueError('analysis option should either be x or y')

    if summary != 'd' and summary != 'criticality':
        raise ValueError('summary option should either be d or criticality')

    logical = True

    return logical

def analysis_x(input_data, weight_data):
    """ 
    Compute the vector of sample differences. For two samples with features s1, s2,...sM and s'1, s'2,...s'M , with
    weight of feature i equal to wi, the sample difference is computed and this is repeated for every pair of samples.

    Parameters
    ----------
    input_data: list of arrays
         An appropriate of list of N-by-M arrays, where N is the number of samples and M is the number of features
         
    weight_data: array
         An appropriate 1-by-M array, where M is the number of features

    Returns
    -------
    res: array
         Array of differences for every pair of samples
    """
    res = weight_data * np.abs(input_data[0] - input_data[1])
    res = np.nansum(res, axis=1)
    return res

def analysis_y(input_data, weight_data):
    """ 
    Compute the vector of sample discrepancies. For two samples with features s1, s2,...sM and s'1, s'2,...s'M , with
    weight of feature i equal to wi, the sample discrepancy is computed and this is repeated for every pair of samples.

    Parameters
    ----------
    input_data: list of arrays
         An appropriate of list of N-by-M arrays, where N is the number of samples and M is the number of features
         
    weight_data: array
         An appropriate 1-by-M array, where M is the number of features

    Returns
    -------
    res: array
         Array of discrepancies for every pair of samples
    """
    res = weight_data * (input_data[0] - input_data[1])**2
    res = np.nansum(res, axis=1)
    res = np.sqrt(res)
    return res

def summary_cri(input_data, cri):
    """ 
    Compute the number of elements in a vector exceeding a chosen threshold value.

    Parameters
    ----------
    input_data: array 
         Array containing elements that we want to compare with a chosen threshold value
         
    cri: int or float
         Chosen threshold value
         
    Returns
    -------
    res: int
         Number of elements in the array exceeding the chosen threshold value
    """
    res = np.sum(input_data > cri)
    print("criticality:", res, "results above", cri)
    return res

def summary_d(input_data):
    """ 
    Compute the average of a vector.

    Parameters
    ----------
    input_data: array
             An array of which we want to compute the average
         
    Returns
    -------
    res: int or float
         Average of the elements in the array, computed as sum of all elements divided by
         the total number of elements
    """
    res = np.average(input_data)
    print("d-index:", res)
    return  res

def YAML_Read(path):
    """ 
    Read a YAML file and convert it into a dictionary.

    Parameters
    ----------
    path: str
         The location of the YAML file
         
    Returns
    -------
    my_data: dict
         An appropriate dictionary containing all the info stored in the YAML file,
         precisely for each workflow the chosen algorithm, summary and the location
         of samples and weights files are specified
    """
    with open(path) as yaml_file:
        my_data = yaml.safe_load(yaml_file)
    return my_data

def process():
    """ 
    Function called when inputs are given from the command-line interface
    """
    parser = ArgumentParser(description="comparesamples <sample file 1> <sample file 2> \
        [--summary <measure>] \
        [--analysis <algorithm>] [--weights <weights file>]")
    parser.add_argument('--analysis', help="analysis input should be x or y", type=str)
    parser.add_argument('--summary', help="summary input should be either d or criticality", type=str)
    parser.add_argument('--weights', help="file path of weights", type=str)
    parser.add_argument('--criticality', help = "critical cut off", type = int)
    parser.add_argument('--config', help = 'YAML file input')
    parser.add_argument('file1', help="file path of data1")
    parser.add_argument('file2', help="file path of data2")
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

if __name__ == "__main__":
    """ 
    Command-line interface
    """
    process()

