import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "out");
const portArgument = process.argv.indexOf("--port");
const port = portArgument >= 0 ? Number(process.argv[portArgument + 1]) : 3000;
const types = { ".css": "text/css", ".html": "text/html", ".js": "text/javascript", ".json": "application/json", ".svg": "image/svg+xml", ".txt": "text/plain" };

const server = createServer(async (request, response) => {
  const requestPath = decodeURIComponent((request.url ?? "/").split("?")[0]);
  const relative = requestPath === "/" ? "index.html" : requestPath.replace(/^\/+/, "");
  const candidate = path.resolve(root, relative);
  if (!candidate.startsWith(`${root}${path.sep}`) && candidate !== root) { response.writeHead(400); response.end("Bad request"); return; }
  const files = [candidate, path.join(candidate, "index.html")];
  for (const file of files) {
    try {
      if (!(await stat(file)).isFile()) continue;
      response.writeHead(200, { "Content-Type": types[path.extname(file)] ?? "application/octet-stream" });
      response.end(await readFile(file));
      return;
    } catch { /* try the next candidate */ }
  }
  try { response.writeHead(404, { "Content-Type": "text/html" }); response.end(await readFile(path.join(root, "404.html"))); }
  catch { response.writeHead(404); response.end("Not found"); }
});
server.listen(port, "127.0.0.1", () => console.log(`Static preview listening on http://127.0.0.1:${port}`));
