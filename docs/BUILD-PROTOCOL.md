# Build Protocol — Nimbus: Cloud Clash

| Phase | Gem | Status |
|---|---|---|
| 1 Define | Amethyst | Done |
| 2 Plan | Sapphire | Done |
| 3 Build | Onyx | Worlds 1–4 done |
| 4 Ship | Ruby | v35 live on GitHub Pages |
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
- [x] v30: Hex prompt logo, GitHub Pages site with home-screen icon, full source in the repo with a build check in CI.
- [x] v31: AZ-900 crunch pack (58 questions, 16 cards, 14 duels) checked against the July 20, 2026 outline.
- [x] v32: AZ-104 pack (15 stops, 137 cards, 130 questions, 59 duels, 15 bosses, mocks), fifth domain colour, three new 3D models (NSG evaluation, hub and spoke, Load Balancer vs Application Gateway).
- [x] v33: UI polish. Pop-up messages moved to the top on phones, exam weights shown as domain chips in the Codex, 3D model labels always face you, Ready to book checklist with a progress bar, last shadows removed.
- [x] v34: SC-500 pack (12 stops, 105 cards, 100 questions, 52 duels, 12 bosses, mocks). All four certs on the route now have content.
- [x] v35: SC-500 facts verified and fixed, practice assessment note, 3 new models (PIM, Key Vault, Sentinel); Mistake review; offline support; Learn links on every SC-900, AZ-104 and SC-500 stop.
- [ ] Dajoni plays on iPhone and reports anything off.

## 5 · Maintain (Emerald)
- [ ] SC-500: swap in the practice assessment link when Microsoft releases it, and re-check the Security for AI stop before the exam.
- [ ] AZ-104: check against the AI Skills Navigator practice assessment.
- [ ] Retune enemy HP from real play.
- [ ] Check SC-900 questions against the new practice assessments on AI Skills Navigator.
- [ ] A Cloud Clash world per cert (Cloud Clash is AZ-900 only today).
- [ ] Add questions where topic pools are small (Shared responsibility, Cost model).
- [ ] After each practice assessment, add duel pairs and campaign threats for the new mix-ups.
