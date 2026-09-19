export const APP_ENVIRONMENTS = ["LOCAL", "PREVIEW", "PRODUCTION"] as const;
export type AppEnvironment = (typeof APP_ENVIRONMENTS)[number];

function parseEnvironment(value: string | undefined): AppEnvironment {
  const normalized = (value ?? "LOCAL").toUpperCase();
  if ((APP_ENVIRONMENTS as readonly string[]).includes(normalized)) return normalized as AppEnvironment;
  throw new Error(`Unsupported NEXLABS_ENV: ${value}`);
}

function parseOrigin(value: string | undefined): URL | undefined {
  if (!value) return undefined;
  const origin = new URL(value);
  if (origin.pathname !== "/" || origin.search || origin.hash) {
    throw new Error("NEXT_PUBLIC_SITE_ORIGIN must contain an origin without a path, query, or hash");
  }
  return origin;
}

export interface RuntimeConfig {
  environment: AppEnvironment;
  origin?: URL;
  isProduction: boolean;
  isIndexable: boolean;
}

export function getRuntimeConfig(): RuntimeConfig {
  const environment = parseEnvironment(process.env.NEXLABS_ENV);
  const origin = parseOrigin(process.env.NEXT_PUBLIC_SITE_ORIGIN);
  return {
    environment,
    origin,
    isProduction: environment === "PRODUCTION",
    isIndexable: environment === "PRODUCTION",
  };
}

export function assertReleaseEnvironment(config = getRuntimeConfig()): RuntimeConfig {
  if (!config.isProduction) throw new Error("Release validation requires NEXLABS_ENV=PRODUCTION");
  if (!config.origin) throw new Error("Production releases require NEXT_PUBLIC_SITE_ORIGIN");
  return config;
}
