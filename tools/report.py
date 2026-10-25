"""Refresh the generated sections of the maintenance checklist, content/maintenance.md.

Usage: python3 tools/report.py

The checklist is Markdown with task boxes (- [ ] / - [x]); tick an item by changing [ ] to [x], on
GitHub or in an editor. Sections between <!-- generated: name --> and <!-- end generated --> are
rebuilt from the content files each time this runs; an item that was ticked stays ticked. Everything
else in the file is left exactly as it is.
"""
import difflib
import re

import content

PATH = content.CONTENT / "maintenance.md"
TODO_SOURCE = "TO TRACE:"


def surname_like(a, b):
    sa, sb = (a.get("surname") or "").lower(), (b.get("surname") or "").lower()
    return bool(sa and sb) and difflib.SequenceMatcher(None, sa, sb).ratio() >= 0.75


def page_order(c):
    m = re.match(r"(\d+)([a-z]*)", str(c["source_page"]))
    return int(m.group(1)), m.group(2)


def item(text):
    return f"- [ ] {text}"


def card_ref(c, teams):
    return f"`{c['id']}` ({teams[c['team']]['title']}, p{c['source_page']})"


def generated(cards, teams):
    """{section name: Markdown} for the sections rebuilt on every run."""
    out = {}

    by_number = {}
    for c in cards:
        by_number.setdefault(c["number"], []).append(c)
    conflicts = [(n, cs) for n, cs in sorted(by_number.items())
                 if len(cs) > 1 and not all(surname_like(cs[0], c) for c in cs[1:])]
    out["conflicts"] = "\n".join(
        [f"Card numbers given to players with different names ({len(conflicts)}). Usually a typo in the "
         "number or the name; correct the card file, or tick the item if both are right.", ""]
        + [item(f"**{n}**: " + ", ".join(card_ref(c, teams) for c in sorted(cs, key=page_order)))
           for n, cs in conflicts])

    untraced = []
    for c in cards:
        keys = [k for k, v in (c.get("sources") or {}).items() if v.startswith(TODO_SOURCE)]
        if keys:
            untraced.append(item(card_ref(c, teams) + ": " + ", ".join(f"[^{k}]" for k in keys)))
    for f in sorted((content.CONTENT / "features").glob("*.md")):
        _, defs = content.split_footnotes(f.read_text())
        keys = [k for k, v in defs.items() if v.startswith(TODO_SOURCE)]
        if keys:
            untraced.append(item(f"feature `{f.stem}`: " + ", ".join(f"[^{k}]" for k in keys)))
    out["sources"] = "\n".join(
        [f"Footnotes whose source is still `TO TRACE` ({len(untraced)}). Find the reference in the Wikipedia "
         "article the text came from and replace the source line (see the README).", ""] + untraced)

    odd = []
    for c in sorted(cards, key=lambda c: c["number"]):
        for e in c["career"]:
            club, note = e["club"] or "", e["note"] or ""
            prose = len(note) > 120 or (len(club) > 100 and re.search(r"[a-z]\. [A-Z]", club))
            if re.match(r"(Born|Birth)\b", club) or prose:
                odd.append(item(card_ref(c, teams) + f": {e['years'] or 'no years'} row: "
                                + ("the card's header was read as a career row" if re.match(r"(Born|Birth)", club)
                                   else "biography text in the table")))
                break
    out["career"] = "\n".join(
        [f"Career tables with biography text in a row ({len(odd)}), or a card header read as a career row. "
         "Move the text to the biography, or rewrite the row from the .pub page.",
         ""] + odd)

    checks = [("no card scan", lambda c: not c.get("image")),
              ("no career rows", lambda c: not c["career"] and not c.get("see_page")),
              ("no position", lambda c: not c.get("position") and not c.get("see_page")),
              ("no birth line", lambda c: not c.get("born") and not c.get("see_page"))]
    parts = ["Cards with a missing detail. Often the book simply has none; check the .pub page and fill "
             "it in, or tick the item.", ""]
    for label, test in checks:
        hits = sorted((c for c in cards if test(c)), key=lambda c: c["number"])
        parts += [f"<details><summary>{label} ({len(hits)})</summary>", ""]
        parts += [item(card_ref(c, teams)) for c in hits]
        parts += ["", "</details>", ""]
    out["details"] = "\n".join(parts).rstrip()
    return out


def checked(text):
    """Item texts already ticked in the current file."""
    return {re.sub(r"\s+", " ", m.group(1)).strip()
            for m in re.finditer(r"^- \[[xX]\] (.*)$", text, re.M)}


def main():
    teams, _, cards = content.load_all()
    teams = {t["id"]: t for t in teams}
    text = PATH.read_text()
    done = checked(text)
    for name, body in generated(cards, teams).items():
        body = re.sub(r"^- \[ \] (.*)$",
                      lambda m: f"- [x] {m.group(1)}" if re.sub(r"\s+", " ", m.group(1)).strip() in done
                      else m.group(0), body, flags=re.M)
        pattern = re.compile(rf"(<!-- generated: {name} -->\n).*?(<!-- end generated -->)", re.S)
        if not pattern.search(text):
            raise SystemExit(f"{PATH}: no '<!-- generated: {name} -->' section")
        text = pattern.sub(lambda m: m.group(1) + body + "\n" + m.group(2), text)
    PATH.write_text(text)
    boxes = re.findall(r"^- \[([ xX])\]", text, re.M)
    print(f"{sum(b != ' ' for b in boxes)} of {len(boxes)} items done -> {PATH}")


if __name__ == "__main__":
    main()
