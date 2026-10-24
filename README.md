# Pinnace Collection Biographies

A static website of the Pinnace football card biographies, built from Markdown files in `content/`.

## Editing

`content/` is the source of truth. Edit it by hand, or in the GitHub web editor, like a wiki:

- `content/cards/<number>-<surname>.md`: one card. The front matter holds the facts, followed by
  `## Career` (a Markdown table), `## Representative`, `## Honours`, `## Biography` and
  `## Collector notes` (variants, misprints and so on).
- `content/teams/<id>.md`: a team section (title, order, source pages, photos, optional notes).
- `content/features/<id>.md`: a feature article in Markdown (`###` subheadings). `team:` is the
  team section it belongs with, which is where it sits in the original book. Leave it empty for
  the "About the collection" pages. `related:` lists other teams the article mentions. It was
  generated automatically, so prune it as you like.
- `content/img/`: card scans and photographs.

Each card's `uid` is permanent. Visitors' checklists and share links are keyed by it, so never
change or reuse one. A new card gets the next unused number.

## Look and feel

`content/site.md` holds the site-wide settings:

- `style` is the default look: `classic`, `programme` (1920s match programme), `album` (cigarette-card
  album, where cards you don't have show as empty numbered slots), `club` (team pages in the club's colours)
  or `matchday` (programme + album + club).
- `style_picker: yes` shows a "Style" switcher in the corner of every page so visitors can try each look.
  Links can preselect one with `?style=album`. Set it to `no` once a style is chosen.

Club colours come from the `colours:` line in each team file (`#primary, #secondary`). Teams left blank use
the site's normal colours. The styles themselves are layers in `web/style.css` (search for "styles").
Every page has a light/dark button; until a visitor uses it, the site follows their device setting.

## Editing on GitHub

The site is published with GitHub Pages. Every push to `main` rebuilds and redeploys it
(`.github/workflows/pages.yml`), which takes about a minute.

To fix a biography or add a card, open its file under `content/` on github.com, click the pencil
icon, edit, and commit. Others can propose changes as pull requests for the maintainer to review.
Images are added with "Add file → Upload files" into `content/img/`.

## Build locally

The build uses only the Python standard library.

    python3 tools/build.py
    cd site && python3 -m http.server 8731      # then open http://localhost:8731

`site/` is plain HTML, CSS and JS and can be uploaded as is to GitHub Pages, S3 or any static host.

## Migration from Publisher

`content/` was extracted from the original MS Publisher files, which are not kept in this
repository. From now on `content/` is the master copy: edit it directly.

## Checklists

Checklists are stored in each visitor's browser. There are no accounts and no server.

- **Share link:** the list is encoded in the URL (one bit per card uid). The person you send it to
  sees a read-only view and can copy it into their own checklist.
- **History:** the last 10 versions are kept. A snapshot is taken before the first change in each
  visit, before loading a backup or shared list, before a restore, and on each share.
- **Backup:** save the list to, or load it from, a JSON file.
