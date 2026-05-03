#this is the patient
class Patient:
    """Represents a patient."""

    def __init__(self, patient_id, severity, arrival_time):
        '''
        Initilizes new patient. Takes three pieces of info severity, arrival_time, and patient ID
        Checks for invalid inputs such as severity not between 1-5, arrival time below 0, and patient id below 0 
        '''
        if not isinstance(severity, int) or not (1 <= severity <= 5): #checks if variable is int between 1-5
            raise ValueError(f"Invalid severity {severity}; must be int in 1..5.") #throws error if not
        if arrival_time < 0: #checks if value is above 0
            raise ValueError(f"Invalid arrival_time {arrival_time}; must be >= 0.") #throws error if not
        if patient_id < 0: #checks if value is above 0
            raise ValueError(f"Invalid patient_id {patient_id}; must be >= 0.") #throws error if not
        #patient arrival info:
        self.patient_id = patient_id 
        self.severity = severity
        self.arrival_time = arrival_time
        #patient post arrival info:
        self.treatment_start = None
        self.treatment_duration = 0.0
        self.discharge_time = None

    def __lt__(self, other):
        '''Compares two patients and orders them in terms of severity and arrival time'''
        if self.severity != other.severity: #checks if severity is not equal
            return self.severity < other.severity #if not equal more severe patient goes first
        return self.arrival_time < other.arrival_time # if equal first arrival goes first

    def __str__(self):
        '''controls print(patient)'''
        wait = self.wait_time #pulls the current wait time
        wait_str = f"{wait:.1f}" if wait is not None else "N/A" #formats wait time to 1 decimal
        return (f"Patient #{self.patient_id:04d} | sev={self.severity} | "
                f"arrived={self.arrival_time:6.2f}m | wait={wait_str}m | "
                f"treat={self.treatment_duration:5.2f}m") #formats string and sends it out

    @property
    def wait_time(self):
        '''Minutes spent waiting'''
        if self.treatment_start is None: #if treatment has not started yet wait time is undefined
            return None
        return self.treatment_start - self.arrival_time #calculates wait time
