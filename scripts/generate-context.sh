#!/bin/sh
# Incremental context generator (Onion Model)
# Usage: scripts/generate-context.sh [base_branch] [output_file]

set -e
BASE_BRANCH="${1:-main}"
OUT="${2:-.mcp/context_incremental.txt}"

mkdir -p .mcp
echo "# AI Development System Context (Incremental / Onion Model)" > "$OUT"
echo "" >> "$OUT"

# Layer 0 — Laws
for f in docs/ARCHITECTURE.md docs/CONVENTIONS.md; do
  if [ -f "$f" ]; then
    echo "=== $f ===" >> "$OUT"
    cat "$f" >> "$OUT"
    echo "" >> "$OUT"
  fi
done

# Latest ADRs (up to 5)
ls -1t docs/adr/ADR-*.md 2>/dev/null | head -n 5 | while read -r adr; do
  echo "--- $adr ---" >> "$OUT"
  cat "$adr" >> "$OUT"
  echo "" >> "$OUT"
done

# Layer 1 — Delta
echo "=== git diff $BASE_BRANCH...HEAD ===" >> "$OUT"
git diff "$BASE_BRANCH...HEAD" >> "$OUT" || true
echo "" >> "$OUT"

# Changed files content
CHANGED=$(git diff --name-only "$BASE_BRANCH...HEAD" || true)
for file in $CHANGED; do
  if [ -f "$file" ]; then
    echo "=== $file ===" >> "$OUT"
    cat "$file" >> "$OUT"
    echo "" >> "$OUT"
  fi
done

echo "✅ Wrote incremental context: $OUT"
