import { readFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const content = JSON.parse(await readFile(path.join(root, "content", "site", "site.json"), "utf8"));
const internal = [...(content.navigation ?? []), content.hero?.primaryAction, content.hero?.secondaryAction].filter((link) => link && link.href.startsWith("/") && !link.external);
const errors = [];
for (const link of internal) {
  const routePath = link.href === "/" ? path.join(root, "app", "page.tsx") : path.join(root, "app", link.href.replace(/^\//, ""), "page.tsx");
  if (!existsSync(routePath)) errors.push(`internal link has no route: ${link.href}`);
}
for (const link of [...(content.evidence ?? []), content.hero?.primaryAction, content.hero?.secondaryAction].filter(Boolean)) {
  if (link.external) {
    try { if (new URL(link.href).protocol !== "https:") errors.push(`external link is not HTTPS: ${link.href}`); }
    catch { errors.push(`invalid external URL: ${link.href}`); }
  }
}
if (errors.length) { console.error(errors.join("\n")); process.exit(1); }
console.log(`Link validation passed: ${internal.length} internal link(s), external evidence links structurally valid.`);
