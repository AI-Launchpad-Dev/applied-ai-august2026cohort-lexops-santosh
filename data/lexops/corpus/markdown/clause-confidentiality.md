# Playbook: Confidentiality

**NORTHWIND SYSTEMS ENTERPRISE NEGOTIATION PLAYBOOK**
**SECTION 4: CONFIDENTIALITY**
**DOCUMENT ID: NW-PLK-2026-04**
**OWNER: LEGAL & COMPLIANCE**

---

### 4.1 Preferred Position (Model Clause Language)

The Legal Team shall insert the following text without modification as the standard confidentiality provision in all Northwind Enterprise Master Subscription Agreements:

> **4.1 Protection of Confidential Information.** Each party ("Receiving Party") agrees that all code, inventions, business, technical, and financial information disclosed to it by the other party ("Disclosing Party") under this Agreement, including the terms of this Agreement and the pricing hereunder, constitute confidential information of the Disclosing Party ("Confidential Information"). Confidential Information shall not include information that: (a) is or becomes generally known to the public without breach of any obligation owed to the Disclosing Party; (b) was known to the Receiving Party prior to disclosure without confidentiality restrictions; (c) is independently developed by the Receiving Party without reference to or use of the Disclosing Party’s Confidential Information; or (d) is rightfully received from a third party without duty of confidentiality. 
> 
> **4.2 Obligations and Standard of Care.** The Receiving Party shall hold the Disclosing Party’s Confidential Information in strict confidence, shall use at least the same degree of care it uses to protect its own confidential information of like nature (but no less than a reasonable standard of care), and shall not disclose such Confidential Information to any third party except to its employees, contractors, legal counsel, and financial advisors who need to know such information and are bound by confidentiality obligations at least as restrictive as those herein. 
> 
> **4.3 Compelled Disclosure.** If the Receiving Party is legally compelled by deposition, interrogatory, request for documents, subpoena, civil investigative demand, or similar judicial or regulatory process to disclose any Confidential Information, the Receiving Party shall, to the extent legally permitted, provide the Disclosing Party with prompt written notice of at least **ten (10) business days** prior to such disclosure to allow the Disclosing Party to seek a protective order or other appropriate remedy.
> 
> **4.4 Duration and Destruction.** The obligations under this Section 4 shall survive the termination or expiration of this Agreement for a period of **five (5) years**, except that trade secrets shall be protected for as long as they qualify as trade secrets under applicable law. Upon termination of this Agreement or written request, the Receiving Party shall promptly destroy or return all tangible Confidential Information, provided that the Receiving Party may retain one (1) copy of Confidential Information solely for archival, legal, and compliance audit purposes, subject to continuing confidentiality obligations.

---

### 4.2 Fallback Position

If the counterparty rejects the Preferred Position, the Legal Team is authorized to concede the following modifications sequentially before escalating:

1. **Duration:** The survival period in Section 4.4 may be reduced from five (5) years to **three (3) years** post-termination, provided trade secrets retain perpetual protection.
2. **Notice of Compelled Disclosure:** The notice period in Section 4.3 may be reduced from ten (10) business days to **five (5) business days**, or "prompt written notice prior to disclosure" if five days is prohibited by court order, provided Northwind retains the right to intervene.
3. **Return of Data:** The return/destruction obligation in Section 4.4 may permit automated back-up tape retention under standard disaster recovery cycles, provided such backups are overwritten in the ordinary course of business within **ninety (90) days** and remain encrypted.

---

### 4.3 Walk-Away Position

The Legal Team shall terminate negotiations or refuse contract execution if the counterparty insists on any of the following terms regarding confidentiality:

