"""Generate the static site from the Markdown files in content/.

Usage: .venv/bin/python tools/build.py

Writes site/ (plain HTML/CSS/JS, no server needed; upload the folder to S3 or open locally).
"""
import difflib
import hashlib
import html
import json
import re
import shutil
from pathlib import Path

import content

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web"
SITE = ROOT / "site"

esc = html.escape

# Named looks a maintainer can pick in content/site.md. Each is a set of layers styled in style.css.
STYLES = {"classic": "", "programme": "programme", "album": "album", "club": "club",
          "matchday": "programme album club"}
SETTINGS = {"style": "classic", "style_picker": "yes"}

# Appended to asset URLs so browsers fetch the new file after each change instead of a cached copy.
VERSION = ""


def club_style(sec):
    """CSS variables for a team's colours, or "" when its `colours:` line is blank."""
    cols = (sec or {}).get("colours") or []
    if not cols:
        return ""
    first = cols[0].lstrip("#")
    lum = sum(w * int(first[i:i + 2], 16) for w, i in ((.299, 0), (.587, 2), (.114, 4))) / 255
    return (f' style="--club1:{cols[0]};--club2:{cols[1] if len(cols) > 1 else cols[0]};'
            f'--club-ink:{"#111" if lum > .6 else "#fff"}"')


def head_script():
    """Applies the saved theme and style before the page draws, so it doesn't flash."""
    picker = SETTINGS.get("style_picker") == "yes"
    return ("<script>(function () { var d = document.documentElement, S = " + json.dumps(STYLES) + ";\n"
            "window.pinnaceStyle = function (name) {\n"
            "  if (!(name in S)) name = " + json.dumps(SETTINGS["style"]) + ";\n"
            "  d.dataset.preset = name; d.dataset.style = S[name];\n"
            "  if (/programme/.test(S[name]) && !document.getElementById('font-programme')) {\n"
            "    var l = document.createElement('link'); l.id = 'font-programme'; l.rel = 'stylesheet';\n"
            "    l.href = 'https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&display=swap';\n"
            "    document.head.appendChild(l); }\n"
            "};\n"
            "var s = null; try {\n"
            "  var t = localStorage.getItem('pinnace-theme'); if (t) d.dataset.theme = t;\n"
            + ("  s = new URLSearchParams(location.search).get('style');\n"
               "  if (s in S) localStorage.setItem('pinnace-style', s); else s = localStorage.getItem('pinnace-style');\n"
               if picker else "") +
            "} catch (e) {}\n"
            "pinnaceStyle(s); })();</script>")


def style_picker():
    if SETTINGS.get("style_picker") != "yes":
        return ""
    opts = "".join(f'<option value="{k}">{k.capitalize()}</option>' for k in STYLES)
    return f'<label class="style-picker no-print">Style <select id="style-picker">{opts}</select></label>'


PAGER = {}  # "players/0042-bown.html" -> ((path, label) or None, (path, label) or None); set in main()


def sequence(paths_and_labels):
    """Previous/next links for pages read in this order."""
    items = list(paths_and_labels)
    return {path: (items[i - 1] if i else None, items[i + 1] if i + 1 < len(items) else None)
            for i, (path, _) in enumerate(items)}


def pager(key, up):
    """Floating previous/next buttons for the page at `key` (its path from the site root)."""
    prev, nxt = PAGER.get(key, (None, None))
    if not (prev or nxt):
        return ""

    def btn(target, rel, text):
        if not target:
            return f'<span class="pager-off" aria-hidden="true">{text}</span>'
        return (f'<a href="{up}{target[0]}" rel="{rel}" data-pager="{rel}" title="{esc(target[1])}">'
                f'{text}<span class="pager-label">{esc(target[1])}</span></a>')

    return (f'<nav class="pager" aria-label="Previous and next">{btn(prev, "prev", "‹ Previous")}'
            f'{btn(nxt, "next", "Next ›")}</nav>')


def page(title, body, depth=0, active="", club=None, robots="", key=None):
    up = "../" * depth
    nav = [("index.html", "Teams", "teams"), ("features.html", "Features", "features"),
           ("players.html", "Players", "players"), ("checklist.html", "My checklist", "checklist")]
    links = "".join(f'<a href="{up}{h}"{" aria-current=page" if k == active else ""}>{t}</a>'
                    for h, t, k in nav)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">{f'<meta name="robots" content="{robots}">' if robots else ""}
<title>{esc(title)} · Pinnace Collection Biographies</title>
<link rel="stylesheet" href="{up}style.css?v={VERSION}">
{head_script()}
</head>
<body{club_style(club)}>
<header class="site">
  <a class="brand" href="{up}index.html">Pinnace Collection <span>Biographies</span></a>
  <nav>{links}</nav>
  <div class="site-search" role="search" data-up="{up}">
    <input type="search" id="site-search" placeholder="Search teams, features, players" aria-label="Search teams, features and players"
      autocomplete="off" aria-controls="site-search-results" aria-expanded="false">
    <ul id="site-search-results" role="listbox" hidden></ul>
  </div>
  <button type="button" class="theme-toggle" id="theme-toggle" aria-label="Switch between light and dark">◐</button>
