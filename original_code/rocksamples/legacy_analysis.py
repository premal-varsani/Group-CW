import pytest
import numpy as np

#from comparesamples import comparesamples



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



def test_correct_data_input_no():
    with pytest.raises(ValueError) as e:
        load_file(['data1.csv'])
        assert e.match('Incorrect number of input files')

def test_correct_sample_input():
    with pytest.raises(ValueError) as e:
        load_file(['testdata1.csv', 'data2.csv'])
        assert e.match('The two locations have different sample numbers')

def test_correct_feature_input():
    with pytest.raises(ValueError) as e:
        load_file(['testdata2.csv', 'data2.csv'])
        assert e.match('The two locations have different sample features')

def test_correct_analysis_x():
    a = analyse(load_file(['data1.csv', 'data2.csv']),load_weight('weights.csv'), 'x' , 'd' ,5)
    assert a == 4.7
 
'''
def test_correct_input_form():
    #tests for correct schema 
    with pytest.raises(ValueError) as e:
        load_file(['testdata1.csv', 'data2.csv'])
        assert e.match('The two locations have different feature or sample numbers')
'''
