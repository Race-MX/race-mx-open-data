"""Write calendar.csv, venues.csv and latest-winners.csv from the race.mx JSON files."""
import csv, json, os

here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

def write(src, key, dst):
    rows = json.load(open(os.path.join(here, src), encoding="utf-8"))[key]
    cols = []
    for r in rows:
        for k in r:
            if k not in cols:
                cols.append(k)
    with open(os.path.join(here, dst), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in cols})
    print(dst, len(rows), "rows")

write("calendar.json", "events", "calendar.csv")
write("venues.json", "venues", "venues.csv")
write("winners.json", "winners", "latest-winners.csv")