</header>
<main>
{body}
</main>
<footer class="site">Text and research from the Pinnace Bio Project. Your checklist is saved in this browser only.</footer>
<div class="floating no-print">{pager(key, up) if key else ""}{style_picker()}</div>
<script src="{up}search-index.js?v={VERSION}"></script>
<script src="{up}app.js?v={VERSION}"></script>
</body>
</html>
"""


# ---------------------------------------------------------------- club linking

def club_parts(club):
    return [p for p in re.split(r",\s*|\s+&\s+", club) if p.strip()]


def resolve(part, aliases):
    return aliases.get(content.norm(part))


def club_html(club, aliases, up):
    out = []
    for part in re.split(r"(,\s*|\s+&\s+)", club):
        sid = resolve(part, aliases) if part.strip(", &") else None
        out.append(f'<a href="{up}teams/{sid}.html">{esc(part)}</a>' if sid else esc(part))
    return "".join(out)


# ---------------------------------------------------------------- fragments

def card_tile(c, up, sections_by_id=None):
    img = (f'<img src="{up}img/{c["image"]}" alt="Card {c["number"]}: {esc(c["name"])}" loading="lazy">'
           if c.get("image") else '<div class="noimg">No image</div>')
    img = f'<span class="slot" data-n="No. {c["number"]}">{img}</span>'
    team = (f'<span class="tile-team">{esc(sections_by_id[c["team"]]["title"])}</span>'
            if sections_by_id else "")
    return f"""<li class="tile" data-card="{c['id']}">
  <a href="{up}players/{c['id']}.html">{img}<span class="num">No. {c['number']}</span>
  <span class="tile-name">{esc(c['name'])}</span>{team}
  <span class="tile-pos">{esc(c.get('position') or '')}</span></a>
  <label class="have"><input type="checkbox" data-have="{c['uid']}"> Have it</label>
</li>"""


def career_table(c, aliases, up):
    if not c["career"]:
        return ""
    rows = []
    for e in c["career"]:
        years = e["years"].replace("-", "–")
        rows.append(f"<tr><td class=yr>{esc(years)}</td><td>{club_html(e['club'], aliases, up)}"
                    f"{' <small>' + esc(e['note']) + '</small>' if e['note'] else ''}</td>"
                    f"<td class=n>{'' if e['apps'] is None else e['apps']}</td>"
                    f"<td class=n>{'' if e['goals'] is None else e['goals']}</td></tr>")
    return ("<h2>Career</h2><table class=career><thead><tr><th>Years</th><th>Club</th>"
            "<th class=n>Apps</th><th class=n>Goals</th></tr></thead><tbody>"
            + "".join(rows) + "</tbody></table>")


def same_player(a, b):
    """Two cards with one number are versions of the same card if the surnames (nearly) agree."""
    sa, sb = (a.get("surname") or "").lower(), (b.get("surname") or "").lower()
    return bool(sa and sb) and difflib.SequenceMatcher(None, sa, sb).ratio() >= 0.75


def player_page(c, sec, others_same_number, aliases, sections_by_id):
    up = "../"
    facts = [("Card", f"No. {c['number']}"), ("Position", c.get("position")), ("Height", c.get("height")),
             ("Born", c.get("born")), ("Died", c.get("died"))]
    dl = "".join(f"<dt>{k}</dt><dd>{esc(str(v))}</dd>" for k, v in facts if v)
    flags = []
    variants = [o for o in others_same_number if same_player(c, o)]
    others = [o for o in others_same_number if o not in variants]
    if variants:
        links = ", ".join(f'<a href="{o["id"]}.html">{esc(sections_by_id[o["team"]]["title"])}</a>' for o in variants)
        flags.append(f"Card {c['number']} was also issued with a different club on the front: {links}. "
                     "Each version is listed separately in the checklist.")
    if others:
        links = ", ".join(f'<a href="{o["id"]}.html">{esc(o["name"])}</a>' for o in others)
        flags.append(f"Card number {c['number']} is also given to {links}. "
                     "One of these may be a typo.")
    if c.get("see_page"):
        t = SOURCES.target(c["see_page"], c["number"], c.get("surname") or "")
        if t and t[0] != f"players/{c['id']}.html":
            flags.append(f'The full biography is on <a href="{up}{t[0]}">{esc(t[1])}</a>.')
    flag_html = "".join(f'<p class="flag">{f}</p>' for f in flags)
    fn = Notes(c.get("sources"))
    check_sources(f"content/cards/{c['id']}.md", c["bio"] + c["collector_notes"] + c["representative"]
                  + c["honours"], c.get("sources") or {})
    rep = ("<h2>Representative honours</h2><ul>" + "".join(f"<li>{inline(r, fn)}</li>" for r in c["representative"])
           + "</ul>") if c["representative"] else ""
    hon = ("<h2>Honours</h2><ul>" + "".join(f"<li>{inline(h, fn)}</li>" for h in c["honours"]) + "</ul>"
           ) if c["honours"] else ""
    bio = "".join(f"<p>{inline(b, fn)}</p>" for b in c["bio"] if not re.match(r"^see page", b, re.I))
    bio = f"<h2>Biography</h2>{bio}" if bio else ""
    notes = "".join(f"<p>{inline(n, fn)}</p>" for n in c["collector_notes"])
    notes = f'<h2>Collector notes</h2><div class="collector">{notes}</div>' if notes else ""
    also = sorted({sid for e in c["career"] for p in club_parts(e["club"])
                   for sid in [resolve(p, aliases)] if sid and sid != sec["id"]})
    also_html = ("<p class=also>Also played for: " + ", ".join(
        f'<a href="{up}teams/{s}.html">{esc(sections_by_id[s]["title"])}</a>' for s in also) + "</p>"
                 ) if also else ""
    img = (f'<img class="scan" src="{up}img/{c["image"]}" alt="Card {c["number"]}: {esc(c["name"])}">'
           if c.get("image") else "")
    nick = f'<p class="note">{inline(c["name_note"])}</p>' if c.get("name_note") else ""
    body = f"""<p class="crumbs"><a href="{up}index.html">Teams</a> › <a href="{up}teams/{sec['id']}.html">{esc(sec['title'])}</a></p>
