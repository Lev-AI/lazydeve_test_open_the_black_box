#!/bin/sh
# Create ADR from template with auto-increment ID
# Usage: scripts/create-adr.sh <slug>
set -e

SLUG="$1"
if [ -z "$SLUG" ]; then
  echo "Usage: scripts/create-adr.sh <slug>"
  exit 1
fi

mkdir -p docs/adr

LAST=$(ls -1 docs/adr/ADR-[0-9][0-9][0-9]-*.md 2>/dev/null | sed -E 's/.*ADR-([0-9]+)-.*/\1/' | sort -n | tail -1)
if [ -z "$LAST" ]; then
  NEXT=1
else
  NEXT=$((LAST + 1))
fi

ID=$(printf "%03d" "$NEXT")
FILE="docs/adr/ADR-$ID-$SLUG.md"

cat > "$FILE" <<'EOF'
# ADR-XXX: <Title>

**Status:** Draft | Accepted | Rejected
**Date:** YYYY-MM-DD
**Deciders:** <names>

## Context
<What problem are we solving?>

## Decision
<What did we decide?>

## Rationale
<Why this decision?>

## Consequences
<Good and bad effects>

## Alternatives Considered
<Other options>

## References
- Links / docs / PRs
EOF

# Replace placeholders
DATE=$(date +%Y-%m-%d)
sed -i.bak -e "s/ADR-XXX/ADR-$ID/g" -e "s/YYYY-MM-DD/$DATE/g" "$FILE" 2>/dev/null || true
rm -f "$FILE.bak" 2>/dev/null || true

echo "✅ Created $FILE"
echo "Next:"
echo "  1) Fill sections"
echo "  2) Commit: git commit -m "docs(adr): add ADR-$ID $SLUG""
