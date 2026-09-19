import Link from "next/link";
import type { AnchorHTMLAttributes, ReactNode } from "react";

export function TextLink({ href, children, ...props }: { href: string; children: ReactNode } & AnchorHTMLAttributes<HTMLAnchorElement>) {
  return <Link href={href} {...props}>{children}</Link>;
}

export function ExternalLink({ href, children, ...props }: { href: string; children: ReactNode } & AnchorHTMLAttributes<HTMLAnchorElement>) {
  return <a href={href} rel="noreferrer" target="_blank" {...props}>{children}<span className="sr-only"> (opens in a new tab)</span></a>;
}