<article class="player">
  <div class="player-card">{img}
    <label class="have big"><input type="checkbox" data-have="{c['uid']}"> I have this card</label>
  </div>
  <div class="player-text">
    <h1>{esc(c['name'])}</h1>{nick}
    {flag_html}
    <dl class="facts">{dl}</dl>
    {also_html}
    {career_table(c, aliases, up)}
    {notes}{rep}{bio}{hon}
    {fn.html()}
  </div>
</article>"""
    return page(c["name"], body, depth=1, club=sec, key=f"players/{c['id']}.html")


def feature_item(f, up, teams_by_id=None, show_team=False):
    team = ""
    if show_team and f.get("team"):
        team = f'<span class="feature-team">{esc(teams_by_id[f["team"]]["title"])}</span>'
    return (f'<li><a href="{up}features/{f["id"]}.html">{team}<span class="feature-title">{esc(f["title"])}</span>'
            f'<span class="feature-blurb">{esc(blurb(f["body"]))}</span></a></li>')


def team_page(sec, cards, transfers_in, sections_by_id, features, mentioned_in):
    up = "../"
    hero = (f'<img class="hero" src="{up}img/{sec["images"][0]}" alt="{esc(sec["title"])} team photograph">'
            if sec["images"] else "")
    gallery = "".join(f'<figure><img src="{up}img/{im}" alt="" loading="lazy"></figure>' for im in sec["images"][1:])
    notes = render_md(sec["body"])
    extra = f'<section class="feature">{gallery}<div>{notes}</div></section>' if gallery or notes else ""
    feats = ""
    if features:
        feats = '<ul class="features">' + "".join(feature_item(f, up) for f in features) + "</ul>"
    if mentioned_in:
        feats += ('<p class="also">Also mentioned in: ' + ", ".join(
            f'<a href="{up}features/{f["id"]}.html">{esc(f["title"])}</a>' for f in mentioned_in) + "</p>")
    if cards:
        count = (f'<span data-count-have="{" ".join(str(c["uid"]) for c in cards)}">0</span> of {len(cards)} '
                 f'cards collected')
        grid = '<ul class="grid">' + "".join(card_tile(c, up) for c in cards) + "</ul>"
    else:
        count = ""
        grid = ('<p class="flag">The player biographies for this team have not been added to the site yet.</p>')
    tin = ""
    if transfers_in:
        tin = ("<h2>Also played here</h2><p>Cards from other sections whose careers include "
               f"{esc(sec['title'])}.</p><ul class=grid>"
               + "".join(card_tile(c, up, sections_by_id) for c in transfers_in) + "</ul>")
    body = f"""<p class="crumbs"><a href="{up}index.html">Teams</a></p>
<h1>{esc(sec['title'])}</h1>
<p class="count">{count}</p>
{feats}
{hero}
{grid}
{extra}
{tin}"""
    return page(sec["title"], body, depth=1, club=sec, key=f"teams/{sec['id']}.html")


def index_page(teams, cards_by_team):
    items = []
    for s in sorted(teams, key=lambda t: t["title"].lower()):
        cs = cards_by_team.get(s["id"], [])
        thumb = f'<img src="img/{s["images"][0]}" alt="" loading="lazy">' if s["images"] else '<div class="nothumb"></div>'
        count = (f'<span data-count-have="{" ".join(str(c["uid"]) for c in cs)}">0</span> / {len(cs)} cards'
                 if cs else "Biographies coming soon")
        items.append(f"""<li{' class="pending"' if not cs else ''}{club_style(s)}><a href="teams/{s['id']}.html">{thumb}<span class="team-name">{esc(s['title'])}</span>
<span class="team-count">{count}</span></a></li>""")
    body = f"""<h1>Pinnace Collection Biographies</h1>
