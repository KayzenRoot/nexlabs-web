import type { MetadataRoute } from "next";
import { getRuntimeConfig } from "@/lib/runtime/env";

export const dynamic = "force-static";

export default function robots(): MetadataRoute.Robots {
  const config = getRuntimeConfig();
  const origin = config.origin?.toString();
  return {
    rules: {
      userAgent: "*",
      allow: config.isIndexable ? "/" : [],
      disallow: config.isIndexable ? [] : "/",
    },
    sitemap: config.isIndexable && origin ? `${origin}sitemap.xml` : undefined,
  };
}
