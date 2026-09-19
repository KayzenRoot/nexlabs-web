# Workflow instructions

GitHub workflows must use least privilege, pinned action commits, exact candidate checkout, bounded timeouts and deterministic local commands. Do not add secrets, third-party browser scripts or production-domain requirements to ordinary PR validation. Governance must remain an independent required check and is also invoked from `quality`; its required-check migration is independently verified.
