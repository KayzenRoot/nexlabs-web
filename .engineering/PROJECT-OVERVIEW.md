# NexLabs Web Project Overview

Status: `BROWNFIELD_GEF_HIVE_ADOPTION`

## Project

NexLabs Technology institutional web foundation, repository `KayzenRoot/nexlabs-web`.

## Mission

Provide a static-first, accessible institutional shell for NexLabs Technology and later CP packages without inventing unapproved founder, contact, legal or graphical facts.

## Current boundary

CP-01, CP-01R and CP-01F are approved on `main`. CP-02 design-system implementation is present in PR #12. CP-02R adopts GEF/HIVE governance and repairs the PR before any promotion.

## Canonical sources

Product state lives under `docs/project-brain/`. Repository state is the exact Git candidate. GEF records under `.engineering/` are governance bridges and evidence indexes, not replacements for canonical product sources.

## Runtime boundary

Next.js static export produces `out/` for Cloudflare Workers + Static Assets. HIVE remains a separate local-first runtime and is never vendored into this website repository.
