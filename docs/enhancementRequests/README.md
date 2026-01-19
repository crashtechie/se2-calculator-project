# Enhancement Requests

This directory contains all enhancement requests for the SE2 Calculator Project.

## Naming Convention

**Format:** `<status>-enh<0000000>-<short-description>.md`

**Components:**
- `<status>` - Current status: `inReview`, `inProgress`, or `completed`
- `<0000000>` - 7-digit sequential number starting from 0000001
- `<short-description>` - Brief kebab-case description

**Examples:**
- `inReview-enh0000001-add-user-authentication.md`
- `inProgress-enh0000002-export-build-orders-csv.md`
- `completed-enh0000003-dark-mode-support.md`

## Status Definitions

| Status | Description |
|--------|-------------|
| `inReview` | Enhancement is being reviewed and discussed |
| `inProgress` | Enhancement is actively being implemented |
| `completed` | Enhancement has been implemented and merged |

## Workflow

1. **Create** - Copy `enhancementRequestTemplate.md` and rename with next sequential number
2. **Review** - File starts with `inReview-` status
3. **Approve** - Once approved, rename to `inProgress-`
4. **Complete** - When merged, rename to `completed-`

## Creating a New Enhancement Request

1. Copy the template:
   ```bash
   cp enhancementRequestTemplate.md inReview-enh0000001-your-description.md
   ```

2. Fill in all sections of the template

3. Update the Enhancement ID in the document to match the filename number

4. Commit and create a pull request for review

## Renaming on Status Change

When status changes, rename the file:
```bash
# Moving from review to in progress
git mv inReview-enh0000001-feature.md inProgress-enh0000001-feature.md

# Moving from in progress to completed
git mv inProgress-enh0000001-feature.md completed-enh0000001-feature.md
```

## Current Enhancements

Check this directory for all enhancement requests. Filter by status prefix to see:
- `inReview-*` - Pending review
- `inProgress-*` - Currently being worked on
- `completed-*` - Finished enhancements
