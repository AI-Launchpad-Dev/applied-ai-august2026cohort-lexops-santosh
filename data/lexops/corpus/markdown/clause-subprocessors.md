# Playbook: Subprocessor Approval

# NORTHWIND SYSTEMS INTERNAL NEGOTIATION PLAYBOOK
## SECTION 14: SUBPROCESSOR APPROVAL AND MANAGEMENT

### 14.1 Preferred Position (Model Clause Language)

Northwind Systems shall maintain the right to engage third-party subprocessors to process Customer Personal Data in connection with the provision of the Services, provided that Northwind Systems complies with the conditions set forth in this Section 14.1.

1. **General Authorization.** Customer hereby provides general written authorization for Northwind Systems to engage the subprocessors listed in the Northwind Subprocessor Repository, accessible at `https://legal.northwind-systems.com/subprocessors`, as of the Effective Date.
2. **Notice of New Subprocessors.** Northwind Systems shall notify Customer of any intended addition or replacement of any subprocessor at least thirty (30) days prior to such subprocessor processing any Customer Personal Data, by updating the Subprocessor Repository or by sending an email notification to the administrative contact designated in the Order Form.
3. **Objection Right.** Customer may object to Northwind Systems’ appointment of a new subprocessor on reasonable data protection grounds by providing written notice to Northwind Systems within fourteen (14) days of receiving notice pursuant to Section 14.1(2). Such objection notice must set out the specific objective data protection reasons for the objection.
4. **Resolution and Termination.** Upon receipt of a timely objection pursuant to Section 14.1(3), Northwind Systems shall use commercially reasonable efforts to make available to Customer a change in the Services or recommend a commercially reasonable change to avoid the processing of Customer Personal Data by the objected-to subprocessor. If Northwind Systems is unable to provide such alternative within thirty (30) days of receipt of the objection, either party may terminate the affected Order Form upon written notice, without penalty, provided that Customer shall pay for Services rendered up to the date of termination. Failure to object within fourteen (14) days shall be deemed approval of the new subprocessor.

---

### 14.2 Fallback Position

If Customer rejects the Preferred Position during negotiations, the legal team is authorized to execute the following fallback terms:

1. **Shortened Notice Window.** The notice period for new subprocessors under Section 14.1(2) may be reduced to twenty-one (21) days, provided the objection window under Section 14.1(3) is adjusted to ten (10) days.
2. **Specific Affiliate Exception.** Northwind Systems may explicitly exempt its wholly owned corporate affiliate, Northwind Data Ops Inc., from the objection mechanism, provided such entity is bound by data protection obligations no less restrictive than those applicable to Northwind Systems under the Agreement.
3. **Cure Period Extension.** The resolution period under Section 14.1(4) may be extended from thirty (30) days to forty-five (45) days to allow Northwind Systems sufficient time to source alternative infrastructure providers.

---

### 14.3 Walk-Away Position

Legal counsel must terminate negotiations or reject the contract if the counterparty demands any of the following terms regarding subprocessors:

1. **Prior Specific Written Consent.** Any requirement for prior, specific, non-general written consent or positive opt-in for every individual subprocessor.
2. **Unilateral Veto Without Termination Rights.** A right for Customer to veto or prohibit a subprocessor without granting Northwind Systems the corresponding right to terminate the contract if the veto prevents service delivery.
3. **Financial Penalties on Subprocessor Changes.** Any provision imposing financial penalties, retroactive fee refunds, or liquidated damages linked directly to the addition or replacement of a subprocessor.
4. **Jurisdictional Restrictions Requiring Pre-Approval.** A blanket prohibition on subprocessing outside of the European Economic Area (EEA) or United States that cannot be cured by standard contractual clauses or equivalent transfer mechanisms, or any clause requiring individual legal review and sign-off for each subprocessor located in Tier-2 or Tier-3 jurisdictions as classified by Northwind Security.

---

### 14.4 Numeric and Categorical Thresholds

The following strict thresholds govern all subprocessor negotiations and operational exception handling:

