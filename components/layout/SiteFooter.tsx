import { siteContent } from "@/content/site";
import Link from "next/link";

export function SiteFooter() {
  return (
    <footer className="site-footer">
      <div className="shell footer-inner">
        <p>{siteContent.identity.corporateName}</p>
        <p>AI-native developer infrastructure. Built from Brazil for a global market.</p>
        <nav aria-label="Footer navigation"><ul className="footer-links">{siteContent.navigation.filter((item) => !item.external).map((item) => <li key={item.href}><Link href={item.href}>{item.label}</Link></li>)}<li><Link href="/privacy">Privacy</Link></li><li><a href="https://github.com/KayzenRoot" rel="noreferrer" target="_blank">GitHub<span className="sr-only"> (opens in a new tab)</span></a></li></ul></nav>
      </div>
    </footer>
  );
}
