# Change Intelligence

Change intelligence turns source updates into reviewable packets. It is not a
claim that a legal or technical requirement changed unless the packet contains
reviewed evidence.

## Assumptions

- The source manifest is the first layer of truth for status, dates, official
  locators, and replacement relationships.
- A document family may have multiple versions, drafts, replacements, or planned
  revisions.
- Public repositories should store metadata-level change packets by default.
- Provision-level diffs belong in private/BYOD processing unless the source text
  is safe to redistribute.

## Recommended Flow

1. Refresh source manifest metadata.
2. Compare status, dates, replacement relation, and official locator.
3. If authorized text is available, compare provisions by stable locator.
4. Classify changes as metadata refresh, new version, replacement, provision
   change, withdrawal, or unknown.
5. Generate review tasks for low-confidence or high-impact changes.
6. Keep unresolved issues explicit.

## Version Graph Fields

A change packet should preserve:

- old and new document IDs;
- old and new source IDs;
- relation type;
- old and new status;
- old and new effective dates when known;
- evidence locators.

## Watchlist Fields

A future watchlist record should include:

- source ID;
- official URL;
- check cadence;
- last checked time;
- last seen status;
- last seen hash or metadata fingerprint;
- next review task.
