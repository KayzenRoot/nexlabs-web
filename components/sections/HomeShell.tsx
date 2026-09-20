import { siteContent } from "@/content/site";
import { EvidenceCard } from "@/components/brand/EvidenceCard";
import { HeroCopy } from "@/components/brand/HeroCopy";
import { HeroVisualSlot, VisualSlot } from "@/components/media/VisualSlot";
import { TechnicalDiagram } from "@/components/diagram/TechnicalDiagram";
import { ContentSectionView } from "@/components/sections/ContentSectionView";
import { Heading } from "@/components/ui/Typography";
import { Container, Section } from "@/components/ui/Layout";

function homeSection(id: string) {
  const section = siteContent.homeSections.find((item) => item.id === `home-${id}`);
  if (!section) throw new Error(`Missing home section: ${id}`);
  return section;
}

export function HomeShell() {
  const h02 = homeSection("h02");
  const h03 = homeSection("h03");
  const h04 = homeSection("h04");
  const h05 = homeSection("h05");
  const h06 = homeSection("h06");
  const h07 = homeSection("h07");
  const h08 = homeSection("h08");
  const h09 = homeSection("h09");

  return (
    <>
      <Section className="hero" aria-labelledby="home-heading"><Container size="wide" className="hero-grid"><HeroCopy hero={siteContent.hero} /><HeroVisualSlot /></Container></Section>
      <Section className="home-story-section" aria-labelledby={`${h02.id}-heading`}><Container size="reading"><ContentSectionView section={h02} /></Container></Section>
      <Section className="evidence-section" aria-labelledby={`${h03.id}-heading`}><Container size="content" className="section-grid"><ContentSectionView section={h03} /><VisualSlot label="Static HIVE system view" description="A neutral visual boundary for future approved media." /></Container></Section>
      <Section className="system-story-section" aria-labelledby={`${h04.id}-heading`}><Container size="content" className="section-grid"><ContentSectionView section={h04} /><TechnicalDiagram /></Container></Section>
      <Section className="principles-section" aria-labelledby={`${h05.id}-heading`}><Container size="content"><ContentSectionView section={h05} /></Container></Section>
      <Section className="evidence-section" aria-labelledby={`${h06.id}-heading`}><Container size="content" className="section-grid"><ContentSectionView section={h06} /><div><Heading level={2} eyebrow="Evidence" id="home-evidence-heading">Public starting points.</Heading>{siteContent.evidence.map((evidence) => <EvidenceCard evidence={evidence} key={evidence.id} />)}</div></Container></Section>
      <Section className="home-story-section" aria-labelledby={`${h07.id}-heading`}><Container size="reading"><ContentSectionView section={h07} /></Container></Section>
      <Section className="home-story-section" aria-labelledby={`${h08.id}-heading`}><Container size="reading"><ContentSectionView section={h08} /></Container></Section>
      <Section className="final-cta-section" aria-labelledby={`${h09.id}-heading`}><Container size="reading"><ContentSectionView section={h09} /></Container></Section>
    </>
  );
}
