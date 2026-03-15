#!/bin/sh
# Main commit
# Usage: scripts/commit-main.sh <type> <scope> <message...>
# type: feat|fix|refactor|docs|test|chore

set -e
TYPE="$1"
SCOPE="$2"
shift 2 || true
MSG="$*"

if [ -z "$TYPE" ] || [ -z "$SCOPE" ] || [ -z "$MSG" ]; then
  echo "Usage: scripts/commit-main.sh <type> <scope> <message...>"
  exit 1
fi

git add -A
git commit -m "$TYPE($SCOPE): $MSG"
