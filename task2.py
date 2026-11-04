from collections import defaultdict
import csv
from pathlib import Path
from tabulate import tabulate

STUDENT = "Ivan Petrenko, PZ-11"

print(STUDENT)

totals = defaultdict(float)
counts = defaultdict(int)

path = Path("data/expenses.csv")

with path.open("r", encoding="utf-8-sig", newline="") as file:
    lines = (line for line in file if line.strip() and not line.lstrip().startswith("#"))
    reader = csv.DictReader(lines)

    for row in reader:
        category = (row.get("category") or row.get("Category") or row.get("категорія") or "").strip()
        amount_text = (row.get("amount") or row.get("sum") or row.get("total") or row.get("сума") or "").strip()

        if not category or not amount_text:
            continue

        amount_text = amount_text.replace(",", ".")
        amount = float(amount_text)
        totals[category] += amount
        counts[category] += 1

rows = []
grand_total = 0
grand_count = 0

for category in sorted(totals):
    rows.append([category, counts[category], f"{totals[category]:.2f}"])
    grand_total += totals[category]
    grand_count += counts[category]

rows.append(["TOTAL", grand_count, f"{grand_total:.2f}"])

print(tabulate(rows, headers=["category", "count", "total"], tablefmt="github"))
