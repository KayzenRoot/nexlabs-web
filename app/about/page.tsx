import type { Metadata } from "next";
import { InstitutionalPage } from "@/components/sections/InstitutionalPage";
import { siteContent } from "@/content/site";
import { buildSiteMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildSiteMetadata("/about");

export default function AboutPage() {
  return <InstitutionalPage page={siteContent.pages["/about"]} />;
}
