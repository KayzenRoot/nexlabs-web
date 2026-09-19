import { siteContent } from "@/content/site";
import Link from "next/link";

export function SiteHeader() {
  return (
    <header className="site-header">
      <div className="shell header-inner">
        <Link className="wordmark" href="/" aria-label="NexLabs home">
          <span aria-hidden="true">N</span>
          <span>{siteContent.identity.brand}</span>
        </Link>
        <nav aria-label="Primary navigation">
          <ul className="nav-list">
            {siteContent.navigation.map((item) => (
              <li key={item.href}>
                {item.external ? <a href={item.href}>{item.label}</a> : <Link href={item.href}>{item.label}</Link>}
              </li>
            ))}
            <li>
              <a href="https://github.com/KayzenRoot" rel="noreferrer" target="_blank">
                GitHub<span className="sr-only"> (opens in a new tab)</span>
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}
