import pytest
import numpy as np
from pathlib import Path

from comparesamples import (load_file,
                            load_weight,
                            analyse,
                            check_input
                            )


def test_check_input():
    file_path = ["test/default_positive_1.csv", "test/default_positive_2.csv"]
    input_data= load_file(file_path)
    weight_data=1
    analysis='x'
    summary='d'
    cri=5
    
    # positive case 1 for default parameters
    assert check_input(input_data=input_data, weight_data=weight_data, \
         analysis=analysis, summary=summary, cri=cri) == True

    # negative case 1 load file
    with pytest.raises(ValueError, match='The input path should be file1_path, file2_path'):
        load_file(['test/default_positive_1.csv'])

    # negative case 2 load file
    with pytest.raises(ValueError, match='The two locations have different sample numbers'):
        input_data_temp = load_file(['test/test_negative_input_data1.csv', 'test/default_positive_2.csv'])

    # negative case 3 load file
    with pytest.raises(ValueError, match='The two locations have different sample features'):
        input_data_temp = load_file(['test/test_negative_input_data2.csv', 'test/default_positive_2.csv'])

    # negative case 1 input_data
    input_data_temp = [[1]]
    with pytest.raises(ValueError, match='Incorrect number of input files'):
        check_input(input_data=input_data_temp, weight_data=weight_data, \
         analysis=analysis, summary=summary, cri=cri)


    # positive case 1 weight_data list
    weight_data_temp = np.ones([len(input_data[0]),1])
    assert check_input(input_data=input_data, weight_data=weight_data_temp, \
         analysis=analysis, summary=summary, cri=cri) == True

    # negative case 1 weight_data int negative
    weight_data_temp = - 1
    with pytest.raises(ValueError, match='weights should be all positive'):
        check_input(input_data=input_data, weight_data=weight_data_temp, \
         analysis=analysis, summary=summary, cri=cri)

    # negative case 2 weight_data list
    weight_data_temp = - np.ones([len(input_data[0]),1])
    with pytest.raises(ValueError, match='weights should be all positive'):
        check_input(input_data=input_data, weight_data=weight_data_temp, \
         analysis=analysis, summary=summary, cri=cri)

    # negative case 1 analysis = None
    analysis_temp = None
    with pytest.raises(ValueError, match='analysis option should either be x or y'):
        check_input(input_data=input_data, weight_data=weight_data, \
         analysis=analysis_temp, summary=summary, cri=cri)

    # negative case 2 analysis != 'x' or 'y'
    analysis_temp = 'z'
    with pytest.raises(ValueError, match='analysis option should either be x or y'):
        check_input(input_data=input_data, weight_data=weight_data, \
         analysis=analysis_temp, summary=summary, cri=cri)

    # negative case 1 summary = None
    summary_temp = None
    with pytest.raises(ValueError, match='summary option should either be d or criticality'):
        check_input(input_data=input_data, weight_data=weight_data, \
         analysis=analysis, summary=summary_temp, cri=cri)

    # negative case 2 summary = "z"
    summary_temp = "z"
    with pytest.raises(ValueError, match='summary option should either be d or criticality'):
        check_input(input_data=input_data, weight_data=weight_data, \
         analysis=analysis, summary=summary_temp, cri=cri)


    # negative case 1 cri = None
    cri_temp = None
    with pytest.raises(ValueError, match='cri option should be either int or float number'):
        check_input(input_data=input_data, weight_data=weight_data, \
         analysis=analysis, summary=summary, cri=cri_temp)

    # negative case 2 cri = -1
    cri_temp = "z"
    with pytest.raises(ValueError, match='cri option should be either int or float number'):
        check_input(input_data=input_data, weight_data=weight_data, \
         analysis=analysis, summary=summary, cri=cri_temp)


