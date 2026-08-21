# Playbook: Data Protection and Processing

# NORTHWIND SYSTEMS INTERNAL LEGAL PLAYBOOK
## SECTION 14: DATA PROTECTION AND PROCESSING

---

### 14.1 Scope and Application
This Section 14 governs all commercial agreements entered into by Northwind Systems, Inc. ("Northwind") where Northwind processes Customer Personal Data as a processor, or where Personal Data is otherwise transferred between the parties. No sales executive, account manager, or legal counsel may depart from the positions set forth herein without express written authorization pursuant to Section 14.5.

---

### 14.2 Preferred Position (Model Clause Language)

Northwind shall process Customer Personal Data solely in accordance with documented instructions from Customer and pursuant to the Data Processing Addendum (DPA) attached as Exhibit D. 

**14.2.1 Limitation of Liability:** Northwind's total aggregate liability arising out of or related to data protection, security breaches, or violations of Exhibit D shall be subject to the overall limitation of liability set forth in the Master Services Agreement, which shall in no event exceed **one times (1x)** the total fees paid or payable by Customer to Northwind in the **twelve (12)** months preceding the incident.

**14.2.2 Security Incident Notification:** In the event of a confirmed security incident impacting Customer Personal Data, Northwind shall notify Customer without undue delay and in any event no later than **seventy-two (72)** hours after becoming aware of the incident.

**14.2.3 Audit Rights:** Customer may audit Northwind’s compliance with Exhibit D at Customer's sole expense, no more than once per **twelve (12)** month period, upon at least **thirty (30)** days' prior written notice, and subject to reasonable confidentiality and operational security controls.

**14.2.4 Data Return and Deletion:** Upon termination of the agreement, Northwind shall, at Customer's election, return or securely delete all Customer Personal Data within **ninety (90)** days, except as required by applicable law.

---

### 14.3 Fallback Position

If counterparty rejects the Preferred Position, legal counsel is authorized to negotiate the following fallback thresholds:

*   **Liability Cap:** May be increased to a maximum of **two times (2x)** annual contract value (ACV), or a monetary floor of **$250,000**, whichever is greater, strictly limited to direct damages arising from a data breach caused by Northwind’s gross negligence or willful misconduct.
*   **Notice Period:** May be shortened to **forty-eight (48)** hours, provided Northwind retains the right to provide initial notice with phased updates as forensic investigation proceeds.
*   **Audit Rights:** May permit audits twice per **twelve (12)** month period upon **fourteen (14)** days' notice, provided such audits are conducted by an independent third-party auditor bound by strict confidentiality.
*   **Cure Period:** Northwind shall be afforded a mandatory **thirty (30)** day cure period to remedy any documented material breach of data protection obligations before Customer may terminate the underlying agreement.

---

### 14.4 Walk-Away Position

Legal counsel must terminate negotiations or escalate immediately if the counterparty insists upon any of the following terms:

1.  **Unlimited Liability:** Any demand for an uncapped liability limit, super-caps exceeding **three times (3x)** fees, or exclusion of data protection liabilities from the Master Services Agreement's overall liability cap.
2.  **Unilateral Direct Audits:** Any right for Customer personnel or non-certified competitors to directly inspect Northwind production servers, source code, or physical data center facilities.
3.  **Indemnification Demands:** Any requirement for Northwind to provide an uncapped, standalone indemnity for third-party regulatory fines or private class-action lawsuits arising from data processing activities.
4.  **Immediate Deletion/No Retention:** Any requirement to delete or anonymize backup archives or audit logs in a timeframe shorter than **thirty (30)** days, or any restriction preventing Northwind from retaining anonymized, aggregated telemetry data for platform optimization.

---

### 14.5 Escalation Matrix and Named Deviations

The following specific deviations from the Playbook require formal written sign-off from the designated internal authority:

| Deviation Type | Trigger Condition | Escalation Target |
| :--- | :--- | :--- |
| **Super-Cap Request** | Counterparty demands liability cap between **3x and 5x** ACV for data breach. | Chief Financial Officer (Marcus Vance) |
| **Direct Facility Access** | Counterparty insists on physical or logical access to Northwind production environments by Customer engineers. | Chief Technology Officer (Elena Rostova) |
| **Regulatory Fine Indemnity** | Counterparty requires Northwind to indemnify Customer for GDPR/CCPA regulatory fines levied directly against Customer. | General Counsel (Sarah Jenkins) |

---

### 14.6 Worked Examples of Counterparty Language

#### 14.6.1 Acceptable Counterparty Language (Passes Review)

> *"Vendor shall notify Customer of any confirmed Security Incident impacting Customer Personal Data within forty-eight (48) hours of confirmation. Vendor’s aggregate liability for breaches of Data Protection provisions shall be capped at two times (2x) the total fees paid by Customer in the preceding twelve-month period, subject to the general limitation of liability in Section 11 of the Agreement."*
> 
> **Why Acceptable:** Falls within authorized fallback thresholds (48-hour notice, 2x liability cap) and ties back to the master limitation of liability.

> *"Upon termination, Processor shall, within sixty (60) days, delete all Customer Data residing in active databases, provided that Processor may retain archival backup copies for up to one hundred eighty (180) days subject to continued compliance with this DPA."*
> 
> **Why Acceptable:** Provides a reasonable deletion window and protects standard disaster recovery backup retention cycles without violating walk-away triggers.

#### 14.6.2 Unacceptable Counterparty Language (Fails Review — Requires Revision or Escalation)

> *"Processor shall be strictly liable for any and all regulatory fines, penalties, and third-party claims arising from a data breach, without regard to any limitation of liability or liability cap set forth in the Agreement."*
> 
> **Why Unacceptable:** Violates Walk-Away Position item 1 (un-capped liability) and item 3 (indemnification/fines). Must be struck down and replaced with model clause language.

> *"Customer or its designated representatives shall have the right to conduct unannounced on-site security audits of Processor’s data centers and interview engineering personnel at any time during normal business hours."*
> 
> **Why Unacceptable:** Violates Walk-Away Position item 2 (unilateral direct audits) and creates severe operational and security vulnerabilities. Must be restricted to annual, noticed audits via third-party SOC 2 reports or certified auditors.
