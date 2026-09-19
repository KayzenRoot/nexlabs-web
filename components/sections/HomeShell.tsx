import { siteContent } from "@/content/site";
import { EvidenceCard } from "@/components/brand/EvidenceCard";
import { HeroCopy } from "@/components/brand/HeroCopy";
import { PrincipleCard } from "@/components/brand/PrincipleCard";
import { HeroVisualSlot } from "@/components/media/VisualSlot";
import { TechnicalDiagram } from "@/components/diagram/TechnicalDiagram";
import { Heading } from "@/components/ui/Typography";
import { Container, Section } from "@/components/ui/Layout";

export function HomeShell() {
  const { hero } = siteContent;
  return (
    <>
      <Section className="hero" aria-labelledby="home-heading">
        <Container size="wide" className="hero-grid"><HeroCopy hero={hero} /><HeroVisualSlot /></Container>
      </Section>
      <Section className="evidence-section" aria-labelledby="evidence-heading"><Container size="content" className="section-grid"><div><Heading level={2} eyebrow="Engineering evidence" id="evidence-heading">A public starting point.</Heading>{siteContent.evidence.map((evidence) => <EvidenceCard evidence={evidence} key={evidence.id} />)}</div><TechnicalDiagram /></Container></Section>
      <Section className="principles-section" aria-labelledby="principles-heading"><Container size="content"><Heading level={2} eyebrow="System principles" id="principles-heading">Coherence is a product feature.</Heading><div className="principles-grid"><PrincipleCard label="Context continuity" description="Keep project decisions legible as AI-assisted work changes shape." /><PrincipleCard label="Evidence over assumptions" description="Expose the public starting points that can be inspected and challenged." /><PrincipleCard label="Governed execution" description="Make the path from intent to reliable software observable and deliberate." /></div></Container></Section>
    </>
  );
}
