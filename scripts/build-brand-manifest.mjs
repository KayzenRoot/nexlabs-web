import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const sourcePath = path.join(root, "content", "site", "site.json");
const outputPath = path.join(root, "public", "brand", "manifest.json");
const site = JSON.parse(await readFile(sourcePath, "utf8"));
const manifest = {
  schemaVersion: 1,
  site: site.identity.corporateName,
  assets: [],
};
await writeFile(outputPath, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
console.log(`Brand manifest written: ${path.relative(root, outputPath)}`);
