import { siteContent } from "@/content/site";

export function SiteFooter() {
  return (
    <footer className="site-footer">
      <div className="shell footer-inner">
        <p>{siteContent.identity.corporateName}</p>
        <p>Early-stage technology initiative building from Brazil for a global market.</p>
      </div>
    </footer>
  );
}
