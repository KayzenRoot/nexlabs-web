import { assertReleaseEnvironment, getRuntimeConfig } from "@/lib/runtime/env";

describe("environment contract", () => {
  afterEach(() => {
    delete process.env.NEXLABS_ENV;
    delete process.env.NEXT_PUBLIC_SITE_ORIGIN;
  });

  it("defaults to local without a secret or domain", () => {
    expect(getRuntimeConfig()).toMatchObject({ environment: "LOCAL", isProduction: false, isIndexable: false });
  });

  it("keeps preview non-indexable with an optional preview origin", () => {
    process.env.NEXLABS_ENV = "PREVIEW";
    process.env.NEXT_PUBLIC_SITE_ORIGIN = "https://preview.example.invalid";

    expect(getRuntimeConfig()).toMatchObject({ environment: "PREVIEW", isProduction: false, isIndexable: false });
  });

  it("fails closed for production without an origin", () => {
    process.env.NEXLABS_ENV = "PRODUCTION";
    expect(getRuntimeConfig()).toMatchObject({ isProduction: true, isIndexable: false, origin: undefined });
    expect(() => assertReleaseEnvironment()).toThrow("NEXT_PUBLIC_SITE_ORIGIN");
  });

  it("rejects a non-HTTPS production origin", () => {
    process.env.NEXLABS_ENV = "PRODUCTION";
    process.env.NEXT_PUBLIC_SITE_ORIGIN = "http://example.invalid";

    expect(getRuntimeConfig()).toMatchObject({ isProduction: true, isIndexable: false });
    expect(() => assertReleaseEnvironment()).toThrow("HTTPS");
  });

  it("accepts a valid explicit HTTPS production origin", () => {
    process.env.NEXLABS_ENV = "PRODUCTION";
    process.env.NEXT_PUBLIC_SITE_ORIGIN = "https://example.invalid";
    expect(assertReleaseEnvironment().origin?.origin).toBe("https://example.invalid");
  });
});
