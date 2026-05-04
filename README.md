# AAI551Final
Final for AAI 551. Simulates an ER queue.

Project Name : ER Simulation
Team Members: John Callinan (20011148)  & Taj Dhillon (20015125) 
Emails: jcallina@stevens.edu & tdhillon@stevens.edu

Project Description: 
This project simulates one 8 hour emergency room shift queue. This program uses a priority queue to 
manage which patients get treated first. Patients are given a severity level from 1 - 5 and are treated
by any doctors that are available in priority order (1 being most critical). If 2 patients have the 
same severity level, they are given priority based on their arrival time. This simulation tracks 
patients wait times, treatment durations, and discharge times and then puts that information on CSV
files. 



Depencencies and Libraries:
-Python 3
-Numpy
-Pandas
-Pytest
-CSV
-OS
-Random
-Time


File/Module Structure:
Patient Class: This class represents a single ER patient
ERQueue: Queue class that admits patients into a queue
generate_patients(): generator function that creates patient objects with random severities and
  a realistic ER arrival pattern.
save_patients_to_csv() / load_patients_from_csv() : saves and loads data to CSV with the the data
  that is connected to the patient objects.
run_simulation(): simulates the er queue shift with a number of doctors and treatment based on severity.
compute_metrics(): calculates overall and per-severity statistics of wait times. 
analyze_results(): does an anlysis using lambda, map, list comprehensions and filter 
main(): The main function : generates the pateint roster, saves to CSV, loads from CSV, runs the 
  simulation, saves the results and prints important metrics.

How to run:
Place all the necessary files into a folder and open in Jupiter Notebook. Run the main.ipynb.

Contributions:

John Callinan:
Patient Class
CSV read/write 
pytest test functions
main()

Taj Dhillon:
ERQueue class / error exception
generate_patients()
analysis
readme

