import heapq
from patients import Patient
#tBelow here is the ER queue using compostion with Patients inside
class QueueError(Exception):
    '''Raises error if issue with queue'''
    pass


class ERQueue:
    '''Priority Queue'''

    def __init__(self):
        '''Initializes the queue'''
        self._heap = [] #the list that heapq will uses as a binary heap
        self._admitted_count = 0 #total number of patients ever admitted

    def admit(self, patient):
        '''Adds a patient to the queue'''
        if not isinstance(patient, Patient): #makes sure the passed object is a patient object
            raise TypeError(f"admit() expected Patient, got {type(patient).__name__}") #rasies error if not
        heapq.heappush(self._heap, patient)#adds patient to the heap and re-arranges the list 
        self._admitted_count += 1 #increase total number of patients admitted

    def next_patient(self):
        '''Pop and return highest priority patient'''
        if not self._heap: #empty waiting room. Our own error
            raise QueueError("Cannot get next patient: queue is empty.") #our error
        return heapq.heappop(self._heap)#removes and returns the smallest item in the heap

    def __len__(self):
        '''Allows you to do len(queue) to get the num of patients waiting'''
        return len(self._heap)

    def __bool__(self):
        '''Faster cleaner way to check if queue or while queue to check if at least one patient in queue'''
        return bool(self._heap)

    def __str__(self):
        '''Prints the number of people in the queue and total people admitted today'''
        return f"ERQueue(waiting={len(self._heap)}, total_admitted={self._admitted_count})"