<p class="lede">Biographies of the players on the Pinnace football cards, arranged by club, compiled by Michael Postles.
Tick the cards you own and your checklist is kept on this device.
New here? Start with <a href="features.html#about">About the collection</a>, or browse all <a href="features.html">features</a>.</p>
<h2 class="band">Teams</h2>
<ul class="teams">{''.join(items)}</ul>"""
    return page("Teams", body, active="teams")


def features_index(features, teams_by_id):
    about = [f for f in features if not f.get("team")]
    by_team = {}
    for f in features:
        if f.get("team"):
            by_team.setdefault(f["team"], []).append(f)
    groups = "".join(
        f'<section class="feature-group"><h2><a href="teams/{tid}.html">{esc(teams_by_id[tid]["title"])}</a></h2>'
        f'<ul class="features">{"".join(feature_item(f, "") for f in fs)}</ul></section>'
        for tid, fs in sorted(by_team.items(), key=lambda kv: teams_by_id[kv[0]]["title"].lower()))
    body = f"""<h1>Features</h1>
<p class="lede">Articles from the collection. Each one also appears at the top of the team section it belongs with.</p>
<section id="about" class="feature-group"><h2>About the collection</h2>
<ul class="features">{''.join(feature_item(f, "") for f in about)}</ul></section>
{groups}"""
    return page("Features", body, active="features")


def blurb(md, n=160):
    text = " ".join(p for p in content.paragraphs(md) if not p.startswith("#"))
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0] + "…"


# A web address; brackets inside it are kept when balanced, e.g. wiki/David_Steele_(footballer).
URL = re.compile(r"\b(?:https?://|www\.)(?:\([^\s()<\[\]]*\)|[^\s()<\[\]])*(?:\([^\s()<\[\]]*\)|[^\s()<\[\].,;:!?'\"])")


class Notes:
    """Footnotes for one page, numbered in the order they are first cited."""

    def __init__(self, defs=None):
        self.defs, self.order = dict(defs or {}), []

    def ref(self, m):
        key = m.group(1)
        first = key not in self.order
        if first:
            self.order.append(key)
        n = self.order.index(key) + 1
        anchor = f' id="ref-{esc(key)}"' if first else ""
        return f'<sup class="fnref"><a href="#fn-{esc(key)}"{anchor}>{n}</a></sup>'

    def html(self):
        keys = [k for k in self.order if k in self.defs] + [k for k in self.defs if k not in self.order]
        if not keys:
            return ""
        items = "".join(
            f'<li id="fn-{esc(k)}">{source_html(self.defs[k])}'
            + (f' <a class="back" href="#ref-{esc(k)}" aria-label="Back to the text">↩</a>' if k in self.order else "")
            + "</li>" for k in keys)
        return f'<section class="sources"><h2>Sources</h2><ol>{items}</ol></section>'


TODO_SOURCE = "TO TRACE:"  # set by tools/extract.py on citations whose source is not known yet
PROBLEMS = []  # citations to fix, printed at the end of the build


def source_html(text):
    if text.startswith(TODO_SOURCE):
        return '<span class="untraced">Source not yet traced.</span>'
    return inline(text)


def check_sources(where, text_parts, defs):
    """Note citations that point nowhere, and sources still waiting to be traced."""
    cited = set(re.findall(r"\[\^([\w-]+)\]", " ".join(text_parts)))
    for k in sorted(cited - set(defs)):
        PROBLEMS.append(f"{where}: [^{k}] has no source line")
    for k, v in defs.items():
        if v.startswith(TODO_SOURCE):
            PROBLEMS.append(f"{where}: [^{k}] source not traced yet")
    for m in re.findall(r"(?<!\^)\[\d+\]", " ".join(text_parts)):
        PROBLEMS.append(f"{where}: bare marker {m} should be a footnote like [^{m[1:-1]}]")


class SourcePages:
    """Where each page of the original Publisher files ended up on the site.

    The text still says things like "(see page 136)"; the site has no page numbers, so those become
    links to the player, feature or team the page holds."""

    def __init__(self, teams, features, cards):
        self.feature = {p: f for f in features for p in f["pages"]}
        self.team = {p: t for t in teams for p in t["pages"]}
        self.cards = {}
        for c in cards:
            self.cards.setdefault(str(c["source_page"]), []).append(c)

    def target(self, page, number=None, before=""):
        """(path from the site root, label) for something on `page`, or None."""
        page = str(page)
        if page in self.feature:
            f = self.feature[page]
            return f"features/{f['id']}.html", f["title"]
        here = self.cards.get(page, [])
        pick = [c for c in here if number and c["number"] == number]
        pick = pick or [c for c in here if c.get("surname") and c["surname"] in before[-150:]]
        pick = pick or (here if len(here) == 1 else [])
        if pick:
            return f"players/{pick[-1]['id']}.html", pick[-1]["name"]
        if page in self.team:
            t = self.team[page]
            return f"teams/{t['id']}.html", t["title"]
        return None


SOURCES = None  # set in main()
PAGE = r"\d{1,4}[a-z]?\b"
PAGES = rf"pages?\s+({PAGE})(?:\s*(?:&|and|-|to)\s*({PAGE}))?"
PAGE_REF = re.compile(
    # "(see page 136)", "(See article, page 155 & 156)", "(see Card 1858, Page 585)"
    rf"(?P<paren>\s*\(([^()]*\b{PAGES}[^()]*)\))"
    # "Continues on page 478." / "Continued page 71c": continuations are already joined up
    rf"|(?P<cont>\s*\b(?i:continue[sd]?)\s+(?:on\s+|from\s+)?(?-i:{PAGES})\.?)"
    # "see page 51", "is on page 6 of this book", "card 137 page 24"
    # (lower-case "page" only: "William Page 1896-1981" is a person)
    rf"|(?P<bare>\b(?i:on\s+|at\s+)?(?-i:{PAGES})(?:\s+(?:of|in)\s+this\s+book)?)", re.I)


def page_refs(text, up):
    """Split text into plain strings and HTML for its page cross-references.

    References become links to whatever the page holds now; ones that point nowhere are dropped."""
    out, last = [], 0
    for m in PAGE_REF.finditer(text):
        out.append(text[last:m.start()])
        last = m.end()
        if m.group("cont"):
            continue
        whole = m.group(0)
        number = re.search(r"\bcard\s+(\d+)", m.group(2) if m.group("paren") else text[max(0, m.start() - 30):m.end()], re.I)
        pages = re.findall(rf"(?:pages?\s+|&\s*|and\s+|-\s*|to\s+)({PAGE})", whole, re.I)
        links = []
        for pg in pages:
            t = SOURCES and SOURCES.target(pg, int(number.group(1)) if number else None, text[:m.start()])
            if t and t not in links:
                links.append(t)
        html = " and ".join(f'<a href="{up}{h}">{esc(lbl)}</a>' for h, lbl in links)
        if m.group("paren"):
            if links:
                out.append(("html", f" (see {html})"))
        else:
            lead = re.match(r"\s*(on|at)\s", whole, re.I)
            out.append(("html", f"with {html}" if lead else html) if links else ("drop", ""))
    out.append(text[last:])
    # A sentence pointing at a page that is not on the site ("* See page 86 in this book.") goes.
    while any(isinstance(seg, tuple) and seg[0] == "drop" for seg in out):
        i = next(i for i, seg in enumerate(out) if isinstance(seg, tuple) and seg[0] == "drop")
        before = out[i - 1] if i and isinstance(out[i - 1], str) else ""
        after = out[i + 1] if i + 1 < len(out) and isinstance(out[i + 1], str) else ""
        start = max(before.rfind(". "), before.rfind("! "), before.rfind("? "))
        start = start + 1 if start >= 0 else 0
        end = re.search(r"[.!?](\s|$)", after)
        before, after = before[:start], after[end.end():] if end else ""
        out[i - 1:i + 2] = [before.rstrip() + (" " if before.strip() and after.strip() else "") + after.lstrip()]
    return out


def link(url):
    href = url if url.startswith("http") else "https://" + url
    href = re.sub(r"^https://www\.([\w-]+\.wordpress\.com)", r"https://\1", href)  # WordPress has no www.
    return f'<a href="{href}">{url}</a>'


def inline(text, notes=None, up="../"):
    """Escape a line of text, link web addresses and page cross-references, and turn [^key] into a
    footnote reference.

    An address written as <https://...> is linked exactly; bare ones lose trailing punctuation."""
    def plain(t):
        parts = re.split(r"<(https?://[^\s>]+)>", t)
        return "".join(link(esc(part)) if i % 2 else URL.sub(lambda m: link(m.group(0)), esc(part))
                       for i, part in enumerate(parts))

    out = "".join(seg[1] if isinstance(seg, tuple) else plain(seg) for seg in page_refs(text, up))
    if notes is not None:
        out = re.sub(r"\[\^([\w-]+)\]", notes.ref, out)
    return out


