import type { MetadataRoute } from "next";
import { getRuntimeConfig } from "@/lib/runtime/env";

export const dynamic = "force-static";

export default function sitemap(): MetadataRoute.Sitemap {
  const config = getRuntimeConfig();
  const origin = config.origin ?? new URL("http://localhost:3000");
  return [
    {
      url: new URL("/", origin).toString(),
      lastModified: new Date("2026-09-19"),
      changeFrequency: "monthly",
      priority: 1,
    },
  ];
}
