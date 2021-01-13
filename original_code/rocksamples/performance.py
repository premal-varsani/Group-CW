import timeit
from timeit import repeat
from matplotlib import pyplot as plt
import numpy as np
from comparesamples import analysis_x, analysis_y, summary_cri, summary_d

def generate_random_inputs(a, b):
    """
    This function is used to create random values in a given shape (a, b)
    """
    random_array = np.random.rand(a, b)
    return random_array

def random_array(feature):
    """
    This function uses the generate_random_inputs function to return an array of random numbers
    """
    for i in range(2, feature):
        """
        The a and b variables generate 10 random features
        """
        a = generate_random_inputs(i, 10)
        b = generate_random_inputs(i, 10)
        c = generate_random_inputs(i, 1) #generating the weights used in the analysis algorithm
        input_data = [[a], [b]]
    
    input_data = np.array(input_data)
    return input_data, c #returns the array of random numbers, as well as the generated weights

def speed(feature):
    """
    This function runs the algorithm needed to compute the d-index
    """
    input_data, c = random_array(feature)
    d = analysis_x(input_data, c)
    res = summary_d(input_data=d)
    return res

def linear_time():
    """
    A function which computes the linear search time
    """ 
    SETUP_CODE = ''' 
    
    from __main__ import analysis_x 
    from __main__ import summary_d 
    from __main__ import speed
    from __main__ import feature
    '''
    #the timeit.repeat module will take SETUP_CODE as the second argument and takes the modules used in the main computation    
    
    TEST_CODE = ''' 
    
    speed(feature)
    '''
    #the timeit.repeat module will take TEST_CODE as the first argument for which we measure the execution time  
    
    time = timeit.repeat(stmt=TEST_CODE, setup=SETUP_CODE, repeat=1, number = 1) #this line of code uses the timeit module to time how long it takes to run the code
                                                                                 #the repeat argument specifies how many times the timeit module runs
                                                                                 #the number argument specifies the number of executions
    return time


    
if __name__ == "__main__": 

    features = [] #creating an empty list which the range of features will be appended to
    times = [] #creating an empty list that stores the time taken to execute each iteration
    for i in range(10, 10000):

        feature = i
        time = linear_time() 
        features.append(feature) #the features within the specified range will populate the features list, which is originally empty
        times.append(time) #the time taken to execute each iteration will also be stored inside the times list
    
    #plotting the "time_features" graph
    plt.plot(features, times)
    plt.title("Samples with a range of features") 
    plt.ylabel('Seconds (s)')
    plt.xlabel('No. of features')
    plt.show()
    plt.savefig("time_features.png") #saves the plot

    samples = [] #creating an empty list that will store the sample range
    times1 = [] #creating another empty list to store the time taken to execute each iteration
    for n in range(10, 10000):
        sample = n
        time1 = linear_time()
        samples.append(sample)#populating the empty samples list
        times1.append(time1) #populating the empty times list

    #plotting the "time_samples" graph
    plt.plot(samples, times1)
    plt.title("Range of samples with 10 features") 
    plt.ylabel('Seconds (s)')
    plt.xlabel('No. of samples')
    plt.show()
    plt.savefig("time_samples.png") #saves the plot

