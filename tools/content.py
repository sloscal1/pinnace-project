"""Read and write the Markdown content files that are the site's source of truth.

Layout:
    content/site.md            site-wide settings (default style, style picker on/off)
    content/teams/<id>.md      team section: front matter + optional notes. `colours` is the club's
                               shirt colours as "#primary, #secondary" (blank = site colours).
    content/features/<id>.md   feature article: front matter + Markdown body. `team` is the team
                               section it belongs with (empty for "About the collection");
                               `related` lists other teams it mentions.
    content/cards/<id>.md      one card/biography: front matter + Career/Biography/... sections.
                               Sources are Markdown footnotes: `[^1]` in the text and `[^1]: ...`
                               lines under `## Sources` (in features, at the end of the body).
    content/img/               card scans and photographs

Front matter is a block of `key: value` lines between `---` fences. Values are plain text;
`uid`, `number` and `order` are integers, and `images` / `pages` are comma-separated lists.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

INT_KEYS = {"uid", "number", "order", "see_page"}
LIST_KEYS = {"images", "pages", "related", "colours"}


# ---------------------------------------------------------------- front matter

def split_front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if key in INT_KEYS:
            meta[key] = int(value) if value else None
        elif key in LIST_KEYS:
            meta[key] = [v.strip() for v in value.split(",") if v.strip()]
        else:
            meta[key] = value or None
    return meta, m.group(2)


def front_matter(meta, keys):
    lines = ["---"]
    for k in keys:
        v = meta.get(k)
        if isinstance(v, list):
            v = ", ".join(v)
        lines.append(f"{k}: {'' if v is None else v}")
    return "\n".join(lines + ["---", ""])


def sections(body):
    """Split a Markdown body into {heading: text} on `## ` headings."""
    out, cur = {}, None
    for line in body.splitlines():
        m = re.match(r"^##\s+(.*)$", line)
        if m:
            cur = m.group(1).strip()
            out[cur] = []
        elif cur:
            out[cur].append(line)
    return {k: "\n".join(v).strip() for k, v in out.items()}


def paragraphs(text):
    return [re.sub(r"\s*\n\s*", " ", p).strip() for p in re.split(r"\n\s*\n", text or "") if p.strip()]


FOOTNOTE_DEF = re.compile(r"^\[\^([\w-]+)\]:\s*(.+)$")


def split_footnotes(text):
    """Separate Markdown footnote definitions (`[^key]: source`) from the text around them.

    In the text, `[^key]` marks the place a source supports. Returns (text, {key: source})."""
    keep, notes = [], {}
    for line in (text or "").splitlines():
        m = FOOTNOTE_DEF.match(line.strip())
        if m:
            notes[m.group(1)] = m.group(2).strip()
        else:
            keep.append(line)
    return "\n".join(keep), notes


def bullets(text):
    return [l[2:].strip() for l in (text or "").splitlines() if l.startswith("- ")]


# ---------------------------------------------------------------- cards

CARD_KEYS = ["uid", "number", "name", "full_name", "nickname", "surname", "name_note", "team",
             "position", "height", "born", "died", "image", "source_page", "see_page"]
CAREER_COLS = ["Years", "Club", "Apps", "Goals", "Note"]


def cell(v):
    return "" if v is None else str(v).replace("|", "/")


def career_to_md(career):
    """The `## Career` section for a list of career rows."""
    out = ["## Career\n", "| " + " | ".join(CAREER_COLS) + " |", "|" + "---|" * len(CAREER_COLS)]
    for e in career:
        years = "" if e["from"] is None else (f"{e['from']}-{e['to']}" if e["to"] else str(e["from"]))
        out.append("| " + " | ".join(cell(v) for v in (years, e["club"], e["apps"], e["goals"], e["note"])) + " |")
    return "\n".join(out) + "\n"


def card_to_md(c):
    out = [front_matter(c, CARD_KEYS)]
    if c["career"]:
        out.append(career_to_md(c["career"]))
    for heading, key in (("Representative", "representative"), ("Honours", "honours")):
        if c[key]:
            out.append(f"## {heading}\n")
            out += [f"- {x}" for x in c[key]]
            out.append("")
    if c["bio"]:
        out.append("## Biography\n")
        out.append("\n\n".join(c["bio"]))
        out.append("")
    if c.get("sources"):
        out.append("## Sources\n")
        out += [f"[^{k}]: {v}" for k, v in c["sources"].items()]
        out.append("")
    out.append("## Collector notes\n")
    out.append("\n\n".join(c.get("collector_notes", [])))
    return "\n".join(out).rstrip() + "\n"


def parse_career(text):
    rows = []
    for line in (text or "").splitlines():
        if not line.startswith("|") or re.match(r"^\|[\s:|-]+\|$", line) or "Years" in line.split("|")[1]:
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        cols += [""] * (len(CAREER_COLS) - len(cols))
        years, club, apps, goals, note = cols[:5]
        m = re.match(r"^(\d{4})(?:\s*[-–]\s*(\d{4}))?$", years)
        rows.append({"from": int(m.group(1)) if m else None, "to": int(m.group(2)) if m and m.group(2) else None,
                     "years": years, "club": club, "apps": int(apps) if apps.isdigit() else (apps or None),
                     "goals": int(goals) if goals.isdigit() else (goals or None), "note": note or None})
    return rows


CAREER_YEARS = re.compile(r"^(\d{4})(?:-(\d{4}))?$")
FIRST_YEAR, LAST_YEAR = 1870, 1960  # the cards' players were active between the 1880s and the 1950s
CLUBS_NAMED_WITH_A_YEAR = ("B 1903",)  # Boldklubben 1903, Copenhagen
POSITION_WORDS = {"inside", "outside", "centre", "center", "right", "left", "wing", "winger", "forward", "half",
                  "back", "full", "goalkeeper", "keeper", "defender"}


def career_problems(row):
    """What is wrong with a career row (as parse_career returns it), as a list of messages.

    Years is blank (the book gives no dates for some early clubs), a year, or a range of years;
    the club has no years, apps or goals in it and is not the card's position, height or birth
    line; apps and goals are whole numbers or blank."""
    out = []
    years = row["years"]
    m = CAREER_YEARS.match(years)
    if years and not m:
        out.append(f"years '{years}' should be a year (1921) or a range (1921-1923)")
    elif m:
        start, end = int(m.group(1)), int(m.group(2) or m.group(1))
        if start > end:
            out.append(f"years '{years}' are not in chronological order")
        if not (FIRST_YEAR <= start <= LAST_YEAR and FIRST_YEAR <= end <= LAST_YEAR):
            out.append(f"years '{years}' are outside {FIRST_YEAR}-{LAST_YEAR}")
    club = row["club"] or ""
    if re.search(r"\b1[89]\d\d\b", club) and club not in CLUBS_NAMED_WITH_A_YEAR:
        out.append("the club has a year in it")
    words = re.findall(r"[a-z]+", club.lower())
    if (re.search(r"\d'\s*\d", club) or re.match(r"(Born|Birth|Died|Death)\b", club)
            or (words and set(words) <= POSITION_WORDS)):
        out.append("the club is the card's position, height or birth line")
    if re.search(r"\b(apps?|appa|goals?)\b", club, re.I):
        out.append("the club has apps or goals in it")
    for key in ("apps", "goals"):
        if row[key] is not None and not isinstance(row[key], int):
            out.append(f"{key} '{row[key]}' should be a number or blank")
    return out


def load_card(path):
    meta, body = split_front_matter(path.read_text())
    s = sections(body)
    meta.update(id=path.stem, career=parse_career(s.get("Career")),
                representative=bullets(s.get("Representative")), honours=bullets(s.get("Honours")),
                bio=paragraphs(s.get("Biography")), collector_notes=paragraphs(s.get("Collector notes")),
                sources=split_footnotes(s.get("Sources"))[1])
    return meta


# ---------------------------------------------------------------- teams and features

SECTION_KEYS = ["title", "order", "pages", "images", "colours"]
FEATURE_KEYS = ["title", "order", "team", "related", "pages", "images"]


def section_to_md(s):
    body = "\n\n".join(s.get("notes", []))
    if s.get("kind") == "feature":
        body = s["body"]
    keys = FEATURE_KEYS if s.get("kind") == "feature" else SECTION_KEYS
    return front_matter(s, keys) + ("\n" + body.strip() + "\n" if body.strip() else "")


def load_section(path, kind):
    meta, body = split_front_matter(path.read_text())
    meta.update(id=path.stem, kind=kind, body=body.strip(), images=meta.get("images") or [],
                pages=meta.get("pages") or [], related=meta.get("related") or [])
    return meta


def load_all():
    teams = [load_section(p, "team") for p in sorted((CONTENT / "teams").glob("*.md"))]
    features = [load_section(p, "feature") for p in sorted((CONTENT / "features").glob("*.md"))]
    cards = [load_card(p) for p in sorted((CONTENT / "cards").glob("*.md"))]
    key = lambda s: (s.get("order") or 0, s["id"])
    return sorted(teams, key=key), sorted(features, key=key), cards


# ---------------------------------------------------------------- team names

# Abbreviations used in section titles and on the cards.
ABBREV = {"utd": "united", "co": "county", "alex": "alexandra", "acc": "academical", "pa": "park avenue",
          "ath": "athletic", "rov": "rovers", "c": "city", "t": "town", "w": "wanderers", "r": "rovers"}


def norm(s):
    s = re.sub(r"\(.*?\)", "", s.lower())
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9& ]+", " ", s)).strip()


def team_aliases(teams):
    """Map normalised spellings ("bristol c", "derby county", "celtic") to team ids."""
    aliases = {}
    for t in teams:
        words = norm(t["title"]).split()
        if not words:
            continue
        expanded = " ".join(ABBREV.get(w, w) for w in words[1:])
        forms = {" ".join(words), (words[0] + " " + expanded).strip()}
        if words[0] == "glasgow" and len(words) > 1:
            forms.add(" ".join(words[1:]))
        if len(words) > 1:
            last = words[-1]
            for abbr in {last[0], last[:3], last[:4]}:
                forms.add(" ".join(words[:-1] + [abbr]))
        for f in forms:
            aliases.setdefault(f, t["id"])
    return aliases


CLUB_SUFFIX = re.compile(r"^\s+(Athletic|United|Utd|Rovers|City|Town|County|Wanderers|Albion|Hotspur|F\.?C\b)")


def find_mentions(text, teams, exclude=()):
    """Team ids whose (capitalised) name appears in free text, in order of first mention."""
    found = {}
    for alias, tid in team_aliases(teams).items():
        if tid in exclude or len(alias) < 5:
            continue
        words = [w.capitalize() if w != "&" else w for w in alias.split()]
        for m in re.finditer(r"\b" + r"\s+".join(re.escape(w) for w in words) + r"\b", text):
            before, after = text[max(0, m.start() - 30):m.start()], text[m.end():m.end() + 30]
            # A one-word club name inside another proper noun ("James Nelson", "Nelson Steam
            # Navigation") or starting a sentence ("Reading the ...") is probably not the club.
            if len(words) == 1 and (re.search(r"(^|[.!?]\s+|\b[A-Z][a-z]+\s+)$", before)
                                    or (re.match(r"^\s+[A-Z][a-z]", after) and not CLUB_SUFFIX.match(after))):
                continue
            found[tid] = min(found.get(tid, m.start()), m.start())
            break
    return sorted(found, key=found.get)
