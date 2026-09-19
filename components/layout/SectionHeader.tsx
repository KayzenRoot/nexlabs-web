import type { ReactNode } from "react";
import { Heading } from "@/components/ui/Typography";

export function SectionHeader({ eyebrow, children, id }: { eyebrow?: string; children: ReactNode; id?: string }) {
  return <header className="section-header"><Heading level={2} eyebrow={eyebrow} id={id}>{children}</Heading></header>;
}
