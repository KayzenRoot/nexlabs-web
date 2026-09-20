import type { ActionLink, ContentSection, InstitutionalPage } from "@/lib/content/types";

const external = (label: string, href: string): ActionLink => ({ label, href, external: true });
const internal = (label: string, href: string): ActionLink => ({ label, href, external: false });

export const homeSections = [
  {
    id: "home-h02",
    eyebrow: "THE CONTEXT PROBLEM",
    heading: "More intelligence does not automatically create more continuity.",
    body: "Long-running software projects still need durable context, efficient retrieval, traceable decisions and reliable engineering controls.",
  },
  {
    id: "home-h03",
    eyebrow: "FIRST FLAGSHIP",
    heading: "HIVE turns project context into infrastructure.",
    body: "The pinned HIVE repository describes a local-first platform for project context, memory, retrieval, token optimization and governed execution.",
    links: [external("Explore HIVE", "https://github.com/KayzenRoot/hive"), internal("HIVE overview", "/hive")],
  },
  {
    id: "home-h04",
    eyebrow: "FROM INFORMATION TO CONTEXT",
    heading: "Fragment. Index. Retrieve. Assemble. Resolve.",
    body: "Useful context is not the same as more context. This is a conceptual system story, not a literal HIVE architecture diagram.",
    items: [
      { label: "Fragment", body: "Recognize the distributed pieces of a project." },
      { label: "Index", body: "Give useful information a durable identity." },
      { label: "Retrieve", body: "Find what matters for the current task." },
      { label: "Assemble", body: "Shape a smaller working context." },
      { label: "Resolve", body: "Turn context into a deliberate next step." },
    ],
  },
  {
    id: "home-h05",
    eyebrow: "HOW WE BUILD",
    heading: "Systems around intelligence.",
    items: [
      { label: "Continuity", body: "Preserve useful project knowledge beyond one interaction." },
      { label: "Retrieval", body: "Find relevant information without treating all history equally." },
      { label: "Efficiency", body: "Reduce repeated context movement where architecture can help." },
      { label: "Governance", body: "Make important actions observable, reviewable and controlled." },
      { label: "Evidence", body: "Prefer verifiable behavior over unsupported claims." },
    ],
  },
  {
    id: "home-h06",
    eyebrow: "PUBLIC ENGINEERING",
    heading: "Inspect the work, not just the claim.",
    body: "The HIVE repository is the public technical starting point for the first NexLabs flagship. Its current license and rights statement remain the source of truth.",
    links: [external("View HIVE on GitHub", "https://github.com/KayzenRoot/hive"), internal("Evidence and rights", "/open-source")],
  },
  {
    id: "home-h07",
    eyebrow: "NEXLABS",
    heading: "AI-native software needs an infrastructure layer of its own.",
    body: "NexLabs is exploring infrastructure around increasingly capable AI-assisted development systems, starting with context, retrieval, memory, evidence and control.",
  },
  {
    id: "home-h08",
    eyebrow: "BUILT FROM BRAZIL",
    heading: "Global ambition. Engineering first.",
    body: "NexLabs is an early-stage technology initiative being built from Brazil for a global developer and technology market.",
  },
  {
    id: "home-h09",
    heading: "Explore what we're building.",
    links: [internal("Explore HIVE", "/hive"), internal("Contact NexLabs", "/contact"), external("GitHub", "https://github.com/KayzenRoot")],
  },
] satisfies ContentSection[];

