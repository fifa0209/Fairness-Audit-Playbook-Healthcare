# 02. Fairness Definition Selection

## 2.1 Healthcare-Specific Fairness Framework

**Selected Primary Definition: Timely Approval Fairness**

> Every critically ill patient should have equal chance of approval if clinical need is confirmed, regardless of whether a GP or a surgeon submits the request.

### Mathematical Formalization

$P(\text{Approval} \mid \text{Clinical\_Justification} = \text{True}, \text{Emergency} = \text{True})$ should be equal across:
* $\text{Request\_Originator} \in \{\text{GP}, \text{Surgeon}\}$
* $\text{Premium\_Level} \in \{\text{Limited}, \text{Full}\}$
* $\text{Geographic\_Location} \in \{\text{Rural}, \text{Urban}\}$

---

## 2.2 Fairness Metrics Selection

### Primary Metrics

| Metric | Formalization | Rationale |
| :--- | :--- | :--- |
| **Equal Opportunity** (Clinical Merit-Based) | $P(\text{Approval} \mid \text{Clinically\_Justified} = \text{True}, \text{Requester} = \text{GP}) = P(\text{Approval} \mid \text{Clinically\_Justified} = \text{True}, \text{Requester} = \text{Surgeon})$ | Clinical justification should determine approval, not requester role. |
| **Demographic Parity** (Coverage Equity) | $P(\text{Approval} \mid \text{Emergency} = \text{True}, \text{Premium} = \text{Limited}) = P(\text{Approval} \mid \text{Emergency} = \text{True}, \text{Premium} = \text{Full})$ | Emergency medical need should not depend on coverage tier. |
| **Predictive Parity** (Outcome Reliability) | $P(\text{Medical\_Necessity} = \text{True} \mid \text{Approved}, \text{Premium} = \text{Limited}) = P(\text{Medical\_Necessity} = \text{True} \mid \text{Approved}, \text{Premium} = \text{Full})$ | Approval decisions should have consistent meaning (reliability) across coverage types. |

---

## 2.3 Regulatory Alignment

**Healthcare Equity Standards:**

* **Emergency Medical Treatment and Labor Act (EMTALA):** Non-discrimination in emergency care.
* **Affordable Care Act:** Essential health benefits and non-discrimination provisions.
* **State Insurance Regulations:** Prompt payment and fair claims processing requirements.