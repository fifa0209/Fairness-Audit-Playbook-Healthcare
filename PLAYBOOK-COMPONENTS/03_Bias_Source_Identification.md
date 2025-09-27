# 03. : Bias Source Identification

## 3.1 Systematic Bias Source Mapping

### 3.1.1 Data-Level Bias Sources

| Bias Type | Description |
| :--- | :--- |
| **Historical Bias** | Training data reflects past policy preferences for specialist requests; premium-based historical approval patterns embedded. |
| **Sampling Bias** | Under-representation of rural emergency cases and limited premium patients in training data. |
| **Measurement Bias** | "Clinical urgency" definitions favor certain request formats; risk assessment optimized for cost control rather than patient outcomes. |

### 3.1.2 Algorithm-Level Bias Sources

| Bias Type | Description |
| :--- | :--- |
| **Optimization Objective Bias** | Cost minimization objectives that penalize approvals; efficiency metrics favor rapid rejection. |
| **Feature Engineering Bias** | Request originator type weighted heavily; premium level used as direct input rather than controlling for medical necessity. |
| **Model Architecture Bias** | Decision trees create hard cutoffs based on requester credentials; ensemble methods amplify historical approval patterns. |

### 3.1.3 Deployment-Level Bias Sources

| Bias Type | Description |
| :--- | :--- |
| **Organizational Implementation Bias** | Case manager training reinforces historical patterns; performance incentives focus on denial rates. |
| **System Integration Bias** | EHR systems flag GP requests for additional scrutiny; workflow automation routes specialist requests to expedited review. |

---

## 3.2 Bias Source Priority Matrix

This matrix prioritizes bias sources based on severity, likelihood, and relevance to the case study.

| Bias Source | Severity (1-3) | Likelihood (1-3) | Relevance (1-3) | Priority Score (Max 27) | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Requester role discrimination | High (3) | High (3) | High (3) | **27** | **Critical** |
| Premium-based approval disparities | High (3) | High (3) | High (3) | **27** | **Critical** |
| Geographic access inequities | Medium (2) | High (3) | High (3) | **18** | **High** |
| Emergency vs. elective misclassification | High (3) | Medium (2) | High (3) | **18** | **High** |
| Cost optimization over patient outcomes | Medium (2) | Medium (2) | High (3) | **12** | **Medium** |