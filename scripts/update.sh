#!/bin/sh
# Refresh the snapshot from race.mx and rebuild the CSVs. Run from the repo root.
set -e
cd "$(dirname "$0")/.."
for f in data/calendar.json data/venues.json data/winners.json data/winners-history.json data/winners-history.csv; do
  curl -sfL "https://race.mx/$f" -o "$f"
done
curl -sfL "https://race.mx/race-calendar.ics" -o data/race-calendar.ics
python3 scripts/to_csv.py
echo "Snapshot updated: $(date -u +%Y-%m-%dT%H:%MZ)"
