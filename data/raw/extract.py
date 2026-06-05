import csv
from pathlib import Path

inp = Path("data/raw/1429_1.csv")
out = Path("data/raw/reviews_1500.csv")

with inp.open(encoding="utf-8", newline="") as fin, out.open("w", encoding="utf-8", newline="") as fout:
    reader = csv.DictReader(fin)
    writer = csv.DictWriter(fout, fieldnames=["id", "title", "text"])
    writer.writeheader()

    n = 0
    for row in reader:
        text = (row.get("reviews.text") or "").strip()
        if not text:
            continue
        writer.writerow({
            "id": (row.get("reviews.id") or "").strip() or str(n),
            "title": (row.get("reviews.title") or "").strip(),
            "text": text,
        })
        n += 1
        if n >= 1500:
            break

print(f"Wrote {n} rows to {out}")