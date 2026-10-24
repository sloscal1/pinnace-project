"""Generate the static site from the Markdown files in content/.

Usage: .venv/bin/python tools/build.py

Writes site/ (plain HTML/CSS/JS, no server needed; upload the folder to S3 or open locally).
"""
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


def page(title, body, depth=0, active="", club=None):
    up = "../" * depth
    nav = [("index.html", "Teams", "teams"), ("features.html", "Features", "features"),
           ("players.html", "Players", "players"), ("checklist.html", "My checklist", "checklist")]
    links = "".join(f'<a href="{up}{h}"{" aria-current=page" if k == active else ""}>{t}</a>'
                    for h, t, k in nav)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
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
{style_picker()}
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


def player_page(c, sec, others_same_number, aliases, sections_by_id, pages_to_section):
    up = "../"
    facts = [("Card", f"No. {c['number']}"), ("Position", c.get("position")), ("Height", c.get("height")),
             ("Born", c.get("born")), ("Died", c.get("died"))]
    dl = "".join(f"<dt>{k}</dt><dd>{esc(str(v))}</dd>" for k, v in facts if v)
    flags = []
    if others_same_number:
        links = ", ".join(f'<a href="{o["id"]}.html">{esc(o["name"])}</a>' for o in others_same_number)
        flags.append(f"Card number {c['number']} is also given to {links} in the source pages. "
                     "One of these may be a typo.")
    if c.get("see_page"):
        target = pages_to_section.get(str(c["see_page"]))
        where = (f' (<a href="{up}teams/{target["id"]}.html">{esc(target["title"])}</a>)'
                 if target else " (not yet included in this demo)")
        flags.append(f"The full biography is on source page {c['see_page']}{where}.")
    flag_html = "".join(f'<p class="flag">{f}</p>' for f in flags)
    rep = ("<h2>Representative honours</h2><ul>" + "".join(f"<li>{esc(r)}</li>" for r in c["representative"])
           + "</ul>") if c["representative"] else ""
    hon = ("<h2>Honours</h2><ul>" + "".join(f"<li>{esc(h)}</li>" for h in c["honours"]) + "</ul>"
           ) if c["honours"] else ""
    bio = "".join(f"<p>{esc(b)}</p>" for b in c["bio"] if not re.match(r"^see page", b, re.I))
    bio = f"<h2>Biography</h2>{bio}" if bio else ""
    notes = "".join(f"<p>{esc(n)}</p>" for n in c["collector_notes"])
    notes = f'<h2>Collector notes</h2><div class="collector">{notes}</div>' if notes else ""
    also = sorted({sid for e in c["career"] for p in club_parts(e["club"])
                   for sid in [resolve(p, aliases)] if sid and sid != sec["id"]})
    also_html = ("<p class=also>Also played for: " + ", ".join(
        f'<a href="{up}teams/{s}.html">{esc(sections_by_id[s]["title"])}</a>' for s in also) + "</p>"
                 ) if also else ""
    img = (f'<img class="scan" src="{up}img/{c["image"]}" alt="Card {c["number"]}: {esc(c["name"])}">'
           if c.get("image") else "")
    nick = f'<p class="note">{esc(c["name_note"])}</p>' if c.get("name_note") else ""
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
    <p class="source">Source: page {c['source_page']} of the Pinnace Bio Project.</p>
  </div>
</article>"""
    return page(c["name"], body, depth=1, club=sec)


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
                 f'cards collected · source pages {sec["pages"][0]}–{sec["pages"][-1]}')
        grid = '<ul class="grid">' + "".join(card_tile(c, up) for c in cards) + "</ul>"
    else:
        count = f'Source pages {sec["pages"][0]}–{sec["pages"][-1]}'
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
    return page(sec["title"], body, depth=1, club=sec)


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


def render_md(md):
    """Minimal Markdown: ### headings, - lists and paragraphs."""
    out = []
    for block in re.split(r"\n\s*\n", md or ""):
        block = block.strip()
        if not block:
            continue
        if block.startswith("#"):
            level = min(len(block) - len(block.lstrip("#")), 4)
            out.append(f"<h{level}>{esc(block.lstrip('#').strip())}</h{level}>")
        elif block.startswith("- "):
            out.append("<ul>" + "".join(f"<li>{esc(i)}</li>" for i in content.bullets(block)) + "</ul>")
        else:
            out.append("<p>" + esc(re.sub(r"\s*\n\s*", " ", block)) + "</p>")
    return "".join(out)


