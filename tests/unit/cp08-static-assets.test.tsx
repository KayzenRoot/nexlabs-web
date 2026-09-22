import { render } from "@testing-library/react";
import { StaticContextCore } from "@/components/three/StaticContextCore";
import { contextCoreStaticFallbacks } from "@/three/core/contextCoreAssets";

describe("CP-08 responsive static hero derivatives", () => {
  it.each([
    "landscape",
    "portrait",
    "square",
  ] as const)("keeps the accepted PNG fallback and serves local AVIF/WebP for %s", (framing) => {
    const fallback = contextCoreStaticFallbacks[framing];
    const sourceRatio = { landscape: "16x9", portrait: "4x5", square: "1x1" }[framing];
    const { container } = render(<StaticContextCore />);
    const picture = container.querySelector(`.context-core-static-${framing}`);

    expect(fallback.url).toBe(`/images/context-core/hero-${sourceRatio}.png`);
    expect(picture?.querySelector('source[type="image/avif"]')?.getAttribute("srcset")).toBe(fallback.avifUrl);
    expect(picture?.querySelector('source[type="image/webp"]')?.getAttribute("srcset")).toBe(fallback.webpUrl);
    expect(picture?.querySelector("img")?.getAttribute("src")).toBe(fallback.url);
    expect(picture?.querySelector("img")?.getAttribute("alt")).toBe("");
    expect(fallback.avifUrl).toMatch(/^\/release-visuals\/hero\/.+\.avif$/);
    expect(fallback.webpUrl).toMatch(/^\/release-visuals\/hero\/.+\.webp$/);
  });
});
