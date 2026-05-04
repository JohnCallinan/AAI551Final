import pytest
from patients import Patient
from er_queue import ERQueue, QueueError
from sim import generate_patients, run_simulation
#patient validation tests:
def test_patient_invalid_severity():
    '''checks that patient only accepts values between 1-5'''
    with pytest.raises(ValueError):
        Patient(1, 0, 0)
    with pytest.raises(ValueError):
        Patient(1, 6, 0)


def test_patient_invalid_arrival_time():
    '''checks against negative number in arrival time'''
    with pytest.raises(ValueError):
        Patient(1, 3, -5)


def test_patient_lt_orders_by_severity():
    '''checks that __lt__ priorizes severity over time'''
    assert Patient(1, 1, 100) < Patient(2, 5, 0)


def test_patient_lt_breaks_ties_by_arrival():
    '''checks that __lt__ breaks ties of severity with arrival time'''
    assert Patient(1, 3, 10) < Patient(2, 3, 20)

#ER queue tests
def test_queue_pops_most_severe_first():
    '''checks next patient waiting is always most severe'''
    q = ERQueue()
    q.admit(Patient(1, 4, 0))
    q.admit(Patient(2, 1, 10))
    q.admit(Patient(3, 3, 5))
    nxt = q.next_patient()
    assert nxt.patient_id == 2 and nxt.severity == 1


def test_queue_same_severity_fifo():
    '''checks that if patients have same severiy they are returned based on arrival time'''
    q = ERQueue()
    q.admit(Patient(1, 2, 20))
    q.admit(Patient(2, 2, 5))
    q.admit(Patient(3, 2, 10))
    assert q.next_patient().patient_id == 2
    assert q.next_patient().patient_id == 3
    assert q.next_patient().patient_id == 1


def test_queue_empty_raises():
    '''checks that if next_patient is called on an empty queue
       that the custom error is called '''
    with pytest.raises(QueueError):
        ERQueue().next_patient()
