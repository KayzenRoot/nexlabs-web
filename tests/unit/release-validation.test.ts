import { execFileSync } from "node:child_process";
import path from "node:path";

const validator = path.resolve("scripts/validate-release.mjs");

function runValidator(environment: Record<string, string | undefined>) {
  const childEnvironment = { ...process.env };
  for (const [key, value] of Object.entries(environment)) {
    if (value === undefined) delete childEnvironment[key];
    else childEnvironment[key] = value;
  }

  try {
    return {
      status: 0,
      output: execFileSync(process.execPath, [validator], { env: childEnvironment, encoding: "utf8" }),
    };
  } catch (error) {
    const failure = error as { status?: number; stderr?: string };
    return { status: failure.status ?? 1, output: failure.stderr ?? "" };
  }
}

describe("release validator", () => {
  it.each([
    [{ NEXLABS_ENV: undefined, NEXT_PUBLIC_SITE_ORIGIN: undefined }, "NEXLABS_ENV=PRODUCTION"],
    [{ NEXLABS_ENV: "PREVIEW", NEXT_PUBLIC_SITE_ORIGIN: undefined }, "NEXLABS_ENV=PRODUCTION"],
    [{ NEXLABS_ENV: "PRODUCTION", NEXT_PUBLIC_SITE_ORIGIN: undefined }, "NEXT_PUBLIC_SITE_ORIGIN"],
    [{ NEXLABS_ENV: "PRODUCTION", NEXT_PUBLIC_SITE_ORIGIN: "http://example.invalid" }, "HTTPS"],
    [{ NEXLABS_ENV: "PRODUCTION", NEXT_PUBLIC_SITE_ORIGIN: "not-a-url" }, "valid URL"],
  ] as const)("rejects %j", (environment, reason) => {
    const result = runValidator(environment);
    expect(result.status).not.toBe(0);
    expect(result.output).toContain(reason);
  });

  it("accepts an explicit HTTPS production origin", () => {
    const result = runValidator({
      NEXLABS_ENV: "PRODUCTION",
      NEXT_PUBLIC_SITE_ORIGIN: "https://example.invalid",
    });

    expect(result.status).toBe(0);
    expect(result.output).toContain("Release validation passed for https://example.invalid");
  });
});
