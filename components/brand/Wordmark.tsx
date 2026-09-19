import { BrandMark } from "@/components/brand/BrandMark";
import { siteContent } from "@/content/site";

export function Wordmark() {
  return <span className="wordmark"><BrandMark /><span>{siteContent.identity.brand}</span></span>;
}
