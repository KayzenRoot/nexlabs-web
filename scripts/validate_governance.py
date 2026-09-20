from __future__ import annotations

import json
import os
import hashlib
import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "7dac49b7d9182333e58dd1267c33489631d7e65d"
CP05_TRANSITION_BASE = "affd133d9f8650ab91d2f0dd5871220306a3bba0"
CP05_TRANSITION_PDF_SHA256 = "f39f3cdb3127263094c2b279ffcc6818eaf8ff272259b824f31d719931f71754"
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
    ".engineering/evidence/CP05-BLENDER-WORKSTATION-TRANSITION.json", "docs/WORKSTATION-MODE.md",
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
CP04_WORK_ORDER = "NXWEB-WO-0003-CP04-LOGO-EXPLORATION"
CP04_LOCK = "NXWEB-LOCK-0003-CP04-LOGO-EXPLORATION"
CP05_WORK_ORDER = "NXWEB-WO-0004-CP05-BLENDER-CONTEXT-CORE-FOUNDATION"
CP05_LOCK = "NXWEB-LOCK-0004-CP05-BLENDER-CONTEXT-CORE-FOUNDATION"
CP05_RESUME_BASE = "b2737e66d890dff206ac541b4da8b9f42b09c0b1"
cp03_closed = current.get("lastCompletedWorkOrder") == CP03_WORK_ORDER and current.get("productStage") == "CP03_COMPLETE"
cp03_active = current.get("adoptionState") == "GEF_V1_CP03_ADMITTED" and current.get("activeWorkOrder") == CP03_WORK_ORDER
cp04_active = current.get("adoptionState") == "GEF_V1_CP04_ADMITTED" and current.get("activeWorkOrder") == CP04_WORK_ORDER
cp04_closed = current.get("lastCompletedWorkOrder") == CP04_WORK_ORDER and current.get("productStage") == "CP04_COMPLETE" and current.get("reviewState") == "CP04_HG01_SATISFIED" and current.get("nextLegalAction") == "RESUME_CP05_FROM_AUTHORIZED_WORKSTATION"
workstation_transition_active = current.get("adoptionState") == "GEF_V1_CP05_WORKSTATION_TRANSITION_IN_REVIEW" and current.get("productStage") == "CP04_COMPLETE" and current.get("reviewState") == "CP05_WORKSTATION_TRANSITION_IN_REVIEW" and current.get("nextLegalAction") == "RESUME_CP05_AFTER_WORKSTATION_TRANSITION_MERGE" and current.get("activeWorkOrder") in {None, ""} and current.get("activeContextLock") in {None, ""}
cp05_active = current.get("adoptionState") == "GEF_V1_CP05_ADMITTED" and current.get("activeWorkOrder") == CP05_WORK_ORDER and current.get("activeContextLock") == CP05_LOCK

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

