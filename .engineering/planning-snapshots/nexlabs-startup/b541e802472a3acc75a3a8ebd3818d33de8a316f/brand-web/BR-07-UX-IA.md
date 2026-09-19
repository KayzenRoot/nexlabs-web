# BR-07 — UX & Information Architecture

Status: PROPOSED
Date: 2026-09-19
Primary objective: institutional credibility + product discovery + program readiness

## 1. UX principle
The website serves two simultaneous modes:

### FAST TRUST
For program reviewers, investors, journalists or visitors with limited time.
They must understand NexLabs and verify legitimacy quickly.

### DEEP EXPLORE
For developers and technically curious visitors.
They can explore HIVE, technology concepts, open-source evidence and interactive 3D storytelling.

Neither path depends on completing the other.

## 2. Primary audiences

### A — Program reviewer
Questions:
- Is this a real technology project/startup?
- What does it build?
- Is there working/public evidence?
- Is the company status represented truthfully?
- How do I verify/contact them?

Primary path:
Home → HIVE → Open Source/GitHub → About → Contact.

### B — Developer / OSS visitor
Questions:
- What problem does HIVE solve?
- How does it work?
- Is it open source?
- Where is the repo/docs?
- Can I inspect/use it?

Primary path:
Home → HIVE → GitHub/docs.

### C — Accelerator / investor
Questions:
- What is the company thesis?
- What is the initial wedge?
- Why could this become larger?
- What exists now?
- Who is building it?

Primary path:
Home → Technology/Thesis → HIVE → About → Contact.

### D — Future customer
Questions:
- What practical problem is solved?
- Is there a product I can evaluate?
- Is it trustworthy?
- What should I do next?

Primary path:
Home → HIVE → Product evidence → Contact/GitHub.

## 3. Proposed V1 sitemap

/
Home

/hive
HIVE product page

/technology
NexLabs technology thesis and engineering principles

/open-source
OSS commitment, repositories/evidence

/about
Company story, factual stage/location, founder/company thesis

/contact
Simple contact paths

/privacy
Privacy notice appropriate to actual site behavior

Optional only if justified before launch:
/brand or /press
/resources

Do NOT create empty “Solutions”, “Customers”, “Pricing”, “Careers”, “Partners” or “News” pages merely to look larger.

## 4. Global navigation

Desktop:
NexLabs mark
Technology
HIVE
Open Source
About
[GitHub]
[Contact]

Mobile:
compact mark + accessible menu trigger.
Same information hierarchy.

Navigation remains understandable with JavaScript/3D unavailable.

## 5. Homepage architecture

### H00 — Global header
Immediate brand + primary routes.

### H01 — Hero / Context Core
Brand: NexLabs
Thesis: Infrastructure for AI-native software.
Hero proposition candidate: Build with AI. Keep the system coherent.
Supporting copy explains developer-infrastructure focus.
CTA 1: Explore HIVE
CTA 2: View GitHub
3D: Context Core.

### H02 — Problem
Core idea:
Model capability alone does not preserve the coherence of a long-running software project.

Explain context loss, repeated ingestion, retrieval and governance without fear-based copy.

### H03 — HIVE
Introduce initial flagship.
Show:
- durable project context/memory;
- retrieval;
- token-efficiency mechanisms;
- governed development/execution;
- OSS status.
CTA: Explore HIVE.

### H04 — System Story
Interactive/diagram hybrid.
Visual narrative:
Fragment → Index → Retrieve → Assemble → Resolve.

This section connects brand metaphor to product problem without pretending to be a literal architecture diagram.

### H05 — Engineering Principles
Candidate pillars:
- Context continuity
- Evidence over assumptions
- Efficient retrieval
- Governed execution
- Open engineering

Exact claims checked against HIVE/company truth before launch.

### H06 — Open Source / Evidence
HIVE repository.
Apache-2.0.
Visible links to public technical evidence.
No fake GitHub metrics.

