import Link from "next/link";
import type { AnchorHTMLAttributes } from "react";

type ActionProps = AnchorHTMLAttributes<HTMLAnchorElement> & {
  href: string;
  variant?: "primary" | "secondary" | "quiet";
  external?: boolean;
};

export function Action({ children, className = "", variant = "secondary", external, href, ...props }: ActionProps) {
  const classes = ["action", `action-${variant}`, className].filter(Boolean).join(" ");
  const label = <>{children}{external ? <span className="sr-only"> (opens in a new tab)</span> : null}</>;
  if (external) {
    return <a className={classes} href={href} rel="noreferrer" target="_blank" {...props}>{label}</a>;
  }
  return <Link className={classes} href={href} {...props}>{label}</Link>;
}

export function ExternalEvidenceLink({ href, children, ...props }: ActionProps) {
  return <Action href={href} external variant="quiet" {...props}>{children}</Action>;
}