if cp05_active:
    work_order = read(f".engineering/work-orders/{CP05_WORK_ORDER}.md")
    lock = data(f".engineering/context-locks/{CP05_LOCK}.json")
    evidence = data(f".engineering/evidence/{CP05_WORK_ORDER}.json")
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"cannot resolve CP-05 resumed Git state: {exc}")
    if branch != "codex/cp05-blender-context-core":
        fail("resumed CP-05 must execute on codex/cp05-blender-context-core")
    if current.get("activeWorkOrder") != CP05_WORK_ORDER or current.get("activeContextLock") != CP05_LOCK:
        fail("CP-05 resumed Work Order and Context Lock identity mismatch")
    if lock.get("workOrder") != CP05_WORK_ORDER or lock.get("lockId") != CP05_LOCK:
        fail("CP-05 resumed Work Order and Context Lock pairing mismatch")
    if lock.get("authorizedBase") != CP05_RESUME_BASE or lock.get("admissionHead") != CP05_TRANSITION_BASE or lock.get("planningSource") != PLANNING:
        fail("CP-05 resumed Context Lock base/source lineage mismatch")
    expected_digest = hashlib.sha256((ROOT / f".engineering/work-orders/{CP05_WORK_ORDER}.md").read_bytes()).hexdigest()
    if expected_digest != "0e4a323eb64834034d836cb7fb138bfa025979e03303c4d65720ae3de248d4b0":
        fail("CP-05 Work Order changed unexpectedly during resume")
    if lock.get("workOrderSha256") != expected_digest:
        fail("CP-05 resumed Context Lock Work Order digest mismatch")
    if evidence.get("workOrder", {}).get("id") != CP05_WORK_ORDER or evidence.get("contextLock", {}).get("id") != CP05_LOCK:
        fail("CP-05 resumed evidence Work Order and Context Lock identity mismatch")
    if evidence.get("workOrder", {}).get("sha256") != expected_digest or evidence.get("contextLock", {}).get("workOrderSha256") != expected_digest:
        fail("CP-05 resumed evidence Work Order digest mismatch")
    if current.get("productStage") != "CP05_IN_PROGRESS" or current.get("reviewState") != "CP05_RESUMED_AFTER_BLENDER_AUTHORIZATION" or current.get("nextLegalAction") != "EXECUTE_CP05_WO_B3D_001_THROUGH_006":
        fail("CP-05 GEF state is not the resumed execution state")
    if lock.get("status") not in {"OPEN", "ACTIVE"} or "Status: `IN_PROGRESS`" not in work_order:
        fail("CP-05 resumed lifecycle requires an OPEN/ACTIVE lock and IN_PROGRESS Work Order")
    if not subprocess.run(["git", "merge-base", "--is-ancestor", CP05_RESUME_BASE, head], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
        fail("CP-05 resumed protected main is not an ancestor of exact Git HEAD")
    for historical_head in ("e6eef9346f72ff6bb4f0350a6cd765bcf665346f", "e0794aea77aaca34b19baf2adeb153d3df24774c"):
        try:
            subprocess.run(["git", "cat-file", "-e", historical_head], cwd=ROOT, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except (OSError, subprocess.CalledProcessError):
            fail(f"CP-05 historical blocked head is missing: {historical_head}")
    for heading in ("## OBJECTIVE", "## CONTEXT/HIVE PREFLIGHT", "## CANONICAL BASIS", "## SCOPE", "## OUT OF SCOPE", "## BLENDER/MCP GATE", "## REPOSITORY AND DETERMINISM", "## SELECTED-LOGO BOUNDARY", "## ACCEPTANCE CRITERIA", "## TESTS", "## DELIVERABLES", "## REVIEW FORMAT", "## STOP CONDITION", "## EXECUTION REFERENCES"):
        if heading not in work_order:
            fail(f"CP-05 Work Order missing section: {heading}")
    transition = data(".engineering/evidence/CP05-BLENDER-WORKSTATION-TRANSITION.json")
    if transition.get("status") != "AUTHORIZED" or transition.get("git", {}).get("protectedMainHead") != CP05_RESUME_BASE:
        fail("CP-05 resumed workstation authorization is not bound to protected main")
    capabilities = transition.get("capabilities", {})
    if capabilities.get("BLENDER_MCP_READY") is not True or capabilities.get("BLENDER_PRODUCTION_AUTHORIZED") is not True or capabilities.get("UGAS_CORE_INSTALLED") is not True or capabilities.get("UGAS_GENERATION_PROVIDER_READY") is not False or capabilities.get("UGAS_GENERATION_AUTHORIZED") is not False:
        fail("CP-05 resumed capability split is incomplete or unsafe")
    for policy_name in ("AGENTS.md", "docs/WORKSTATION-MODE.md"):
        policy = read(policy_name)
        for fact in ("BLENDER_MCP_READY=true", "BLENDER_PRODUCTION_AUTHORIZED=true", "UGAS_CORE_INSTALLED=true", "UGAS_GENERATION_PROVIDER_READY=false", "UGAS_GENERATION_AUTHORIZED=false"):
            if fact not in policy:
                fail(f"{policy_name} is missing resumed capability fact: {fact}")
    blender = evidence.get("blender", {})
    if blender.get("status") != "PASS_LIVE_PREFLIGHT" or blender.get("version") != "5.2.1 LTS" or blender.get("addon", {}).get("protocolVersion") != 7 or blender.get("tools", {}).get("getAddonStatus") != "PASS" or blender.get("tools", {}).get("getSceneInfo") != "PASS" or blender.get("sceneMutationPerformed") is not False:
        fail("CP-05 resumed Blender/MCP preflight receipt is incomplete")
    policy_gate = evidence.get("policyGate", {})
    if policy_gate.get("status") not in {"AUTHORIZED", "PASS"} or policy_gate.get("code") not in {"BLENDER_PRODUCTION_AUTHORIZED", "REPOSITORY_WORKSTATION_POLICY_AUTHORIZED"}:
        fail("CP-05 resumed policy gate is not authorized")
    if evidence.get("outOfScopeConfirmed", {}).get("selectedLogoIntegration") is not False or evidence.get("outOfScopeConfirmed", {}).get("runtimeThree") is not False or evidence.get("outOfScopeConfirmed", {}).get("ugasProviderStarted") is not False:
        fail("CP-05 resumed evidence claims forbidden out-of-scope work")
    if evidence.get("verdict") not in {"IN_PROGRESS", "READY_FOR_REVIEW", "BLOCKED"} or evidence.get("reviewState") != "CP05_RESUMED_AFTER_BLENDER_AUTHORIZATION":
        fail("CP-05 resumed evidence verdict/state is not bounded")
    hive = evidence.get("hive", {})
    project = hive.get("project", {})
    task = hive.get("task", {})
    mcp = hive.get("mcp", {})
    if hive.get("status") != "PASS" or project.get("state") != "READY" or project.get("workingTreeClean") is not True:
        fail("CP-05 resumed HIVE project receipt is not READY with a clean tree")
    hive_candidate_head = project.get("head")
    if hive_candidate_head != head:
        try:
            receipt_parent = subprocess.check_output(["git", "rev-parse", "HEAD^"], cwd=ROOT, text=True).strip()
        except (OSError, subprocess.CalledProcessError) as exc:
            fail(f"cannot resolve CP-05 resumed HIVE receipt parent: {exc}")
        if receipt_parent != hive_candidate_head:
            fail("CP-05 resumed HIVE receipt is not bound to exact candidate or receipt parent")
    if task.get("intakeStatus") != "READY" or task.get("extractedTextAvailable") is not True or task.get("originalBlobSha256") != expected_digest:
        fail("CP-05 resumed HIVE task is not READY, extracted and digest-bound")
    if project.get("indexRunId") in {None, ""} or project.get("corpusRunId") in {None, ""}:
        fail("CP-05 resumed HIVE project receipt is missing index/corpus runs")
    for receipt in ("projectStatus", "checkpointRead", "contextSearch", "coreContextBuild", "mcpContextBuild"):
        if mcp.get(receipt) != "PASS":
            fail(f"CP-05 resumed HIVE MCP receipt missing PASS: {receipt}")
    for build_name in ("contextBuildDefault", "contextBuildMinimal"):
        build = mcp.get(build_name, {})
        if build.get("status") != "PASS" or build.get("budgetSatisfied") is not True or build.get("requiredContextExceedsHardBudget") is not False:
            fail(f"CP-05 resumed HIVE {build_name} receipt is not a bounded PASS")
    hierarchy = read(".engineering/SOURCE-HIERARCHY.md")
    if "Status: `CP05_IN_PROGRESS_BLENDER_AUTHORIZED`" not in hierarchy:
        fail("CP-05 Source Hierarchy is not in the resumed authorized state")
elif cp04_active:
    work_order = read(f".engineering/work-orders/{CP04_WORK_ORDER}.md")
    lock = data(f".engineering/context-locks/{CP04_LOCK}.json")
    evidence = data(f".engineering/evidence/{CP04_WORK_ORDER}.json")
    if current.get("activeWorkOrder") != CP04_WORK_ORDER or current.get("activeContextLock") != CP04_LOCK:
        fail("CP-04 active Work Order and Context Lock identity mismatch")
    if lock.get("workOrder") != CP04_WORK_ORDER or lock.get("lockId") != CP04_LOCK:
        fail("CP-04 Work Order and Context Lock pairing mismatch")
    if lock.get("authorizedBase") != "b989606949bd362a2bd63d039448505f3220918e" or lock.get("planningSource") != PLANNING:
        fail("CP-04 Context Lock base/source mismatch")
    expected_digest = hashlib.sha256((ROOT / f".engineering/work-orders/{CP04_WORK_ORDER}.md").read_bytes()).hexdigest()
    if lock.get("workOrderSha256") != expected_digest or lock.get("executionWorkOrderSha256") != expected_digest:
        fail("CP-04 Context Lock Work Order digest mismatch")
    if evidence.get("workOrder", {}).get("id") != CP04_WORK_ORDER or evidence.get("contextLock", {}).get("id") != CP04_LOCK:
        fail("CP-04 evidence Work Order and Context Lock identity mismatch")
    if evidence.get("workOrder", {}).get("sha256") != expected_digest or evidence.get("contextLock", {}).get("workOrderSha256") != expected_digest:
        fail("CP-04 evidence Work Order digest mismatch")
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"cannot resolve Git HEAD: {exc}")
    if lock.get("admissionHead") != "b989606949bd362a2bd63d039448505f3220918e":
        fail("CP-04 admission head is not bound to the expected synchronized base")
    if lock.get("status") not in {"OPEN", "ACTIVE"}:
        fail("CP-04 requires an OPEN or ACTIVE Context Lock")
    if current.get("productStage") != "CP04_IN_PROGRESS" or current.get("reviewState") not in {"CP04_IMPLEMENTATION_IN_PROGRESS", "CP04_HUMAN_SELECTION_PENDING"}:
        fail("CP-04 GEF state is not an admitted implementation or human-selection state")
    if "Status: `IN_PROGRESS`" not in work_order:
        fail("CP-04 requires an IN_PROGRESS Work Order")
    if evidence.get("verdict") not in {"IN_PROGRESS", "HUMAN_SELECTION_REQUIRED", "BLOCKED"}:
        fail("CP-04 evidence verdict is not a bounded lifecycle state")
    for heading in ("## OBJECTIVE", "## CONTEXT/HIVE PREFLIGHT", "## CANONICAL BASIS", "## SCOPE", "## OUT OF SCOPE", "## FILES/SOURCES TO READ", "## REQUIREMENTS", "## ARCHITECTURE RULES", "## CONSTRAINTS", "## ACCEPTANCE CRITERIA", "## TESTS", "## DELIVERABLES", "## REVIEW FORMAT", "## STOP CONDITION", "## EXECUTION REFERENCES / CANONICAL REFERENCES"):
        if heading not in work_order:
            fail(f"CP-04 Work Order missing section: {heading}")
    if current.get("reviewState") == "CP04_HUMAN_SELECTION_PENDING":
        if evidence.get("verdict") != "HUMAN_SELECTION_REQUIRED" or evidence.get("candidateIds") != ["NX-D-01", "NX-D-02", "NX-D-03", "NX-C-01", "NX-C-02", "NX-C-03", "NX-B-01", "NX-B-02", "NX-B-03"]:
            fail("CP-04 human-selection evidence is missing the exact nine-candidate batch")
        if evidence.get("hive", {}).get("status") != "PASS" or evidence.get("local", {}).get("status") != "PASS":
            fail("CP-04 human-selection state requires passing HIVE and local evidence")
        if evidence.get("canonicalSelection") is not False or evidence.get("runtimeWiring") is not False:
            fail("CP-04 human-selection state must not claim canonical selection or runtime wiring")
        candidate_head = lock.get("candidateHead")
        reviewed_head = lock.get("reviewedCandidateHead")
        receipt_head = lock.get("reviewReceiptHead")
        proof_head = evidence.get("git", {}).get("proofHead")
        if not all(isinstance(value, str) and value for value in (candidate_head, reviewed_head, receipt_head, proof_head)):
            fail("CP-04 human-selection state requires candidate, reviewed, receipt and proof heads")
        if candidate_head != reviewed_head:
            fail("CP-04 human-selection state must keep candidate and reviewed heads aligned")
        hive = evidence.get("hive", {})
        hive_project = hive.get("project", {})
        hive_mcp = hive.get("mcp", {})
        if hive_project.get("head") != candidate_head or hive_mcp.get("checkpointHead") != candidate_head:
            fail("CP-04 HIVE project and checkpoint receipt heads must match the corrected candidate head")
        if hive_project.get("state") != "READY" or hive_project.get("workingTreeClean") is not True:
            fail("CP-04 HIVE project receipt must be READY with a clean working tree")
        if hive_project.get("indexRunId") in {None, ""} or hive_project.get("corpusRunId") in {None, ""}:
            fail("CP-04 HIVE project receipt is missing current index/corpus run identifiers")
        if hive_mcp.get("checkpointBlobSha") in {None, ""} or hive_mcp.get("contextFingerprint") in {None, ""}:
            fail("CP-04 HIVE MCP receipt is missing the corrected checkpoint blob or context fingerprint")
        for build_name in ("contextBuildDefault", "contextBuildMinimal"):
            build = hive_mcp.get(build_name, {})
            if build.get("status") != "PASS" or build.get("budgetSatisfied") is not True or build.get("requiredContextExceedsHardBudget") is not False:
                fail(f"CP-04 HIVE {build_name} receipt is not a bounded PASS")
        def is_cp04_ancestor(ancestor: str, descendant: str) -> bool:
            try:
                subprocess.run(["git", "merge-base", "--is-ancestor", ancestor, descendant], cwd=ROOT, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
            except (OSError, subprocess.CalledProcessError):
                return False
        for role, value in (("candidate", candidate_head), ("reviewed", reviewed_head), ("receipt", receipt_head), ("proof", proof_head)):
            if not is_cp04_ancestor(value, head):
                fail(f"CP-04 {role} head is not an ancestor of exact Git HEAD {head}")
        if evidence.get("hosted", {}).get("status") != "PASS":
            fail("CP-04 human-selection state requires hosted checks evidence")
    else:
        if lock.get("candidateHead") not in {None, ""}:
            try:
                subprocess.run(["git", "merge-base", "--is-ancestor", lock["candidateHead"], head], cwd=ROOT, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except (OSError, subprocess.CalledProcessError):
                fail("CP-04 in-progress candidate head must be an ancestor of exact Git HEAD")
        if evidence.get("git", {}).get("proofHead") not in {None, "", head}:
            fail("CP-04 in-progress evidence proof head mismatch")
elif workstation_transition_active:
    transition = data(".engineering/evidence/CP05-BLENDER-WORKSTATION-TRANSITION.json")
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        local_branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
        branch = local_branch or os.environ.get("GITHUB_HEAD_REF", "").strip()
        remote_main_head = subprocess.check_output(["git", "rev-parse", "origin/main"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"cannot resolve workstation transition Git state: {exc}")
    if branch != "codex/cp05-blender-workstation-transition":
        fail("workstation transition must execute on codex/cp05-blender-workstation-transition")
    if remote_main_head != CP05_TRANSITION_BASE:
        fail("workstation transition origin/main is not the synchronized protected base")
    git_receipt = transition.get("git", {})
    candidate_head = git_receipt.get("transitionCandidateHead")
    if candidate_head != git_receipt.get("receiptCommitParent"):
        fail("workstation transition receipt candidate and receipt-parent bindings disagree")
    try:
        subprocess.run(["git", "merge-base", "--is-ancestor", CP05_TRANSITION_BASE, candidate_head], cwd=ROOT, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "merge-base", "--is-ancestor", candidate_head, head], cwd=ROOT, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (OSError, subprocess.CalledProcessError):
        fail("workstation transition candidate is not based on protected main")
    if transition.get("schemaVersion") != "nexlabs-web-cp05-workstation-transition-v1" or transition.get("status") != "IN_REVIEW":
        fail("workstation transition receipt is not in the bounded IN_REVIEW state")
    source = transition.get("sourceDocument", {})
    if source.get("name") != "NEXLABS-CP05-BLENDER-WORKSTATION-TRANSITION-AUTHORIZATION.pdf" or source.get("sha256") != CP05_TRANSITION_PDF_SHA256:
        fail("workstation transition source binding is incomplete")
    if transition.get("base", {}).get("mainSha") != CP05_TRANSITION_BASE or transition.get("base", {}).get("branch") != branch:
        fail("workstation transition base/branch receipt mismatch")
    local_state = transition.get("localState", {})
    if local_state.get("preservedBlockedBranch") != "codex/cp05-blender-context-core" or local_state.get("preserved") is not True:
        fail("workstation transition did not preserve the blocked CP-05 branch")
    if local_state.get("blockedCandidateHead") != "e6eef9346f72ff6bb4f0350a6cd765bcf665346f" or local_state.get("blockedReceiptHead") != "e0794aea77aaca34b19baf2adeb153d3df24774c":
        fail("workstation transition preserved-branch receipt is incomplete")
    capabilities = transition.get("capabilities", {})
    if capabilities.get("BLENDER_MCP_READY") is not True or capabilities.get("BLENDER_PRODUCTION_AUTHORIZED") is not True:
        fail("workstation transition Blender capability split is incomplete")
    if capabilities.get("UGAS_CORE_INSTALLED") is not True or capabilities.get("UGAS_GENERATION_PROVIDER_READY") is not False or capabilities.get("UGAS_GENERATION_AUTHORIZED") is not False:
        fail("workstation transition UGAS capability split is unsafe or incomplete")
    blender = capabilities.get("blender", {})
    if blender.get("version") != "5.2.1 LTS" or blender.get("addonVersion") != "1.7" or blender.get("protocolVersion") != 7 or blender.get("getAddonStatus") != "PASS" or blender.get("getSceneInfo") != "PASS":
        fail("workstation transition Blender/MCP capability evidence is incomplete")
    agents_source = read("AGENTS.md")
    workstation_source = read("docs/WORKSTATION-MODE.md")
    for policy_name, policy_source in (("AGENTS.md", agents_source), ("docs/WORKSTATION-MODE.md", workstation_source)):
        if "BLENDER_MCP_READY=true" not in policy_source or "BLENDER_PRODUCTION_AUTHORIZED=true" not in policy_source:
            fail(f"{policy_name} does not declare the authorized Blender capability split")
        if "UGAS_CORE_INSTALLED=true" not in policy_source or "UGAS_GENERATION_PROVIDER_READY=false" not in policy_source or "UGAS_GENERATION_AUTHORIZED=false" not in policy_source:
            fail(f"{policy_name} does not preserve the fail-closed UGAS capability split")
    if transition.get("scope", {}).get("sceneMutation") is not False or transition.get("scope", {}).get("cp05ProductImplementation") is not False or transition.get("scope", {}).get("ugasGeneration") is not False:
        fail("workstation transition claims forbidden product or generation work")
    if transition.get("hosted", {}).get("status") != "NOT_STARTED" or transition.get("hosted", {}).get("merge") != "NOT_EXECUTED" or transition.get("hosted", {}).get("postMergeChecks") != "NOT_CLAIMED":
        fail("workstation transition cannot claim hosted or post-merge evidence before the PR exists")
    if section(canonical, "## STATUS") != "CP-04 COMPLETE" or section(canonical, "## VERSION") != "NEXLABS-WEB CP-05 BLENDER WORKSTATION TRANSITION":
        fail("workstation transition checkpoint does not preserve CP-04 completion")
    if "BLENDER_MCP_UNAVAILABLE" in section(canonical, "## BLOCKERS") or "RUNTIME_BRAND_PROMOTION_PENDING" not in section(canonical, "## BLOCKERS") or "EXTERNAL_SIMILARITY_RESEARCH_NOT_PERFORMED" not in section(canonical, "## BLOCKERS"):
        fail("workstation transition checkpoint blocker vocabulary is incorrect")
    if "Status: `CP05_BLENDER_WORKSTATION_TRANSITION_IN_REVIEW`" not in read(".engineering/SOURCE-HIERARCHY.md"):
        fail("Source Hierarchy is not in the workstation transition review state")
elif cp04_closed:
    work_order = read(f".engineering/work-orders/{CP04_WORK_ORDER}.md")
    lock = data(f".engineering/context-locks/{CP04_LOCK}.json")
    evidence = data(f".engineering/evidence/{CP04_WORK_ORDER}.json")
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"cannot resolve CP-04 closure Git HEAD: {exc}")
    if current.get("lastCompletedWorkOrder") != CP04_WORK_ORDER or current.get("activeWorkOrder") not in {None, ""} or current.get("activeContextLock") not in {None, ""}:
        fail("CP-04 closure must have no active Work Order or Context Lock")
    if lock.get("workOrder") != CP04_WORK_ORDER or lock.get("lockId") != CP04_LOCK:
        fail("CP-04 closed Work Order and Context Lock pairing mismatch")
    expected_digest = hashlib.sha256((ROOT / f".engineering/work-orders/{CP04_WORK_ORDER}.md").read_bytes()).hexdigest()
    execution_digest = "7923e12c03ec892e985d3f8c37d40428b08486c6cfdd3c6f91cb6c420edf7361"
    if lock.get("workOrderSha256") != expected_digest or lock.get("executionWorkOrderSha256") != execution_digest:
        fail("CP-04 closed Context Lock Work Order digest or execution digest mismatch")
    if evidence.get("workOrder", {}).get("id") != CP04_WORK_ORDER or evidence.get("contextLock", {}).get("id") != CP04_LOCK:
        fail("CP-04 closure evidence Work Order and Context Lock identity mismatch")
    if evidence.get("workOrder", {}).get("sha256") != expected_digest or evidence.get("workOrder", {}).get("executionSha256") != execution_digest:
        fail("CP-04 closure evidence Work Order digest mismatch")
    if evidence.get("contextLock", {}).get("workOrderSha256") != expected_digest or evidence.get("contextLock", {}).get("executionWorkOrderSha256") != execution_digest:
        fail("CP-04 closure evidence Context Lock digest mismatch")
    if lock.get("status") != "CLOSED" or "Status: `COMPLETED`" not in work_order:
        fail("CP-04 closure requires a CLOSED Context Lock and COMPLETED Work Order")
    if current.get("reviewState") != "CP04_HG01_SATISFIED" or current.get("nextLegalAction") != "RESUME_CP05_FROM_AUTHORIZED_WORKSTATION":
        fail("CP-04 GEF closure/workstation-resume vocabulary is incomplete")
    hierarchy = read(".engineering/SOURCE-HIERARCHY.md")
    if "Status: `CP04_COMPLETE_READY_FOR_CP05_ADMISSION`" not in hierarchy:
        fail("CP-04 Source Hierarchy is not closed for CP-05 admission")
    transition = data(".engineering/evidence/CP05-BLENDER-WORKSTATION-TRANSITION.json")
    if transition.get("status") != "AUTHORIZED":
        fail("CP-05 Blender workstation transition is not authorized")
    capabilities = transition.get("capabilities", {})
    if capabilities.get("BLENDER_MCP_READY") is not True or capabilities.get("BLENDER_PRODUCTION_AUTHORIZED") is not True:
        fail("authorized workstation is missing Blender readiness/authorization")
    if capabilities.get("UGAS_GENERATION_PROVIDER_READY") is not False or capabilities.get("UGAS_GENERATION_AUTHORIZED") is not False:
        fail("authorized workstation must keep UGAS generation fail-closed")
    if transition.get("scope", {}).get("sceneMutation") is not False or transition.get("scope", {}).get("cp05ProductImplementation") is not False:
        fail("workstation authorization transition must remain non-product")
    agents_policy = read("AGENTS.md")
    workstation_policy = read("docs/WORKSTATION-MODE.md")
    for policy_name, policy_source in (("AGENTS.md", agents_policy), ("docs/WORKSTATION-MODE.md", workstation_policy)):
        if "BLENDER_PRODUCTION_AUTHORIZED=true" not in policy_source or "UGAS_GENERATION_AUTHORIZED=false" not in policy_source:
            fail(f"{policy_name} does not reflect the authorized Blender / fail-closed UGAS policy")
    if section(canonical, "## STATUS") != "CP-04 COMPLETE" or section(canonical, "## VERSION") != "NEXLABS-WEB CP-04 HG-01 CLOSURE":
        fail("CP-04 canonical checkpoint is not in the closure state")
    if evidence.get("verdict") != "APPROVED" or evidence.get("reviewState") != "CP04_HG01_SATISFIED":
        fail("CP-04 closure evidence does not describe HG-01 satisfaction")
    if evidence.get("candidateIds") != ["NX-D-01", "NX-D-02", "NX-D-03", "NX-C-01", "NX-C-02", "NX-C-03", "NX-B-01", "NX-B-02", "NX-B-03"]:
        fail("CP-04 closure evidence lost the exact nine-candidate history")
    selection = evidence.get("selectionDecision", {})
    if selection.get("status") != "SATISFIED" or selection.get("gate") != "HG-01" or selection.get("candidateId") != "NX-C-02" or selection.get("candidateRevision") != "r1" or selection.get("candidateSha256") != "16daeac469520dbae6ba224dbd87bc8f07510c734940d35412248f32d2364165":
        fail("CP-04 closure evidence does not bind the selected NX-C-02 candidate")
    if evidence.get("canonicalSelection") is not False or evidence.get("runtimeWiring") is not False:
        fail("CP-04 closure must not claim runtime canonical promotion")
    if any("PENDING" in str(item) or "HUMAN_GATE_HG_01" in str(item) for item in evidence.get("knownBlockers", [])):
        fail("CP-04 closure retains a stale HG-01 pending blocker")
    closure_head = lock.get("reviewedCandidateHead")
    closure_candidate_head = evidence.get("git", {}).get("closureCandidateHead")
    if not isinstance(closure_candidate_head, str) or not closure_candidate_head:
        fail("CP-04 closure is missing the closure candidate head")
    if closure_head != "b7c2e8f8f08a196c37dc0e070e3a228e2c742f3d" or lock.get("candidateHead") != closure_head or lock.get("reviewReceiptHead") != closure_head:
        fail("CP-04 closure head bindings do not match the independently reviewed exact head")
    proof_head = evidence.get("git", {}).get("proofHead")
    if proof_head != closure_head or evidence.get("git", {}).get("reviewedCandidateHead") != closure_head or evidence.get("git", {}).get("reviewReceiptHead") != closure_head:
        fail("CP-04 closure Git evidence does not bind the reviewed exact head")
    def is_cp04_closure_ancestor(ancestor: str, descendant: str) -> bool:
        try:
            subprocess.run(["git", "merge-base", "--is-ancestor", ancestor, descendant], cwd=ROOT, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except (OSError, subprocess.CalledProcessError):
            return False
    if not is_cp04_closure_ancestor(closure_head, head) or not is_cp04_closure_ancestor(closure_candidate_head, head):
        fail(f"CP-04 closure reviewed head {closure_head} is not an ancestor of exact Git HEAD {head}")
    hosted = evidence.get("hosted", {})
    hosted_pr = hosted.get("pullRequest", {})
    if hosted.get("status") != "PASS" or hosted_pr.get("number") != 23 or hosted_pr.get("status") != "OPEN" or hosted_pr.get("observedHead") != closure_candidate_head:
        fail("CP-04 hosted closure evidence is not bound to the reviewed exact head")
    if hosted_pr.get("quality", {}).get("status") != "PASS" or hosted_pr.get("quality", {}).get("head") != closure_candidate_head or hosted_pr.get("Governance", {}).get("status") != "PASS" or hosted_pr.get("Governance", {}).get("head") != closure_candidate_head:
        fail("CP-04 hosted quality/Governance checks are not PASS on the reviewed exact head")
    if hosted.get("merge") != "NOT_EXECUTED" or hosted.get("postMergeChecks") != "NOT_CLAIMED":
        fail("CP-04 closure evidence claims merge or post-merge checks")
    hive = evidence.get("hive", {})
    hive_project = hive.get("project", {})
    hive_mcp = hive.get("mcp", {})
    if hive.get("status") != "PASS" or hive_project.get("state") != "READY" or hive_project.get("workingTreeClean") is not True:
        fail("CP-04 closure requires a READY clean HIVE project receipt")
    if hive_project.get("head") != closure_candidate_head or hive_mcp.get("checkpointHead") != closure_candidate_head:
        fail("CP-04 HIVE closure receipt head mismatch")
    if hive_mcp.get("projectStatus") != "PASS" or hive_mcp.get("checkpointRead") != "PASS" or hive_mcp.get("contextSearch") != "PASS" or hive_mcp.get("coreContextBuild") != "PASS" or hive_mcp.get("mcpContextBuild") != "PASS":
        fail("CP-04 HIVE closure read-only validation receipts are incomplete")
    for build_name in ("contextBuildDefault", "contextBuildMinimal"):
        build = hive_mcp.get(build_name, {})
        if build.get("status") != "PASS" or build.get("budgetSatisfied") is not True or build.get("requiredContextExceedsHardBudget") is not False:
            fail(f"CP-04 HIVE closure {build_name} receipt is not a bounded PASS")
elif cp03_closed:
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
    if current.get("productStage") != "CP03_COMPLETE" or current.get("reviewState") != "CP03_VERIFIED_COMPLETE":
        fail("CP-03 GEF state is not the verified protected squash completion state")
    if current.get("nextLegalAction") != "ADMIT_CP04_WITH_NEW_WORK_ORDER" or current.get("activeWorkOrder") not in {None, ""} or current.get("activeContextLock") not in {None, ""}:
        fail("CP-03 completion must stop before CP-04 admission")
    if lock.get("status") != "CLOSED":
        fail("CP-03 completion requires a CLOSED Context Lock")
    if "Status: `COMPLETED`" not in work_order:
        fail("CP-03 completion requires a COMPLETED Work Order")
    hierarchy = read(".engineering/SOURCE-HIERARCHY.md")
    if "Status: `CP03_COMPLETE_READY_FOR_NEXT_ADMISSION`" not in hierarchy:
        fail("CP-03 Source Hierarchy is not closed for the next admission")
    backlog = read("docs/project-brain/14-BACKLOG.md")
    if "cp-03 institutional pages" in backlog.lower():
        fail("CP-03 institutional pages remain in the future backlog")
    if "CP-04 logo exploration/selection" not in backlog:
        fail("CP-04 logo exploration/selection is missing from the future backlog")
    if section(canonical, "## PHASE") != "CP-03 verified post-merge complete":
        fail("checkpoint phase is not the verified CP-03 post-merge closure vocabulary")
    if evidence.get("verdict") != "APPROVED" or evidence.get("reviewState") != "CP03_VERIFIED_COMPLETE":
        fail("CP-03 evidence does not describe the verified completion")
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
    if correction_pr.get("number") != 20 or correction_pr.get("status") != "MERGED" or correction_pr.get("reviewedHead") != "b60e3e518956127819e8a3d54b1dc33610b985b8" or correction_pr.get("mergeSha") != "1064e7832eae36a42485d5b040300edf2092be94" or correction_pr.get("mergeMethod") != "SQUASH":
        fail("CP-03 correction PR evidence does not bind PR #20 to resulting main")
    correction_pre_merge = correction_pr.get("preMergeChecks", {})
    if correction_pre_merge.get("head") != correction_pr.get("reviewedHead") or correction_pre_merge.get("quality", {}).get("status") != "PASS" or correction_pre_merge.get("Governance", {}).get("status") != "PASS":
        fail("CP-03 correction PR pre-merge checks are not PASS on the reviewed head")
    correction_resulting_main = correction_pr.get("resultingMainChecks", {})
    if correction_resulting_main.get("head") != correction_pr.get("mergeSha") or correction_resulting_main.get("quality", {}).get("status") != "PASS" or correction_resulting_main.get("Governance", {}).get("status") != "PASS":
        fail("CP-03 resulting-main checks are not PASS on the correction merge SHA")
    if correction_pr.get("merge") != "EXECUTED" or correction_pr.get("postMergeChecks") != "PASS":
        fail("CP-03 correction PR merge or resulting-main checks are not recorded as complete")
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
if workstation_transition_active:
    if adoption_state != "GEF_V1_CP05_WORKSTATION_TRANSITION_IN_REVIEW":
        fail("invalid workstation transition adoption state")
    if current.get("activeWorkOrder") not in {None, ""} or current.get("activeContextLock") not in {None, ""}:
        fail("workstation transition cannot retain an active product Work Order or Context Lock")
    if transition.get("status") != "IN_REVIEW" or transition.get("scope", {}).get("cp05ProductImplementation") is not False:
        fail("workstation transition requires bounded non-product evidence")
elif cp05_active:
    if adoption_state != "GEF_V1_CP05_ADMITTED":
        fail("invalid resumed CP-05 adoption state")
    if lock.get("status") not in {"OPEN", "ACTIVE"}:
        fail("resumed CP-05 requires an OPEN or ACTIVE Context Lock")
    if "Status: `IN_PROGRESS`" not in work_order:
        fail("resumed CP-05 requires an IN_PROGRESS Work Order")
elif cp04_active:
    if adoption_state != "GEF_V1_CP04_ADMITTED":
        fail("invalid CP-04 adoption state")
    if lock.get("status") not in {"OPEN", "ACTIVE"}:
        fail("active CP-04 requires an OPEN or ACTIVE Context Lock")
    if "Status: `IN_PROGRESS`" not in work_order:
        fail("active CP-04 requires an IN_PROGRESS Work Order")
elif cp04_closed:
    if adoption_state != "GEF_V1_CP04_ADMITTED":
        fail("invalid CP-04 completion adoption state")
    if current.get("activeWorkOrder") not in {None, ""} or current.get("activeContextLock") not in {None, ""}:
        fail("completed CP-04 cannot retain an active Work Order or Context Lock")
    if lock.get("status") != "CLOSED":
        fail("completed CP-04 requires a CLOSED Context Lock")
    if evidence.get("verdict") != "APPROVED":
        fail("completed CP-04 requires APPROVED evidence")
    if "Status: `COMPLETED`" not in work_order:
        fail("completed CP-04 requires the Work Order to be marked COMPLETED")
elif cp03_closed:
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
