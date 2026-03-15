#!/bin/sh
# Quick checkpoint commit (enforced by commit-msg hook)
# Usage: scripts/commit-checkpoint.sh <scope> <message...>

set -e
SCOPE="$1"
shift || true
MSG="$*"

if [ -z "$SCOPE" ] || [ -z "$MSG" ]; then
  echo "Usage: scripts/commit-checkpoint.sh <scope> <message...>"
  exit 1
fi

git add -A
git commit -m "checkpoint($SCOPE): $MSG"
