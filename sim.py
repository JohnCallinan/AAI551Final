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


#running of the simulation:
def run_simulation(patients, num_doctors=2, seed=None):
    '''Runs the er sim. num_doctors defaults to 2 with no seed'''
    if num_doctors < 1: #need at least one doctor
        raise ValueError(f"num_doctors must be >= 1, got {num_doctors}")#throws error if no doctor
    if not patients:#if no patients
        return []#return

    rng = random.Random(seed)#setup an indpendent random
    queue = ERQueue() #priority queue
    doctor_free_at = [0.0] * num_doctors  # time each doctor becomes free
    arrivals = sorted(patients, key=lambda p: p.arrival_time) #sort patients by arrivals
    arrival_idx = 0#pointer to the arribal list tracking which patient comes in next
    completed = [] #finished patients accumulate here

    while arrival_idx < len(arrivals) or queue:
        # picks next available doctor 
        doc = min(range(num_doctors), key=lambda i: doctor_free_at[i])#Finds the docotor free soonest and breaks ties with lower index
        now = doctor_free_at[doc]#sim clock when the doctor will be free

        # Admit any patients who arrived while the doctor was busy
        while arrival_idx < len(arrivals) and arrivals[arrival_idx].arrival_time <= now:
            queue.admit(arrivals[arrival_idx])
            arrival_idx += 1

        # Handles what to do if doctors are idle
        if not queue: #if queue is empty
            if arrival_idx >= len(arrivals): #if no more patients are coming
                break #end
            now = arrivals[arrival_idx].arrival_time #jumps clock forward to next arrival time
            doctor_free_at[doc] = now #update doctors free time to match
            #admit all patients arriving at this arrival time
            while arrival_idx < len(arrivals) and arrivals[arrival_idx].arrival_time <= now:
                queue.admit(arrivals[arrival_idx])
                arrival_idx += 1

        # Treat highest priority patient 
        patient = queue.next_patient() #checks for the most critical patient
        base_time = {1: 45, 2: 30, 3: 20, 4: 12, 5: 7}[patient.severity] #checks treatment time based on severity
        duration = max(1.0, rng.gauss(mu=base_time, sigma=base_time * 0.25)) #adds some randomness to this time
        #fill the patients attributes with information:
        patient.treatment_start = now
        patient.treatment_duration = round(duration, 3)
        patient.discharge_time = round(now + duration, 3)
        #update doctors schedule 
        doctor_free_at[doc] = patient.discharge_time
        #add patient to the finished list
        completed.append(patient)

    return completed #returns completed list
