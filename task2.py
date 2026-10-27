import csv
import math
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

NAME = "Your Name"
SURNAME = "Your Surname"
GROUP = "Your Group"
EXPENSES_FILE = Path(__file__).parent / "data" / "expenses.csv"
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def month_info(day):
    first = day.replace(day=1)
    if first.month == 12:
        next_first = date(first.year + 1, 1, 1)
    else:
        next_first = date(first.year, first.month + 1, 1)
    return (next_first - first).days, next_first


def main():
    print(f"{NAME} {SURNAME}, {GROUP}")
    if not EXPENSES_FILE.is_file():
        print(f"error: missing file {EXPENSES_FILE}; copy your work-22 expenses.csv to lab30/data/expenses.csv", file=sys.stderr)
        sys.exit(1)

    entries = []
    with EXPENSES_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        for line_number, line in enumerate(file, 1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            try:
                row = next(csv.reader([line], delimiter=";"))
                if len(row) < 3:
                    raise ValueError("expected date;category;amount;...")
                day = date.fromisoformat(row[0].strip())
                amount = float(row[2].strip())
                if not math.isfinite(amount) or amount < 0:
                    raise ValueError("amount must be a non-negative number")
                entries.append((day, amount))
            except (ValueError, StopIteration) as error:
                print(f"warning: line {line_number}: {error}; skipped", file=sys.stderr)

    if not entries:
        print("error: no valid expense rows found", file=sys.stderr)
        sys.exit(1)

    first_day = min(day for day, _ in entries)
    last_day = max(day for day, _ in entries)
    days_count = (last_day - first_day).days + 1
    totals = defaultdict(list)
    for day, amount in entries:
        totals[day].append(amount)
    daily = {first_day + timedelta(days=i): math.fsum(totals[first_day + timedelta(days=i)]) for i in range(days_count)}

    print(f"period: {first_day:%d.%m.%Y} ({first_day:%A}) - {last_day:%d.%m.%Y} ({last_day:%A}), {days_count} days")
    print("\nweekday      total")
    weekday_totals = [math.fsum(amount for day, amount in entries if day.weekday() == index) for index in range(7)]
    for weekday, total in zip(WEEKDAYS, weekday_totals):
        print(f"{weekday:<12}{total:>8.2f}")

    all_amounts = [amount for amount in daily.values()]
    total = math.fsum(all_amounts)
    average = total / days_count
    variance = math.fsum((value - average) ** 2 for value in all_amounts) / days_count
    stddev = math.sqrt(variance)
    top_day = max(daily, key=daily.get)
    no_spend = sum(value == 0 for value in daily.values())
    month_days, next_month = month_info(last_day)
    days_left = (next_month - last_day).days - 1
    forecast = average * month_days

    print(f"\ntotal:        {total:.2f}")
    print(f"per day:      {average:.2f} +- {stddev:.2f}")
    print(f"top day:      {top_day:%d.%m.%Y} ({top_day:%A}), {daily[top_day]:.2f}")
    print(f"no-spend days: {no_spend}")
    print(f"days in {last_day:%B}: {month_days}, left after {last_day:%d.%m}: {days_left}")
    print(f"month forecast: {forecast:.2f}")

    for sample in (date(2026, 12, 15), date(2028, 2, 10)):
        count, _ = month_info(sample)
        print(f"month check {sample.isoformat()}: {count} days")


if __name__ == "__main__":
    main()
