import { readFile, stat } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const manifestPath = path.join(root, "public", "brand", "manifest.json");
const manifest = JSON.parse(await readFile(manifestPath, "utf8"));
if (!Array.isArray(manifest.assets)) { console.error("brand manifest assets must be an array"); process.exit(1); }
for (const asset of manifest.assets) {
  if (!asset.path || asset.path.includes("..")) { console.error(`unsafe asset path: ${asset.path}`); process.exit(1); }
  const info = await stat(path.join(root, "public", asset.path));
  if (info.size > 5 * 1024 * 1024) { console.error(`asset exceeds CP-01 5 MiB placeholder limit: ${asset.path}`); process.exit(1); }
}
console.log(`Asset validation passed: ${manifest.assets.length} manifest asset(s), no oversized assets.`);
