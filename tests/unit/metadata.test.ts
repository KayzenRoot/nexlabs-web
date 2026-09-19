import { buildSiteMetadata } from "@/lib/metadata";

describe("metadata helper", () => {
  it("keeps local builds non-indexable without inventing an origin", () => {
    delete process.env.NEXLABS_ENV;
    delete process.env.NEXT_PUBLIC_SITE_ORIGIN;
    const metadata = buildSiteMetadata();
    expect(metadata.metadataBase).toBeUndefined();
    expect(metadata.robots).toEqual({ index: false, follow: false });
  });

  it("creates canonical production metadata only from an explicit origin", () => {
    process.env.NEXLABS_ENV = "PRODUCTION";
    process.env.NEXT_PUBLIC_SITE_ORIGIN = "https://example.invalid";
    const metadata = buildSiteMetadata();
    expect(metadata.alternates?.canonical).toBe("/");
    expect(metadata.robots).toEqual({ index: true, follow: true });
    delete process.env.NEXLABS_ENV;
    delete process.env.NEXT_PUBLIC_SITE_ORIGIN;
  });
});
