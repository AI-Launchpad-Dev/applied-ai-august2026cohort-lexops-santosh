# Playbook: Service Levels and Service Credits

**NORTHWIND SYSTEMS INTERNAL NEGOTIATION PLAYBOOK**
**SECTION 4: SERVICE LEVELS AND SERVICE CREDITS**

---

### 4.1 Preferred Northwind Position (Model Clause Language)

**4.1.1 Availability Target.** Northwind Systems ("Northwind") shall use commercially reasonable efforts to make the Subscription Service available with an uptime percentage of at least 99.5% ("Availability Target") during each calendar month, excluding Scheduled Maintenance and Emergency Maintenance.

**4.1.2 Scheduled and Emergency Maintenance.** Scheduled Maintenance shall not exceed eight (8) hours per calendar month and shall be performed outside Northwind’s normal business hours (8:00 AM to 6:00 PM Eastern Time), upon not less than forty-eight (48) hours’ prior written notice. Emergency Maintenance may be performed at any time upon such notice as is commercially practicable under the circumstances.

**4.1.3 Service Credit Calculation.** If the availability of the Subscription Service falls below the Availability Target in any two (2) consecutive calendar months, Customer’s sole and exclusive remedy, and Northwind’s sole and entire liability, shall be a service credit calculated as a percentage of the monthly subscription fee attributable to the affected Subscription Service ("Monthly Fee") for the month in which the failure occurred, as follows:

*   Availability between 98.0% and 99.49%: a credit equal to five percent (5%) of the Monthly Fee;
*   Availability between 95.0% and 97.99%: a credit equal to ten percent (10%) of the Monthly Fee;
*   Availability below 95.0%: a credit equal to twenty percent (20%) of the Monthly Fee.

**4.1.4 Credit Claim Procedure.** To receive a service credit, Customer must submit a written claim via Northwind’s support portal within thirty (30) days following the end of the month in which the Availability Target was missed. Failure to comply with this requirement shall forfeit the right to receive any credit. Service credits shall be applied against subsequent invoices and are non-refundable; no cash refunds shall be issued.

**4.1.5 Aggregate Cap.** Total service credits issued to Customer in any single calendar quarter shall not exceed twenty-five percent (25%) of the total quarterly subscription fees paid or payable by Customer under the Agreement.

**4.1.6 Exclusions.** Service credits shall not apply to any performance issue caused by: (a) Customer’s equipment, software, or network connections; (b) Force Majeure events; (c) Customer’s breach of the Agreement or unauthorized use of the Subscription Service; or (d) beta, trial, or evaluation releases.

---

### 4.2 Fallback Position

If Customer rejects the 99.5% target or the monthly aggregation model, legal counsel is authorized to fall back to the following amended terms:

*   **Availability Target:** 99.0% availability measured on a quarterly basis.
*   **Service Credit Tiers:** 
    *   98.0% to 98.99%: 5% of quarterly fees;
    *   95.0% to 97.99%: 10% of quarterly fees;
    *   Below 95.0%: 15% of quarterly fees.
*   **Claim Notice Period:** Extended from thirty (30) days to forty-five (45) days following the end of the applicable measurement period.
*   **Quarterly Cap:** Increased to a maximum of thirty-five percent (35%) of the quarterly subscription fees.

---

### 4.3 Walk-Away Position

Legal counsel must reject the agreement or escalate immediately if the counterparty insists on any of the following terms, as they violate Northwind’s risk-tolerance baseline:

1.  An uptime commitment exceeding 99.9% (Five Nines or Four Nines).
2.  Service credits calculated as a percentage of *annual* contract value (ACV) rather than the affected monthly or quarterly fee.
3.  An aggregate annual credit cap exceeding fifty percent (50%) of annual fees, or any provision permitting cash refunds of service credits.
4.  Service credit remedies designated as "non-exclusive" or accompanied by Customer rights to terminate for convenience upon a single SLA breach.

---

### 4.4 Numeric and Categorical Thresholds

1.  **Monetary Floor:** Service credits below fifty dollars ($50.00) in aggregate value for a given period shall not be issued.
2.  **Cure Period:** Northwind shall have thirty (30) days from receipt of written notice of a systemic SLA failure to cure the underlying defect before any termination rights accrue to Customer.
3.  **Notice Period for Scheduled Maintenance:** Minimum of forty-eight (48) hours prior written notice.
4.  **Aggregate Cap Multiplier:** The absolute maximum liability for service credits in any contract year shall not exceed twenty percent (20%) of the total annual recurring revenue (ARR) paid by Customer.

---

### 4.5 Named Deviations Requiring Escalation

1.  **Exclusion of Force Majeure from Uptime Calculations:** If a customer insists that outages caused by cloud infrastructure providers (e.g., AWS, Azure) count toward Northwind's SLA breaches without force majeure protections, **escalate to Arthur Pendelton, VP of Engineering.**
2.  **Termination for Cause Triggered by SLAs:** If a customer requests the right to terminate the master subscription agreement for convenience or for cause if Northwind misses the Availability Target in any two (2) non-consecutive months within a rolling six-month window, **escalate to Sarah Jenkins, Chief Financial Officer.**
3.  **Custom Service Levels (Tiered Enterprise SLAs):** If a customer demands customized performance metrics outside the standard availability and maintenance framework (e.g., specific API response-time latencies tied to credits), **escalate to Marcus Vance, VP of Product.**

---

### 4.6 Counterparty Language Evaluation

#### Acceptable Counterparty Language (Do Not Reject)

*   *Example A:* "In the event of an unscheduled service interruption exceeding four (4) consecutive hours, Northwind shall apply a credit of two percent (2%) of the monthly fee for each additional hour of downtime, up to a maximum of twenty percent (20%) of the monthly fee."
    *   *Rationale:* Aligns with Northwind’s monthly fee structure, includes a clear percentage tier, and respects the 20% aggregate cap.
*   *Example B:* "Customer may offset approved service credits against future undisputed invoices issued by Northwind under this Agreement."
    *   *Rationale:* Standard commercial practice that avoids cash disbursement while clarifying that offsets apply only to undisputed amounts.

#### Unacceptable Counterparty Language (Reject and Replace)

*   *Example C:* "If the service availability drops below 99.9% in any single month, Customer may immediately terminate this Agreement without penalty and receive a full cash refund of all pre-paid annual fees for the remainder of the term."
    *   *Rationale:* Violates walk-away rules regarding annual fee refunds, cash payouts, and unearned termination triggers.
*   *Example D:* "Northwind acknowledges that time is of the essence. For each 0.1% the actual uptime falls below the Availability Target, Northwind shall pay liquidated damages equal to ten percent (10%) of the total annual contract value within thirty (30) days of demand."
    *   *Rationale:* Imposes punitive liquidated damages based on annual contract value rather than service fees, creating an uninsurable liability profile.
