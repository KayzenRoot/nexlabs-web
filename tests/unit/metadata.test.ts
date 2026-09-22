import { buildSiteMetadata } from "@/lib/metadata";
import { siteContent } from "@/content/site";

describe("metadata helper", () => {
  afterEach(() => {
    delete process.env.NEXLABS_ENV;
    delete process.env.NEXT_PUBLIC_SITE_ORIGIN;
  });

  it("keeps local builds non-indexable without inventing an origin", () => {
    delete process.env.NEXLABS_ENV;
    delete process.env.NEXT_PUBLIC_SITE_ORIGIN;
    const metadata = buildSiteMetadata();
    expect(metadata.metadataBase).toBeUndefined();
    expect(metadata.robots).toEqual({ index: false, follow: false });
  });

  it("keeps preview metadata non-indexable even with a preview origin", () => {
    process.env.NEXLABS_ENV = "PREVIEW";
    process.env.NEXT_PUBLIC_SITE_ORIGIN = "https://preview.example.invalid";

    const metadata = buildSiteMetadata();

    expect(metadata.metadataBase).toBeUndefined();
    expect(metadata.alternates).toBeUndefined();
    expect(metadata.robots).toEqual({ index: false, follow: false });
  });

  it("keeps production without an origin non-indexable", () => {
    process.env.NEXLABS_ENV = "PRODUCTION";

    const metadata = buildSiteMetadata();

    expect(metadata.metadataBase).toBeUndefined();
    expect(metadata.alternates).toBeUndefined();
    expect(metadata.robots).toEqual({ index: false, follow: false });
  });

  it("creates canonical production metadata only from an explicit origin", () => {
    process.env.NEXLABS_ENV = "PRODUCTION";
    process.env.NEXT_PUBLIC_SITE_ORIGIN = "https://example.invalid";
    const metadata = buildSiteMetadata();
    expect(metadata.alternates?.canonical).toBe("/");
    expect(metadata.robots).toEqual({ index: true, follow: true });
  });

  it.each([
    ["/", "/release-visuals/og/nexlabs.png"],
    ["/hive", "/release-visuals/og/hive.png"],
    ["/technology", "/release-visuals/og/technology.png"],
  ])("uses the committed local social card for %s without changing canonical copy", (path, image) => {
    const route = siteContent.routes.find((item) => item.path === path);
    const metadata = buildSiteMetadata(path);
    const social = metadata.openGraph;

    expect(social?.title).toBe(route?.title);
    expect(social?.description).toBe(route?.description);
    expect(social?.images).toEqual([{ url: image, width: 1200, height: 630, alt: route?.title }]);
    expect(metadata.twitter).toEqual({ card: "summary_large_image", images: [{ url: image, alt: route?.title }] });
  });
});
