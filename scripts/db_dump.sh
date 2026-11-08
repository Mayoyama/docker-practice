#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
mkdir -p backups

# shellcheck disable=SC2016
docker compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" --clean --if-exists' > backups/pg_dump_$(date +%Y%m%d_%H%M%S).sql