1. **Perpetual General Confidentiality:** Insistence on a perpetual confidentiality obligation for non-trade secret operational or commercial data without a termination threshold.
2. **Unilateral Definition Exclusions:** Inclusion of language that allows the counterparty to claim independent development of Northwind's core SaaS architecture or AI models based on generalized market knowledge.
3. **No-Injunctive-Relief Clauses:** Any provision waiving Northwind's right to seek injunctive or equitable relief for breach of confidentiality without proof of actual monetary damages.
4. **Publicity Restrictions:** Complete prohibition on Northwind naming the customer as a reference or using its logo, where the deal value falls below standard enterprise thresholds requiring mutual non-disclosure of the relationship itself (see Section 9 for marketing rights).

---

### 4.4 Numeric and Categorical Thresholds

The following hard floors, caps, and timelines govern all confidentiality evaluations:

* **Survival Period Floor:** **Three (3) years** post-termination (absolute minimum for general confidential information; trade secrets must remain protected indefinitely).
* **Compelled Disclosure Notice Floor:** **Five (5) business days** (absolute minimum notice required to enable Northwind to file a motion to quash or seek a protective order).
* **Backup Data Retention Cap:** **Ninety (90) days** maximum retention window for disaster recovery archives containing Confidential Information.
* **Damages / Liability Cap Multiplier:** Confidentiality breaches shall be subject to the standard Agreement liability cap of **two times (2x)** the total fees paid or payable by the customer in the preceding twelve (12) month period, unless carving out IP theft or intentional bad-faith disclosure (which requires General Counsel sign-off).

---

### 4.5 Named Deviations Requiring Escalation

The following specific deviations from the Playbook are prohibited unless formally escalated to and approved in writing by the designated executive:

1. **Mutual Perpetual Non-Disclosure for Strategic Evaluations:** Any agreement to keep business discussions or evaluation data confidential in perpetuity. *Escalate to: Chief Executive Officer (Marcus Vance).*
2. **Exclusion of Source Code from Trade Secret Protection:** Any counterparty clause attempting to classify Northwind's proprietary backend architecture, algorithms, or API structures as standard commercial information subject to the 3-to-5-year survival drop-off. *Escalate to: Chief Technology Officer (Elena Rostova).*
3. **Uncapped Liability for Confidentiality Breaches:** Acceptance of an unlimited liability cap specifically tied to breaches of confidentiality or data mishandling where no formal SOC 2 Type II or HIPAA Business Associate Agreement applies. *Escalate to: Chief Financial Officer (David Chen).*

---

### 4.6 Worked Examples of Counterparty Language

#### Acceptable Counterparty Language (Approved for Acceptance)

* **Acceptable Example 1:** *"Either party may disclose Confidential Information to its external auditors, accountants, and legal counsel on a need-to-know basis, provided such advisors are bound by professional ethical duties of confidentiality or written agreements no less restrictive than those herein."*
  * *Rationale:* Standard professional advisor carve-out; does not weaken Northwind's protections and aligns with standard corporate practice.

* **Acceptable Example 2:** *"If Receiving Party is required by law to disclose Confidential Information, it shall provide prompt written notice to Disclosing Party, cooperate in Disclosing Party's efforts to obtain a protective order, and disclose only that portion of the Confidential Information legally required to be disclosed."*
  * *Rationale:* Aligns with the fallback position on compelled disclosure; maintains Northwind's right to protect its assets while accommodating statutory requirements.

#### Unacceptable Counterparty Language (Rejected / Requires Escalation)

* **Unacceptable Example 1:** *"Confidential Information shall not include any information that the Receiving Party can demonstrate was independently conceived or developed by its personnel without access to the Disclosing Party's specific disclosures, even if such development occurs concurrently with the performance of this Agreement."*
  * *Rationale:* **Walk-Away Trigger.** The phrase "concurrently with the performance of this Agreement" creates an unacceptable carve-out that permits the counterparty to reverse-engineer Northwind's platform while under contract and claim independent development.

* **Unacceptable Example 2:** *"Either party may terminate the confidentiality obligations herein upon providing thirty (30) days' prior written notice to the other party, after which all restrictions on the use of disclosed data shall cease."*
  * *Rationale:* **Escalation Required.** This completely undermines the structural integrity of the agreement by allowing unilateral termination of trade secret and proprietary protections post-contract.