def render_md(md, notes=None):
    """Minimal Markdown: ### headings, - lists, paragraphs and [^key] footnotes (collected in `notes`)."""
    md, defs = content.split_footnotes(md)
    if notes is not None:
        notes.defs.update(defs)
    out = []
    for block in re.split(r"\n\s*\n", md or ""):
        block = block.strip()
        if not block:
            continue
        if block.startswith("#"):
            level = min(len(block) - len(block.lstrip("#")), 4)
            out.append(f"<h{level}>{esc(block.lstrip('#').strip())}</h{level}>")
        elif block.startswith("- "):
            out.append("<ul>" + "".join(f"<li>{inline(i, notes)}</li>" for i in content.bullets(block)) + "</ul>")
        else:
            out.append("<p>" + inline(re.sub(r"\s*\n\s*", " ", block), notes) + "</p>")
    return "".join(out)


def feature_page(f, teams_by_id):
    up = "../"
    figs = "".join(f'<figure><img src="{up}img/{im}" alt="" loading="lazy"></figure>' for im in f["images"])
    team = teams_by_id.get(f.get("team"))
    crumb = (f' › <a href="{up}teams/{team["id"]}.html">{esc(team["title"])}</a>' if team
             else f' › <a href="{up}features.html#about">About the collection</a>')
    fn = Notes()
    body_text, defs = content.split_footnotes(f["body"])
    check_sources(f"content/features/{f['id']}.md", [body_text], defs)
    related = [teams_by_id[t] for t in f["related"] if t in teams_by_id]
    related = ('<p class="also">Teams mentioned: ' + ", ".join(
        f'<a href="{up}teams/{t["id"]}.html">{esc(t["title"])}</a>' for t in related) + "</p>") if related else ""
    body = f"""<p class="crumbs"><a href="{up}features.html">Features</a>{crumb}</p>
<article class="feature-article">
<h1>{esc(f['title'])}</h1>
{render_md(f['body'], fn)}
{f'<div class="gallery">{figs}</div>' if figs else ''}
{related}
{fn.html()}
</article>"""
    return page(f["title"], body, depth=1, club=teams_by_id.get(f.get("team")), key=f"features/{f['id']}.html")


