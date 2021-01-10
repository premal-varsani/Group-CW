
import timeit
from timeit import repeat
from matplotlib import pyplot as plt
import numpy as np
from comparesamples import analysis_x, analysis_y, summary_cri, summary_d

# Only have done analysis_x and d, needs more modification to include rest.


def generate_random_inputs(a,b):
    random_array = np.random.rand(a,b)
    return random_array

def random_array(feature):
    for i in range(2,feature):
        a = generate_random_inputs(i,10)
        b = generate_random_inputs(i,10)
        c = generate_random_inputs(i,1)
        input_data = [[a],[b]]


    input_data = np.array(input_data)
    return input_data,c

def speed(feature):
    input_data,c = random_array(feature)
    d = analysis_x(input_data,c)
    
    res = summary_d(input_data=d)

    return res


# compute linear search time 
def linear_time(): 
    SETUP_CODE = ''' 

    
from __main__ import analysis_x 
from __main__ import summary_d 
from __main__ import speed
from __main__ import feature
'''
      
    TEST_CODE = ''' 
    
speed(feature)
    '''
  
    time = timeit.repeat(stmt=TEST_CODE, setup=SETUP_CODE, repeat=, number = 1)
    return time


    
if __name__ == "__main__": 

    features = []
    times = []
    for i in range(3,300):

        feature = i
        time = linear_time() 
        features.append(feature)
        times.append(time)

    plt.plot(features, times)
    plt.ylim(bottom=0) 
    plt.ylabel('seconds')
    plt.xlabel('array size')
    plt.show()
    
