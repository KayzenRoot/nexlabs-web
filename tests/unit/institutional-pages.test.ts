import { siteContent } from "@/content/site";
import { buildSiteMetadata } from "@/lib/metadata";

describe("institutional page contract", () => {
  it("keeps route metadata unique and pages complete", () => {
    const routes = siteContent.routes.filter((route) => route.path !== "/");
    expect(Object.keys(siteContent.pages)).toHaveLength(routes.length);
    expect(new Set(routes.map((route) => route.title)).size).toBe(routes.length);
    for (const route of routes) {
      const page = siteContent.pages[route.path as keyof typeof siteContent.pages];
      expect(page.heading).toBeTruthy();
      expect(page.sections.length).toBeGreaterThan(0);
      expect(buildSiteMetadata(route.path).description).toBe(route.description);
    }
  });
});
