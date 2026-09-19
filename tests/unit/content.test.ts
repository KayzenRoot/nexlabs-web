import { siteContent } from "@/content/site";
import { collectContentErrors } from "@/lib/content/validation";

describe("site content", () => {
  it("accepts the canonical CP-01 content contract", () => {
    expect(collectContentErrors(siteContent)).toEqual([]);
    expect(siteContent.contact.publicEmail).toBeNull();
    expect(siteContent.contact.founder.approved).toBe(false);
  });
});
