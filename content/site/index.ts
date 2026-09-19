import rawSite from "./site.json";
import { assertValidContent } from "@/lib/content/validation";
import type { SiteContent } from "@/lib/content/types";

const typedSite = {
  ...rawSite,
  identity: {
    ...rawSite.identity,
    stage: rawSite.identity.stage as SiteContent["identity"]["stage"],
  },
  navigation: rawSite.navigation.map((item) => ({
    ...item,
    external: item.external ?? false,
  })),
  evidence: rawSite.evidence.map((item) => ({
    ...item,
    kind: item.kind as SiteContent["evidence"][number]["kind"],
  })),
} satisfies SiteContent;

export const siteContent = assertValidContent(typedSite);
