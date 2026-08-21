# Playbook: Force Majeure

**SECTION 12: FORCE MAJEURE**

**12.1 Purpose and Scope**
This section governs the allocation of risk arising from extraordinary, external events that temporarily or permanently impede performance under Northwind Systems B2B SaaS Master Subscription Agreements (MSAs). 

**12.2 Preferred Northwind Position (Model Clause Language)**
The legal team shall utilize the following text as the primary drafting baseline in all outbound Northwind MSAs:

> **12.2.1 Force Majeure Event Defined.** Neither party shall be liable for any failure or delay in the performance of its obligations under this Agreement (excluding payment obligations) if and to the extent such failure or delay is caused by events beyond such party’s reasonable control, including acts of God, natural disasters, epidemics, pandemics, government restrictions, strikes or labor disputes (excluding internal workforce actions of the affected party), utility failures, or malicious cyberattacks originating from nation-state actors, provided that the affected party could not have avoided the event through the implementation of commercially reasonable business continuity and disaster recovery protocols.
> 
> **12.2.2 Notice and Mitigation Requirements.** The affected party shall provide written notice to the other party via certified email within exactly 48 hours of the inception of the Force Majeure Event, detailing the specific operational impacts and estimated duration. The affected party shall use all commercially reasonable efforts to mitigate the effects of the event and resume full performance.
> 
> **12.2.3 Termination Right.** If a Force Majeure Event prevents the provision of the SaaS platform for a continuous period exceeding 30 calendar days, either party may terminate the affected Order Form without penalty upon written notice.
> 
> **12.2.4 SaaS Continuity Exception.** Notwithstanding anything to the contrary herein, an event shall not qualify as a Force Majeure Event if it is caused by power failures within Northwind’s primary hosting infrastructure provider (currently Apex Cloud Solutions US-East Region), routine software bugs, database corruption, or third-party vendor insolvency. Northwind shall maintain redundancy that caps service degradation from infrastructure loss at 4 hours.

**12.3 Fallback Position**
If the counterparty rejects the 48-hour notice window or the 30-day termination threshold, legal counsel is authorized to adjust the parameters within the following bounds without escalation:
*   **Notice Period:** Extendable up to a maximum of 72 hours.
*   **Termination Threshold:** Compressible down to a minimum of 14 consecutive calendar days of service outage.
*   **Financial Adjustment:** The fallback position permits the inclusion of a prorated service credit calculation for downtime exceeding 72 hours, calculated as 1/30th of the monthly recurring fees (MRF) for each full 24-hour period of outage, subject to a monetary floor of $500.00 and an absolute cap of 3.0 times the aggregate monthly fees paid under the affected Order Form.

**12.4 Walk-Away Position**
Legal counsel must cease negotiations and walk away from any clause that incorporates any of the following terms:
*   Inclusion of customer payment obligations within the scope of Force Majeure.
*   A termination threshold of fewer than 7 consecutive calendar days.
*   A liability cap for Force Majeure failures exceeding 5.0 times the annual contract value (ACV).
*   Categorization of routine cloud infrastructure outages, denial-of-service attacks, or software deployment failures as Force Majeure events.

**12.5 Numeric and Categorical Threshold Summary**
All negotiations must adhere strictly to these operational thresholds:
1.  **Monetary Floor for Credits:** $500.00 (below which no credits are processed).
2.  **Liability Cap Multiplier:** Maximum 3.0x monthly recurring fees (fallback) or 0x (preferred).
3.  **Notice Period:** 48 hours preferred; 72 hours absolute maximum fallback.
4.  **Termination Trigger Duration:** 30 calendar days preferred; 14 calendar days absolute minimum fallback.

**12.6 Named Deviations and Escalation Matrix**
Deviations from the Preferred or Fallback positions require prior written approval from the designated authority:
1.  *Deviation Type A:* Acceptance of customer demands to include "cybersecurity breaches originating from non-state actors" or "ransomware attacks" within the definition of Force Majeure. **Escalate to:** Chief Information Security Officer (Marcus Vance).
2.  *Deviation Type B:* Agreement to aggregate liability caps for Force Majeure events exceeding 3.0x ACV up to the absolute walk-away limit of 5.0x ACV. **Escalate to:** Chief Financial Officer (Elena Rostova).
3.  *Deviation Type C:* Acceptance of termination rights triggered by a Force Majeure event lasting less than 14 calendar days (down to the 7-day walk-away floor) for enterprise accounts exceeding $250,000 ACV. **Escalate to:** VP of Global Sales (Sarah Jenkins).

**12.7 Worked Examples of Counterparty Language**

*   **Acceptable Example 1 (Fallback Range):**
    > *"If either party is prevented from performing its obligations by reason of natural catastrophe or acts of war for a period exceeding 14 days, and the affected party provides written notice within 72 hours of the event, either party may terminate the agreement."*
    *Analysis:* Acceptable under Section 12.3. The 14-day termination window and 72-hour notice period fall within approved fallback parameters.

*   **Acceptable Example 2 (Modified Mitigation):**
    > *"Neither party shall be in default for delays caused by nationwide telecommunications grid collapses, provided that notice is delivered within 48 hours and the affected party implements its secondary backup systems within a 24-hour cure period."*
    *Analysis:* Acceptable. Matches the preferred notice period and introduces a commercially reasonable cure period for secondary systems.

*   **Unacceptable Example 1 (Walk-Away Trigger - Payment Relief):**
    > *"Force Majeure shall include any economic downturn, inflation surge, or loss of key customer contracts by Customer, which shall excuse Customer from paying any recurring subscription fees for the duration of the event."*
    *Analysis:* Unacceptable under Section 12.4. Economic hardship is explicitly excluded, and payment obligations can never be excused by Force Majeure.

*   **Unacceptable Example 2 (Walk-Away Trigger - Short Termination):**
    > *"If Northwind fails to deliver the SaaS platform for more than 48 hours due to any external event, including local municipal power grid failures, Customer may immediately terminate this MSA and recover damages up to 10 times the annual contract value."*
    *Analysis:* Unacceptable under Section 12.4. A 48-hour termination trigger violates the 14-day minimum floor, local power failures of hosting facilities are Northwind's operational risk, and a 10x ACV liability cap exceeds the absolute walk-away threshold.
