import { readdir, stat } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const output = path.join(root, "out");
async function bytes(directory) {
  let total = 0;
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const entryPath = path.join(directory, entry.name);
    total += entry.isDirectory() ? await bytes(entryPath) : (await stat(entryPath)).size;
  }
  return total;
}
console.log(`Static output baseline: ${output} (${(await bytes(output) / 1024).toFixed(1)} KiB)`);
