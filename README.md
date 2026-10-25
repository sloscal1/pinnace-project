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

### Sources and footnotes

Cite a source with a Markdown footnote: put `[^1]` (or `[^bbc]`, any short name) where the claim is,
and the source on its own line. In a card it goes under a `## Sources` heading; in a feature, at
the end of the text:

    [^1]: Simpkin, John. "Bob Kelly". Spartacus Educational. https://spartacus-educational.com/...

The site numbers footnotes in order and links them to a Sources list at the bottom of the page.
Web addresses anywhere in the text become links; write one as `<https://...>` if it ends in
punctuation such as a full stop, so the whole address is linked.

Much of the text was copied from Wikipedia with its reference numbers ("[6]") but not the reference
list. The migration turns those into footnotes whose source reads `TO TRACE: ...`; the page shows
"Source not yet traced", and every build lists them (along with footnotes that have no source line)
until the real reference is filled in.

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

## Maintainers page and checklist

`maintainers.html` (not linked from the rest of the site) is the maintainer's view:

- **Checklist**: `content/maintenance.md`, shown with progress. It lists what still needs checking
  or fixing after the move from Publisher. Tick an item by changing `- [ ]` to `- [x]`. Hand-written
  sections can be edited freely; the sections marked "generated" (card numbers given to different
  players, sources to trace, cards missing a detail) are refreshed from the content files by
  `python3 tools/report.py`, which keeps ticks.
- **Page index**: every page of the original Publisher files, with its file name, team section, and
  links to the cards or feature built from it. Filter by page ("26c"), file, team, player or number.
  In the checklist, `p344` links to that row and `0198-mcmenemy` to that card.

The site shows no page numbers, since the book was never published. The content files keep them:
`source_page` and `see_page` on cards, `pages` on teams and features, and `content/source-pages.csv`
for the file names. References in the text such as "(see page 136)" are shown on the site as links
to the player, feature or team that page holds, and dropped if the page is not on the site.

## Editing on GitHub

The site is published with GitHub Pages. Every push to `main` rebuilds and redeploys it
(`.github/workflows/pages.yml`), which takes about a minute.

To fix a biography or add a card, open its file under `content/` on github.com, click the pencil
icon, edit, and commit. Others can propose changes as pull requests for the maintainer to review.
Images are added with "Add file → Upload files" into `content/img/`.

## Copyright

`COPYRIGHT.md` is the copyright statement; the site shows it as `copyright.html`, linked from every
page's footer. In short: the compilation and Michael Postles's own text are © Michael Postles; text
adapted from Wikipedia stays under CC BY-SA; other sources remain their authors' and are credited
where used.

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
