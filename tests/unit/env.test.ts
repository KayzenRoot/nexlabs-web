import { assertReleaseEnvironment, getRuntimeConfig } from "@/lib/runtime/env";

describe("environment contract", () => {
  afterEach(() => {
    delete process.env.NEXLABS_ENV;
    delete process.env.NEXT_PUBLIC_SITE_ORIGIN;
  });

  it("defaults to local without a secret or domain", () => {
    expect(getRuntimeConfig()).toMatchObject({ environment: "LOCAL", isProduction: false, isIndexable: false });
  });

  it("requires an explicit production origin for release validation", () => {
    process.env.NEXLABS_ENV = "PRODUCTION";
    expect(() => assertReleaseEnvironment()).toThrow("NEXT_PUBLIC_SITE_ORIGIN");
    process.env.NEXT_PUBLIC_SITE_ORIGIN = "https://example.invalid";
    expect(assertReleaseEnvironment().origin?.origin).toBe("https://example.invalid");
  });
});
