import { Action } from "@/components/ui/Action";
import { Eyebrow } from "@/components/brand/Eyebrow";
import type { SiteContent } from "@/lib/content/types";

export function HeroCopy({ hero }: { hero: SiteContent["hero"] }) {
  return <div className="hero-copy"><Eyebrow>{hero.eyebrow}</Eyebrow><h1 id="home-heading">{hero.heading}</h1><p className="hero-body">{hero.body}</p><div className="action-row" aria-label="Featured links"><Action href={hero.primaryAction.href} external variant="primary">{hero.primaryAction.label}</Action><Action href={hero.secondaryAction.href} external variant="secondary">{hero.secondaryAction.label}</Action></div></div>;
}
