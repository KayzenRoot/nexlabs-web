from __future__ import annotations

import json
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
    "docs/project-brain/17-BRAND-WEB-SOURCE-MAP.md", "scripts/hive_bootstrap.py", "scripts/hive_mcp.py", ".github/workflows/governance.yml",
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
for name, value in (("manifest", manifest.get("candidateHead")), ("lock", lock.get("candidateHead")), ("evidence", evidence.get("candidateHead"))):
    if value != head:
        fail(f"{name} candidate head {value!r} does not match exact Git HEAD {head}")

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

governance_files = [ROOT / path for path in REQUIRED] + [ROOT / "scripts/validate_governance.py"]
for path in governance_files:
    text = path.read_text(encoding="utf-8")
    if path.name != "validate_governance.py" and re.search(r"\b(?:TODO|TBD)\b", text, re.IGNORECASE):
        fail(f"unresolved governance placeholder in {path.relative_to(ROOT)}")
    if path.name != "validate_governance.py" and re.search(r"(?<![A-Za-z])(?:[A-Za-z]:[\\/]|/Users/|/home/|/mnt/)", text):
        fail(f"machine-specific absolute path in {path.relative_to(ROOT)}")

current = data(".engineering/gef/GEF-CURRENT.json")
if current.get("activeWorkOrder") != WORK_ORDER or current.get("activeContextLock") != LOCK:
    fail("GEF current active identity mismatch")
if current.get("adoptionState") not in {"GEF_V1_ADOPTION_IN_PROGRESS", "GEF_V1_ADOPTED_READY_FOR_GOVERNED_DEVELOPMENT"}:
    fail("invalid GEF adoption state")

print("NexLabs Web governance validation: PASS")
print(f"Exact Git HEAD: {head}")
print(f"GEF v1.0.0: {GEF}")
print(f"HIVE v1.0.0: {HIVE}")
print(f"Required governance artifacts: {len(REQUIRED)}")
