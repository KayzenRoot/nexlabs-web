import type { SiteContent } from "./types";

const PLACEHOLDER_TOKENS = /\[(?:[A-Z0-9_]+)_?(?:REQUIRED|TODO|TBD)\]|lorem ipsum/i;

export function collectContentErrors(content: SiteContent): string[] {
  const errors: string[] = [];

  if (!content.identity.corporateName.trim()) errors.push("identity.corporateName is required");
  if (!content.identity.brand.trim()) errors.push("identity.brand is required");
  if (!content.identity.descriptor.trim()) errors.push("identity.descriptor is required");
  if (content.navigation.length === 0) errors.push("navigation must contain at least one item");
  if (!content.hero.heading.trim()) errors.push("hero.heading is required");
  if (content.evidence.length === 0) errors.push("at least one evidence link is required");
  if (content.contact.founder.approved && (!content.contact.founder.name || !content.contact.founder.bio)) {
    errors.push("approved founder data must include name and bio");
  }

  const strings = JSON.stringify(content);
  if (PLACEHOLDER_TOKENS.test(strings)) errors.push("content contains an unresolved placeholder token");

  for (const item of content.navigation) {
    if (!item.href.startsWith("/") && !item.external) errors.push(`navigation link is not explicitly external: ${item.href}`);
  }

  for (const link of content.evidence) {
    try {
      const url = new URL(link.href);
      if (url.protocol !== "https:") errors.push(`evidence link must use HTTPS: ${link.href}`);
    } catch {
      errors.push(`evidence link is not a valid URL: ${link.href}`);
    }
  }

  return errors;
}

export function assertValidContent<T extends SiteContent>(content: T): T {
  const errors = collectContentErrors(content);
  if (errors.length > 0) throw new Error(`Invalid site content:\n- ${errors.join("\n- ")}`);
  return content;
}
