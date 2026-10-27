import math
import shutil
import sys
from datetime import datetime
from pathlib import Path

NAME = "Your Name"
SURNAME = "Your Surname"
GROUP = "Your Group"
SCRIPT_DIR = Path(__file__).resolve().parent


def human_size(size):
    if size == 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB"]
    index = min(int(math.log(size, 1024)), len(units) - 1)
    value = size / (1024 ** index)
    return f"{value:.1f} {units[index]}"


def main(args):
    print(f"{NAME} {SURNAME}, {GROUP}")
    dry_run = False
    if args and args[0] == "--dry-run":
        dry_run = True
        args = args[1:]
    if len(args) != 1:
        print("usage: python3 task3.py [--dry-run] <dir>")
        return 2

    directory = Path(args[0]).expanduser()
    if not directory.exists() or not directory.is_dir():
        print(f"error: {directory} is not a directory", file=sys.stderr)
        return 1

    files = sorted((item for item in directory.iterdir() if item.is_file()), key=lambda item: item.stat().st_mtime)
    if not files:
        print("no files found, nothing to do")
        return 0

    plan = []
    for file in files:
        stat = file.stat()
        modified = datetime.fromtimestamp(stat.st_mtime)
        folder_name = modified.strftime("%Y-%m")
        destination = directory / folder_name / file.name
        plan.append((file, destination, stat.st_size, modified))
        print(f"{file.name:<22} {human_size(stat.st_size):>8}  {modified:%d.%m.%Y %H:%M}  -> {folder_name}/")

    collisions = [destination for _, destination, _, _ in plan if destination.exists()]
    if collisions:
        print(f"error: {collisions[0]} already exists, nothing was moved", file=sys.stderr)
        return 1

    folder_count = len({destination.parent for _, destination, _, _ in plan})
    if dry_run:
        print(f"{len(files)} files, {folder_count} folders (dry run, nothing moved)")
        return 0

    for _, destination, _, _ in plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
    for source, destination, _, _ in plan:
        shutil.move(str(source), str(destination))

    reports_dir = SCRIPT_DIR / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_path = reports_dir / f"organize_{datetime.now():%Y%m%d_%H%M}.txt"
    with report_path.open("w", encoding="utf-8") as report:
        report.write(f"{NAME} {SURNAME}, {GROUP}\n")
        for source, destination, size, modified in plan:
            report.write(f"{source.name};{human_size(size)};{modified:%d.%m.%Y %H:%M};{destination}\n")
        report.write(f"{len(files)} files, {folder_count} folders\n")
    print(f"{len(files)} files, {folder_count} folders")
    print(f"report saved to: {report_path.relative_to(SCRIPT_DIR)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