def maintainers_page(teams, features, cards):
    """An unlisted page mapping each page of the original Publisher files to what it became here.

    Only the maintainer has the .pub files; this is how they find the page behind a site page (and
    the other way round) when checking or fixing something."""
    import csv
    files = {}
    path = content.CONTENT / "source-pages.csv"
    if path.exists():
        with path.open() as f:
            files = {r["page"]: r["file"] for r in csv.DictReader(f)}
    feature = {p: f for f in features for p in f["pages"]}
    team = {p: t for t in teams for p in t["pages"]}
    titles = {t["pages"][0]: t for t in teams if t["pages"]}
    on_page = {}
    for c in cards:
        on_page.setdefault(str(c["source_page"]), []).append(c)
    rows = []
    for pg in sorted(set(files) | set(feature) | set(team) | set(on_page), key=content_page_key):
        what = []
        if pg in feature:
            f = feature[pg]
            what.append(f'Feature: <a href="features/{f["id"]}.html">{esc(f["title"])}</a>')
        if pg in titles:
            what.append("Title page")
        what += [f'<a href="players/{c["id"]}.html">No. {c["number"]} {esc(c["name"])}</a>'
                 for c in sorted(on_page.get(pg, []), key=lambda c: c["number"])]
        sec = team.get(pg) or (feature[pg].get("team") and {"id": feature[pg]["team"]} if pg in feature else None)
        sec = next((t for t in teams if sec and t["id"] == sec["id"]), None)
        sec_html = f'<a href="teams/{sec["id"]}.html">{esc(sec["title"])}</a>' if sec else ""
        search = " ".join([pg, "p" + pg, files.get(pg, ""), sec["title"] if sec else ""]
                          + [c["name"] + " " + str(c["number"]) for c in on_page.get(pg, [])]).lower()
        rows.append(f'<tr id="p{pg}" data-search="{esc(search)}"><td class="n">{pg}</td><td>{esc(files.get(pg, ""))}</td>'
                    f'<td>{sec_html}</td><td>{"<br>".join(what) or "<span class=note>Nothing on the site</span>"}</td></tr>')
    checklist_md = content.CONTENT / "maintenance.md"
    checklist = (render_checklist(checklist_md.read_text(), {c["id"] for c in cards}, set(files) | set(team))
                 if checklist_md.exists() else "")
    body = f"""<h1>Maintainers</h1>
<p class="lede">The maintenance checklist and an index of the original Publisher pages. This page is not
linked from the rest of the site, but anyone with the address can open it.</p>
<nav class="toc"><a href="#checklist">Checklist</a> · <a href="#page-index">Page index</a></nav>
<section id="checklist" class="checklist">
{checklist}
</section>
<section id="page-index">
<h2>Page index</h2>
<p>Where each page of the original Publisher files ended up. The site itself shows no page numbers; the
content files keep them (<code>source_page</code>, <code>see_page</code>, <code>pages</code>), and
references like "(see page 136)" in the text are shown as links to whatever that page holds.</p>
<input class="search" type="search" placeholder="Filter by page (e.g. 26c), file, team, player or card number" data-filter="#sources">
<table class="list" id="sources"><thead><tr><th class="n">Page</th><th>Publisher file</th><th>Team section</th><th>On the site</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>
</section>"""
    return page("Maintainers", body, robots="noindex")


def checklist_inline(text, card_ids, pages):
    """Markdown-ish inline text for the checklist: `card-id` links to the card, p344 to the page index."""
    out = []
    for i, part in enumerate(re.split(r"`([^`]*)`", text)):
        if i % 2:
            out.append(f'<a href="players/{part}.html"><code>{esc(part)}</code></a>' if part in card_ids
                       else f"<code>{esc(part)}</code>")
            continue
        h = esc(part)
        h = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", h)
        h = re.sub(r"\bp(\d{1,4}[a-z]?)\b",
                   lambda m: f'<a href="#p{m.group(1)}">{m.group(0)}</a>' if m.group(1) in pages else m.group(0), h)
        out.append(h)
    return "".join(out)


