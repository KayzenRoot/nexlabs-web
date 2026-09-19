import { execFileSync } from "node:child_process";
import path from "node:path";

it("keeps generated design token artifacts deterministic and valid", () => {
  execFileSync(process.execPath, [path.join(process.cwd(), "scripts", "validate-tokens.mjs")], { stdio: "pipe" });
});
