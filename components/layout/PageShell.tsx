import type { ReactNode } from "react";
import { Container } from "@/components/ui/Layout";

export function PageShell({ children }: { children: ReactNode }) {
  return <Container size="wide">{children}</Container>;
}
