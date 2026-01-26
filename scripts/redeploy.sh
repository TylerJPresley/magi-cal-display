#!/usr/bin/env bash
# Rebuild and redeploy magi-cal-display
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "==> Building image..."
podman build -t magi-cal-display:latest "$PROJECT_DIR"

echo "==> Stopping and removing old container..."
podman rm -f magi-cal-display 2>/dev/null || true

echo "==> Starting new container..."
podman run -d \
  --name magi-cal-display \
  -p 3000:3000 \
  --env-file "$PROJECT_DIR/magi-cal-display.env.list" \
  magi-cal-display:latest

echo "==> Done. App running at http://localhost:3000"
podman logs -f magi-cal-display
