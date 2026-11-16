# Handoff plan: what is built and what is next

**For:** the next model working on Nimbus (Opus 5.5) · **Written:** Nov 16, 2026 · **Owner:** Dajoni Gomez

This is the plan to finish the cert path in Nimbus: **AZ-900 → SC-900 → AZ-104 → SC-500**. All four packs are built: AZ-104 in v32 (`content/az104/`) and SC-500 in v34 (`content/sc500/`). The steps below are kept as the recipe for adding or rebuilding a pack. What is left is the backlog at the end.

## Where things stand

| Cert | State | Content |
| --- | --- | --- |
| AZ-900 | Built (v31) | 172 cards, 212 questions, 91 duels, 12 stops, 40-level Cloud Clash |
| SC-900 | Built (v28, checked v36) | 112 cards, 102 questions, 46 duels, 14 stops, 12-level Cloud Clash. Checked on Learn against the Oct 21, 2026 outline |
| AZ-104 | Built (v32) | 137 cards, 130 questions, 59 duels, 15 stops, 3 new 3D models, 15-level Cloud Clash. Not yet checked against a Microsoft practice assessment |
| SC-500 | Built (v34, checked v35) | 105 cards, 101 questions, 52 duels, 12 stops, 3 models, 12-level Cloud Clash. Facts checked on Learn. Practice assessment not released yet |

- Live site: https://cop1ouss.github.io/nimbus-cloud-quest/ (GitHub Pages, `main`, root).
- Claude artifact: https://claude.ai/artifact/PoB3gf2GAtn86ZcK5hRMyy (same app; has cloud sync and Ask Nimbo).
- Dajoni's rule: no emoji, no gradients, no shadows; Catppuccin Frappé (Latte for light); JetBrains Mono; plain, short sentences. Every project keeps a README, PRD and Build Protocol up to date.
- Dajoni is in AZ-900 crunch time (practice scores 36%, 70%, 54%; target 80% twice before booking). Do not change AZ-900 behavior while building new packs.

## What a pack is

`src/data_packs.json` → `packs.<id>` = `{meta, cards, questions, sections, duels}`. `content/sc/` is the working example: copy its shape.

- **meta:** `id, code, name, quest, domains{}, weights{}, bosses{"1":[name,""]...}, mix[], quickMix[], fullMins, quickMins, passPct, bookPct, msUrl, studyGuide, taunts{"1":[4 lines]...}`. `mix` must sum to the mock size and have one number per domain.
- **card:** `{id, d, topic, front, back, miss:false}`. `back` supports `**bold**`.
- **question kinds:**
  - one answer: `{q, opts[4], ans:[i], why, kind:'one'}`
  - two answers: same with `ans:[i,j]`, `kind:'two'`, and the text must say "Which TWO"
  - yes/no: `{type:'yn', kind:'yn', q, stmts[3], ans:[1,0,1], why}`
  - match: `{type:'match', kind:'match', q, rows[], choices[], ans[], why}`
- **duel:** `{id, d, a, b, clue, ans:0|1, why, miss:false}`. Two look-alike services and one clue.
- **section (Codex stop):** `{id:'s1', d, title, label, note, why:'', obj[], cold[], traps[], hooks[], topics[], qtopics[], mod, modTitle, units[], models?[]}`. `topics` are the card topics shown in the stop, `qtopics` the question topics. Every card and question topic must belong to a section.
- Ids must be unique inside a pack. Progress is stored per id, so never renumber ids that have shipped.

## Steps

