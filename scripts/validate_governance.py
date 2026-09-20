from __future__ import annotations

import json
import hashlib
import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "7dac49b7d9182333e58dd1267c33489631d7e65d"
PLANNING = "b541e802472a3acc75a3a8ebd3818d33de8a316f"
GEF = "866fe3af8cccc65c929aaf6a47a924401fa448b3"
HIVE = "a53b5b9fcf55c32a5696180fb1b1ef80ccd1edcf"
WORK_ORDER = "NXWEB-WO-0001-CP02-GEF-HIVE-ADOPTION"
LOCK = "NXWEB-LOCK-0001-CP02-GEF-HIVE-ADOPTION"
HIVE_TOOLS = {"project.list", "project.status", "context.build", "context.search", "memory.search", "memory.get", "checkpoint.read"}

REQUIRED = (
    "AGENTS.md", ".codex/config.toml", ".engineering/BOOTSTRAP-MANIFEST.json", ".engineering/PROJECT-OVERVIEW.md",
    ".engineering/SOURCE-HIERARCHY.md", ".engineering/CHECKPOINT.md", ".engineering/CHECKPOINT.json",
    ".engineering/GITHUB-GOVERNANCE-TARGET.md", ".engineering/gef/GEF-ADOPTION.md", ".engineering/gef/GEF-BASELINE.json",
    ".engineering/gef/GEF-CURRENT.json", ".engineering/gef/GEF-EVIDENCE-SPEC.md", ".engineering/gef/GEF-EXECUTION-PROTOCOL.md",
    ".engineering/gef/GEF-POLICY.md", ".engineering/gef/GEF-PROJECT-PROFILE.json", ".engineering/gef/GEF-REVIEW-PROTOCOL.md",
    ".engineering/gef/GEF-SOURCE-BRIDGE.json", ".engineering/work-orders/NXWEB-WO-0001-CP02-GEF-HIVE-ADOPTION.md",
    ".engineering/context-locks/NXWEB-LOCK-0001-CP02-GEF-HIVE-ADOPTION.json", ".engineering/evidence/NXWEB-WO-0001-CP02-GEF-HIVE-ADOPTION.json",
    "docs/project-brain/00-README-UPLOAD-ORDER.md", "docs/project-brain/01-PROJECT-OVERVIEW.md", "docs/project-brain/02-REQUIREMENTS.md",
    "docs/project-brain/03-SCOPE.md", "docs/project-brain/04-ARCHITECTURE.md", "docs/project-brain/10-SECURITY-GOVERNANCE.md",
    "docs/project-brain/11-TEST-PLAN.md", "docs/project-brain/12-LOCAL-DEPLOYMENT.md", "docs/project-brain/13-CHECKPOINT.md",
    "docs/project-brain/14-BACKLOG.md", "docs/project-brain/15-DEFINITION-OF-DONE.md", "docs/project-brain/16-DECISIONS-LEDGER.md",
    "docs/project-brain/17-BRAND-WEB-SOURCE-MAP.md", "scripts/hive_bootstrap.py", "scripts/hive_prepare.py", "scripts/hive_mcp.py",
    "tests/test_hive_prepare.py", ".github/workflows/governance.yml",
)


def fail(message: str) -> None:
    raise SystemExit(f"GOVERNANCE VALIDATION FAILED: {message}")


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def data(relative: str) -> dict:
    try:
        value = json.loads(read(relative))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON {relative}: {exc}")
    if not isinstance(value, dict):
        fail(f"JSON root is not an object: {relative}")
    return value


def section(text: str, heading: str) -> str:
    lines = text.splitlines()
    if heading not in lines:
        fail(f"missing checkpoint heading: {heading}")
    start = lines.index(heading) + 1
    values = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        if line.strip():
            values.append(line.strip())
    if not values:
        fail(f"checkpoint heading has no value: {heading}")
    return "\n".join(values)


for relative in REQUIRED:
    if not (ROOT / relative).is_file():
        fail(f"missing required file: {relative}")