def render_checklist(md, card_ids, pages):
    """content/maintenance.md as HTML: sections with progress counts, task boxes, collapsible groups."""
    def count(lines):
        boxes = [l for l in lines if re.match(r"- \[[ xX]\] ", l)]
        return sum(1 for l in boxes if not l.startswith("- [ ]")), len(boxes)

    lines = [l for l in md.splitlines() if not l.startswith("<!--") and not l.startswith("# ")]
    done, total = count(lines)
    out = [f'<div class="progress"><div style="width:{100 * done / max(total, 1):.1f}%"></div></div>'
           f'<p class="count">{done} of {total} items done</p>']
    para, items = [], []

    def flush():
        if para:
            out.append("<p>" + checklist_inline(" ".join(para), card_ids, pages) + "</p>")
            para.clear()
        if items:
            out.append('<ul class="tasks">' + "".join(items) + "</ul>")
            items.clear()

    for i, line in enumerate(lines):
        m = re.match(r"- \[([ xX])\] (.*)", line)
        if line.startswith("## "):
            flush()
            j = next((k for k in range(i + 1, len(lines)) if lines[k].startswith("## ")), len(lines))
            d, t = count(lines[i + 1:j])
            out.append(f"<h2>{esc(line[3:])}" + (f' <small>{d} / {t}</small>' if t else "") + "</h2>")
        elif line.startswith("<details>"):
            flush()
            j = next((k for k in range(i + 1, len(lines)) if lines[k].startswith("</details>")), len(lines))
            d, t = count(lines[i + 1:j])
            label = re.sub(r"<[^>]+>", "", line)
            out.append(f"<details><summary>{esc(label)} <small>{d} / {t} done</small></summary>")
        elif line.startswith("</details>"):
            flush()
            out.append("</details>")
        elif m:
            if para:
                flush()
            ticked = m.group(1) != " "
            items.append(f'<li class="task{" done" if ticked else ""}"><input type="checkbox" disabled'
                         f'{" checked" if ticked else ""}> <span>{checklist_inline(m.group(2), card_ids, pages)}</span></li>')
        elif line.startswith("- "):
            items.append(f"<li>{checklist_inline(line[2:], card_ids, pages)}</li>")
        elif line.strip():
            if items:
                flush()
            para.append(line.strip())
        else:
            flush()
    flush()
    return "".join(out)


def content_page_key(pg):
    m = re.match(r"(\d+)([a-z]*)", pg)
    return (int(m.group(1)), m.group(2)) if m else (10 ** 6, pg)


def players_page(cards, sections_by_id):
    rows = "".join(
        f"<tr data-search=\"{esc((c['name'] + ' ' + str(c['number']) + ' ' + sections_by_id[c['team']]['title']).lower())}\">"
        f"<td class=n>{c['number']}</td><td><a href=\"players/{c['id']}.html\">{esc(c['name'])}</a></td>"
        f"<td>{esc(sections_by_id[c['team']]['title'])}</td><td>{esc(c.get('position') or '')}</td></tr>"
        for c in sorted(cards, key=lambda c: (c.get("surname") or "", c.get("full_name") or "")))
    body = f"""<h1>Players</h1>
<input class="search" type="search" placeholder="Search by name, number or team" data-filter="#players">
<table class="list" id="players"><thead><tr><th class=n>No.</th><th>Name</th><th>Section</th><th>Position</th></tr></thead>
<tbody>{rows}</tbody></table>"""
    return page("Players", body, active="players")


def checklist_page(cards, sections_by_id):
    data = [{"id": c["id"], "uid": c["uid"], "n": c["number"], "name": c["name"], "sur": c.get("surname") or "",
             "first": c.get("full_name") or "", "team": sections_by_id[c["team"]]["title"],
             "pos": c.get("position") or ""} for c in cards]
    body = f"""<h1>My checklist</h1>
<div id="viewing" class="viewing no-print" hidden>
  <p>You are viewing <strong id="viewing-label">a shared list</strong> (<span id="viewing-count">0</span> cards). It is read-only.</p>
  <button type="button" id="adopt">Copy into my checklist</button>
  <button type="button" id="leave">Back to my checklist</button>
</div>
<div class="controls no-print">
  <label>Arrange by <select id="order">
    <option value="team">Team, then card number</option>
    <option value="surname">Player surname (A–Z)</option>
    <option value="number">Card number</option>
  </select></label>
  <label>Show <select id="show">
    <option value="all">All cards</option><option value="have">Cards I have</option><option value="need">Cards I need</option>
  </select></label>
  <button type="button" onclick="window.print()">Print</button>
</div>
<div class="controls no-print mine-only">
  <label>Your name <input id="share-name" type="text" placeholder="optional" size="12"></label>
  <button type="button" id="share">Copy share link</button>
  <button type="button" id="export">Save backup</button>
  <label class="button">Load backup<input type="file" id="import" accept="application/json" hidden></label>
</div>
<details class="history no-print mine-only"><summary>Earlier versions</summary>
  <p>The last 10 versions of your checklist are kept in this browser. A share link is a snapshot: it does not change when you tick more cards.</p>
  <ul id="history-list"></ul>
</details>
<p class="count"><span id="have-count">0</span> of {len(cards)} cards collected</p>
<div id="checklist"></div>
<script>window.CARDS = {json.dumps(data, ensure_ascii=False)};</script>"""
    return page("My checklist", body, active="checklist")


