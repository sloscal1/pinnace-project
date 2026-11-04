"""Check the content files for mistakes that should never be published.

Usage: python3 tools/check.py

Prints each problem with the file it is in, and exits with an error if there are any, so the
publish workflow stops before a broken page goes live. Checked so far: career tables (see
content.career_problems), how names and nicknames are written (see content.name_problems), one card
entered twice, and content/merged-cards.csv.
"""
import hashlib
import sys

import content


def main():
    problems = []
    seen = {}
    ids, uids = set(), set()
    for path in sorted((content.CONTENT / "cards").glob("*.md")):
        card = content.load_card(path)
        ids.add(card["id"])
        uids.add(card["uid"])
        for p in content.name_problems(card):
            problems.append(f"{path.relative_to(content.ROOT)}: {p}: {card.get('name')}")
        if card.get("image"):
            digest = hashlib.sha1((content.CONTENT / "img" / card["image"]).read_bytes()).hexdigest()
            twin = seen.setdefault((card["number"], card["team"], (card.get("surname") or "").lower(), digest), card["id"])
            if twin != card["id"]:
                problems.append(f"{path.relative_to(content.ROOT)}: the same card as {twin} (same number, team "
                                "and scan). Combine them and record it in content/merged-cards.csv")
        for row in card["career"]:
            for p in content.career_problems(row):
                problems.append(f"{path.relative_to(content.ROOT)}: {row['years'] or '(no years)'} "
                                f"{row['club'] or ''}: {p}")
    for m in content.load_merged():
        where = f"content/merged-cards.csv: {m['old_id']}"
        if m["card"] not in ids:
            problems.append(f"{where}: no card {m['card']}")
        if m["old_id"] in ids or m["old_uid"] in uids:
            problems.append(f"{where}: its old id or uid is in use again")
    print("\n".join(problems))
    print(f"{len(problems)} problem(s)" if problems else "All checks passed")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
