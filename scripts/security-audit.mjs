import { spawnSync } from "node:child_process";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";

const DIAGNOSTIC_DIR = new URL("../.audit/", import.meta.url);
const DIAGNOSTIC_FILE = new URL("../.audit/security-audit-diagnostic.json", import.meta.url);

function writeDiagnostic(value) {
  mkdirSync(DIAGNOSTIC_DIR, { recursive: true });
  writeFileSync(DIAGNOSTIC_FILE, JSON.stringify(value, null, 2) + "\n", "utf8");
}

const ALLOWED_FALSE_POSITIVE = {
  package: "brace-expansion",
  version: "1.1.21",
  advisory: "GHSA-mh99-v99m-4gvg",
};

function readLock() {
  return JSON.parse(readFileSync(new URL("../package-lock.json", import.meta.url), "utf8"));
}

function advisoryId(item) {
  if (!item || typeof item !== "object") return null;
  const url = String(item.url || "");
  const match = url.match(/GHSA-[A-Za-z0-9-]+/);
  return match ? match[0] : null;
}

function nodeVersions(vulnerability, lock) {
  const nodes = Array.isArray(vulnerability?.nodes) ? vulnerability.nodes : [];
  return nodes.map((node) => ({
    node,
    version: lock.packages?.[node]?.version ?? null,
  }));
}

function isAllowedLeaf(vulnerabilityName, advisory, vulnerability, lock) {
  if (vulnerabilityName !== ALLOWED_FALSE_POSITIVE.package) return false;
  if (advisoryId(advisory) !== ALLOWED_FALSE_POSITIVE.advisory) return false;

  const versions = nodeVersions(vulnerability, lock);
  if (!versions.length) return false;
  return versions.every(({ version }) => version === ALLOWED_FALSE_POSITIVE.version);
}

function isAllowedVulnerability(name, vulnerabilities, lock, visiting = new Set()) {
  if (visiting.has(name)) return false;
  const vulnerability = vulnerabilities[name];
  if (!vulnerability) return false;

  const next = new Set(visiting);
  next.add(name);

  const via = Array.isArray(vulnerability.via) ? vulnerability.via : [];
  if (!via.length) return false;

  for (const item of via) {
    if (typeof item === "string") {
      if (!isAllowedVulnerability(item, vulnerabilities, lock, next)) return false;
      continue;
    }
    if (!["high", "critical"].includes(String(item?.severity || "").toLowerCase())) {
      continue;
    }
    if (!isAllowedLeaf(name, item, vulnerability, lock)) return false;
  }
  return true;
}

function runAudit() {
  return spawnSync(
    process.platform === "win32" ? "npm.cmd" : "npm",
    ["audit", "--json", "--audit-level=high"],
    { encoding: "utf8", shell: false }
  );
}

function safeErrorShape(report) {
  return {
    message: typeof report?.message === "string" ? report.message.slice(0, 1000) : null,
    method: typeof report?.method === "string" ? report.method : null,
    statusCode: Number.isInteger(report?.statusCode) ? report.statusCode : null,
    uri: typeof report?.uri === "string" ? report.uri.replace(/([?&](?:token|key|auth)=[^&]+)/gi, "$1[REDACTED]") : null,
    bodyPrefix: typeof report?.body === "string" ? report.body.slice(0, 2000) : null,
    error: report?.error ?? null,
  };
}

let audit;
let report;
const attempts = [];

for (let attempt = 1; attempt <= 3; attempt += 1) {
  audit = runAudit();

  if (audit.error) {
    attempts.push({ attempt, stage: "spawn", message: audit.error.message });
    continue;
  }

  try {
    report = JSON.parse(audit.stdout || "{}");
  } catch {
    attempts.push({
      attempt,
      stage: "parse",
      auditExitStatus: audit.status,
      stdoutPrefix: String(audit.stdout || "").slice(0, 1000),
      stderrPrefix: String(audit.stderr || "").slice(0, 1000),
    });
    continue;
  }

  if (typeof report.vulnerabilities === "object" && report.vulnerabilities !== null) {
    break;
  }

  attempts.push({
    attempt,
    stage: "shape",
    auditExitStatus: audit.status,
    ...safeErrorShape(report),
  });
  report = undefined;
}

if (!audit || !report || typeof report.vulnerabilities !== "object" || report.vulnerabilities === null) {
  writeDiagnostic({ status: "ERROR", stage: "audit-unavailable", attempts });
  console.error("Security audit endpoint did not return a valid vulnerability report after 3 attempts.");
  console.error(JSON.stringify(attempts, null, 2));
  process.exit(1);
}

const vulnerabilities = report.vulnerabilities;
const lock = readLock();
const blocking = [];
const allowed = [];

for (const [name, vulnerability] of Object.entries(vulnerabilities)) {
  if (!["high", "critical"].includes(vulnerability.severity)) continue;
  if (isAllowedVulnerability(name, vulnerabilities, lock)) {
    allowed.push(name);
  } else {
    blocking.push({
      name,
      severity: vulnerability.severity,
      via: vulnerability.via,
      nodes: vulnerability.nodes,
      fixAvailable: vulnerability.fixAvailable,
    });
  }
}

writeDiagnostic({
  status: blocking.length ? "BLOCKED" : "PASS",
  auditExitStatus: audit.status,
  auditReportVersion: report.auditReportVersion ?? null,
  allowed,
  blocking,
});

if (allowed.length) {
  console.warn(
    "Audit exception applied only to the documented brace-expansion@1.1.21 GHSA-mh99-v99m-4gvg advisory-chain false positive:",
    allowed.join(", ")
  );
}

if (blocking.length) {
  console.error("Blocking HIGH/CRITICAL npm audit findings:");
  console.error(JSON.stringify(blocking, null, 2));
  process.exit(1);
}

console.log("Security audit: PASS (no unapproved HIGH/CRITICAL findings).");
