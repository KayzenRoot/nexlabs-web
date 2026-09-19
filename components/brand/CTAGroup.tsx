import type { ReactNode } from "react";

export function CTAGroup({ children, label }: { children: ReactNode; label?: string }) {
  return <div className="action-row" aria-label={label}>{children}</div>;
}
