import { Action } from "@/components/ui/Action";
import { Heading } from "@/components/ui/Typography";
import type { ContentSection } from "@/lib/content/types";

export function ContentSectionView({ section }: { section: ContentSection }) {
  return (
    <div className="content-section-view">
      <Heading level={2} eyebrow={section.eyebrow} id={`${section.id}-heading`}>{section.heading}</Heading>
      {section.body ? <p className="section-copy">{section.body}</p> : null}
      {section.items?.length ? <div className="content-items">{section.items.map((item) => <article className="content-item" key={item.label}><h3>{item.label}</h3><p>{item.body}</p></article>)}</div> : null}
      {section.links?.length ? <div className="action-row" aria-label={`${section.heading} links`}>{section.links.map((link) => <Action key={link.href} href={link.href} external={link.external} variant={link.external ? "secondary" : "primary"}>{link.label}</Action>)}</div> : null}
    </div>
  );
}
