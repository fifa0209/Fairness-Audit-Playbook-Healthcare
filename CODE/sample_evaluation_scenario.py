import numpy as np
import sys 
import os 
# Add the current directory to sys.path to ensure modules are found when running standalone.
sys.path.append(os.path.dirname(os.path.abspath(__file__))) 

# CORRECT IMPORTS: Assuming generate_sample_data.py and fairness_metrics.py are in the same folder
# The error 'ModuleNotFoundError: No module named 'code...' is usually caused by adding 'code.' 
# to these lines when the files are in the same directory.
from generate_sample_data import generate_fairness_data
from fairness_metrics import statistical_parity_difference, bootstrap_fairness_ci

def run_sample_evaluation():
    """
    Runs a focused evaluation scenario for the reviewer, calculating Statistical 
    Parity Difference (SPD) and its 95% Confidence Interval (CI).
    """
    
    # Configuration
    n_bootstrap = 500  # 500 iterations for quick testing
    
    # 1. Load Data
    data = generate_fairness_data(n_samples=1000)
    print("=========================================================")
    print("=== SAMPLE METRICS EVALUATION FOR FAIRNESS AUDIT (SPD) ===")
    print("=========================================================")
    print(f"-> Data Loaded: {len(data)} recent records simulated.")
    print("-" * 65)

    # Define the metric and its required arguments for the bootstrap function
    metric_func = statistical_parity_difference
    metric_args = ['approved', 'requester_type']
    
    # Calculate initial metric score
    spd_score = metric_func(data['approved'], data['requester_type'])
    
    # Calculate group approval rates for printing
    approval_surgeon = data.loc[data['requester_type'] == 'Surgeon', 'approved'].mean()
    approval_gp = data.loc[data['requester_type'] == 'GP', 'approved'].mean()

    print("--- 1. METRIC CALCULATION: STATISTICAL PARITY DIFFERENCE (SPD) ---")
    print(f"Approval Rate (Surgeon): {approval_surgeon:.4f}")
    print(f"Approval Rate (GP): {approval_gp:.4f}")
    print(f"Calculated SPD Score: {spd_score:.4f}")
    print("-" * 65)

    # 2. Statistical Validation (Bootstrap CI)
    print("--- 2. STATISTICAL VALIDATION: 95% CONFIDENCE INTERVAL ---")
    
    try:
        lower_ci, upper_ci = bootstrap_fairness_ci(
            data=data,
            metric_func=metric_func,
            metric_args=metric_args,
            n_iterations=n_bootstrap
        )
        print(f"Bootstrap Iterations: {n_bootstrap}")
        print(f"95% Confidence Interval for SPD: [{lower_ci:.4f}, {upper_ci:.4f}]")
    except Exception as e:
        print(f"Could not calculate CI: {e}")
        lower_ci, upper_ci = None, None

    print("-" * 65)

    # 3. Interpretation
    print("--- 3. INTERPRETATION FOR REVIEWER ---")
    if lower_ci is not None and lower_ci > 0:
        print("Finding: The SPD score is statistically robust.")
        print("Since the entire 95% CI is above zero, we can state with high confidence")
        print("that a genuine disparity exists in access (overall approval rate) between")
        print("Surgeon and GP requests. This finding requires investigation.")
    elif upper_ci is not None and upper_ci < 0:
        print("Finding: The SPD score is statistically robust (negative disparity).")
    else:
        print("Finding: The disparity (SPD) score of 0.00 is not statistically significant.")
        print("The confidence interval spans zero, indicating the observed difference may")
        print("be due to random chance.")
    print("=========================================================")


if __name__ == '__main__':
    run_sample_evaluation()
