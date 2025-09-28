# 02. Fairness Definition Selection

## 2.1 Healthcare-Specific Fairness Framework

**Selected Primary Definition: Timely Approval Fairness**

> Every critically ill patient should have equal chance of approval if clinical need is confirmed, regardless of whether a GP or a surgeon submits the request.

### Mathematical Formalization

P(Approval | Clinical_Justification = True, Emergency = True) should be equal across:
* Request_Originator ∈ {GP, Surgeon}
* Premium_Level ∈ {Limited, Full}  
* Geographic_Location ∈ {Rural, Urban}

## 2.2 Fairness Metrics Selection

### Primary Metrics

| Metric | Formalization | Rationale |
|--------|---------------|-----------|
| **Equal Opportunity** (Clinical Merit-Based) | P(Approval │ Clinically_Justified = True, Requester = GP) = P(Approval │ Clinically_Justified = True, Requester = Surgeon) | Clinical justification should determine approval, not requester role. |
| **Demographic Parity** (Coverage Equity) | P(Approval │ Emergency = True, Premium = Limited) = P(Approval │ Emergency = True, Premium = Full) | Emergency medical need should not depend on coverage tier. |
| **Predictive Parity** (Outcome Reliability) | P(Medical_Necessity = True │ Approved, Premium = Limited) = P(Medical_Necessity = True │ Approved, Premium = Full) | Approval decisions should have consistent meaning (reliability) across coverage types. |
## 2.3 Regulatory Alignment

**Healthcare Equity Standards:**

* **Emergency Medical Treatment and Labor Act (EMTALA):** Non-discrimination in emergency care.
* **Affordable Care Act:** Essential health benefits and non-discrimination provisions.
* **State Insurance Regulations:** Prompt payment and fair claims processing requirements.
