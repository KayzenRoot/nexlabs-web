# Security Audit Exception Registry

Status: ACTIVE, NARROW EXCEPTION
Date: 2026-09-19

## Purpose

`npm audit --audit-level=high` currently reports the `brace-expansion` advisory `GHSA-mh99-v99m-4gvg` through legacy `minimatch@3.1.5` development-tooling chains.

The locked package is:
- `brace-expansion@1.1.21`

The 1.x maintenance line received the relevant security backports while preserving the CommonJS callable API required by `minimatch@3`. A separate follow-up high advisory, `GHSA-rgw5-rvv9-x895`, records the 1.x patched floor as `1.1.18`. Current package-security databases report `1.1.21` without direct vulnerabilities.

The GitHub advisory record for `GHSA-mh99-v99m-4gvg` has used a flat `<=5.0.7` range that can misclassify the backported 1.x maintenance release.

## Policy

The repository does NOT disable dependency auditing.

`scripts/security-audit.mjs`:
1. runs real `npm audit --json --audit-level=high`;
2. recursively follows propagated vulnerability chains;
3. allows only advisory `GHSA-mh99-v99m-4gvg`;
4. only when the originating package is `brace-expansion`;
5. only when every affected installed node is exactly `1.1.21`;
6. fails for every other HIGH or CRITICAL advisory.

Do not broaden this exception to another package, advisory or version without a new reviewed security decision.

## Why no major override

Forcing `brace-expansion@5` below `minimatch@3` is API-incompatible: legacy minimatch expects the package's CommonJS export itself to be callable.

The repository therefore retains the patched compatible 1.x maintenance release rather than forcing an incompatible major into transitive tooling.

## Revisit triggers

Remove the exception when any of these occurs:
- the advisory database recognizes the 1.x backport correctly;
- upstream consumers stop using minimatch 3.x;
- the lockfile no longer contains brace-expansion 1.x;
- a new advisory affects 1.1.21;
- before a major dependency/toolchain migration.

This exception concerns development/build tooling. It is not permission to suppress unrelated audit findings.
