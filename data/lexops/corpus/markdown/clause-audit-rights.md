# Playbook: Audit Rights

# NORTHWIND SYSTEMS INTERNAL NEGOTIATION PLAYBOOK
## SECTION 14: AUDIT RIGHTS

### 14.1 Scope and Application
This Section 14 governs the negotiation of customer audit rights across all Northwind Systems B2B SaaS master subscription agreements (MSAs) and order forms. Legal team members (Marcus Vance, Sarah Lin, and Priya Patel) must adhere to the preferred, fallback, and walk-away positions detailed herein. Any deviation outside these parameters requires formal escalation pursuant to subsection 14.5.

---

### 14.2 Preferred Northwind Position (Model Clause Language)

**14.2.1 Audit Restrictions.** Customer may, at its sole expense, conduct no more than one (1) audit of Northwind Systems’ systems, books, and records directly pertaining to the Services during any rolling twelve (12) month period. Any such audit shall be conducted solely to verify Northwind Systems’ compliance with the security and data protection obligations set forth in this Agreement.

**14.2.2 Notice and Logistics.** Customer must provide Northwind Systems with at least thirty (30) days prior written notice of any audit request. The audit shall be conducted during Northwind Systems’ normal business hours, without disrupting Northwind Systems’ normal operations, and subject to Northwind Systems’ standard safety, security, and confidentiality policies.

**14.2.3 Third-Party Auditors.** Any audit must be conducted by an independent, nationally recognized certified public accounting firm or cybersecurity auditing firm bound by professional standards of confidentiality, and such firm must not be a competitor of Northwind Systems nor compensated on a contingency-fee basis.

**14.2.4 Cost Allocation.** Customer shall bear all costs and expenses incurred in connection with any audit, including any fees charged by the auditing firm. If an audit reveals a material failure by Northwind Systems to comply with its security or confidentiality obligations under this Agreement resulting in an underpayment or data breach exceeding twenty-five thousand dollars ($25,000), Northwind Systems shall reimburse Customer for the reasonable, documented third-party costs of such audit within thirty (30) days of invoice.

---

### 14.3 Fallback Position

If the counterparty rejects the Preferred Position, the Legal Team is authorized to agree to the following fallback terms:

*   **Frequency:** Maximum of one (1) audit per contract year, provided that audits shall not be cumulative if missed in a prior year.
*   **Notice Period:** Reduced to no less than twenty (20) business days prior written notice.
*   **Cost Threshold for Reimbursement:** Adjusted so that Northwind Systems reimburses third-party audit costs only if a material deficiency results in financial harm or underpayment exceeding fifty thousand dollars ($50,000).
*   **Cure Period:** Northwind Systems shall have thirty (30) days from receipt of the final audit report to cure any identified non-compliance, during which time no termination rights shall accrue to Customer.
*   **Monetary Floor for Claims:** No audit-related claim may be brought by Customer unless the aggregate financial impact on Customer exceeds ten thousand dollars ($10,000).

---

### 14.4 Walk-Away Position

Legal team members must terminate negotiations or reject clauses containing any of the following provisions, as they represent unacceptable risk to Northwind Systems' multi-tenant architecture and operational integrity:

1.  **Unlimited Frequency:** Allowing audits more than once per year, or permitting "continuous," "real-time," or "event-triggered" automated monitoring access to production environments.
2.  **On-Site Physical Access:** Permitting Customer or its representatives physical access to Northwind Systems' server hosting facilities, colocation centers, or engineering workspaces (all audits must be conducted remotely via documentation review, SOC 2 reports, and virtual interviews).
3.  **Source Code Inspection:** Any right to inspect, review, download, or analyze Northwind Systems' proprietary source code, algorithms, or intellectual property.
4.  **Uncapped Cost Liability:** Requiring Northwind Systems to pay for Customer's internal staff time, legal fees, or non-independent auditing expenses regardless of audit findings.

---

### 14.5 Named Deviations and Escalation Matrix

Any contract term that falls outside subsections 14.2 and 14.3 requires written approval prior to signature. The following deviations are strictly assigned to the named escalation authorities:

| Deviation Type | Description | Escalation Authority |
| :--- | :--- | :--- |
| **Enterprise Financial Cap Override** | Customer demands audit cost reimbursement thresholds below twenty-five thousand dollars ($25,000) or fee-multiple caps exceeding three times (3x) annual contract value (ACV). | **Chief Financial Officer (Arthur Pendelton)** |
| **Shortened Notice Period** | Customer insists on an audit notice period of fewer than fifteen (15) business days due to regulatory compliance frameworks (e.g., HIPAA, DORA). | **Chief Information Security Officer (Elena Rostova)** |
| **Competitor-Affiliated Auditor** | Customer requests the use of an auditing firm that maintains active consulting engagements with a direct competitor of Northwind Systems, subject to a strict non-disclosure agreement. | **General Counsel (Marcus Vance)** |

---

### 14.6 Worked Examples of Counterparty Language

#### 14.6.1 Acceptable Counterparty Language (Approved for Use)

> *Example A:* "Customer may audit Northwind’s security controls once per calendar year upon thirty (30) days' prior written notice. Audits shall be conducted remotely by an independent Big-4 accounting firm during normal business hours. Customer shall bear all audit costs unless the audit uncovers a material security breach causing direct financial loss to Customer in excess of $40,000, in which case Northwind shall reimburse reasonable third-party audit expenses."
> *Analysis:* **ACCEPTED.** Notice period exceeds thirty (30) days, frequency is capped at once per year, remote-only restriction is maintained, and the reimbursement threshold exceeds the $25,000 minimum floor.

> *Example B:* "Upon twenty-one (21) days prior written notice, an independent third-party auditor mutually agreed upon by the Parties may review Northwind’s SOC 2 Type II reports and relevant policies annually. Northwind will have a period of forty-five (45) days to remediate any identified operational gaps."
> *Analysis:* **ACCEPTED.** Fallback notice period (21 days) is respected, scope is properly limited to reports and policies (avoiding production server access), and a clear cure period (45 days) is established.

#### 14.6.2 Unacceptable Counterparty Language (Rejected / Requires Escalation)

> *Example C:* "Customer and its designated technical consultants may enter Northwind’s offices and data centers without notice during normal business hours to inspect network hardware, database logs, and source code repositories."
> *Analysis:* **REJECTED.** Violates the walk-away position regarding physical on-site access, shortens notice to zero, and demands source code inspection. Immediate walk-away; no escalation permitted.

> *Example D:* "Customer reserves the right to conduct quarterly on-site security audits at Northwind's expense, and Northwind shall pay all internal and external costs incurred by Customer in conducting such reviews."
> *Analysis:* **REJECTED.** Violates frequency caps (quarterly instead of annual), demands on-site access, and improperly shifts all internal/external costs to Northwind without a deficiency threshold. Requires escalation to CFO if the deal size exceeds $500,000 ACV; otherwise, outright rejected.
