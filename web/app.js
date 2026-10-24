// Checklist state lives in localStorage: { "<card uid>": true }. Uids never change, even if a card file is renamed.
// Sharing encodes the state into the URL (one bit per card uid), so no server is involved.
// The last HISTORY_MAX states are kept as snapshots that can be restored or shared.
(function () {
  var KEY = "pinnace-checklist-v2";
  var HISTORY_KEY = KEY + ":history";
  var HISTORY_MAX = 10;

  function read(key, fallback) {
    try { return JSON.parse(localStorage.getItem(key)) || fallback; } catch (e) { return fallback; }
  }
  function write(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) { /* storage unavailable */ }
  }
  function ids(s) { return Object.keys(s).filter(function (k) { return s[k]; }).sort(); }
  function same(a, b) { return ids(a).join() === ids(b).join(); }

  var state = read(KEY, {});
  var viewing = null; // a shared list being viewed read-only: { state, label }

  // ---------------------------------------------------------------- history

  function history() { return read(HISTORY_KEY, []); }

  function snapshot(reason) {
    var h = history();
    if (h.length && same(h[0].state, state)) return;
    h.unshift({ t: new Date().toISOString(), reason: reason, state: Object.assign({}, state) });
    write(HISTORY_KEY, h.slice(0, HISTORY_MAX));
  }

  // Snapshot the previous state the first time it changes in each visit.
  function snapshotOncePerVisit() {
    try {
      if (sessionStorage.getItem(KEY + ":snap")) return;
      sessionStorage.setItem(KEY + ":snap", "1");
    } catch (e) { /* no session storage: snapshot every change instead */ }
    snapshot("Before changes on " + new Date().toLocaleDateString());
  }

  function replaceState(next, reason) {
    snapshot(reason);
    state = next;
    write(KEY, state);
  }

  // ---------------------------------------------------------------- share links

  function b64url(bytes) {
    var s = "";
    bytes.forEach(function (b) { s += String.fromCharCode(b); });
    return btoa(s).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  }
  function unb64url(str) {
    var s = atob(str.replace(/-/g, "+").replace(/_/g, "/"));
    var out = new Uint8Array(s.length);
    for (var i = 0; i < s.length; i++) out[i] = s.charCodeAt(i);
    return out;
  }
  function encode(s) {
    var max = 0;
    window.CARDS.forEach(function (c) { if (s[c.uid] && c.uid > max) max = c.uid; });
    var bytes = new Uint8Array(Math.ceil((max + 1) / 8));
    window.CARDS.forEach(function (c) { if (s[c.uid]) bytes[c.uid >> 3] |= 1 << (c.uid & 7); });
    return "v1." + b64url(bytes);
  }
  function decode(code) {
    var m = /^v1\.([A-Za-z0-9_-]*)$/.exec(code || "");
    if (!m) return null;
    var bytes = unb64url(m[1]), s = {};
    window.CARDS.forEach(function (c) {
      if ((bytes[c.uid >> 3] || 0) & (1 << (c.uid & 7))) s[c.uid] = true;
    });
    return s;
  }
  function shareUrl(s, label) {
    var url = location.href.split("#")[0] + "#list=" + encode(s);
    return label ? url + "&from=" + encodeURIComponent(label) : url;
  }
  function parseHash() {
    var p = {};
    location.hash.replace(/^#/, "").split("&").forEach(function (kv) {
      var i = kv.indexOf("=");
      if (i > 0) p[kv.slice(0, i)] = decodeURIComponent(kv.slice(i + 1));
    });
    return p;
  }

  // ---------------------------------------------------------------- shared UI

  function current() { return viewing ? viewing.state : state; }

  function refresh() {
    var s = current();
    document.querySelectorAll("[data-have]").forEach(function (box) {
      box.checked = !!s[box.dataset.have];
      box.disabled = !!viewing;
      var tile = box.closest(".tile");
      if (tile) tile.classList.toggle("is-have", box.checked);
    });
    document.querySelectorAll("[data-count-have]").forEach(function (el) {
      var list = el.dataset.countHave.split(" ").filter(Boolean);
      el.textContent = list.filter(function (id) { return s[id]; }).length;
    });
    var hc = document.getElementById("have-count");
    if (hc) hc.textContent = ids(s).length;
  }

  document.addEventListener("change", function (ev) {
    var id = ev.target.dataset && ev.target.dataset.have;
    if (!id || viewing) return;
    snapshotOncePerVisit();
    if (ev.target.checked) state[id] = true; else delete state[id];
    write(KEY, state);
    refresh();
    if (window.CARDS && document.getElementById("show").value !== "all") renderChecklist();
  });

  // Simple table filter for the players list.
  document.querySelectorAll("[data-filter]").forEach(function (input) {
    var rows = document.querySelectorAll(input.dataset.filter + " tbody tr");
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      rows.forEach(function (r) { r.hidden = q && r.dataset.search.indexOf(q) < 0; });
    });
  });

  // ---------------------------------------------------------------- checklist page

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return "&#" + c.charCodeAt(0) + ";"; }); }
  function $(id) { return document.getElementById(id); }

  function renderChecklist() {
    var s = current();
    var order = $("order").value, show = $("show").value;
    var cards = window.CARDS.filter(function (c) { return show === "all" || (show === "have") === !!s[c.uid]; });
    var groups = {}, keys = [];
    function add(k, c) { if (!groups[k]) { groups[k] = []; keys.push(k); } groups[k].push(c); }
    if (order === "team") {
      cards.slice().sort(function (a, b) { return a.team.localeCompare(b.team) || a.n - b.n; })
        .forEach(function (c) { add(c.team, c); });
    } else if (order === "surname") {
      cards.slice().sort(function (a, b) { return a.sur.localeCompare(b.sur) || a.first.localeCompare(b.first); })
        .forEach(function (c) { add(c.sur.charAt(0).toUpperCase(), c); });
    } else {
      cards.slice().sort(function (a, b) { return a.n - b.n; }).forEach(function (c) { add("All cards by number", c); });
    }
    $("checklist").innerHTML = keys.map(function (k) {
      return '<section class="cl-group"><h2>' + esc(k) + ' <small>(' + groups[k].length + ')</small></h2><ul class="cl">' +
        groups[k].map(function (c) {
          return '<li><input type="checkbox" data-have="' + c.uid + '" aria-label="Have ' + esc(c.name) + '">' +
            '<span class="cn">' + c.n + '</span><a href="players/' + c.id + '.html">' + esc(c.name) + '</a>' +
            (order === "team" ? "" : ' <span class="ct">' + esc(c.team) + '</span>') + '</li>';
        }).join("") + "</ul></section>";
    }).join("") || "<p>No cards to show.</p>";
    refresh();
  }

  function renderBanner() {
    var b = $("viewing");
    b.hidden = !viewing;
    document.body.classList.toggle("is-viewing", !!viewing);
    if (!viewing) return;
    $("viewing-label").textContent = viewing.label ? "“" + viewing.label + "”" : "a shared list";
    $("viewing-count").textContent = ids(viewing.state).length;
  }

  function renderHistory() {
    var h = history();
    $("history-list").innerHTML = h.length ? h.map(function (e, i) {
      return '<li><span>' + esc(new Date(e.t).toLocaleString()) + ' · ' + ids(e.state).length + ' cards' +
        '<small> ' + esc(e.reason || "") + '</small></span>' +
        '<button type="button" data-restore="' + i + '">Restore</button>' +
        '<button type="button" data-share-snap="' + i + '">Copy link</button></li>';
    }).join("") : "<li>No earlier versions yet.</li>";
  }

  function copy(text, button) {
    function done() { var t = button.textContent; button.textContent = "Copied"; setTimeout(function () { button.textContent = t; }, 1500); }
    if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function () { prompt("Copy this link", text); });
    else prompt("Copy this link", text);
  }

  function loadFromHash() {
    var p = parseHash(), s = p.list && decode(p.list);
    viewing = s ? { state: s, label: p.from || "" } : null;
    renderBanner();
    renderHistory();
    renderChecklist();
  }

  // ---------------------------------------------------------------- light / dark

  // With no saved choice the page follows the system setting; the button saves an explicit one.
  (function () {
    var btn = $("theme-toggle"), root = document.documentElement, dark = matchMedia("(prefers-color-scheme: dark)");
    if (!btn) return;
    function isDark() { return root.dataset.theme ? root.dataset.theme === "dark" : dark.matches; }
    function label() {
      btn.textContent = isDark() ? "☀" : "☾";
      btn.setAttribute("aria-label", isDark() ? "Switch to light mode" : "Switch to dark mode");
      btn.title = btn.getAttribute("aria-label");
    }
    btn.addEventListener("click", function () {
      root.dataset.theme = isDark() ? "light" : "dark";
      try { localStorage.setItem("pinnace-theme", root.dataset.theme); } catch (e) {}
      label();
    });
    if (dark.addEventListener) dark.addEventListener("change", label);
    label();
  })();

  // ---------------------------------------------------------------- style picker (see content/site.md)

  (function () {
    var pick = $("style-picker");
    if (!pick || !window.pinnaceStyle) return;
    pick.value = document.documentElement.dataset.preset;
    pick.addEventListener("change", function () {
      pinnaceStyle(pick.value);
      try { localStorage.setItem("pinnace-style", pick.value); } catch (e) {}
    });
  })();

  // ---------------------------------------------------------------- header search

  function fold(t) { return String(t).normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase(); }

  // Every query word must appear in the entry; entries whose name starts with the query rank first.
  function searchScore(e, words, q) {
    var name = fold(e[1]), hay = name + " " + fold(e[2]) + " " + fold(e[4]), score = 0;
    for (var i = 0; i < words.length; i++) {
      var at = hay.indexOf(words[i]);
      if (at < 0) return -1;
      if (at === 0 || hay.charAt(at - 1) === " ") score += 1;
    }
    if (name.indexOf(q) === 0) score += 3;
    if (at < name.length) score += 1;
    return score + { Team: .3, Feature: .2, Player: 0 }[e[0]];
  }

  (function () {
    var box = $("site-search"), list = $("site-search-results");
    if (!box || !window.SEARCH) return;
    var up = box.parentNode.dataset.up || "", results = [], active = -1;

    function render() {
      var q = fold(box.value.trim()), words = q.split(/\s+/).filter(Boolean);
      results = !words.length ? [] : window.SEARCH
        .map(function (e) { return { e: e, s: searchScore(e, words, q) }; })
        .filter(function (r) { return r.s >= 0; })
        .sort(function (a, b) { return b.s - a.s || a.e[1].localeCompare(b.e[1]); })
        .slice(0, 12).map(function (r) { return r.e; });
      active = results.length ? 0 : -1;
      list.innerHTML = results.map(function (e, i) {
        return '<li role="option" id="ss-' + i + '"><a href="' + up + e[3] + '"><span class="ss-kind">' + e[0] + '</span>' +
          '<span class="ss-name">' + esc(e[1]) + '</span>' + (e[2] ? '<small>' + esc(e[2]) + '</small>' : "") + '</a></li>';
      }).join("") || (words.length ? '<li class="ss-none">No matches</li>' : "");
      list.hidden = !list.innerHTML;
      box.setAttribute("aria-expanded", String(!list.hidden));
      highlight();
    }
    function highlight() {
      Array.prototype.forEach.call(list.children, function (li, i) { li.classList.toggle("is-active", i === active); });
      if (active >= 0) box.setAttribute("aria-activedescendant", "ss-" + active); else box.removeAttribute("aria-activedescendant");
    }
    box.addEventListener("input", render);
    box.addEventListener("focus", function () { if (box.value.trim()) render(); });
    box.addEventListener("keydown", function (ev) {
      if (ev.key === "ArrowDown" || ev.key === "ArrowUp") {
        if (!results.length) return;
        ev.preventDefault();
        active = (active + (ev.key === "ArrowDown" ? 1 : -1) + results.length) % results.length;
        highlight();
      } else if (ev.key === "Enter" && active >= 0) {
        location.href = up + results[active][3];
      } else if (ev.key === "Escape") {
        list.hidden = true; box.setAttribute("aria-expanded", "false"); box.blur();
      }
    });
    document.addEventListener("click", function (ev) {
      if (!box.parentNode.contains(ev.target)) { list.hidden = true; box.setAttribute("aria-expanded", "false"); }
    });
    // "/" jumps to the search box, as on many sites.
    document.addEventListener("keydown", function (ev) {
      if (ev.key === "/" && !/INPUT|SELECT|TEXTAREA/.test(document.activeElement.tagName)) { ev.preventDefault(); box.focus(); }
    });
  })();

  if (window.CARDS) {
    ["order", "show"].forEach(function (id) {
      var el = $(id);
      try { el.value = localStorage.getItem(KEY + ":" + id) || el.value; } catch (e) {}
      el.addEventListener("change", function () {
        try { localStorage.setItem(KEY + ":" + id, el.value); } catch (e) {}
        renderChecklist();
      });
    });
    $("share").addEventListener("click", function () {
      snapshot("Shared");
      renderHistory();
      copy(shareUrl(state, $("share-name").value.trim()), $("share"));
    });
    $("export").addEventListener("click", function () {
      var blob = new Blob([JSON.stringify(state, null, 1)], { type: "application/json" });
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "pinnace-checklist.json";
      a.click();
    });
    $("import").addEventListener("change", function (ev) {
      var f = ev.target.files[0];
      if (!f) return;
      f.text().then(function (t) {
        try { replaceState(JSON.parse(t) || {}, "Before loading a backup"); renderHistory(); renderChecklist(); }
        catch (e) { console.error(e); }
      });
    });
    $("adopt").addEventListener("click", function () {
      replaceState(Object.assign({}, viewing.state), "Before copying a shared list");
      location.hash = "";
    });
    $("leave").addEventListener("click", function () { location.hash = ""; });
    $("history-list").addEventListener("click", function (ev) {
      var h = history(), r = ev.target.dataset.restore, sh = ev.target.dataset.shareSnap;
      if (r !== undefined) { replaceState(Object.assign({}, h[+r].state), "Before restoring an earlier version"); renderHistory(); renderChecklist(); }
      if (sh !== undefined) copy(shareUrl(h[+sh].state, $("share-name").value.trim()), ev.target);
    });
    window.addEventListener("hashchange", loadFromHash);
    loadFromHash();
  }
  refresh();
})();
