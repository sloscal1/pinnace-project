"""Check the content files for mistakes that should never be published.

Usage: python3 tools/check.py

Prints each problem with the file it is in, and exits with an error if there are any, so the
publish workflow stops before a broken page goes live. Checked so far: career tables (see
content.career_problems).
"""
import sys

import content


def main():
    problems = []
    for path in sorted((content.CONTENT / "cards").glob("*.md")):
        card = content.load_card(path)
        for row in card["career"]:
            for p in content.career_problems(row):
                problems.append(f"{path.relative_to(content.ROOT)}: {row['years'] or '(no years)'} "
                                f"{row['club'] or ''}: {p}")
    print("\n".join(problems))
    print(f"{len(problems)} problem(s)" if problems else "All checks passed")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
