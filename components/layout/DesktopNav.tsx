import Link from "next/link";
import type { NavigationItem } from "@/lib/content/types";

export function DesktopNav({ items }: { items: NavigationItem[] }) {
  return (
    <nav className="desktop-nav" aria-label="Primary navigation">
      <ul className="nav-list">
        {items.map((item) => <li key={item.href}>{item.external ? <a href={item.href} rel="noreferrer" target="_blank">{item.label}<span className="sr-only"> (opens in a new tab)</span></a> : <Link href={item.href}>{item.label}</Link>}</li>)}
        <li><a href="https://github.com/KayzenRoot" rel="noreferrer" target="_blank">GitHub<span className="sr-only"> (opens in a new tab)</span></a></li>
      </ul>
    </nav>
  );
}
