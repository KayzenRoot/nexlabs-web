export type ExternalLinkKind = "github" | "evidence";

export interface NavigationItem {
  label: string;
  href: string;
  external?: boolean;
}

export interface ActionLink {
  label: string;
  href: string;
  external: boolean;
}

export interface EvidenceLink {
  id: string;
  label: string;
  description: string;
  href: string;
  kind: ExternalLinkKind;
}

export interface ContentItem {
  label: string;
  body: string;
}

export interface ContentSection {
  id: string;
  eyebrow?: string;
  heading: string;
  body?: string;
  items?: ContentItem[];
  links?: ActionLink[];
}

export interface InstitutionalPage {
  path: string;
  eyebrow: string;
  heading: string;
  body: string;
  actions: ActionLink[];
  sections: ContentSection[];
}

export interface SiteContent {
  identity: {
    brand: string;
    corporateName: string;
    descriptor: string;
    stage: "pre-incorporation" | "incorporated" | "unknown";
    location: string;
    market: string;
  };
  navigation: NavigationItem[];
  hero: {
    eyebrow: string;
    heading: string;
    body: string;
    primaryAction: ActionLink;
    secondaryAction: ActionLink;
  };
  evidence: EvidenceLink[];
  contact: {
    publicEmail: string | null;
    founder: {
      name: string | null;
      bio: string | null;
      approved: boolean;
    };
  };
  routes: Array<{
    path: string;
    title: string;
    description: string;
    indexable: boolean;
  }>;
  pages: Record<string, InstitutionalPage>;
  homeSections: ContentSection[];
}
