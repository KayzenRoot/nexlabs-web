import type { Metadata } from "next";
import { InstitutionalPage } from "@/components/sections/InstitutionalPage";
import { siteContent } from "@/content/site";
import { buildSiteMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildSiteMetadata("/technology");

export default function TechnologyPage() {
  return <InstitutionalPage page={siteContent.pages["/technology"]} />;
}
