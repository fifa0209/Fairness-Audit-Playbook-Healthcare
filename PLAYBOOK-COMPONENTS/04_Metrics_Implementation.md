# 04. : Comprehensive Metrics Implementation

This section details the mathematical and statistical implementation of selected fairness metrics. The full executable code for these metrics can be found in the **`Code/fairness_metrics.py`** file.

## 4.1 Group Fairness Metrics

### 4.1.1 Statistical Parity (Approval Rate Equity)

* **Implementation Focus:** Approval rate difference between GP and Surgeon requests, and Limited vs. Full Premium.
* **Metric Name:** `statistical_parity_difference`
* **Formula:** $| P(\text{Approval} \mid \text{Group A}) - P(\text{Approval} \mid \text{Group B}) |$
* **Code Reference:** See the `statistical_parity_difference` function in `Code/fairness_metrics.py`.

### 4.1.2 Equal Opportunity (Merit-Based Fairness)

* **Focus:** True Positive Rate (TPR) difference for clinically necessary cases.
* **Metric Name:** `equal_opportunity_difference`
* **Formula:** $| P(\text{Approval} \mid \text{Necessary}, \text{Group A}) - P(\text{Approval} \mid \text{Necessary}, \text{Group B}) |$
* **Code Reference:** See the `equal_opportunity_difference` function in `Code/fairness_metrics.py`.

... (Continue this structure for 4.1.3, 4.2, 4.3, and 4.4)

## 4.4 Statistical Validation

### 4.4.1 Confidence Intervals for Fairness Metrics

Use **bootstrap resampling** ($n=10,000$ iterations) to calculate robust confidence intervals ($\text{CI}$) for all key fairness metrics, ensuring the measured disparity is statistically stable. The implementation for this is provided in the `bootstrap_fairness_ci` function in `Code/fairness_metrics.py`.