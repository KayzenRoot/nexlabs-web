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
  if (content.pages && Object.keys(content.pages).length !== content.routes.filter((route) => route.path !== "/").length) errors.push("institutional pages must match non-home route metadata");
  const routePaths = content.routes.map((route) => route.path);
  if (new Set(routePaths).size !== routePaths.length) errors.push("route paths must be unique");
  const routeTitles = content.routes.map((route) => route.title);
  if (new Set(routeTitles).size !== routeTitles.length) errors.push("route titles must be unique");
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

  for (const route of content.routes) {
    if (!route.path.startsWith("/")) errors.push(`route must be internal: ${route.path}`);
    if (!route.title.trim() || !route.description.trim()) errors.push(`route metadata is incomplete: ${route.path}`);
  }

  for (const page of Object.values(content.pages ?? {})) {
    if (page.actions.length === 0 || page.sections.length === 0) errors.push(`page is incomplete: ${page.path}`);
    if (!routePaths.includes(page.path)) errors.push(`page has no route metadata: ${page.path}`);
    for (const link of [...page.actions, ...page.sections.flatMap((section) => section.links ?? [])]) {
      if (link.external) {
        try { if (new URL(link.href).protocol !== "https:") errors.push(`page link must use HTTPS: ${link.href}`); }
        catch { errors.push(`page link is not a valid URL: ${link.href}`); }
      } else if (!routePaths.includes(link.href)) {
        errors.push(`page link has no route: ${link.href}`);
      }
    }
  }

  return errors;
}

export function assertValidContent<T extends SiteContent>(content: T): T {
  const errors = collectContentErrors(content);
  if (errors.length > 0) throw new Error(`Invalid site content:\n- ${errors.join("\n- ")}`);
  return content;
}
