import { pathToFileURL } from "node:url";

const supportedEnvironments = new Set(["LOCAL", "PREVIEW", "PRODUCTION"]);

export function validateReleaseEnvironment(environment = process.env) {
  const value = (environment.NEXLABS_ENV ?? "LOCAL").toUpperCase();
  if (!supportedEnvironments.has(value)) {
    return { ok: false, reason: `Unsupported NEXLABS_ENV: ${environment.NEXLABS_ENV}` };
  }
  if (value !== "PRODUCTION") {
    return { ok: false, reason: "Release validation requires NEXLABS_ENV=PRODUCTION" };
  }

  const rawOrigin = environment.NEXT_PUBLIC_SITE_ORIGIN;
  if (!rawOrigin) {
    return { ok: false, reason: "Production releases require NEXT_PUBLIC_SITE_ORIGIN" };
  }

  let origin;
  try {
    origin = new URL(rawOrigin);
  } catch {
    return { ok: false, reason: "NEXT_PUBLIC_SITE_ORIGIN must be a valid URL" };
  }

  if (origin.protocol !== "https:") {
    return { ok: false, reason: "Production releases require an HTTPS NEXT_PUBLIC_SITE_ORIGIN" };
  }
  if (origin.pathname !== "/" || origin.search || origin.hash || origin.username || origin.password) {
    return { ok: false, reason: "NEXT_PUBLIC_SITE_ORIGIN must contain an HTTPS origin without credentials, path, query, or hash" };
  }

  return { ok: true, origin: origin.origin };
}

const entrypoint = process.argv[1] ? pathToFileURL(process.argv[1]).href : "";
if (import.meta.url === entrypoint) {
  const result = validateReleaseEnvironment();
  if (!result.ok) {
    console.error(`Release validation failed: ${result.reason}`);
    process.exitCode = 1;
  } else {
    console.log(`Release validation passed for ${result.origin}`);
  }
}
