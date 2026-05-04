import csv
from patients import Patient
#CSV file read and write stuff
#sets the column headers for the CSV file
CSV_FIELDS = ["patient_id", "severity", "arrival_time", "treatment_start",
              "treatment_duration", "discharge_time", "wait_time"]


def save_patients_to_csv(patients, path):
    '''Saves patient info to csv'''
    with open(path, "w", newline="") as f: #safley opens the file
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS) #DictWriter lets us write rows as dicts
        writer.writeheader()#writes the header
        for p in patients: #loops through every patients writing one row per patient using the dict
            writer.writerow({
                "patient_id": p.patient_id,
                "severity": p.severity,
                "arrival_time": p.arrival_time,
                "treatment_start": p.treatment_start,
                "treatment_duration": p.treatment_duration,
                "discharge_time": p.discharge_time,
                "wait_time": p.wait_time,
            })


def load_patients_from_csv(path):
    """Read patients from a csv"""
    patients = [] #sets up empy patients list
    with open(path, "r", newline="") as f: #safley opens the file in read mode
        for row in csv.DictReader(f): #loops through every row using DictReader 
            patients.append(Patient( #add patients to the list and changes the values from strings to the correct type
                patient_id=int(row["patient_id"]),
                severity=int(row["severity"]),
                arrival_time=float(row["arrival_time"]),
            ))
    return patients #returns the list
