import type { Metadata } from "next";
import { InstitutionalPage } from "@/components/sections/InstitutionalPage";
import { siteContent } from "@/content/site";
import { buildSiteMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildSiteMetadata("/privacy");

export default function PrivacyPage() {
  return <InstitutionalPage page={siteContent.pages["/privacy"]} />;
}
