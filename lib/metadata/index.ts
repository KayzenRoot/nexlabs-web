import type { Metadata } from "next";
import { siteContent } from "@/content/site";
import { getRuntimeConfig } from "@/lib/runtime/env";

const socialCards = {
  "/": "/release-visuals/og/nexlabs.png",
  "/hive": "/release-visuals/og/hive.png",
  "/technology": "/release-visuals/og/technology.png",
} as const;

export function buildSiteMetadata(path = "/"): Metadata {
  const config = getRuntimeConfig();
  const title = siteContent.routes.find((route) => route.path === path)?.title ?? siteContent.identity.descriptor;
  const description = siteContent.routes.find((route) => route.path === path)?.description ?? siteContent.hero.body;
  const origin = config.isIndexable ? config.origin : undefined;
  const socialCard = socialCards[path as keyof typeof socialCards];

  return {
    title: {
      default: title,
      template: `%s | ${siteContent.identity.brand}`,
    },
    description,
    applicationName: siteContent.identity.corporateName,
    metadataBase: origin,
    alternates: origin ? { canonical: path } : undefined,
    robots: config.isIndexable ? { index: true, follow: true } : { index: false, follow: false },
    openGraph: {
      type: "website",
      locale: "en_US",
      siteName: siteContent.identity.corporateName,
      title,
      description,
      url: origin ? new URL(path, origin).toString() : undefined,
      images: socialCard ? [{ url: socialCard, width: 1200, height: 630, alt: title }] : undefined,
    },
    twitter: socialCard ? { card: "summary_large_image", images: [{ url: socialCard, alt: title }] } : undefined,
  };
}
