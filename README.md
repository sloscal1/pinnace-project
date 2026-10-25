# Pinnace Collection Biographies

A static website of the Pinnace football card biographies, built from Markdown files in `content/`.

## Maintaining the site: start here

No programming or GitHub experience is needed. Everything below happens in a web browser, on a
computer (a phone works, but is fiddly). The site is at https://sloscal1.github.io/pinnace-project/
and the files behind it are at https://github.com/sloscal1/pinnace-project.

### 1. Get set up (once)

1. **Make a free GitHub account** at https://github.com/signup. Note your username.
2. **Ask the site's owner to add you as a collaborator**, giving them your username. (For the
   owner: on the repository page, Settings → Collaborators → Add people.)
3. **Accept the invitation.** It arrives by email, or open
   https://github.com/sloscal1/pinnace-project/invitations while signed in. Until you accept, GitHub
   will offer to "fork" the project when you try to edit. Don't; accept the invitation instead.

### 2. Find something to do

Open the maintainers page: https://sloscal1.github.io/pinnace-project/maintainers.html (it is not
linked from the rest of the site; bookmark it). The checklist at the top lists what still needs
checking or fixing, with progress. Each item names:

- a card, like `0929-martin`, which links to the card on the site;
- a page, like `p344`, which links to the page index lower down. The index gives the original
  Publisher file (`page344.pub`) for checking against the book.

### 3. Make an edit

Each card, team and feature is a text file under `content/`. To change one:

1. On https://github.com/sloscal1/pinnace-project press `t` (or click "Go to file") and type the
   card's name from the checklist, e.g. `0929-martin`. Click the file.
2. Click the **pencil icon** ("Edit this file"), near the top right of the file.
3. Make the change. The **Preview** tab shows how it reads.
4. Click **Commit changes...** (green button). This is GitHub's "save". Write a short note of what
   you changed, e.g. "Card 929: Bristol City goals", leave "Commit directly to the main branch"
   selected, and click **Commit changes**.
5. About two minutes later the site has your change; reload the page to see it. The repository's
   **Actions** tab shows progress: a yellow dot while it builds, a green tick when it's live. A red
   cross means the site couldn't be built (usually a typo in the file's format, see below): open
   the file again and check your change, or open an issue (section 5).

Made a mistake? Every saved version is kept. Open the file, click **History**, and you can see and
copy back any earlier version.

### 4. Tick off the item

The checklist is itself a file, `content/maintenance.md`. Edit it as above and change the item's
`- [ ]` to `- [x]`. Hand-written items (and the "Notes" section at the end) can be changed or added
freely. The sections marked "generated" are refreshed automatically each time the site is
published: an item disappears once the problem it describes is fixed, and ticked items stay ticked.

### What the files look like

A card file (here `content/cards/0929-martin.md`, shortened) starts with lines of facts between
`---` lines, then sections:

    ---
    uid: 169
    number: 929
    name: James Colin Martin
    born: 2nd December 1898, Stoke on Trent, Staffordshire, England
    ...
    ---

    ## Career

    | Years | Club | Apps | Goals | Note |
    |---|---|---|---|---|
    | 1926-1927 | Bristol C | 40 | 16 |  |

    ## Biography

    Paragraphs of text, with a blank line between paragraphs.

    ## Collector notes

    Variants, misprints and so on.

- Facts are `name: value`, one per line. Leave the value empty rather than deleting the line.
- Never change a card's `uid`: visitors' saved checklists depend on it.
- Each career row has five cells separated by `|`, even when some are empty: years, club, apps,
  goals, note. Years are written `1926-1927` or `1926`.
- To credit a source, see "Sources and footnotes" below.
- To replace a card scan: open the `content/img` folder, click **Add file → Upload files**, and
  upload the new image with exactly the same file name as the old one (the card file's `image:`
  line gives it, e.g. `card-0929-martin.jpg`).

### 5. Contact the owner about bigger things

For anything beyond fixing the content of a page, open an **issue**: a message thread the owner is
notified about. For example: the site looks broken or won't build, a change would affect many
pages, an idea for a new feature, or you're unsure how something should be done.

1. Go to https://github.com/sloscal1/pinnace-project/issues and click **New issue**.
2. Choose **Bigger problem or idea** and fill in the boxes. Include links to the pages concerned;
   screenshots can be dragged into the box.
3. Click **Submit new issue**. Replies appear on the issue and are emailed to you.

Issues are public, so don't put private details in them.

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

    [^1]: Simkin, John. "Robert Kelly". Spartacus Educational. https://spartacus-educational.com/...

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
  players, career rows, sources to trace, cards missing a detail) are refreshed from the content
  files by `python3 tools/report.py`, which keeps ticks. The publish step runs it too, so the
  maintainers page is always current.
- **Page index**: every page of the original Publisher files, with its file name, team section, and
  links to the cards or feature built from it. Filter by page ("26c"), file, team, player or number.
  In the checklist, `p344` links to that row and `0198-mcmenemy` to that card.

The site shows no page numbers, since the book was never published. The content files keep them:
`source_page` and `see_page` on cards, `pages` on teams and features, and `content/source-pages.csv`
for the file names. References in the text such as "(see page 136)" are shown on the site as links
to the player, feature or team that page holds, and dropped if the page is not on the site.

## Publishing

The site is published with GitHub Pages. Every change saved to `main` rebuilds and redeploys it
(`.github/workflows/pages.yml`), which takes about two minutes.

## Copyright

`COPYRIGHT.md` is the copyright statement; the site shows it as `copyright.html`, linked from every
page's footer ("© Copyright and sources"). In short: the compilation and Michael Postles's own text are © Michael Postles; text
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