def feature_page(f, teams_by_id):
    up = "../"
    figs = "".join(f'<figure><img src="{up}img/{im}" alt="" loading="lazy"></figure>' for im in f["images"])
    team = teams_by_id.get(f.get("team"))
    crumb = (f' › <a href="{up}teams/{team["id"]}.html">{esc(team["title"])}</a>' if team
             else f' › <a href="{up}features.html#about">About the collection</a>')
    related = [teams_by_id[t] for t in f["related"] if t in teams_by_id]
    related = ('<p class="also">Teams mentioned: ' + ", ".join(
        f'<a href="{up}teams/{t["id"]}.html">{esc(t["title"])}</a>' for t in related) + "</p>") if related else ""
    body = f"""<p class="crumbs"><a href="{up}features.html">Features</a>{crumb}</p>
<article class="feature-article">
<h1>{esc(f['title'])}</h1>
{render_md(f['body'])}
{f'<div class="gallery">{figs}</div>' if figs else ''}
{related}
<p class="source">Source: page{'s' if len(f['pages']) > 1 else ''} {', '.join(f['pages'])} of the Pinnace Bio Project.</p>
</article>"""
    return page(f["title"], body, depth=1, club=teams_by_id.get(f.get("team")))


def players_page(cards, sections_by_id):
    rows = "".join(
        f"<tr data-search=\"{esc((c['name'] + ' ' + str(c['number']) + ' ' + sections_by_id[c['team']]['title']).lower())}\">"
        f"<td class=n>{c['number']}</td><td><a href=\"players/{c['id']}.html\">{esc(c['name'])}</a></td>"
        f"<td>{esc(sections_by_id[c['team']]['title'])}</td><td>{esc(c.get('position') or '')}</td></tr>"
        for c in sorted(cards, key=lambda c: (c["surname"], c["full_name"])))
    body = f"""<h1>Players</h1>
<input class="search" type="search" placeholder="Search by name, number or team" data-filter="#players">
<table class="list" id="players"><thead><tr><th class=n>No.</th><th>Name</th><th>Section</th><th>Position</th></tr></thead>
<tbody>{rows}</tbody></table>"""
    return page("Players", body, active="players")


def checklist_page(cards, sections_by_id):
    data = [{"id": c["id"], "uid": c["uid"], "n": c["number"], "name": c["name"], "sur": c["surname"],
             "first": c["full_name"], "team": sections_by_id[c["team"]]["title"],
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
    site_md = content.CONTENT / "site.md"
    if site_md.exists():
        SETTINGS.update(content.split_front_matter(site_md.read_text())[0])
    if SETTINGS.get("style") not in STYLES:
        raise SystemExit(f"content/site.md: style must be one of {', '.join(STYLES)}")
    sections_by_id = {s["id"]: s for s in teams}
    pages_to_section = {p: s for s in teams for p in s["pages"]}
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
    (SITE / "index.html").write_text(index_page(teams, by_team))
    (SITE / "features.html").write_text(features_index(features, sections_by_id))
    (SITE / "players.html").write_text(players_page(cards, sections_by_id))
    (SITE / "checklist.html").write_text(checklist_page(cards, sections_by_id))
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
            player_page(c, sections_by_id[c["team"]], dupes, aliases, sections_by_id, pages_to_section))
    print(f"Built {len(teams)} teams, {len(features)} features and {len(cards)} player pages into {SITE}")


if __name__ == "__main__":
    main()
