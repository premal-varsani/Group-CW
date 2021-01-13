import pytest
import numpy as np
from pathlib import Path
from comparesamples import (load_file,
                            load_weight,
                            analyse,
                            check_input
                            ) #importing all the necessary functions to carry out the tests

def test_check_input():
    """
    A function that runs the tests.

    Raises
    ------
    ValueError
         If the input of the file paths are incorrect
    
    ValueError
         If the input of the file paths contain different sample numbers
    
    ValueError
         If the input of the file paths contain a different number of features
    
    ValueError
         If the user inputs an invalid number of sample files
    
    ValueError
         If the weights are negative integers
    
    ValueError
         If the array for weights contains negative integers
    
    ValueError
         If no analysis method is chosen
    
    ValueError
         If the analysis method chosen by the user is different from `x` or `y`
    
    ValueError
         If no summary measure is chosen
    
    ValueError
         If the summary measure is different from `d` or `criticality`
    
    ValueError
         If no criticality is chosen
    
    ValueError
         If the criticality is not a number or float
    """
    file_path = ["test/default_positive_1.csv", "test/default_positive_2.csv"]
    input_data= load_file(file_path) #using the function from comparesamples.py which reads the .csv files to use here
    weight_data=1 #initialising the weight
    analysis='x' #initialising which algorithm is used
    summary='d' #initialising the d-index calculation
    cri=5 #initialising the criticality
    
    #testing the default parameters
    assert check_input(input_data=input_data, weight_data=weight_data, \
         analysis=analysis, summary=summary, cri=cri) == True #test will pass

    #handling an error when the inputs of the file paths are incorrect
    with pytest.raises(ValueError, match='The input path should be file1_path, file2_path'):
        load_file(['test/default_positive_1.csv'])

    #handling an error where the user inputs two file paths with different sample numbers
    with pytest.raises(ValueError, match='The two locations have different sample numbers'):
        input_data_temp = load_file(['test/test_negative_input_data1.csv', 'test/default_positive_2.csv'])

    #handling an error for when the user tries to compare two file locations with a different number of features
    with pytest.raises(ValueError, match='The two locations have different sample features'):
        input_data_temp = load_file(['test/test_negative_input_data2.csv', 'test/default_positive_2.csv'])

    #handling an error for when the user inputs an invalid number of sample files
    input_data_temp = [[1]]
    with pytest.raises(ValueError, match='Incorrect number of input files'):
        check_input(input_data=input_data_temp, weight_data=weight_data, \
         analysis=analysis, summary=summary, cri=cri)

    #testing the weights
    weight_data_temp = np.ones([len(input_data[0]),1])
    assert check_input(input_data=input_data, weight_data=weight_data_temp, \
         analysis=analysis, summary=summary, cri=cri) == True #all weights are positive so this test will pass

    #handling an error for when a weight is negative
    weight_data_temp = - 1 #negative weight, test will fail
    with pytest.raises(ValueError, match='weights should be all positive'):
        check_input(input_data=input_data, weight_data=weight_data_temp, \
         analysis=analysis, summary=summary, cri=cri)

    #handling another case of negative weights
    weight_data_temp = - np.ones([len(input_data[0]),1]) #negative weights, test will fail
    with pytest.raises(ValueError, match='weights should be all positive'):
        check_input(input_data=input_data, weight_data=weight_data_temp, \
         analysis=analysis, summary=summary, cri=cri)

    #handling an error for when an invalid analysis method is chosen
    analysis_temp = None #no analysis method is chosen, test will fail
    with pytest.raises(ValueError, match='analysis option should either be x or y'):
        check_input(input_data=input_data, weight_data=weight_data, \
         analysis=analysis_temp, summary=summary, cri=cri)

    #handling another case for an invalid analysis method
    analysis_temp = 'z' #the analysis is not either x or y, test will fail
    with pytest.raises(ValueError, match='analysis option should either be x or y'):
        check_input(input_data=input_data, weight_data=weight_data, \
         analysis=analysis_temp, summary=summary, cri=cri)

    #handling an error for when the user does not specify the summary measure
    summary_temp = None #no summary is chosen, test will fail
    with pytest.raises(ValueError, match='summary option should either be d or criticality'):
        check_input(input_data=input_data, weight_data=weight_data, \
         analysis=analysis, summary=summary_temp, cri=cri)

    #handling an error for when the user does not input a valid summary measure
    summary_temp = "z" #the summary measure is not either d or criticality, test will fail
    with pytest.raises(ValueError, match='summary option should either be d or criticality'):
        check_input(input_data=input_data, weight_data=weight_data, \
         analysis=analysis, summary=summary_temp, cri=cri)

    #handling an error for when the user does not specify the criticality
    cri_temp = None #criticality is not specified, test will fail
    with pytest.raises(ValueError, match='cri option should be either int or float number'):
        check_input(input_data=input_data, weight_data=weight_data, \
         analysis=analysis, summary=summary, cri=cri_temp)

    #handling another error for criticality which is caused by the user inputting an invalid format
    cri_temp = "z" #the criticality is not a number, test will fail
    with pytest.raises(ValueError, match='cri option should be either int or float number'):
        check_input(input_data=input_data, weight_data=weight_data, \
         analysis=analysis, summary=summary, cri=cri_temp)


