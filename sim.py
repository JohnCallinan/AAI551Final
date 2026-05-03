import numpy as np
import random
from patients import Patient
from er_queue import ERQueue
#this is how patients are generated
def generate_patients(shift_minutes=480, avg_arrivals_per_hour=6.0, seed=None):
    '''This is a patient generator defaulting to an 8 hour shift with 6 arrivals per hour'''
    if shift_minutes <= 0: #checks that the shift is a postive number
        raise ValueError(f"shift_minutes must be > 0, got {shift_minutes}") #throws error if not
    if avg_arrivals_per_hour <= 0:#checks that arrivals will happen
        raise ValueError(f"avg_arrivals_per_hour must be > 0, got {avg_arrivals_per_hour}")#throws error if not

    rng = np.random.default_rng(seed)#random number generator 
    severity_weights = [0.05, 0.10, 0.25, 0.35, 0.25]  #probablity that each level of severity show up 
    mean_gap = 60.0 / avg_arrivals_per_hour #finds average gap between patients in minutes
    #starting generator state:
    current_time = 0.0
    pid = 0
    while True:
        '''Produces patients until shift ends'''
        current_time += rng.exponential(scale=mean_gap) #creates gaps between arrivals with exponetial distribution
        if current_time >= shift_minutes: #if current time is greater than shift time end loop
            return
        severity = int(rng.choice([1, 2, 3, 4, 5], p=severity_weights))#declares patient severity
        yield Patient(pid, severity, round(float(current_time), 3)) #sets up patient to be yeilded
        pid += 1 #increment patient id 
