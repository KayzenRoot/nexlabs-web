import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const content = JSON.parse(await readFile(path.join(root, "content", "site", "site.json"), "utf8"));
const errors = [];
const required = ["identity", "navigation", "hero", "evidence", "contact", "routes"];
for (const key of required) if (!(key in content)) errors.push(`missing top-level field: ${key}`);
if (content.identity?.stage !== "pre-incorporation") errors.push("identity.stage must remain pre-incorporation until a canonical decision changes it");
if (!Array.isArray(content.navigation) || content.navigation.length === 0) errors.push("navigation must contain at least one item");
if (!content.hero?.heading || !content.hero?.body) errors.push("hero heading and body are required");
if (!Array.isArray(content.evidence) || content.evidence.length === 0) errors.push("at least one evidence link is required");
if (content.contact?.founder?.approved && (!content.contact.founder.name || !content.contact.founder.bio)) errors.push("approved founder data must include name and bio");
const serialized = JSON.stringify(content);
if (/\[(?:[A-Z0-9_]+)_?(?:REQUIRED|TODO|TBD)\]|lorem ipsum/i.test(serialized)) errors.push("unresolved placeholder token found");
for (const link of content.evidence ?? []) {
  try { if (new URL(link.href).protocol !== "https:") errors.push(`evidence link is not HTTPS: ${link.href}`); }
  catch { errors.push(`invalid evidence URL: ${link.href}`); }
}
if (errors.length) { console.error(errors.join("\n")); process.exit(1); }
console.log("Content validation passed: optional founder/contact data remains explicitly unavailable.");
