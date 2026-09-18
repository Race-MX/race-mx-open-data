---
license: cc-by-4.0
language:
- en
pretty_name: Race.mx Mexican Motorsport Open Data
tags:
- motorsport
- mexico
- formula-1
- baja-1000
- nascar
- sports
size_categories:
- n<1K
configs:
- config_name: winners_history
  data_files: data/winners-history.csv
  default: true
- config_name: calendar
  data_files: data/calendar.csv
- config_name: venues
  data_files: data/venues.csv
- config_name: latest_winners
  data_files: data/latest-winners.csv
---

# Race.mx Mexican Motorsport Open Data

Open data on motorsport in Mexico, published by [Race.mx](https://race.mx), an independent English-language guide to racing in Mexico:

- **Winners history**: every Formula 1 Mexican / Mexico City Grand Prix since 1962, Baja 1000 overall winners since 1967, Baja 500 winners since 2010, every Formula E Mexico City E-Prix, and NASCAR Mexico Series champions since 2004.
- **Race calendar**: the current season's major races in Mexico (F1, SCORE desert racing, NASCAR Mexico Series, Formula E), with dates, venue and status (scheduled, completed, cancelled).
- **Venues**: circuits and start/finish locations with location, length, surface, lap record and coordinates.

Every figure is taken from an official source (the series, promoter, circuit or a government agency) or from two independent reputable outlets. The source page for each row is linked in the data. Race.mx publishes corrections openly; see its [editorial standards](https://race.mx/editorial-standards/).

## Files

| File | What it contains |
|---|---|
| `data/winners-history.csv` / `.json` | Year-by-year winners for each race series, one row per race |
| `data/calendar.csv` / `.json` | Current-season race calendar with status |
| `data/venues.csv` / `.json` | Tracks and start/finish venues |
| `data/latest-winners.csv` / `winners.json` | Most recent winner of each headline race |
| `data/race-calendar.ics` | The calendar as an iCalendar feed |

The files here are a snapshot. The live versions, updated whenever the site changes, are at:

- https://race.mx/data/winners-history.json and https://race.mx/data/winners-history.csv
- https://race.mx/data/calendar.json
- https://race.mx/data/venues.json
- https://race.mx/data/winners.json
- https://race.mx/race-calendar.ics

To refresh the snapshot, run `scripts/update.sh`.

## Notes on the data

- **Winners history.** The winners table has different columns for different series (for example `fastest_car_truck` and `fastest_motorcycle` for SCORE races, `pole_position` for F1). `status` is `held`, `not_held` or `cancelled`. The Baja 1000 before 2000 has one overall winner per year; from 2000 SCORE lists the fastest car/truck and fastest motorcycle separately, and `outright_fastest` records which was quicker.
- **Calendar.** `status` is derived from the dates unless the organizer has cancelled, postponed or rescheduled the event.
- **Venues.** `length` is the main circuit length; some venues have more than one layout (the venue page explains which one each series uses). Desert-race start/finish locations have no fixed length.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). You can reuse, adapt and redistribute the data, including commercially, as long as you credit **Race.mx** and link to https://race.mx.

## Citation

> Race.mx (2026). *Race.mx Mexican Motorsport Open Data*. https://race.mx/open-data/

See `CITATION.cff` for machine-readable citation metadata.

## Contact and corrections

Spotted an error? Email contact@race.mx with the row and your source. Corrections are made on race.mx and flow into the next snapshot.
