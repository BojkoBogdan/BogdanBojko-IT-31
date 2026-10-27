import csv
import math
import random
import sys
from datetime import datetime
from pathlib import Path

NAME = "Your Name"
SURNAME = "Your Surname"
GROUP = "Your Group"
YEAR = 2007
BASE_DIR = Path(__file__).resolve().parent
HISTORY_FILE = BASE_DIR / "results" / "history.csv"


def build_questions():
    random.seed(YEAR)
    square = random.choice([144, 169, 196, 225, 256, 289, 324])
    factorial_n = random.randint(3, 6)
    a = random.randint(24, 96)
    b = random.randint(12, 48)
    comb_n = random.randint(6, 10)
    comb_k = random.randint(2, comb_n - 2)
    percent = random.choice([5, 10, 15, 20, 25])
    amount = random.choice([160, 200, 240, 260, 320, 400])
    return [
        (f"sqrt({square})", math.isqrt(square)),
        (f"{factorial_n}!", math.factorial(factorial_n)),
        (f"gcd({a}, {b})", math.gcd(a, b)),
        (f"comb({comb_n}, {comb_k})", math.comb(comb_n, comb_k)),
        (f"{percent}% of {amount}", percent * amount // 100),
    ]


def read_history():
    records = []
    if not HISTORY_FILE.exists():
        return records
    with HISTORY_FILE.open("r", encoding="utf-8", newline="") as file:
        for row in csv.reader(file, delimiter=";"):
            if not row or row[0].startswith("#") or len(row) != 3:
                continue
            try:
                records.append((datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S"), int(row[1]), float(row[2])))
            except ValueError:
                continue
    return records


def main():
    print(f"{NAME} {SURNAME}, {GROUP}")
    questions = build_questions()
    started = datetime.now()
    score = 0
    for index, (question, answer) in enumerate(questions, 1):
        response = input(f"{index}) {question} = ").strip()
        try:
            correct = int(response) == answer
        except ValueError:
            correct = False
        if correct:
            score += 1
            print("   correct")
        else:
            print(f"   wrong, answer: {answer}")
    finished = datetime.now()
    seconds = (finished - started).total_seconds()

    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    new_file = not HISTORY_FILE.exists()
    with HISTORY_FILE.open("a", encoding="utf-8", newline="") as file:
        if new_file:
            file.write("# datetime;score;seconds\n")
        writer = csv.writer(file, delimiter=";", lineterminator="\n")
        writer.writerow([finished.strftime("%Y-%m-%d %H:%M:%S"), score, f"{seconds:.1f}"])

    print(f"score: {score}/5, time: {seconds:.1f} s")
    history = read_history()
    best = max(history, key=lambda record: (record[1], -record[2]))
    print(f"attempts: {len(history)}, best: {best[1]}/5 in {best[2]:.1f} s ({best[0]:%Y-%m-%d %H:%M})")


if __name__ == "__main__":
    try:
        main()
    except (OSError, KeyboardInterrupt) as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)
