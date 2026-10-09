# Publication notes

## Package contents

README.md is the proposed repository landing page. docs/EVIDENCE-INDEX.md links all 47 screenshots. docs/PORTFOLIO-SUMMARY.md contains project wording and interview material. Existing application source files are not included or changed.

## Screenshot handling

Images are copied without pixel edits. Duplicate upload suffixes and extensions have been removed. Filenames 22, 37, 42, 46, and 47 were adjusted to avoid implying independent validation, direct database inspection, or a proven downstream update.

The inspected screenshots keep credential fields masked and do not print the bearer-token environment variable. They still show test-user email addresses, a lab tenant hostname, audit IDs, and some machine or account context. Confirm these are intended public lab identities; redact personal details in publication copies if needed. No claim that every screenshot is sanitized is made.

## GitHub upload

1. Extract the ZIP locally.
2. In the repository, select Add file → Upload files.
3. Upload the screenshots and docs folders and README.md, preserving their relative paths.
4. Review the replacement README and commit the documentation change. Keep app.py and requirements.txt unchanged.
5. Open README.md and the evidence index on GitHub to confirm image rendering and links.

Suggested commit message: Document complete Okta lab with 47 screenshots and verified outcome boundaries

This documentation has been checked locally for all image links and screenshot numbering. The upload instructions above also support future manual documentation updates.

