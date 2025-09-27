import numpy as np
import pandas as pd

def generate_fairness_data(n_samples=1000):
    """
    Generates synthetic emergency medical request data with intentional bias 
    to test fairness metrics.
    """
    
    # 1. Base Feature Generation
    data = pd.DataFrame({
        'case_id': np.arange(n_samples),
        'requester_type': np.random.choice(['GP', 'Surgeon'], n_samples, p=[0.75, 0.25]),
        'premium_level': np.random.choice(['Limited', 'Full'], n_samples, p=[0.4, 0.6]),
        'location_rural': np.random.choice([True, False], n_samples, p=[0.3, 0.7]),
        
        # Clinical Features (Symptom Severity used in Priority Score)
        'symptom_severity': np.random.randint(1, 11, n_samples),  # Scale 1-10
        'diagnostic_uncertainty': np.random.rand(n_samples),      # Scale 0-1
        'time_sensitivity': np.random.rand(n_samples),            # Scale 0-1

        # New Features Required for Priority Score Formula
        'scope': np.random.randint(1, 6, n_samples),             # Scale 1-5
        'persistence': np.random.randint(1, 11, n_samples),      # Scale 1-10
        'historical_alignment': np.random.rand(n_samples),       # Scale 0-1
        'intervention_feasibility': np.random.rand(n_samples),   # Scale 0-1
        
        'clinical_necessity': np.random.rand(n_samples) > 0.4
    })
    
    # 2. Priority Score Calculation (New Implementation)
    data['priority_score'] = (
        (data['symptom_severity'] * 0.3) +             # Severity (Symptom Severity)
        (data['scope'] * 0.2) +                        # Scope
        (data['persistence'] * 0.2) +                  # Persistence
        (data['historical_alignment'] * 0.2) +         # Historical Alignment
        (data['intervention_feasibility'] * 0.1)       # Intervention Feasibility
    )

    # 3. Injecting Intentional Bias (Model outcome simulation)
    # Surgeons get a base 10% bonus chance of approval
    data['approved'] = data['clinical_necessity'].apply(lambda x: 0.85 if x else 0.4)
    data.loc[data['requester_type'] == 'Surgeon', 'approved'] += 0.10
    
    # Limited premium users have a longer processing time (Operational Bias)
    data['processing_minutes'] = data.apply(
        lambda row: np.random.randint(13, 18) if row['premium_level'] == 'Limited' else np.random.randint(8, 12),
        axis=1
    )
    
    # Convert probability to final binary outcome
    data['approved'] = data['approved'] > np.random.rand(n_samples)

    #  This line resolves the FutureWarning by ensuring the column is a clean integer (0 or 1)
    data['approved'] = data['approved'].astype(int) 

    # Line 74
    return data

if __name__ == '__main__':
    # Example usage for testing
    df = generate_fairness_data(n_samples=50)
    print("--- Sample Data Generated (with Priority Score) ---")
    print(df[['symptom_severity', 'scope', 'priority_score', 'approved']].head())
    print(f"\nPriority Score Min/Max: {df['priority_score'].min():.2f} / {df['priority_score'].max():.2f}")
