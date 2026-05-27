# Source Access Policy

Standards and regulatory material often has mixed access and redistribution
rules. This repo defaults to a conservative public boundary.

## Access Levels

- `public_web`: public official web page or notice.
- `public_metadata`: metadata is public, full text is not redistributed here.
- `restricted_standard`: paid, licensed, or access-controlled standard.
- `private_document`: enterprise or user-provided private file.
- `unknown`: access status is not yet verified.

## Redistribution Policies

- `public_ok`: content can be stored publicly.
- `metadata_only`: public repo stores metadata and locators only.
- `private_processing_only`: text can be processed only in a private workspace.
- `do_not_store`: do not persist the content.
- `unknown`: block public publication until reviewed.

## Default Rules

1. Public repositories should store source metadata, locators, hashes, and run
   logs, not restricted standards text.
2. Restricted standards should be handled as bring-your-own-document inputs in a
   private workspace.
3. Public examples must be synthetic or clearly public-domain/public-license.
4. Every source manifest record must include access and redistribution fields.
5. If policy is unknown, treat it as `metadata_only` or `private_processing_only`
   until a human reviewer decides otherwise.
