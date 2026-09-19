import { ExternalEvidenceLink } from "@/components/ui/Action";
import type { EvidenceLink } from "@/lib/content/types";

export function EvidenceCard({ evidence }: { evidence: EvidenceLink }) {
  return <article className="evidence-card"><p className="evidence-id">{evidence.id}</p><h3>{evidence.label}</h3><p>{evidence.description}</p><ExternalEvidenceLink href={evidence.href}>Open on GitHub</ExternalEvidenceLink></article>;
}