1. **Notice Period Threshold:** Minimum acceptable notice period for new subprocessor additions is **fourteen (14) days**. Under no circumstances shall Northwind accept a notice period below fourteen (14) days.
2. **Objection Cure Period Threshold:** The maximum cure or remediation period granted to Northwind Systems to resolve a subprocessor objection before termination rights accrue is **thirty (30) days** (extendable to forty-five (45) days under Fallback, Section 14.2).
3. **Subprocessor Liability Cap Multiple:** Total aggregate liability arising from a subprocessor data breach or unauthorized disclosure attributable to Northwind Systems' failure to vet a subprocessor shall be capped at **two times (2x)** the total fees paid or payable by Customer under the applicable Order Form in the preceding twelve (12) months, subject to the overall Master Services Agreement liability cap.
4. **Monetary Floor for Individual Indemnity Claims:** No subprocessor-related indemnity claim or fee clawback shall be processed unless the verified direct damages exceed a monetary floor of **fifty thousand United States Dollars ($50,000 USD)** per occurrence.

---

### 14.5 Named Deviations Requiring Escalation

Any contract modification that falls outside the Fallback Position requires formal written approval from the designated internal authority before signature:

1. **Waiver of General Authorization for Core Cloud Infrastructure:** If a customer insists on approving AWS, Microsoft Azure, or Snowflake as primary cloud subprocessing infrastructure, the deviation must be escalated to **Chief Technology Officer (CTO) Marcus Vance** and **Chief Information Security Officer (CISO) Elena Rostova** for operational feasibility review.
2. **Acceptance of Customer-Mandated Specific Subprocessors:** If a customer demands that Northwind use a specific subprocessor nominated by the Customer (e.g., a specific localization vendor or security monitor), the deviation must be escalated to **VP of Engineering Sarah Jenkins** to confirm API compatibility and security integration.
3. **Unlimited or Super-Capped Liability for Subprocessor Actions:** If a customer demands liability for subprocessor defaults that exceeds the 2x fee multiple or pierces the general liability cap, the deviation must be escalated to **Chief Executive Officer (CEO) Arthur Pendelton** and **General Counsel Victoria Sterling**.

---

### 14.6 Worked Examples of Counterparty Language

#### Acceptable Counterparty Language (Passed by Legal)

* **Example 1 (Notice via RSS/Portal):** 
  > "Vendor shall provide Customer with at least thirty (30) days’ prior notice of any intended addition or replacement of a subprocessor by updating its online subprocessor portal and notifying Customer's designated security contact via electronic mail. Customer may object on reasonable data protection grounds within fourteen (14) days of such notice."
  * *Rationale:* Matches Preferred Position intent, provides clear mechanics, and preserves operational flexibility.

* **Example 2 (Bifurcated Affiliate/Infrastructure Rule):** 
  > "Notwithstanding Section 14.1, Vendor may utilize its affiliated entities and Tier-1 cloud service providers (Amazon Web Services and Microsoft Azure) as subprocessors without individual prior notice, provided that Vendor maintains a publicly accessible list updated at least fifteen (15) days prior to onboarding any new non-affiliated subprocessor."
  * *Rationale:* Carves out standard hyperscalers and affiliates, which aligns with Northwind infrastructure realities without triggering walk-away criteria.

#### Unacceptable Counterparty Language (Rejected by Legal)

* **Example 1 (Prior Written Consent Mandate):** 
  > "Vendor shall not appoint a third-party subprocessor to process Customer Data without the prior specific written consent of Customer, which consent shall not be unreasonably withheld, delayed, or conditioned. Any unauthorized subprocessor appointment shall constitute a material breach incapable of cure."
  * *Rationale:* Violates Walk-Away Position 1 (Prior Specific Written Consent) and removes unilateral termination balance.

* **Example 2 (Financial Penalty Clause):** 
  > "If Customer objects to a new subprocessor and Vendor cannot provide an alternative within fifteen (15) days, Customer may terminate the Agreement and receive an immediate pro-rata refund of all prepaid fees for the remainder of the term, plus a liquidated damages penalty equal to six (6) months of recurring fees."
  * *Rationale:* Violates Walk-Away Position 3 (Financial penalties / fee refunds linked to subprocessor changes) and exceeds liability caps.
