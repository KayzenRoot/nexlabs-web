import { spawnSync } from "node:child_process";

const scripts = process.argv.slice(2);
if (scripts.length === 0) {
  console.error("Usage: node scripts/run-sequence.mjs <npm-script> [...]");
  process.exit(2);
}

const npm = process.platform === "win32" ? "npm.cmd" : "npm";
const npmExecPath = process.env.npm_execpath;
for (const script of scripts) {
  const command = npmExecPath
    ? process.execPath
    : process.platform === "win32"
      ? process.env.ComSpec ?? "cmd.exe"
      : npm;
  const args = npmExecPath
    ? [npmExecPath, "run", script]
    : process.platform === "win32"
      ? ["/d", "/s", "/c", `"${npm}" run ${script}`]
      : ["run", script];
  const result = spawnSync(command, args, {
    cwd: process.cwd(),
    env: process.env,
    stdio: "inherit",
  });

  if (result.error) {
    console.error(`Failed to run npm script ${script}: ${result.error.message}`);
    process.exit(1);
  }
  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }
  if (result.signal) {
    console.error(`npm script ${script} terminated by ${result.signal}`);
    process.exit(1);
  }
}
