import sitemap from "@/app/sitemap";

describe("sitemap contract", () => {
  afterEach(() => {
    delete process.env.NEXLABS_ENV;
    delete process.env.NEXT_PUBLIC_SITE_ORIGIN;
  });

  it.each(["LOCAL", "PREVIEW"] as const)("publishes no URLs in %s", (environment) => {
    process.env.NEXLABS_ENV = environment;
    expect(sitemap()).toEqual([]);
  });

  it("publishes no fallback URL for production without an origin", () => {
    process.env.NEXLABS_ENV = "PRODUCTION";
    expect(sitemap()).toEqual([]);
  });

  it("publishes the explicit HTTPS production URL", () => {
    process.env.NEXLABS_ENV = "PRODUCTION";
    process.env.NEXT_PUBLIC_SITE_ORIGIN = "https://example.invalid";

    expect(sitemap()).toEqual([
      {
        url: "https://example.invalid/",
        lastModified: new Date("2026-09-19"),
        changeFrequency: "monthly",
        priority: 1,
      },
    ]);
  });
});
