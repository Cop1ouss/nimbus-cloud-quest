# Build Protocol — Nimbus: Cloud Clash

| Phase | Gem | Status |
|---|---|---|
| 1 Define | Amethyst | Done |
| 2 Plan | Sapphire | Done |
| 3 Build | Onyx | Worlds 1–4 done |
| 4 Ship | Ruby | v29 published |
| 5 Maintain | Emerald | Ongoing |

## 1 · Define (Amethyst)
- [x] Problem: misses are look-alike service mix-ups under pressure (Practice Assessment 2, 70%).
- [x] Goal: 80%+ twice before booking AZ-900.
- [x] Decision: build Cloud Clash inside Nimbus (shared XP and weak spots), not as a separate app.

## 2 · Plan (Sapphire)
- [x] GDD v1 (core loop, 3 mechanics, 4 worlds).
- [x] PRD with acceptance criteria.
- [x] Scope: World 1 first (10 levels + CapEx Colossus).
- [x] Look: Uncook Catppuccin Frappé, JetBrains Mono.

## 3 · Build (Onyx)
- [x] Campaign data in `data_packs.json` (cards, threats, levels).
- [x] Engine: deck/hand/discard with reshuffle, credits, answer to cast, intents, counters, guards, throughput, stars.
- [x] Tenant board with shared-responsibility strips.
- [x] Map, keyboard controls, sounds, saving.
- [x] World 2: Architecture and Services (availability-zone lanes, zone-redundant row, region pair, Zone Hydra).
- [x] World 3: Management and Governance (locks, Policy, cost tools, monitoring, Policy Warden).
- [x] World 4: Exam Day gauntlet (4 levels, final boss).
- [x] Whole-app game UI: Frappé/Latte tokens, JetBrains Mono, Hub home, renamed tabs.
- [x] Fix: campaign progress now survives reload (was dropped by the save loader).
- [x] Marketplace: perks and card upgrades, credits wallet.
- [x] On-Call Shift (endless) with loadout and drafts.
- [x] Daily Incident (date-seeded).
- [x] Collection with proven and foil cards.
- [x] Exam objectives tracker and 7 new badges.
- [x] Emoji replaced with line icons and hexagon badges.

## 4 · Ship (Ruby)
- [x] Automated playthrough of all 40 levels, a loss path, and phone + desktop screenshots.
- [x] Published to the Nimbus artifact (same link).
- [x] v27 quick-fix bundle: progress backup and restore, badges checked on open, On-Call loadout guard.
- [x] Accessibility pass (axe-core, WCAG 2 AA) on every tab and Cloud Clash view in Frappé and Latte: 0 violations.
- [x] v28: renamed to Nimbus: Cloud Quest. SC-900 opened as a second cert path (14 stops, 112 cards, 102 questions, 46 duels, 12 bosses, mocks), built from the October 21, 2026 skills outline.
- [x] v28: four interactive 3D models in the Codex (defense in depth, Zero Trust, Azure hierarchy, regions and zones).
- [x] v29: bosses rebuilt as 3D block figures. Hierarchy model rebuilt as nested containers. Four new structure models: shared responsibility, virtual network, Conditional Access, Defender XDR.
- [ ] Dajoni plays on iPhone and reports anything off.

## 5 · Maintain (Emerald)
- [ ] Retune enemy HP from real play.
- [ ] SC-900: add Microsoft Learn unit links per stop, and a Cloud Clash world if wanted.
- [ ] Add questions where topic pools are small (Shared responsibility, Cost model).
- [ ] After each practice assessment, add duel pairs and campaign threats for the new mix-ups.