canonical = read("docs/project-brain/13-CHECKPOINT.md")
bridge = read(".engineering/CHECKPOINT.md")
machine = data(".engineering/CHECKPOINT.json")
for heading in ("## STATUS", "## VERSION", "## PHASE", "## OBJECTIVE", "## IN PROGRESS", "## BLOCKERS", "## NEXT STEP"):
    canonical_value = section(canonical, heading)
    if section(bridge, heading) != canonical_value:
        fail(f"checkpoint bridge drift: {heading}")
field_map = {"status": "## STATUS", "version": "## VERSION", "phase": "## PHASE", "objective": "## OBJECTIVE", "inProgress": "## IN PROGRESS", "blockers": "## BLOCKERS", "nextStep": "## NEXT STEP"}
if machine.get("canonicalCheckpoint") != "docs/project-brain/13-CHECKPOINT.md":
    fail("machine checkpoint canonical path mismatch")
for field, heading in field_map.items():
    if machine.get(field) != section(canonical, heading):
        fail(f"machine checkpoint drift: {field}")

current = data(".engineering/gef/GEF-CURRENT.json")
CP03_WORK_ORDER = "NXWEB-WO-0002-CP03-INSTITUTIONAL-PAGES"
CP03_LOCK = "NXWEB-LOCK-0002-CP03-INSTITUTIONAL-PAGES"
cp03_closed = current.get("lastCompletedWorkOrder") == CP03_WORK_ORDER and current.get("productStage") == "CP03_COMPLETE"
cp03_active = current.get("adoptionState") == "GEF_V1_CP03_ADMITTED" and current.get("activeWorkOrder") == CP03_WORK_ORDER

manifest = data(".engineering/BOOTSTRAP-MANIFEST.json")
if manifest.get("project") != "KayzenRoot/nexlabs-web" or manifest.get("mode") != "EXISTING_PROJECT / BROWNFIELD":
    fail("bootstrap identity mismatch")
if manifest.get("planningSource", {}).get("commit") != PLANNING:
    fail("planning source binding mismatch")
if manifest.get("gef", {}).get("releaseCommit") != GEF or manifest.get("gef", {}).get("version") != "1.0.0":
    fail("GEF pin mismatch")
if manifest.get("hive", {}).get("releaseCommit") != HIVE or manifest.get("hive", {}).get("version") != "1.0.0":
    fail("HIVE pin mismatch")

profile = data(".engineering/gef/GEF-PROJECT-PROFILE.json")
if profile.get("gefVersion") != "1.0.0" or profile.get("pinnedUpstreams", {}).get("planning") != PLANNING:
    fail("GEF profile pin mismatch")
expected_hierarchy = ["docs/project-brain/13-CHECKPOINT.md", "docs/project-brain/16-DECISIONS-LEDGER.md", "docs/project-brain/03-SCOPE.md", "docs/project-brain/15-DEFINITION-OF-DONE.md", "docs/project-brain/04-ARCHITECTURE.md", "docs/project-brain/02-REQUIREMENTS.md"]
if profile.get("sourceHierarchy", [])[:6] != expected_hierarchy:
    fail("source hierarchy order mismatch")
source_bridge = data(".engineering/gef/GEF-SOURCE-BRIDGE.json")
if source_bridge.get("canonicalCheckpoint") != "docs/project-brain/13-CHECKPOINT.md":
    fail("GEF source bridge checkpoint mismatch")
for domain, path in {"PROJECT_STATE": "docs/project-brain/13-CHECKPOINT.md", "DECISION": "docs/project-brain/16-DECISIONS-LEDGER.md", "SCOPE": "docs/project-brain/03-SCOPE.md", "REQUIREMENT": "docs/project-brain/02-REQUIREMENTS.md", "ARCHITECTURE": "docs/project-brain/04-ARCHITECTURE.md", "SECURITY": "docs/project-brain/10-SECURITY-GOVERNANCE.md", "COMPLETION": "docs/project-brain/15-DEFINITION-OF-DONE.md", "VALIDATION": "docs/project-brain/11-TEST-PLAN.md", "DEPLOYMENT": "docs/project-brain/12-LOCAL-DEPLOYMENT.md"}.items():
    if source_bridge.get("domains", {}).get(domain) != path:
        fail(f"source bridge mismatch: {domain}")

