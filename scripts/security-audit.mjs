import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";

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

const audit = spawnSync(
  process.platform === "win32" ? "npm.cmd" : "npm",
  ["audit", "--json", "--audit-level=high"],
  { encoding: "utf8", shell: false }
);

if (audit.error) {
  console.error("Security audit could not start:", audit.error.message);
  process.exit(1);
}

let report;
try {
  report = JSON.parse(audit.stdout || "{}");
} catch {
  console.error(audit.stdout);
  console.error(audit.stderr);
  console.error("Security audit returned invalid JSON.");
  process.exit(1);
}

if (report.error || typeof report.vulnerabilities !== "object" || report.vulnerabilities === null || !report.metadata) {
  console.error("Security audit did not return a valid vulnerability report.");
  console.error(JSON.stringify(report, null, 2));
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