export const institutionalPages = {
  "/hive": {
    path: "/hive",
    eyebrow: "HIVE BY NEXLABS",
    heading: "Durable context infrastructure for AI-assisted development.",
    body: "The pinned HIVE v1.0.0 repository describes a local-first platform for project context, memory, retrieval, token optimization and governed execution. It is a stable release candidate, not a published stable release.",
    actions: [external("View HIVE on GitHub", "https://github.com/KayzenRoot/hive"), internal("Technology thesis", "/technology")],
    sections: [
      { id: "hive-problem", heading: "A long project should not start from zero every time context changes.", body: "AI-assisted development spans repositories, documents, decisions, prompts, checkpoints and execution history. HIVE is designed to organize that information into persistent project context that can be retrieved progressively." },
      { id: "hive-capabilities", eyebrow: "CAPABILITY SURFACE", heading: "Context with explicit boundaries.", items: [
        { label: "Project context", body: "Maintain durable project state beyond one model interaction." },
        { label: "Retrieval", body: "Use lexical, semantic and hybrid retrieval with deterministic fallback." },
        { label: "Progressive context", body: "Expose useful context levels instead of loading everything at once." },
        { label: "Efficiency", body: "Apply adaptive token budgeting, fingerprints and delta context." },
        { label: "Governed execution", body: "Keep assistance and system action behind explicit governance boundaries." },
        { label: "Observability", body: "Expose operational state through bounded, provenance-labelled surfaces." },
      ] },
      { id: "hive-architecture", eyebrow: "ARCHITECTURE", heading: "Local-first infrastructure with explicit system boundaries.", body: "The repository documents persistent storage, retrieval, context management, caching, governance and observability components. Git remains the canonical source history; derived artifacts do not replace it." },
      { id: "hive-rights", eyebrow: "PUBLIC SOURCE AND RIGHTS", heading: "Publicly inspectable does not mean open-source licensed.", body: "The pinned repository LICENSE says All Rights Reserved and grants viewing and evaluation rights only. NexLabs does not publish an Apache-2.0 claim for this source." , links: [external("Read the repository", "https://github.com/KayzenRoot/hive"), external("Read the license", "https://github.com/KayzenRoot/hive/blob/main/LICENSE")] },
    ],
  },
  "/technology": {
    path: "/technology",
    eyebrow: "TECHNOLOGY THESIS",
    heading: "Intelligence needs infrastructure.",
    body: "More capable AI systems create new possibilities for software development, but capability alone does not solve continuity, retrieval, evidence, efficiency or control.",
    actions: [internal("See HIVE", "/hive"), internal("Read the evidence", "/open-source")],
    sections: [
      { id: "technology-context", heading: "Context should persist.", body: "Project knowledge should survive beyond individual sessions and model windows." },
      { id: "technology-retrieval", heading: "Relevance beats volume.", body: "The useful working set is rarely the entire history. Infrastructure should help identify and assemble what matters now." },
      { id: "technology-efficiency", heading: "Move less. Reuse more.", body: "Repeatedly transferring the same information is an architectural cost. Structured context, caching and incremental approaches can reduce repetition." },
      { id: "technology-governance", heading: "Capability needs boundaries.", body: "As development systems gain autonomy, actions, permissions, evidence and review become part of the infrastructure problem." },
      { id: "technology-open", heading: "Infrastructure should remain inspectable.", body: "HIVE provides the current public implementation evidence for this thesis; future concepts remain directions, not shipped products." },
    ],
  },
  "/open-source": {
    path: "/open-source",
    eyebrow: "PUBLIC ENGINEERING",
    heading: "Engineering you can inspect.",
    body: "NexLabs treats public implementation as technical evidence. HIVE is publicly viewable, but its pinned repository states All Rights Reserved and is not an open-source license.",
    actions: [external("Repository", "https://github.com/KayzenRoot/hive"), internal("HIVE overview", "/hive")],
    sections: [
      { id: "oss-hive", eyebrow: "HIVE", heading: "A public technical starting point.", body: "The HIVE repository contains the implementation, documentation and engineering history available for inspection. Rights and reuse remain governed by its current LICENSE.", links: [external("Repository", "https://github.com/KayzenRoot/hive"), external("License", "https://github.com/KayzenRoot/hive/blob/main/LICENSE"), external("Documentation", "https://github.com/KayzenRoot/hive/tree/main/docs")] },
      { id: "oss-evidence", heading: "Evidence before adjectives.", body: "Public source makes architecture and engineering decisions inspectable. Repository visibility, popularity and release badges are not substitutes for product evidence." },
    ],
  },
  "/about": {
    path: "/about",
    eyebrow: "ABOUT NEXLABS",
    heading: "Building the infrastructure around AI-native software.",
    body: "NexLabs Technology is an early-stage technology initiative being built from Brazil for a global market, focused on developer infrastructure for complex AI-assisted software development.",
    actions: [internal("Technology thesis", "/technology"), internal("Contact NexLabs", "/contact")],
    sections: [
      { id: "about-story", heading: "Start with the hard infrastructure problem.", body: "Increasingly capable AI systems still operate inside projects that need memory, context, retrieval, governance and engineering discipline. HIVE is the first flagship built around that observation." },
      { id: "about-stage", heading: "Early, technical and evidence-driven.", body: "NexLabs is in an early formation stage. Product development and public technical evidence come before claims about incorporation, scale, customers or traction." },
      { id: "about-founder", heading: "Founder information is not published yet.", body: "No founder biography or personal details are rendered until public facts are explicitly approved and verified." },
    ],
  },
  "/contact": {
    path: "/contact",
    eyebrow: "NEXLABS CONTACT",
    heading: "Contact NexLabs.",
    body: "For technical conversations, open-source collaboration and future program inquiries, use the verified public channel below.",
    actions: [external("Open NexLabs on GitHub", "https://github.com/KayzenRoot")],
    sections: [
      { id: "contact-github", eyebrow: "VERIFIED CHANNEL", heading: "GitHub is the current public contact path.", body: "The NexLabs GitHub organization is the available public channel for repository questions and technical collaboration. A public business email and contact form are not published in this increment.", links: [external("Open GitHub", "https://github.com/KayzenRoot")] },
    ],
  },
  "/privacy": {
    path: "/privacy",
    eyebrow: "PRIVACY",
    heading: "A small site should make small, clear claims.",
    body: "This static institutional site does not publish analytics, forms, advertising cookies or third-party embeds in the current increment.",
    actions: [internal("Return home", "/")],
    sections: [
      { id: "privacy-theme", heading: "Theme preference.", body: "The theme selector may store the chosen dark, light or system preference in browser local storage. This preference is not sent to NexLabs." },
      { id: "privacy-hosting", heading: "Hosting and requests.", body: "The deployed host may process ordinary network requests under its own infrastructure and policies. No additional tracking service is configured by this repository." },
      { id: "privacy-changes", heading: "If behavior changes, this page changes too.", body: "Analytics, forms, cookies, embeds or other processing will not be described here until they are actually introduced and reviewed." },
    ],
  },
} satisfies Record<string, InstitutionalPage>;