if cp03_closed:
    work_order = read(".engineering/work-orders/NXWEB-WO-0002-CP03-INSTITUTIONAL-PAGES.md")
    lock = data(".engineering/context-locks/NXWEB-LOCK-0002-CP03-INSTITUTIONAL-PAGES.json")
    evidence = data(".engineering/evidence/NXWEB-WO-0002-CP03-INSTITUTIONAL-PAGES.json")
    if current.get("lastCompletedWorkOrder") != CP03_WORK_ORDER or current.get("activeWorkOrder") not in {None, ""} or current.get("activeContextLock") not in {None, ""}:
        fail("CP-03 closure must have no active Work Order or Context Lock")
    if lock.get("workOrder") != CP03_WORK_ORDER or lock.get("lockId") != CP03_LOCK:
        fail("CP-03 closed Work Order and Context Lock identity mismatch")
    if lock.get("authorizedBase") != "d94f9b5520834ef05d0adc735ac7422068780ae1" or lock.get("planningSource") != PLANNING:
        fail("CP-03 closed Context Lock base/source mismatch")
    expected_digest = hashlib.sha256((ROOT / ".engineering/work-orders/NXWEB-WO-0002-CP03-INSTITUTIONAL-PAGES.md").read_bytes()).hexdigest()
    execution_digest = "a73c512ab90fc8162e7d562cdbfd1d2ae30e2059c99b6ee0a37cbcf94d23c575"
    if lock.get("workOrderSha256") != expected_digest or lock.get("executionWorkOrderSha256") != execution_digest:
        fail("CP-03 closed Context Lock Work Order digest binding mismatch")
    if evidence.get("workOrder", {}).get("id") != CP03_WORK_ORDER or evidence.get("contextLock", {}).get("id") != CP03_LOCK:
        fail("CP-03 closure evidence Work Order and Context Lock identity mismatch")
    if evidence.get("workOrder", {}).get("sha256") != expected_digest or evidence.get("contextLock", {}).get("workOrderSha256") != expected_digest:
        fail("CP-03 closure evidence Work Order digest mismatch")
    if evidence.get("workOrder", {}).get("executionSha256") != execution_digest or evidence.get("contextLock", {}).get("executionWorkOrderSha256") != execution_digest:
        fail("CP-03 closure evidence lost the execution Work Order digest")
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"cannot resolve Git HEAD: {exc}")
    reviewed = lock.get("reviewedCandidateHead")
    promotion_anchor = lock.get("promotionAnchor")
    if not isinstance(reviewed, str) or not reviewed or lock.get("candidateHead") != reviewed or lock.get("candidateHeadRole") != "independent_review_input_head":
        fail("CP-03 closed Context Lock reviewed candidate binding is missing or untyped")
    if promotion_anchor != "d8760304bc7b156ae82b725ff787f0be461d45a3" or lock.get("promotionAnchorRole") != "protected_squash_merge_anchor":
        fail("CP-03 squash promotion anchor is missing or untyped")
    if lock.get("reviewReceiptHead") != promotion_anchor or lock.get("reviewReceiptHeadRole") != "protected_squash_merge_anchor":
        fail("CP-03 closed review receipt is not bound to the protected squash anchor")

    def is_cp03_closure_ancestor(ancestor: str, descendant: str) -> bool:
        try:
            subprocess.run(["git", "merge-base", "--is-ancestor", ancestor, descendant], cwd=ROOT, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            return False

    if not is_cp03_closure_ancestor(promotion_anchor, head):
        fail(f"CP-03 protected squash promotion anchor {promotion_anchor} is not an ancestor of exact Git HEAD {head}")
    try:
        reviewed_tree = subprocess.check_output(["git", "rev-parse", f"{reviewed}^{{tree}}"], cwd=ROOT, text=True).strip()
        promotion_tree = subprocess.check_output(["git", "rev-parse", f"{promotion_anchor}^{{tree}}"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"CP-03 squash tree proof could not be resolved: {exc}")
    if reviewed_tree != promotion_tree:
        fail(f"CP-03 reviewed head tree {reviewed_tree} differs from squash promotion tree {promotion_tree}")
    if lock.get("reviewedHeadTree") != reviewed_tree or lock.get("promotionAnchorTree") != promotion_tree:
        fail("CP-03 Context Lock tree proof does not match Git")
    if current.get("productStage") != "CP03_COMPLETE" or current.get("reviewState") != "CP03_COMPLETE_CANDIDATE":
        fail("CP-03 GEF state is not the protected squash completion candidate state")
    if current.get("nextLegalAction") != "ADMIT_CP04_WITH_NEW_WORK_ORDER" or current.get("activeWorkOrder") not in {None, ""} or current.get("activeContextLock") not in {None, ""}:
        fail("CP-03 completion must stop before CP-04 admission")
    if lock.get("status") != "CLOSED":
        fail("CP-03 completion requires a CLOSED Context Lock")
    if "Status: `COMPLETED`" not in work_order:
        fail("CP-03 completion requires a COMPLETED Work Order")
    hierarchy = read(".engineering/SOURCE-HIERARCHY.md")
    if "Status: `CP03_COMPLETE_READY_FOR_NEXT_ADMISSION`" not in hierarchy:
        fail("CP-03 Source Hierarchy is not closed for the next admission")
    if evidence.get("verdict") != "APPROVED" or evidence.get("reviewState") != "CP03_COMPLETE_CANDIDATE":
        fail("CP-03 evidence does not describe the corrected completion candidate")
    if evidence.get("git", {}).get("proofHead") != promotion_anchor or evidence.get("git", {}).get("reviewedCandidateHead") != reviewed:
        fail("CP-03 closure evidence reviewed/promotion head mismatch")
    if evidence.get("git", {}).get("reviewReceiptHead") != promotion_anchor:
        fail("CP-03 closure evidence review receipt mismatch")
    if evidence.get("git", {}).get("reviewedHeadTree") != reviewed_tree or evidence.get("git", {}).get("promotionAnchorTree") != promotion_tree:
        fail("CP-03 closure evidence tree proof mismatch")
    hosted = evidence.get("hosted", {})
    merged_pr = hosted.get("mergedPullRequest", {})
    if merged_pr.get("number") != 19 or merged_pr.get("status") != "MERGED" or merged_pr.get("mergeMethod") != "SQUASH" or merged_pr.get("reviewedHead") != reviewed or merged_pr.get("mergeSha") != promotion_anchor:
        fail("CP-03 merged PR evidence does not bind the reviewed head to the squash anchor")
    promotion = hosted.get("promotion", {})
    if promotion.get("reviewedHead") != reviewed or promotion.get("promotionAnchor") != promotion_anchor or promotion.get("reviewedHeadTree") != reviewed_tree or promotion.get("promotionAnchorTree") != promotion_tree or promotion.get("treeEquivalent") is not True:
        fail("CP-03 hosted squash promotion tree proof is incomplete")
    pre_merge = hosted.get("preMergeChecks", {})
    if pre_merge.get("head") != reviewed or pre_merge.get("quality", {}).get("status") != "PASS" or pre_merge.get("Governance", {}).get("status") != "PASS":
        fail("CP-03 pre-merge checks are not PASS on the reviewed head")
    initial_post_merge = hosted.get("initialPostMergeChecks", {})
    if initial_post_merge.get("head") != promotion_anchor or initial_post_merge.get("classification") != "SQUASH_PROMOTION_LINEAGE_FALSE_NEGATIVE" or initial_post_merge.get("quality", {}).get("status") != "FAILURE" or initial_post_merge.get("Governance", {}).get("status") != "FAILURE":
        fail("CP-03 initial post-merge failure classification is missing")
    correction_pr = hosted.get("correctionPullRequest", {})
    if correction_pr.get("merge") != "NOT_EXECUTED" or correction_pr.get("postMergeChecks") != "NOT_CLAIMED":
        fail("CP-03 correction PR must remain unmerged with no post-merge claim")
    for heading in ("## OBJECTIVE", "## CONTEXT/HIVE PREFLIGHT", "## CANONICAL BASIS", "## SCOPE", "## OUT OF SCOPE", "## FILES/SOURCES TO READ", "## REQUIREMENTS", "## ARCHITECTURE RULES", "## CONSTRAINTS", "## ACCEPTANCE CRITERIA", "## TESTS", "## DELIVERABLES", "## REVIEW FORMAT", "## STOP CONDITION", "## EXECUTION REFERENCES / CANONICAL REFERENCES"):
        if heading not in work_order:
            fail(f"CP-03 Work Order missing section: {heading}")
elif cp03_active:
    work_order = read(".engineering/work-orders/NXWEB-WO-0002-CP03-INSTITUTIONAL-PAGES.md")
    lock = data(".engineering/context-locks/NXWEB-LOCK-0002-CP03-INSTITUTIONAL-PAGES.json")
    evidence = data(".engineering/evidence/NXWEB-WO-0002-CP03-INSTITUTIONAL-PAGES.json")
    if current.get("activeWorkOrder") != "NXWEB-WO-0002-CP03-INSTITUTIONAL-PAGES" or current.get("activeContextLock") != "NXWEB-LOCK-0002-CP03-INSTITUTIONAL-PAGES":
        fail("CP-03 active Work Order and Context Lock identity mismatch")
    if lock.get("workOrder") != current.get("activeWorkOrder") or lock.get("lockId") != current.get("activeContextLock"):
        fail("CP-03 Work Order and Context Lock pairing mismatch")
    if lock.get("authorizedBase") != "d94f9b5520834ef05d0adc735ac7422068780ae1" or lock.get("planningSource") != PLANNING:
        fail("CP-03 Context Lock base/source mismatch")
    expected_digest = hashlib.sha256((ROOT / ".engineering/work-orders/NXWEB-WO-0002-CP03-INSTITUTIONAL-PAGES.md").read_bytes()).hexdigest()
    if lock.get("workOrderSha256") != expected_digest:
        fail("CP-03 Context Lock Work Order digest mismatch")
    if evidence.get("workOrder", {}).get("id") != current.get("activeWorkOrder") or evidence.get("contextLock", {}).get("id") != current.get("activeContextLock"):
        fail("CP-03 evidence Work Order and Context Lock identity mismatch")
    if evidence.get("workOrder", {}).get("sha256") != expected_digest or evidence.get("contextLock", {}).get("workOrderSha256") != expected_digest:
        fail("CP-03 evidence Work Order digest mismatch")
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"cannot resolve Git HEAD: {exc}")
    candidate = lock.get("candidateHead")
    reviewed = lock.get("reviewedCandidateHead")
    receipt = lock.get("reviewReceiptHead")
    if not isinstance(candidate, str) or not candidate or not isinstance(reviewed, str) or not reviewed:
        fail("CP-03 Context Lock candidate head is missing")
    if candidate != reviewed or lock.get("candidateHeadRole") != "independent_review_input_head":
        fail("CP-03 Context Lock candidate/review lineage role mismatch")
    if not isinstance(receipt, str) or not receipt or lock.get("reviewReceiptHeadRole") != "governance_correction_commit_parent_of_evidence_receipt_commit":
        fail("CP-03 Context Lock review receipt head is missing or untyped")

    def is_cp03_ancestor(ancestor: str, descendant: str) -> bool:
        try:
            subprocess.run(["git", "merge-base", "--is-ancestor", ancestor, descendant], cwd=ROOT, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            return False

    try:
        if not is_cp03_ancestor(candidate, head):
            fail(f"CP-03 candidate head {candidate} is not an ancestor of exact Git HEAD {head}")
        if not is_cp03_ancestor(receipt, head):
            fail(f"CP-03 review receipt head {receipt} is not an ancestor of exact Git HEAD {head}")
    except (OSError, subprocess.CalledProcessError):
        fail("CP-03 candidate/review receipt lineage could not be resolved")
    if current.get("productStage") != "CP03_IN_REVIEW" or current.get("reviewState") != "INDEPENDENT_REVIEW_CORRECTION_PENDING":
        fail("CP-03 GEF state is not the independent-review correction state")
    if current.get("nextLegalAction") in {None, "", "PREPARE_HIVE_TASK"}:
        fail("CP-03 GEF next legal action is stale after HIVE preparation")
    if lock.get("status") not in {"OPEN", "ACTIVE"}:
        fail("CP-03 review state requires an OPEN or ACTIVE Context Lock")
    if "Status: `IN_PROGRESS`" not in work_order:
        fail("CP-03 review state requires an IN_PROGRESS Work Order")
    hierarchy = read(".engineering/SOURCE-HIERARCHY.md")
    if "Status: `CP03_IN_REVIEW`" not in hierarchy:
        fail("CP-03 Source Hierarchy is still pre-admission or has an unknown review state")
    if evidence.get("verdict") != "CORRECTION REQUIRED" or evidence.get("reviewState") != "INDEPENDENT_REVIEW_CORRECTION_PENDING":
        fail("CP-03 evidence does not describe the pending independent-review correction")
    if evidence.get("git", {}).get("proofHead") != reviewed or evidence.get("git", {}).get("reviewedCandidateHead") != reviewed:
        fail("CP-03 evidence reviewed candidate head mismatch")
    if evidence.get("git", {}).get("reviewReceiptHead") != receipt:
        fail("CP-03 evidence review receipt head mismatch")
    hosted = evidence.get("hosted", {})
    if hosted.get("remoteBranch", {}).get("status") != "PUBLISHED" or hosted.get("pullRequest", {}).get("number") != 19 or hosted.get("pullRequest", {}).get("status") != "OPEN":
        fail("CP-03 hosted branch or PR evidence is not published/open")
    checks = hosted.get("reviewedCandidateChecks", {})
    if checks.get("head") != reviewed or checks.get("quality", {}).get("status") != "PASS" or checks.get("Governance", {}).get("status") != "PASS":
        fail("CP-03 reviewed candidate hosted checks are not PASS on the exact reviewed head")
    if hosted.get("merge") != "NOT_EXECUTED" or hosted.get("postMergeChecks") != "NOT_CLAIMED":
        fail("CP-03 evidence claims merge or post-merge checks before protected merge")
    for heading in ("## OBJECTIVE", "## CONTEXT/HIVE PREFLIGHT", "## CANONICAL BASIS", "## SCOPE", "## OUT OF SCOPE", "## FILES/SOURCES TO READ", "## REQUIREMENTS", "## ARCHITECTURE RULES", "## CONSTRAINTS", "## ACCEPTANCE CRITERIA", "## TESTS", "## DELIVERABLES", "## REVIEW FORMAT", "## STOP CONDITION", "## EXECUTION REFERENCES / CANONICAL REFERENCES"):
        if heading not in work_order:
            fail(f"CP-03 Work Order missing section: {heading}")
else:
    lock = data(".engineering/context-locks/NXWEB-LOCK-0001-CP02-GEF-HIVE-ADOPTION.json")
    evidence = data(".engineering/evidence/NXWEB-WO-0001-CP02-GEF-HIVE-ADOPTION.json")
    if lock.get("lockId") != LOCK or lock.get("workOrder") != WORK_ORDER or evidence.get("contextLock") != LOCK or evidence.get("workOrder") != WORK_ORDER:
        fail("Work Order and Context Lock pairing mismatch")
    if lock.get("authorizedBase") != BASE or lock.get("planningSource") != PLANNING:
        fail("Context Lock base/source mismatch")
    if evidence.get("authorizedBase") != BASE or evidence.get("planningSource") != PLANNING:
        fail("evidence base/source mismatch")
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"cannot resolve Git HEAD: {exc}")
    try:
        parent_head = subprocess.check_output(["git", "rev-parse", "HEAD^"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"cannot resolve the receipt parent Git HEAD: {exc}")
    candidate_values = {manifest.get("candidateHead"), lock.get("candidateHead"), evidence.get("candidateHead")}
    promotion_anchor = evidence.get("github", {}).get("promotionAnchor")

    def is_ancestor(ancestor: str, descendant: str) -> bool:
        try:
            subprocess.run(["git", "merge-base", "--is-ancestor", ancestor, descendant], cwd=ROOT, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            return False

    if candidate_values == {head}:
        pass
    elif candidate_values == {parent_head} and evidence.get("candidateHeadRole") == "implementation_commit_parent_of_receipt_commit":
        print(f"Receipt commit: {head}; implementation candidate: {parent_head}")
    elif isinstance(promotion_anchor, str) and promotion_anchor and is_ancestor(promotion_anchor, head):
        print(f"Post-merge lineage: promotion anchor {promotion_anchor} is an ancestor of {head}")
    else:
        fail(f"candidate heads {candidate_values!r} do not bind to exact Git HEAD {head}, its declared receipt parent {parent_head}, or a verified promotion anchor")

    work_order = read(".engineering/work-orders/NXWEB-WO-0001-CP02-GEF-HIVE-ADOPTION.md")
    for heading in ("## OBJECTIVE", "## HIVE PREFLIGHT", "## CANONICAL BASIS", "## CONTEXT BUDGET", "## RISK / ASSURANCE", "## SCOPE", "## OUT OF SCOPE", "## FILES / SEAMS", "## REQUIREMENTS", "## ARCHITECTURE RULES", "## CONSTRAINTS", "## ACCEPTANCE CRITERIA", "## TESTS", "## EVIDENCE", "## DELIVERABLES", "## REVIEW FORMAT PT-BR", "## STOP CONDITION"):
        if heading not in work_order:
            fail(f"Work Order missing section: {heading}")
    if WORK_ORDER not in work_order:
        fail("active Work Order identity missing")

try:
    config = tomllib.loads(read(".codex/config.toml"))
except tomllib.TOMLDecodeError as exc:
    fail(f"invalid Codex TOML: {exc}")
server = config.get("mcp_servers", {}).get("hive", {})
if server.get("required") is not True or server.get("enabled") is not True or server.get("command") != "python" or server.get("args") != ["scripts/hive_mcp.py"]:
    fail("HIVE MCP server contract mismatch")
if set(server.get("enabled_tools", [])) != HIVE_TOOLS or len(server.get("enabled_tools", [])) != len(HIVE_TOOLS):
    fail("HIVE MCP tool allowlist mismatch")

prepare_source = read("scripts/hive_prepare.py")
if "activeWorkOrder" not in prepare_source or "GEF_CURRENT" not in prepare_source:
    fail("HIVE preparation must resolve the active GEF Work Order dynamically")
if "DEFAULT_WORK_ORDER" in prepare_source:
    fail("HIVE preparation must not hardcode one lifecycle Work Order as its default")
if "extracted_text_available" not in prepare_source or "intake_status" not in prepare_source:
    fail("HIVE preparation must fail closed on task extraction readiness")

agents_source = read("AGENTS.md")
if "scripts/hive_prepare.py" not in agents_source or "GEF-CURRENT.json" not in agents_source:
    fail("AGENTS HIVE-first preflight must bind preparation to the active GEF Work Order")

governance_files = [ROOT / path for path in REQUIRED] + [ROOT / "scripts/validate_governance.py"]
for path in governance_files:
    text = path.read_text(encoding="utf-8")
    if path.name != "validate_governance.py" and re.search(r"\b(?:TODO|TBD)\b", text, re.IGNORECASE):
        fail(f"unresolved governance placeholder in {path.relative_to(ROOT)}")
    if path.name != "validate_governance.py" and re.search(r"(?<![A-Za-z])(?:[A-Za-z]:[\\/]|/Users/|/home/|/mnt/)", text):
        fail(f"machine-specific absolute path in {path.relative_to(ROOT)}")

adoption_state = current.get("adoptionState")
if cp03_closed:
    if adoption_state != "GEF_V1_CP03_ADMITTED":
        fail("invalid CP-03 completion adoption state")
    if current.get("activeWorkOrder") not in {None, ""} or current.get("activeContextLock") not in {None, ""}:
        fail("completed CP-03 cannot retain an active Work Order or Context Lock")
    if lock.get("status") != "CLOSED":
        fail("completed CP-03 requires a CLOSED Context Lock")
    if evidence.get("verdict") != "APPROVED":
        fail("completed CP-03 requires APPROVED evidence")
    if evidence.get("knownBlockers"):
        fail("completed CP-03 cannot retain known blockers")
    if "Status: `COMPLETED`" not in work_order:
        fail("completed CP-03 requires the Work Order to be marked COMPLETED")
elif cp03_active:
    if adoption_state != "GEF_V1_CP03_ADMITTED":
        fail("invalid CP-03 adoption state")
    if lock.get("status") not in {"OPEN", "ACTIVE"}:
        fail("active CP-03 requires an OPEN or ACTIVE Context Lock")
    if "Status: `IN_PROGRESS`" not in work_order:
        fail("active CP-03 requires an IN_PROGRESS Work Order")
elif adoption_state == "GEF_V1_ADOPTION_IN_PROGRESS":
    if current.get("activeWorkOrder") != WORK_ORDER or current.get("activeContextLock") != LOCK:
        fail("GEF current active identity mismatch")
    if lock.get("status") != "ACTIVE":
        fail("active GEF adoption requires an ACTIVE Context Lock")
elif adoption_state == "GEF_V1_ADOPTED_READY_FOR_GOVERNED_DEVELOPMENT":
    if current.get("activeWorkOrder") not in {None, ""} or current.get("activeContextLock") not in {None, ""}:
        fail("completed GEF adoption cannot retain an active Work Order or Context Lock")
    if current.get("lastCompletedWorkOrder") != WORK_ORDER:
        fail("completed GEF adoption must bind the completed Work Order")
    if lock.get("status") != "CLOSED":
        fail("completed GEF adoption requires a CLOSED Context Lock")
    if evidence.get("verdict") != "APPROVED":
        fail("completed GEF adoption requires APPROVED evidence")
    if evidence.get("knownBlockers"):
        fail("completed GEF adoption cannot retain known blockers")
    required_checks = set(evidence.get("github", {}).get("ruleset", {}).get("requiredChecks", []))
    if not {"quality", "Governance"}.issubset(required_checks):
        fail("completed GEF adoption requires quality and Governance in the ruleset evidence")
    if evidence.get("github", {}).get("postMergeQuality", {}).get("status") != "PASS":
        fail("completed GEF adoption requires a passing post-merge quality receipt")
    if evidence.get("github", {}).get("postMergeGovernance", {}).get("status") != "PASS":
        fail("completed GEF adoption requires a passing post-merge Governance receipt")
    if evidence.get("hive", {}).get("mcp", {}).get("status") != "PASS":
        fail("completed GEF adoption requires verified HIVE MCP evidence")
    if "Status: `COMPLETED`" not in work_order:
        fail("completed GEF adoption requires the Work Order to be marked COMPLETED")
else:
    fail("invalid GEF adoption state")

print("NexLabs Web governance validation: PASS")
print(f"Exact Git HEAD: {head}")
print(f"GEF v1.0.0: {GEF}")
print(f"HIVE v1.0.0: {HIVE}")
print(f"Required governance artifacts: {len(REQUIRED)}")
