import numpy as np
import pandas as pd
from scipy import stats # Needed for chi-square and statistical validation

# --- HELPER FUNCTION: Normalization ---
def normalize(data_series):
    """
    Performs Min-Max normalization on a pandas Series of features.
    Required for clinical_similarity.
    """
    min_val = data_series.min()
    max_val = data_series.max()
    if max_val == min_val:
        # Return a series of zeros if all values are the same
        return data_series.copy() - min_val 
    return (data_series - min_val) / (max_val - min_val)

# --- 4.1 Group Fairness Metrics ---

def statistical_parity_difference(approvals: pd.Series, requester_type: pd.Series):
    """Calculate approval rate difference between GP and Surgeon requests"""
    # Assuming approvals and requester_type are pandas Series/NumPy arrays
    gp_approval_rate = approvals[requester_type == 'GP'].mean()
    surgeon_approval_rate = approvals[requester_type == 'Surgeon'].mean()
    return abs(gp_approval_rate - surgeon_approval_rate)

def equal_opportunity_difference(approvals: pd.Series, clinical_necessity: pd.Series, requester_type: pd.Series):
    """Calculate True Positive Rate (TPR) difference for clinically necessary cases"""
    # Filter for necessary cases for each group
    gp_tpr_mask = (clinical_necessity == True) & (requester_type == 'GP')
    surgeon_tpr_mask = (clinical_necessity == True) & (requester_type == 'Surgeon')

    # Calculate mean approval rate (TPR) only where clinical necessity is True
    gp_tpr = approvals[gp_tpr_mask].mean() if gp_tpr_mask.any() else 0
    surgeon_tpr = approvals[surgeon_tpr_mask].mean() if surgeon_tpr_mask.any() else 0

    return abs(gp_tpr - surgeon_tpr)

def predictive_parity_difference(medical_necessity: pd.Series, approvals: pd.Series, premium_level: pd.Series):
    """Calculate Positive Predictive Value (PPV) difference between premium levels"""
    # PPV = P(Medical_Necessity=True | Approved)
    limited_ppv_mask = (approvals == 1) & (premium_level == 'Limited')
    full_ppv_mask = (approvals == 1) & (premium_level == 'Full')

    limited_ppv = medical_necessity[limited_ppv_mask].mean() if limited_ppv_mask.any() else 0
    full_ppv = medical_necessity[full_ppv_mask].mean() if full_ppv_mask.any() else 0

    return abs(limited_ppv - full_ppv)

# --- 4.2 Individual Fairness Metrics ---

def clinical_similarity(case1: pd.Series, case2: pd.Series):
    """Define clinical similarity for emergency cases using normalized features."""
    features = ['symptom_severity', 'diagnostic_uncertainty', 'time_sensitivity',
                'alternative_available', 'specialist_recommendation']

    # Use the defined helper function 'normalize'
    # NOTE: Normalization is applied here purely for feature distance calculation.
    case1_normalized = normalize(case1[features])
    case2_normalized = normalize(case2[features])

    # Calculate Euclidean distance between the normalized feature vectors
    distance = np.linalg.norm(case1_normalized - case2_normalized)

    # Simplified inverse distance for similarity (0 to 1)
    similarity = max(0, 1 - distance) 
    
    return similarity

def individual_fairness_violation(cases: pd.DataFrame, approvals: pd.Series, threshold=0.1):
    """Identify cases where similar patients receive different treatment"""
    violations = []
    # Using iterrows for simplicity, but performance will be slow on large datasets
    for i, case1 in cases.iterrows():
        for j, case2 in cases.iterrows():
            # Check for different outcomes and high similarity
            if i != j and abs(approvals.loc[i] - approvals.loc[j]) > threshold:
                if clinical_similarity(case1, case2) > 0.9: # Threshold for high similarity
                    violations.append((i, j, approvals.loc[i], approvals.loc[j]))
    return violations

# --- 4.3 Intersectional Fairness Analysis ---

def intersectional_fairness_analysis(data: pd.DataFrame):
    """Analyze fairness across multiple demographic intersections"""
    # Assumes binary columns 'premium_limited', 'requester_gp', 'location_rural' exist
    intersections = [
        ('premium_limited', 'requester_gp'),
        ('premium_limited', 'location_rural'),
        ('requester_gp', 'location_rural'),
        ('premium_limited', 'requester_gp', 'location_rural')
    ]

    results = {}
    for intersection in intersections:
        mask = np.ones(len(data), dtype=bool)
        # Build the mask based on intersection conditions
        for condition in intersection:
            mask &= (data[condition] == True)

        if mask.sum() > 30:  # Minimum sample size for statistical relevance
            approval_rate = data[mask]['approved'].mean()
            avg_processing_time = data[mask]['processing_minutes'].mean()
            results[intersection] = {
                'approval_rate': approval_rate,
                'processing_time': avg_processing_time,
                'sample_size': mask.sum()
            }

    return results

# --- 4.4 Statistical Validation ---

def bootstrap_fairness_ci(data: pd.DataFrame, metric_func, metric_args: list, n_bootstrap=10000, alpha=0.05):
    """
    Calculate confidence intervals for fairness metrics.
    Correctly passes required columns from the resampled data 
    to the metric function.
    """
    bootstrap_metrics = []
    for _ in range(n_bootstrap):
        sample = data.sample(len(data), replace=True)
        
        # CORRECTED CALL: Unpack the required columns (Series) and pass them
        try:
            # We use * to unpack the list of arguments into separate function arguments
            metric = metric_func(*[sample[arg] for arg in metric_args])
            bootstrap_metrics.append(metric)
        except Exception as e:
            # In a real scenario, we might want to log this error, but for a demo, 
            # we just skip and use the successful runs.
            continue 

    if not bootstrap_metrics:
        return None, None
        
    lower = np.percentile(bootstrap_metrics, 100 * alpha/2)
    upper = np.percentile(bootstrap_metrics, 100 * (1 - alpha/2))

    return lower, upper

def fairness_significance_test(group1_approvals: pd.Series, group2_approvals: pd.Series):
    """
    Test statistical significance of approval rate differences using Chi-square test.
    Includes robust Cramer's V calculation.
    """
    
    # Group1 Approved and Denied counts
    g1_approved = group1_approvals.sum()
    g1_denied = len(group1_approvals) - g1_approved

    # Group2 Approved and Denied counts
    g2_approved = group2_approvals.sum()
    g2_denied = len(group2_approvals) - g2_approved
    
    # Check if groups are empty to prevent error
    if (g1_approved + g1_denied == 0) or (g2_approved + g2_denied == 0):
        return {
            'chi2_statistic': 0.0,
            'p_value': 1.0,
            'significant': False,
            'effect_size': 0.0
        }

    contingency_table = [
        [g1_approved, g1_denied],
        [g2_approved, g2_denied]
    ]

    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    
    # Calculate Cramer's V (Effect Size) robustly: V = sqrt(chi2 / N)
    N = len(group1_approvals) + len(group2_approvals)
    cramers_v = np.sqrt(chi2 / N)

    return {
        'chi2_statistic': chi2,
        'p_value': p_value,
        'significant': p_value < 0.05,
        'effect_size': cramers_v 
    }