1. **Re-check the outline.** Fetch the study guide URL in `content/outlines.json` for the cert and compare objectives. The AZ-104 page showed "as of October 26, 2023" on Nov 16, 2026, which is old: confirm it is still current. Update `outlines.json` if anything changed.
2. **Add a fifth domain colour (AZ-104 only).** The app has `--d1` to `--d4`. In `src/head.html` add `--d5` to both the Frappé and Latte token lines and `.d5{--c:var(--d5)}`. The Latte value must pass 4.5:1 on `#eff1f5`. Then grep `src/app.js` for anything that assumes at most 4 domains.
3. **Build AZ-104 first** (it comes before SC-500 on the path). Create `content/az104/` with a lib, content files and a build script, copying `content/sc/`. Read stops, domains and objectives from `content/outlines.json`.
   - Per stop: at least 8 cards, 8 questions and 3 duels. Associate-level exams are scenario-heavy, so most questions should be "You need to... What should you do?" with one best answer. Include case-style sets of yes/no statements.
   - Ground every fact in Microsoft Learn (the Microsoft Learn MCP tools, or `learn.microsoft.com`). Do not write limits, SKUs or retention numbers from memory.
   - Keep the build script's self-checks: topics belong to sections, each stop meets the minimums, each domain has enough questions for `mix`.
   - Remove the cert from `data['planned']` when its pack is added (see `sc_build.py`).
4. **Build SC-500** the same way in `content/sc500/`. It reuses a lot of SC-900 and AZ-104 ground at a deeper level. The "Security for AI" stop covers new products (Entra Agent ID, Foundry guardrails, Defender for AI): verify each against current docs.
5. **3D models.** Add models to `MODELS` in `src/app.js` (boxes are `[part, x, y, z, w, d, h, level, label]`) and list them in a section's `models`. Good candidates: NSG rule evaluation, hub-and-spoke with Azure Firewall, load balancer vs Application Gateway, backup vault and Site Recovery, PIM activation flow, Key Vault access, Sentinel pipeline.
6. **Verify.** `python3 build.py`, then the tests in `tests/` (README has the commands). Extend `tests/t42.py` to switch to each new cert, open every stop, and start a quiz, duel, boss and mock. `tests/t41.py` (axe-core) must report 0 violations in Frappé and Latte. Check 390px and 1280px widths for overflow.
7. **Ship.** Commit `src/`, `content/`, `index.html` and docs. CI fails if `index.html` is stale. Push to `main`; Pages updates in about a minute. For the Claude artifact run `python3 build.py --artifact` and publish `artifact.html` to the artifact URL above.
8. **Docs.** Add a section to `docs/PRD.md`, tick `docs/BUILD-PROTOCOL.md`, update the README counts, and copy the PRD and Build Protocol to the Claude project folder "IT DocsUs".

## Things that have gone wrong before

- **Save data:** only keys returned by `fresh()` in `src/app.js` survive a reload. Any new top-level state key must be added there. `merge()` deep-clones because cloud data arrives frozen.
- **`sc_build.py` also edits AZ-900 sections** (it attaches models). A new build script must not overwrite another pack's fields by accident.
- **Text contrast:** never dim text with `opacity`; use a token colour. This failed the accessibility scan once.
- **Design rules:** the foil card effect was once a gradient and had to be replaced. No gradients, shadows or emoji.
- **Tests:** seed `localStorage` with `page.evaluate` then reload (an init script races). Playwright will not click `aria-disabled` buttons.
- **Git:** commit as `Claude <noreply@anthropic.com>` or GitHub marks commits Unverified. Claude cannot enable Pages or create repos; Dajoni does that.

## Backlog after the packs

0. SC-500: swap `msUrl` for the real practice assessment when Microsoft publishes it and remove `msNote`. (Facts and models done in v35.)

1. SC-900 checked on Learn in v36. Still open: compare with the Microsoft practice assessment (Dajoni takes it), then AZ-104.
2. ~~Learn links per stop~~ done in v35 (`content/learn_units.py`).
3. ~~A Cloud Clash world per cert~~ done in v36 (`content/camp_certs.py`, saves in `state.campx`).
4. ~~Offline support~~ done in v35 (`sw.js`, GitHub Pages only).
5. ~~Review mode from missed questions~~ done in v35 (Arena → Mistake review).
6. Rebalance Cloud Clash enemy HP from Dajoni's real play, and fix whatever his iPhone playtest finds.
7. Refresh the Anki deck export with the newer cards.
