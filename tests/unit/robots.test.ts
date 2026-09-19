import robots from "@/app/robots";

describe("robots contract", () => {
  afterEach(() => {
    delete process.env.NEXLABS_ENV;
    delete process.env.NEXT_PUBLIC_SITE_ORIGIN;
  });

  it.each(["LOCAL", "PREVIEW"] as const)("disallows all crawling in %s", (environment) => {
    process.env.NEXLABS_ENV = environment;

    expect(robots()).toEqual({
      rules: {
        userAgent: "*",
        allow: [],
        disallow: "/",
      },
      sitemap: undefined,
    });
  });

  it("allows crawling and publishes the sitemap in production", () => {
    process.env.NEXLABS_ENV = "PRODUCTION";
    process.env.NEXT_PUBLIC_SITE_ORIGIN = "https://example.invalid";

    expect(robots()).toEqual({
      rules: {
        userAgent: "*",
        allow: "/",
        disallow: [],
      },
      sitemap: "https://example.invalid/sitemap.xml",
    });
  });
});
