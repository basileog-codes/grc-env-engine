# GRC Environment Simulation Engine (grc-env-engine)

This repository serves as my personal lab environment for studying Governance, Risk, and Compliance (GRC) and Information Technology General Controls (ITGC). It contains both the custom tools I write to simulate corporate workflows and my analysis files for individual compliance case studies.

My goal with this workspace is to bridge the gap between computer science concepts and practical risk management frameworks.

---

## Repository Structure

/tools/
This directory holds the engineering tools I build to automate or simulate compliance tasks.
* /env_engine/ - A custom Python script designed to simulate the administrative delays, local database state tracking, and stakeholder communication friction that occur during real-world audit fieldwork.

/labs/
This directory holds my documentation and evidence files for individual labs across different training platforms.
* /meridian_financial/ - An ITGC case study focused on a mid-sized fintech company with a $2B transaction volume, evaluating access controls and change management within a DevOps model.

---

## My Audit Methodology

When analyzing systems in the lab folders, I document all control failures and deficiencies using the standard CCCEE structure:

1. Condition: What gap or exception was discovered in the evidence.
2. Criteria: What specific policy, framework, or regulation was violated.
3. Cause: Why the system or process failed.
4. Effect: The actual financial, operational, or security risk to the business.
5. Evaluation: Actionable recommendations to remediate the issue.

---

## Active Work & Status

* Meridian Financial Case Study: Mapping out the database access logs and cross-referencing user permissions under the /labs/ directory.
* Environment Engine Tool: Local workspace and Git configurations are initialized; developing the core Python logic engine next under the /tools/ directory.