# ---------------------------------------------------------------- main

def search_index(teams, features, cards, sections_by_id):
    """Entries for the header search: [kind, label, detail, path, extra words to match]."""
    rows = []
    for t in teams:
        rows.append(["Team", t["title"], "", f"teams/{t['id']}.html", ""])
    for f in features:
        team = sections_by_id.get(f.get("team"))
        rows.append(["Feature", f["title"], team["title"] if team else "About the collection",
                     f"features/{f['id']}.html", ""])
    for c in sorted(cards, key=lambda c: (c["number"], c["id"])):
        extra = " ".join(x for x in (c.get("full_name"), c.get("nickname"), str(c["number"])) if x)
        rows.append(["Player", c["name"], f"#{c['number']} · {sections_by_id[c['team']]['title']}",
                     f"players/{c['id']}.html", extra])
    return "window.SEARCH = " + json.dumps(rows, ensure_ascii=False, separators=(",", ":")) + ";\n"


def main():
    teams, features, cards = content.load_all()
    for c in cards:
        c["name"] = c.get("name") or f"Card {c['number']}"  # placeholder entries with no text yet
    site_md = content.CONTENT / "site.md"
    if site_md.exists():
        SETTINGS.update(content.split_front_matter(site_md.read_text())[0])
    if SETTINGS.get("style") not in STYLES:
        raise SystemExit(f"content/site.md: style must be one of {', '.join(STYLES)}")
    sections_by_id = {s["id"]: s for s in teams}
    global SOURCES
    SOURCES = SourcePages(teams, features, cards)
    aliases = content.team_aliases(teams)
    by_team, by_number = {}, {}
    for c in sorted(cards, key=lambda c: (c["number"], c["id"])):
        by_team.setdefault(c["team"], []).append(c)
        by_number.setdefault(c["number"], []).append(c)

    if SITE.exists():
        shutil.rmtree(SITE)
    for d in ("teams", "players", "features"):
        (SITE / d).mkdir(parents=True)
    shutil.copytree(content.CONTENT / "img", SITE / "img")
    for f in WEB.iterdir():
        shutil.copy(f, SITE / f.name)

    index_js = search_index(teams, features, cards, sections_by_id)
    (SITE / "search-index.js").write_text(index_js)
    global VERSION
    digest = hashlib.sha1(index_js.encode())
    for f in sorted(WEB.iterdir()):
        digest.update(f.read_bytes())
    VERSION = digest.hexdigest()[:8]
    # Reading order: teams alphabetically (as on the home page), players by card number within a team
    # (as on the team page), features in book order.
    alpha = sorted(teams, key=lambda t: t["title"].lower())
    PAGER.update(sequence((f"teams/{t['id']}.html", t["title"]) for t in alpha))
    PAGER.update(sequence((f"players/{c['id']}.html", f"{c['name']} ({t['title']})")
                          for t in alpha for c in by_team.get(t["id"], [])))
    PAGER.update(sequence((f"features/{f['id']}.html", f["title"]) for f in features))
    (SITE / "index.html").write_text(index_page(teams, by_team))
    (SITE / "features.html").write_text(features_index(features, sections_by_id))
    (SITE / "players.html").write_text(players_page(cards, sections_by_id))
    (SITE / "checklist.html").write_text(checklist_page(cards, sections_by_id))
    (SITE / "maintainers.html").write_text(maintainers_page(teams, features, cards))
    for f in features:
        (SITE / "features" / f"{f['id']}.html").write_text(feature_page(f, sections_by_id))
    for s in teams:
        transfers_in = [c for c in cards if c["team"] != s["id"] and any(
            resolve(p, aliases) == s["id"] for e in c["career"] for p in club_parts(e["club"]))]
        (SITE / "teams" / f"{s['id']}.html").write_text(
            team_page(s, by_team.get(s["id"], []), transfers_in, sections_by_id,
                      [f for f in features if f.get("team") == s["id"]],
                      [f for f in features if s["id"] in f["related"]]))
    for c in cards:
        dupes = [o for o in by_number[c["number"]] if o is not c]
        (SITE / "players" / f"{c['id']}.html").write_text(
            player_page(c, sections_by_id[c["team"]], dupes, aliases, sections_by_id))
    if PROBLEMS:
        print(f"{len(PROBLEMS)} citation(s) to check:\n  " + "\n  ".join(PROBLEMS))
    print(f"Built {len(teams)} teams, {len(features)} features and {len(cards)} player pages into {SITE}")


if __name__ == "__main__":
    main()
