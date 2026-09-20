import type { Metadata } from "next";
import { InstitutionalPage } from "@/components/sections/InstitutionalPage";
import { siteContent } from "@/content/site";
import { buildSiteMetadata } from "@/lib/metadata";

export const metadata: Metadata = buildSiteMetadata("/hive");

export default function HivePage() {
  return <InstitutionalPage page={siteContent.pages["/hive"]} />;
}
