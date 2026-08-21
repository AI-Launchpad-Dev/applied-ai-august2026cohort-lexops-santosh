# Playbook: Termination and Survival

# NORTHWIND SYSTEMS INTERNAL LEGAL PLAYBOOK
## SECTION 8: TERMINATION AND SURVIVAL

---

### 8.1 PREFERRED NORTHWIND POSITION (MODEL CLAUSE LANGUAGE)

**8.1.1 Termination for Convenience.** Either Party may terminate this Agreement, or any active Order Form, for any reason or no reason, upon providing one hundred twenty (120) days prior written notice to the other Party. Termination for convenience by Customer shall not entitle Customer to any refund of prepaid, unearned subscription fees.

**8.1.2 Termination for Cause.** A Party may terminate this Agreement immediately upon written notice if the other Party: (a) materially breaches this Agreement and fails to cure such material breach within thirty (30) days after receipt of written notice specifying the breach; or (b) becomes the subject of a petition in bankruptcy or any proceeding relating to insolvency, receivership, liquidation, or assignment for the benefit of creditors.

**8.1.3 Effect of Termination.** Upon expiration or termination of this Agreement for any reason: (a) all rights, licenses, and subscriptions granted to Customer hereunder shall immediately terminate; (b) Customer shall immediately cease all use of the Northwind Services; (c) each Party shall return or destroy all Confidential Information of the other Party in accordance with Section 12; and (d) Customer shall immediately pay to Northwind all unpaid fees accrued up to the effective date of termination, including any accelerated remaining fees under active Order Forms where termination is initiated by Customer pursuant to Section 8.1.1 or by Northwind pursuant to Section 8.1.2(a).

**8.1.4 Survival.** The following provisions shall survive the expiration or termination of this Agreement for any reason: Section 5 (Fees and Payment), Section 9 (Confidentiality), Section 11 (Limitation of Liability), Section 12 (Indemnification), and this Section 8.4, together with any other provisions which by their nature are intended to survive.

---

### 8.2 FALLBACK POSITION

**8.2.1 Termination for Convenience.** Customer may terminate this Agreement for convenience upon providing ninety (90) days prior written notice, subject to Customer paying an early termination fee equal to fifty percent (50%) of the subscription fees that would have otherwise been payable for the remainder of the then-current subscription term, subject to a monetary floor of twenty-five thousand United States Dollars ($25,000 USD). Northwind retains the right to terminate for convenience upon one hundred twenty (120) days prior written notice without penalty.

**8.2.2 Termination for Cause Cure Period.** The cure period for material breach under Section 8.1.2(a) may be extended to forty-five (45) days for non-monetary breaches, provided the breaching party initiates commercially reasonable cure efforts within ten (10) days of receiving notice.

---

### 8.3 WALK-AWAY POSITION

Legal counsel shall not agree to any contract containing terms that breach the following limits without explicit written approval:

*   **Customer Convenience Notice Period:** Shorter than sixty (60) days.
*   **Customer Termination Right for Convenience Refund:** Any requirement for Northwind to refund prepaid, unearned fees upon Customer termination for convenience.
*   **Material Breach Cure Period:** Greater than sixty (60) days.
*   **Survival Clause Omissions:** Any agreement where Section 11 (Limitation of Liability) or Section 12 (Indemnification) fails to survive termination.

---

### 8.4 SPECIFIC NUMERIC AND CATEGORICAL THRESHOLDS

1.  **Notice for Convenience (Customer):** Preferred: 120 days. Fallback: 90 days. Absolute Walk-Away Threshold: 60 days.
2.  **Cure Period for Material Breach:** Standard: 30 days. Extended (Fallback for complex technical integration breaches only): 45 days. Walk-Away Threshold: >60 days.
3.  **Monetary Floor for Early Termination Fees:** $25,000 USD (Applies to all enterprise tier accounts where convenience termination penalties apply).
4.  **Cap on Termination Liability / Accelerated Fees:** Maximum recovery for unexpired terms capped at 3.0x the average monthly recurring revenue (MRR) calculated over the preceding six (6) month period.

---

### 8.5 MANDATED DEVIATIONS REQUIRING ESCALATION

The following deviations from the Preferred or Fallback positions require formal written approval from the named executive officer before contract execution:

1.  **Mutual Termination for Convenience:** Any agreement granting Customer the right to terminate for convenience *without* an early termination fee or without the mandatory 90-day notice period. 
    *   *Escalate To:* Chief Revenue Officer (CRO) and General Counsel (GC).
2.  **Extended Insolvency Cure Windows:** Any agreement extending the bankruptcy/insolvency termination trigger grace period beyond the statutory default or adding mandatory pre-termination mediation for financial distress.
    *   *Escalate To:* Chief Financial Officer (CFO).
3.  **Data Extraction Transition Periods Exceeding Thresholds:** Any obligation requiring Northwind to maintain customer data access, API endpoints, or transition support post-termination for a period exceeding thirty (30) days without professional services fees.
    *   *Escalate To:* Chief Technology Officer (CTO) and VP of Customer Success.

---

### 8.6 WORKED EXAMPLES OF COUNTERPARTY LANGUAGE

#### ACCEPTABLE COUNTERPARTY LANGUAGE (Approved for use without escalation)

*   **Example A.1 (Mutual Termination for Convenience with Notice):** 
    > *"Either party may terminate this Agreement for convenience by providing the other party with ninety (90) days prior written notice. If Customer terminates pursuant to this Section, Customer shall pay for all services rendered up to the effective date of termination and a convenience fee equal to the remaining subscription fees due for the active term, capped at three (3) months of the then-current subscription fees."*
    *   *Why acceptable:* Fits within Fallback parameters (90 days notice) and includes a fee cap well within the 3.0x MRR limit.

*   **Example A.2 (Cure Period Extension for Technical Integration):** 
    > *"In the event of a material breach relating to API synchronization errors, the cure period set forth in Section 8.1.2 shall be extended to forty-five (45) days, provided that the breaching party provides weekly progress reports to the non-breaching party."*
    *   *Why acceptable:* Matches the Fallback position (45 days) for non-monetary technical breaches and includes a performance condition (progress reports).

#### UNACCEPTABLE COUNTERPARTY LANGUAGE (Prohibited; requires rejection or escalation)

*   **Example U.1 (Unilateral Customer Convenience with Full Refund):** 
    > *"Customer may terminate this Order Form at any time during the initial term upon thirty (30) days written notice, and upon such termination, Northwind shall promptly refund all prepaid unused fees calculated on a pro-rata daily basis."*
    *   *Why unacceptable:* Violates three Walk-Away thresholds: 30-day notice (below 60-day minimum), requires refund of unearned prepaid fees, and lacks any termination fee floor.

*   **Example U.2 (Excessive Cure Window):** 
    > *"Neither party shall be in default of this Agreement unless it fails to remedy a material breach within ninety (90) days after receipt of detailed written notice from the aggrieved party."*
    *   *Why unacceptable:* Exceeds the absolute Walk-Away threshold of 60 days for material breach cure periods, leaving Northwind exposed to unmitigated platform abuse or non-payment.
