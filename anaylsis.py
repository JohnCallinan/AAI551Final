import numpy as np
import pandas as pd
#anaylsis done here
def compute_metrics(patients):
    '''Calculate metrics and stats'''
    waits = [p.wait_time for p in patients if p.wait_time is not None]#collects wait time for all patients skipping those untreated
    if not waits:
        return {}#if nobody was treated return empty list

    df = pd.DataFrame([{"severity": p.severity, "wait_time": p.wait_time} for p in patients])#builds a pandas data fream for per severity grouping
    #compute the metrics we want 
    metrics = {
        "total_patients": len(patients),
        "avg_wait_minutes": float(np.mean(waits)),
        "median_wait_minutes": float(np.median(waits)),
        "max_wait_minutes": float(np.max(waits)),
        "min_wait_minutes": float(np.min(waits)),
        "stdev_wait_minutes": float(np.std(waits)),
    }
    for sev, group in df.groupby("severity"):
        metrics[f"avg_wait_sev{sev}"] = float(group["wait_time"].mean())#per severity wait times
    return metrics #return the metrics


def analyze_results(patients):
    '''Using filter, lambda, map, and list comprehension'''
    # filter + lambda creates a list of patients of severity 1 and 2
    critical = list(filter(lambda p: p.severity <= 2, patients))

    # list comprehension collects wait times for severity 4 or 5 patients 
    low_acuity_waits = [p.wait_time for p in patients if p.severity >= 4]

    # map + lambda is used to simulate if there as a staffing shortage increassing wait time by 20%
    shortage_waits = list(map(lambda w: w * 1.20,
                              [p.wait_time for p in patients if p.wait_time is not None]))
    #Builds and returns a dictioanry using these functions
    return {
        "critical_patient_count": len(critical), #how many crit patients are there severity 1 and 2
        "critical_avg_wait": (sum(p.wait_time for p in critical) / len(critical) if critical else 0.0), #average wait time for severity 1 and 2 patients returns 0.0 if none
        "low_acuity_avg_wait": (sum(low_acuity_waits) / len(low_acuity_waits) if low_acuity_waits else 0.0),#average wait time for severity 4 and 5 patients returns 0.0 if none
        "projected_avg_wait_with_shortage": (sum(shortage_waits) / len(shortage_waits) if shortage_waits else 0.0),#what would the average wait time be if increased by 20% 
    }
