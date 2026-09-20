import { Action } from "@/components/ui/Action";
import { Container, Section } from "@/components/ui/Layout";
import { ContentSectionView } from "@/components/sections/ContentSectionView";
import type { InstitutionalPage as InstitutionalPageContent } from "@/lib/content/types";

export function InstitutionalPage({ page }: { page: InstitutionalPageContent }) {
  return (
    <>
      <Section className="institutional-hero" aria-labelledby={`${page.path.slice(1)}-page-heading`}>
        <Container size="reading">
          <p className="eyebrow">{page.eyebrow}</p>
          <h1 id={`${page.path.slice(1)}-page-heading`}>{page.heading}</h1>
          <p className="hero-body">{page.body}</p>
          <div className="action-row" aria-label="Page actions">
            {page.actions.map((action) => <Action key={action.href} href={action.href} external={action.external} variant={action.external ? "secondary" : "primary"}>{action.label}</Action>)}
          </div>
        </Container>
      </Section>
      {page.sections.map((section, index) => <Section className={index % 2 ? "institutional-section institutional-section-alt" : "institutional-section"} aria-labelledby={`${section.id}-heading`} key={section.id}><Container size="reading"><ContentSectionView section={section} /></Container></Section>)}
    </>
  );
}
