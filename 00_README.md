# 🩺 MLOps Fairness Audit Playbook (Healthcare)

This project contains the documentation and executable code for auditing machine learning models used in **healthcare requests** (e.g., medical procedure pre-approvals) for fairness.  

The primary goal is to **identify and statistically validate disparities** in model outcomes across different protected groups (e.g., requester type, premium level) and complex **intersectional subgroups**.

---

## 💾 Project Structure

The project is divided into two main components: **documentation** and **code**.

## 🗺️ Playbook Components

**Documentation**

This playbook is organized into six core components and a comprehensive case study. Navigate through the files below to conduct a full fairness audit.


| Part | Title | Focus Area | File Link |
| :--- | :--- | :--- | :--- |
| **I** | **Historical Context Assessment** | Identifying patterns of historical and systemic bias. | [01_Historical_Context.md](PLAYBOOK-COMPONENTS/01_Historical_Context.md) |
| **II** | **Fairness Definition Selection** | Establishing a healthcare-specific fairness framework and metrics. | [02_Fairness_Definition.md](PLAYBOOK-COMPONENTS/02_Fairness_Definition.md) |
| **III** | **Bias Source Identification** | Mapping and prioritizing bias across data, algorithm, and deployment. | [03_Bias_Source_Identification.md](PLAYBOOK-COMPONENTS/03_Bias_Source_Identification.md) |
| **IV** | **Comprehensive Metrics Implementation** | Detailed technical implementation of group, individual, and intersectional fairness metrics. | [04_Metrics_Implementation.md](PLAYBOOK-COMPONENTS/04_Metrics_Implementation.md) |
| **V** | **Implementation Guide** | A four-phase audit workflow and intervention framework. | [05_Part_V_Implementation_Guide.md](PLAYBOOK-COMPONENTS/05_Implementation_Guide.md) |
| **VI** | **Validation Framework** | Defining success metrics and the process for internal/external validation. | [06_Part_VI_Validation_Framework.md](PLAYBOOK-COMPONENTS/06_Validation_Framework.md) |
| **VII** | **Case Study Application** | **Emergency CT Scan Approval System** scenario and lessons learned. | [07_Case_Study_Application.md](Case-Study/07_Case_Study_Application.md) |

---
**Code**

| Directory / File | Description |
|------------------|-------------|
| `CODE/` | Contains all executable Python scripts for data generation and metric calculation. |
| `CODE/fairness_metrics.py` | Core file containing all statistical fairness metric implementations (SPD, EOD, PPV, Bootstrap CI). |
| `CODE/generate_sample_data.py` | Utility script that creates synthetic medical data with intentional bias and calculates the Priority Score feature. |
| `CODE/sample_evaluation_scenario.py` | The main test script to run a focused audit and print results, demonstrating the use of metrics and statistical validation. |
| `README.md` (this file) | Project overview and setup instructions. |
---


## ✨ Key Features Implemented

- **Comprehensive Metric Suite**: Implements Statistical Parity, Equal Opportunity, and Predictive Parity.  
- **Individual Fairness**: Uses normalized features to calculate *Clinical Similarity Score* and identify specific unfair outcomes.  
- **Intersectional Analysis**: Audit disparities across compound subgroups (e.g., *Limited Premium AND Rural Location*).  
- **Statistical Validation**: Utilizes *Bootstrap Resampling* to calculate Confidence Intervals (CI) and the *Chi-Square Test* to prove the statistical significance and robustness of observed fairness violations.  
- **Custom Feature Engineering**: Data generation includes creation of a weighted *Priority Score* based on multiple clinical features.  

---

## 🚀 Getting Started

### Prerequisites
You need **Python 3.8+** and the following libraries:  

```bash
pip install numpy pandas scipy
```

### Execution
To run the sample evaluation scenario and verify all metrics and statistical functions are working, execute the following script from the project root directory:  

```bash
python CODE/sample_evaluation_scenario.py
```

---

## 📊 Sample Validation Output

The following output confirms a **statistically significant disparity** in the overall approval rate (*Statistical Parity Difference*) between **Surgeons** and **General Practitioners (GPs)**.

```
=========================================================
=== SAMPLE METRICS EVALUATION FOR FAIRNESS AUDIT (SPD) ===
=========================================================
-> Data Loaded: 1000 recent records simulated.
-----------------------------------------------------------------

--- 1. METRIC CALCULATION: STATISTICAL PARITY DIFFERENCE (SPD) ---
Approval Rate (Surgeon): 0.7500
Approval Rate (GP): 0.6320
Calculated SPD Score: 0.1180
-----------------------------------------------------------------

--- 2. STATISTICAL VALIDATION: 95% CONFIDENCE INTERVAL ---
Bootstrap Iterations: 500
95% Confidence Interval for SPD: [0.0588, 0.1779]

--- 3. INTERPRETATION FOR REVIEWER ---
Finding: The SPD score of 0.1180 is robust.
Since the entire 95% CI is above zero, we can state with high confidence
that a genuine disparity exists in access (overall approval rate) between
Surgeon and GP requests. This finding requires investigation.
=========================================================
```