### H07 — NexLabs Thesis
Expand from HIVE to the broader company:
infrastructure around increasingly capable AI development systems.

Do not present unbuilt products as shipped.

### H08 — About / Origin
Built from Brazil for a global market.
Pre-incorporation status need not dominate marketing copy, but factual company/legal representations must remain accurate.

### H09 — Contact / Final CTA
Developer: GitHub.
Program/investor/business: contact.
No fake office address.

### H10 — Footer
NexLabs Technology.
Navigation.
GitHub.
Contact.
Privacy.
Factual copyright/brand line.

## 6. 60-second credibility path

Within one minute, without interacting with 3D, a reviewer should find:
0–10 s: NexLabs name + what it builds.
10–20 s: HIVE exists and has a clear purpose.
20–35 s: public OSS/GitHub evidence.
35–50 s: company thesis and Brazil/global context.
50–60 s: contact route and institutional identity.

## 7. HIVE page

### P01 Hero
What HIVE is.

### P02 Problem
Context continuity / repeated context / governance challenge.

### P03 Capability map
Use evidence-backed capabilities only.

### P04 Architecture story
High-level diagram based on canonical HIVE documentation.

### P05 Open source
License/repository/docs.

### P06 Evidence
Tests/release/security/docs as verifiable, current evidence.

### P07 CTA
GitHub / documentation.

No pricing or hosted-product promise unless actually available.

## 8. Technology page
Purpose: company thesis, not fake research publication.

Sections:
- AI-native software infrastructure thesis;
- context as infrastructure;
- retrieval and efficiency;
- governance/evidence;
- open systems/interoperability direction;
- HIVE as current implementation evidence.

Future concepts explicitly labeled research/direction where applicable.

## 9. Open Source page
Purpose:
- why NexLabs uses OSS strategically;
- HIVE;
- license;
- repository links;
- contribution/security links where current.

Do not imply a large OSS community without evidence.

## 10. About page
Content:
- NexLabs Technology;
- company thesis;
- built from Brazil, global-market intent;
- current stage represented accurately;
- founder section only with founder-approved public details;
- HIVE as initial flagship;
- contact.

Avoid invented office/team photography.

## 11. Contact page
V1 should minimize infrastructure.

Preferred contact methods:
- founder-approved business email once available;
- GitHub;
- optional simple form only if spam/privacy/hosting implications are solved at BR-09/14.

No phone/home address required for marketing presentation unless legally necessary.

## 12. Privacy
Privacy page reflects actual behavior.
If no analytics/form/cookies, do not copy a giant template claiming systems we do not use.
If analytics/form is added, disclose accurately.

## 13. CTA hierarchy
Primary product CTA: Explore HIVE.
Primary evidence CTA: View GitHub.
Institutional CTA: Contact NexLabs.

Avoid multiple competing primary buttons in each viewport.

## 14. 3D allocation
Home Hero: high-value interactive 3D.
System Story: technical 3D/diagram hybrid.
Other pages: lighter reused visual grammar.
Do not run a full hero-grade scene on every page.

## 15. Mobile IA
Preserve content order.
Move evidence upward where needed.
Do not force mobile visitors through large visual scenes before product explanation.
Use simplified/static 3D when performance controller chooses it.

## 16. SEO information architecture
Each indexable page has:
- unique title;
- unique description;
- canonical URL;
- structured headings;
- meaningful internal links;
- OG/social metadata;
- crawlable semantic content independent of canvas.

Structured data is added only when schema truthfully matches the organization/product state.

## 17. Empty-state rule
A smaller truthful site is better than a large empty corporate shell.
No page exists unless it provides useful, factual content.

## 18. Acceptance criteria
BR-07 freezes when:
- sitemap approved;
- every page has a purpose and primary CTA;
- four audience journeys are complete;
- 60-second credibility path works without 3D;
- mobile hierarchy is defined;
- no empty/fake corporate pages exist;
- content requirements are sufficient for BR-08;
- architecture is compatible with BR-09 technical planning.
