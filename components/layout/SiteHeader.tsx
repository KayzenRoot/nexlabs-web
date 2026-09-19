import { siteContent } from "@/content/site";
import Link from "next/link";
import { DesktopNav } from "@/components/layout/DesktopNav";
import { MobileNav } from "@/components/layout/MobileNav";
import { ThemeController } from "@/components/system/ThemeController";
import { Wordmark } from "@/components/brand/Wordmark";

export function SiteHeader() {
  return (
    <header className="site-header">
      <div className="shell header-inner">
        <Link href="/" aria-label="NexLabs home"><Wordmark /></Link>
        <div className="header-tools"><DesktopNav items={siteContent.navigation} /><MobileNav items={siteContent.navigation} /><ThemeController /></div>
      </div>
    </header>
  );
}
