#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."

if [ ! -d "backups" ]; then
    echo "backup folder not found. Unable to complete restore." >&2
    exit 1
fi

# shellcheck disable=SC2012
DUMP="${1:-$(ls -t backups/*.sql | head -n 1)}"

# shellcheck disable=SC2016
docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < "$DUMP"