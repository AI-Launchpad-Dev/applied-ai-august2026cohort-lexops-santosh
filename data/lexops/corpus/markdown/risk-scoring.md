# Clause Risk Scoring Methodology

# NORTHWIND SYSTEMS INTERNAL LEGAL OPERATIONS POLICY
**Document Ref:** SOP-L-2024-04  
**Subject:** Clause Risk Scoring Methodology and Approval Routing  
**Effective Date:** January 15, 2024  
**Applicability:** Northwind Systems Legal Department (Counsel: Marcus Vance, Sarah Chen, Priya Patel)

---

### 1.0 PURPOSE AND SCOPE
This Standard Operating Procedure establishes the mandatory risk scoring methodology for all inbound and non-standard outbound commercial contract reviews at Northwind Systems. Every Master Services Agreement (MSA), Enterprise Software Agreement (ESA), and associated addendum must be evaluated using the 0-100 risk scoring algorithm detailed herein prior to execution.

### 2.0 CLAUSE FAMILY WEIGHTINGS
The aggregate risk score of a contract is calculated by summing the weighted risk scores across eight designated clause families. The total weight across all families equals 100%.

| Ref | Clause Family | Assigned Weight (%) |
| :--- | :--- | :--- |
| CF-01 | Limitation of Liability & Damages | 25% |
| CF-02 | Indemnification | 20% |
| CF-03 | Intellectual Property Ownership & Licensing | 15% |
| CF-04 | Term, Termination & Suspension | 10% |
| CF-05 | Data Privacy, Security & Confidentiality | 10% |
| CF-06 | Warranties, Service Levels & Disclaimers | 10% |
| CF-07 | Governing Law, Dispute Resolution & Venue | 5% |
| CF-08 | Assignment, Subcontracting & Change of Control | 5% |
| **Total** | | **100%** |

### 3.0 RISK SCORE CALCULATION AND POINT DEDUCTIONS
The baseline score for any unmodified Northwind Systems standard template is 0 (zero) points (representing zero deviation risk). For each commercial deviation from Northwind standard posture, legal counsel shall apply the following mandatory point deductions (expressed as negative point values against a 100-point ceiling, or conversely, positive risk increments; for this methodology, risk is scored from 0 to 100, where 100 represents maximum operational exposure). 

#### 3.1 Named Deviations and Point Values
1. **Uncapped Liability (CF-01):** Failure to cap aggregate liability at twelve (12) months trailing twelve months (TTM) fees paid or payable, or failure to exclude consequential/indirect damages.  
   *Penalty:* **+35 points**
2. **Indemnity Without a Cap (CF-02):** Provision of third-party IP or general indemnification that is not subject to the overall limitation of liability cap or a standalone financial cap equal to or less than 2x TTM fees.  
   *Penalty:* **+25 points**
3. **Unilateral Termination for Convenience (CF-04):** Customer right to terminate for convenience upon less than thirty (30) days written notice without payment of a termination fee covering all non-cancellable commitments and professional services rendered.  
   *Penalty:* **+15 points**
4. **Unrestricted Assignment (CF-08):** Customer right to assign the agreement to a direct competitor of Northwind Systems without prior written consent, or assignment without requiring the assignee to assume all obligations in writing.  
   *Penalty:* **+10 points**
5. **Data Ownership Surrender (CF-03):** Transferring ownership of Northwind pre-existing IP, derivative works, or aggregated/anonymized telemetry data to the customer.  
   *Penalty:* **+15 points**
6. **Unilateral SLA Penalties (CF-06):** Service level credit remedies exceeding 30% of monthly recurring revenue (MRR) in any single billing cycle, or failure to make service credits the sole and exclusive remedy for uptime failures.  
   *Penalty:* **+10 points**

### 4.0 RISK SCORE BANDS AND APPROVAL ROUTING
Contracts shall be categorized into one of three risk score bands upon completion of the legal review. The resulting score dictates the mandatory internal sign-off route. Automated or self-service contracting tools integrated into the Northwind CRM (Salesforce) are programmed to enforce these routing rules strictly.

#### 4.1 Low Risk Band (Score: 0 – 25)
* **Operational Definition:** Minor deviations from Northwind standard terms, or use of unaltered Northwind Standard MSA templates with standard commercial inserts (pricing, names, dates).
* **Required Approval Route:** Automated system approval or sign-off by any assigned corporate counsel (Marcus Vance, Sarah Chen, or Priya Patel). No executive escalation required.

#### 4.2 Medium Risk Band (Score: 26 – 70)
* **Operational Definition:** Moderate commercial deviations, including mutual indemnities, non-standard payment terms (e.g., Net 60), or liability caps negotiated up to twenty-four (24) months TTM.
* **Required Approval Route:** Formal written sign-off (email or internal contract lifecycle management system audit trail) by Senior Legal Counsel and approval from the VP of Global Sales.

#### 4.3 High Risk Band (Score: 71 – 100)
* **Operational Definition:** Severe structural departures from Northwind risk policy, including multiple high-penalty deviations (e.g., uncapped liability combined with uncapped indemnities).
* **Required Approval Route:** **Any score above 70 requires General Counsel sign-off and may never be auto-approved.** Furthermore, scores exceeding 85 require dual sign-off from the General Counsel and the Chief Financial Officer (CFO).

---
*End of Policy. Direct compliance questions to General Counsel Marcus Vance.*
