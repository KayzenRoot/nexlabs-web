import type { MetadataRoute } from "next";
import { siteContent } from "@/content/site";
import { getRuntimeConfig } from "@/lib/runtime/env";

export const dynamic = "force-static";

export default function sitemap(): MetadataRoute.Sitemap {
  const config = getRuntimeConfig();
  if (!config.isIndexable || !config.origin) return [];

  const origin = config.origin;
  return siteContent.routes.filter((route) => route.indexable).map((route) => ({
    url: new URL(route.path, origin).toString(),
    lastModified: new Date("2026-09-19"),
    changeFrequency: "monthly" as const,
    priority: route.path === "/" ? 1 : 0.7,
  }));
}
