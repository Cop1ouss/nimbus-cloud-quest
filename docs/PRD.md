# PRD — Nimbus: Cloud Clash (Campaign mode)

**Owner:** Dajoni Gomez · **Status:** Full game loop shipped (v38, live on GitHub Pages) · **Updated:** Nov 18, 2026

## Problem

Practice scores went from 36% to 70%. Misses now come from mixing up look-alike services under time pressure, not from missing knowledge. Flashcards and quizzes drill recall but don't build the habit of *choosing the right service for a situation*. That habit is what the exam tests.

## Goal

Pass AZ-900 with confidence: 80%+ on the Microsoft practice assessment on two attempts before booking.

## Objectives

1. Make "pick the right Azure service for this problem" the core move of a game.
2. Picture concepts. Use a visual tenant where resources live and shared responsibility is shown per resource.
3. Build confidence through many small, winnable levels that each teach one new thing.

## Users

Dajoni, on iPhone (commute, breaks) and desktop. Later: other AZ-900 learners.

## Scope v1 (World 1: Cloud Concepts)

- 10 levels, the last one the CapEx Colossus boss. Each level unlocks 1–2 cards and adds one threat.
- 14 service cards (deploy or action), with costs from 0 to 2 credits.
- 11 threat types, each with a counter card and a "what took you down" lesson.
- Answer to cast: a card asks one question from its topic. Right = it plays; wrong = it fizzles and shows the explanation. After 3 correct casts a card is **proven** and asks only 25% of the time.
- A tenant board with 4 resource slots and a shared-responsibility strip (Data, Apps, OS, Hosts) for each deployed resource.
- Stars per level: win, 80%+ correct checks, no fizzles.
- Progress is shared with Nimbus: XP, streak, and the question weak spots that feed quizzes.
- Look: Uncook Catppuccin Frappé, JetBrains Mono, stroke icons.

## Scope v2 (Worlds 2–4)

- **World 2, Architecture and Services (levels 11–26):** zones, region pairs, compute, networking, storage, identity and security, then the Zone Hydra boss. The tenant board gains three availability-zone lanes plus a zone-redundant row. Zone Outage takes out one telegraphed zone; resources spread across zones or deployed zone-redundant survive.
- **World 3, Management and Governance (levels 27–36):** cost tools, tags, locks, Policy, Purview, Service Trust Portal, ARM templates, Arc, Monitor, Service Health and Advisor, then the Policy Warden boss.
- **World 4, Exam Day (levels 37–40):** fixed mixed decks, ending with a final boss (Elder CapEx Colossus) that throws every domain's threats.
- **Decks:** each world's deck is its own unlocks, so World 2 starts small again. World 4 uses fixed exam decks.
- **Map:** world tabs, with stars per world.

## Scope v3 (replay and progression)

- **Credits wallet:** earned from campaign wins (20 + 10 per star first time, 5 on replays), On-Call incidents (5 each) and the Daily Incident (40, once a day).
- **Marketplace:**
  - Four perks, always active once bought: Reserved Capacity (+1 starting credit), SLA Credit (+4 max uptime), Advisor Insight (see the threat after next), Premium Support (first fizzle refunded).
  - Card upgrades (+2 main effect, or +1 throughput) for 60 credits each.
- **On-Call Shift (endless):**
  - Pick 5–10 unlocked cards as your loadout. Incidents only use threats your loadout can counter, and every 5th incident is a boss.
  - Between incidents, choose heal, max uptime, or 2 copies of a new card.
  - Your best shift is saved.
- **Daily Incident:** the same deck, foe and threats for everyone each day (seeded by date).
- **Collection:** every card, locked or unlocked, showing which threats it counters and its mastery. A card is proven at 3 correct casts and becomes a foil at 10.
- **Exam objectives tracker (Profile):** accuracy per question topic across quizzes, mocks and cast checks.
- **New badges:** World 1–4 cleared, On-Call Hero (10 incidents), Daily Defender, Foil Card.
- **Icons:** emoji replaced with line icons and hexagon badges, per the Uncook design system.

## v27 quick fixes

- **Backup and restore:** Profile → Tools saves all progress as a .json file and restores it after a confirm. Files that are not Nimbus backups are refused.
- **Badges on open:** badges you already qualify for are awarded when the app opens, not only after the next action.
- **Loadout guard:** On-Call Shift will not start with a loadout that has no damage or throughput card.
- **Accessibility:** page language and a top-level heading set; text no longer dimmed with opacity; Latte mute, red and two domain colours darkened to pass 4.5:1.

## v28: Cloud Quest, SC-900 and 3D models

- **Rename:** the app is now Nimbus: Cloud Quest. The header subtitle shows the active cert.
- **SC-900 path:** switch certs by tapping the Nimbus name. SC-900 has its own Codex (14 stops across 4 domains), deck, quizzes, duels, bosses and mock exams (50 questions in 45 minutes, weighted 6/14/19/11 by domain). Progress is kept per cert. XP, streak and badges are shared.
- **3D models:** interactive CSS 3D models inside Codex stops. Drag to turn, tap a part to read what it is, Spread layers to pull the levels apart. Defense in depth and Zero Trust (AZ-900 stop 8, SC-900 stop 1), Azure hierarchy and regions and zones (AZ-900 stop 4), hierarchy again in SC-900 stop 5.
- Cloud Clash stays AZ-900 only.

## v29: 3D bosses and structure models

- **Bosses** are 3D block figures built with the same engine as the models: a server-rack Colossus, a three-headed Zone Hydra and a shielded Policy Warden. They sway in the arena, flash when hit, lunge when they attack and collapse into rubble when beaten. Elder bosses get horns and a red tint. Cloud Clash boss levels use them too.
- **Models show containment:** the hierarchy model is now resources standing in resource groups, in subscriptions, in a management group.
- **New models:** shared responsibility (IaaS, PaaS and SaaS towers coloured by who is responsible), virtual network (subnets, VMs, NSG, VPN gateway), Conditional Access (signals, decision, grant or block), Defender XDR (portal, XDR layer, six services).
- Eight models in total across AZ-900 stops 1, 4, 6, 8 and SC-900 stops 1, 5, 7, 10.

## v30: logo and GitHub Pages

- **Logo:** the Hex prompt mark (a cloud with a `>_` prompt inside a mauve hexagon) in the header, the desktop sidebar, the browser tab and the home-screen icon.
- **Hosting:** the app now runs at cop1ouss.github.io/nimbus-cloud-quest and can be added to the iPhone home screen. Progress stays in each browser; Back up and Restore move it between the Claude artifact and the site.
- **Source in the repo:** `src/` holds the styles, app code and content, `content/` the generators, `tests/` the Playwright checks. `build.py` builds `index.html`, and CI fails if it is out of date.
- Downloads work outside Claude (plain browser download). Ask Nimbo and cloud sync only work inside the Claude artifact.

## v31: AZ-900 crunch pack

- After a 54% practice assessment, AZ-900 content was checked against the skills outline of July 20, 2026 and topped up: 58 new questions, 16 cards and 14 duels (now 212 questions, 172 cards, 91 duels).
- Focus: thin topics (shared responsibility, cost model, resources a VM needs, public vs private endpoints, storage account types, tiers and redundancy, file movement tools, Entra Domain Services, external identities, sovereign regions) and repeat misses (Policy vs locks vs RBAC, cost factors, pricing calculator vs Cost Management, Arc, IaC, monitoring tools).
- Generated by `content/az900_crunch.py`; re-running it replaces the earlier crunch items.

## v32: AZ-104 pack

- **AZ-104 path** opened as the third cert: 15 Codex stops across 5 domains (skills measured as of October 26, 2023, still current on Microsoft Learn on November 16, 2026), 137 cards, 130 questions, 59 duels, 15 bosses, and mocks of 50 questions in 100 minutes weighted 12/9/12/9/8.
- Facts checked against Microsoft Learn on November 16, 2026, including recent changes: Azure Disk Encryption retiring September 15, 2028 (encryption at host instead), Basic Load Balancer and Basic public IP retired, no new NSG flow logs since June 30, 2025 (VNet flow logs instead).
- Fifth domain colour `--d5` (peach in Frappé, #a8430a in Latte, 5.35:1 on the Latte background).
- Three new 3D models: NSG evaluation (stop 12), hub and spoke (stop 11), Load Balancer vs Application Gateway (stop 13). Hierarchy and regions models reused in stops 2, 3 and 8.
- Generated by `content/az104/az_build.py`, which reads stops and objectives from `content/outlines.json` and asserts at least 8 cards and 8 questions per stop.

## v33: UI polish

- Pop-up messages show at the top on phones, so they no longer cover cards and buttons above the tab bar.
- The Codex shows exam weights as one coloured chip per domain instead of a paragraph.
- Labels on top of 3D model blocks turn to face you at any angle.
- Ready to book has a count, a progress bar and round check badges.
- The last three shadows were removed, per the Uncook design rules.

## v34: SC-500 pack

- **SC-500 path** opened as the fourth cert, so the whole route (AZ-900, SC-900, AZ-104, SC-500) now has content: 12 Codex stops across 4 domains (skills measured as shown on Microsoft Learn on November 16, 2026), 105 cards, 100 questions, 52 duels, 12 bosses, mocks of 50 questions in 100 minutes weighted 12/14/12/12.
- Checked on Microsoft Learn on November 16, 2026: Security for AI (Purview DSPM, Copilot Studio runtime protection, Entra Agent ID, AI Gateway, Defender for AI Services, Foundry guardrails), Security Copilot roles and agents, Sentinel roles and data tiers, Defender for Servers plans, Key Vault soft delete and purge protection, Virtual Network Manager admin rules, Defender for Storage, SQL auditing.
- Not re-checked line by line, written from established product behaviour: PIM, Conditional Access, app consent, SQL encryption features, Azure Firewall SKUs, Entra Private Access, AKS and App Service hardening, WAF, EASM, Sentinel connectors, blast radius in Defender XDR. Verify these against the practice assessment when Microsoft publishes one.
- The practice-assessment button links to the SC-500 study guide for now; no practice assessment link was found.
- Each stop links to a Microsoft Learn documentation page instead of a training module.
- Generated by `content/sc500/s5_build.py`. No new 3D models; stops 1, 3 and 6 reuse existing ones.

## v35: SC-500 follow-up, Mistake review, offline, Learn links

- **SC-500 checked:** the facts v34 left unchecked were verified on Microsoft Learn. Fixed: Azure Firewall Standard already has web categories and Basic threat intelligence is alert-only (new question added); blast radius analysis needs the Sentinel data lake; EASM is included in Defender CSPM; Windows Forwarded Events land in WindowsEvent, which many built-in rules do not query.
- **SC-500 practice assessment:** not released yet (Microsoft adds them about eight weeks after an exam leaves beta). The button now opens the cert page and says so.
- **Three SC-500 3D models:** PIM activation (stop 1), Key Vault access (stop 2), Sentinel pipeline (stop 11).
- **Mistake review (Arena):** every question and duel pair you got wrong, from quizzes, mocks, bosses and duels, collects in one place, most-missed first. Each clears after two right answers in a row. Works for every cert.
- **Offline support:** a service worker on the GitHub Pages site caches the app, so the home-screen app opens without signal. New versions load whenever you are online. Not used in the Claude artifact.
- **Learn links per stop:** SC-900 and AZ-104 stops list their Learn module units; SC-500 stops link the matching learning path from the official SC-500 course and list its modules. Generated by `content/learn_units.py`, cached in `content/learn_units.json`, and reapplied by every pack build.

## v36: Cloud Clash for every cert, SC-900 check

- **Cloud Clash for SC-900, AZ-104 and SC-500.** One world per exam domain, three levels each (two fights and a boss): 12, 15 and 12 levels. Each world has a deploy card, four counter cards, one utility card and four threats. Every card's check question comes from a matching topic in that pack. Generated by `content/camp_certs.py` and reapplied by every pack build. Build asserts: every card topic exists in the pack, every icon exists, every threat has exactly one counter.
- **Saves are per cert.** AZ-900 keeps `state.camp`, so existing progress is untouched. Other certs save in `state.campx.<cert>`. The World badges stay tied to AZ-900. Daily Incident and On-Call Shift open after the world 1 boss of the cert you are on. The new campaigns skip the AZ-900 zone lanes and responsibility strip.
- **SC-900 checked** against Microsoft Learn and the skills outline of October 21, 2026: every outline item has cards and questions, and every answer key held up. One fix: the standalone Defender Threat Intelligence portal retired on August 1, 2026, so the card and distractors now say Microsoft Threat Intelligence in the Defender portal. Sentinel's Azure portal end date (after March 31, 2027) confirmed. A check against the Microsoft practice assessment itself still needs Dajoni, as Claude cannot take it.

## v37: AZ-900 Practice Assessment 4 misses

- After a second 70% (Nov 17, 2026), every miss became new AZ-900 items flagged weak so drills serve them first: 18 questions, 11 duel pairs, 5 cards (now 230 questions, 102 duels, 177 cards).
- Focus: Policy vs locks vs RBAC vs Conditional Access, Advisor vs Service Health vs Monitor, tags vs subscriptions, cost factors, horizontal vs vertical scaling, IaaS vs PaaS vs SaaS, region pairs, management groups vs administrative units, Functions vs Container Instances, Cloud Shell.
- Generated by `content/az900_pa4.py`; re-running it replaces the earlier pa4 items.
- Fix: Daily Incident and On-Call Shift stay open in every cert once the AZ-900 CapEx Colossus is beaten (v36 had locked them again after switching certs). Otherwise they open after the selected cert's world 1 boss.

## v38: AZ-900 Practice Assessment 5 misses and rule check

- After a fourth straight 70% (Nov 18, 2026), the 15 misses and 10 fresh rule-check scenarios became AZ-900 items flagged weak: 17 questions, 8 duel pairs, 3 cards (now 247 questions, 110 duels, 180 cards).
- Focus: lock vs Policy for deletion, Policy vs Advisor for compliance, Arc vs Advisor, CLI vs PowerShell, Monitor vs Application Insights for autoscale, health advisories vs service issues, MFA vs Verified ID, SaaS licensing, consumption model, disaster recovery, defense in depth, what is always the customer's.
- Generated by `content/az900_pa5.py`; re-running it replaces the earlier pa5 items.
- **Practice exam log:** Dajoni's Microsoft practice results ship with the app (`content/ms_log.py`, `meta.msLog`) and show in Me → Score history in every copy: 36, 70, 54, 70, 70, 70. Each browser adds only the results it is missing, matched by date and score. The log form now has a date box.

## Out of scope

Leaderboards and sharing.

## Acceptance criteria

- [x] Level 1 opens; level N+1 opens only after level N is cleared.
- [x] An automated playthrough clears all 40 levels with correct answers.
- [x] An automated playthrough clears all 39 SC-900, AZ-104 and SC-500 levels with correct answers, and the AZ-900 save is untouched (tests/t44.py).
- [x] Every threat in every level has a counter card in that level's deck (asserted when the data is built).
- [x] Purchases, upgrades, perks, best shift and daily clears survive reload.
- [x] On-Call Shift and Daily Incident playable end to end in automated runs.
- [x] Wrong answers fizzle cards, and losing shows the threat lesson. Retry takes one tap.
- [x] Stars and card mastery save and survive reload.
- [x] Works at 390px (iPhone) and 1280px; keys 1–5 play cards, Space ends the turn, A–D answer.
- [x] No console errors in automated runs.
- [x] Backup → wipe → restore brings back XP, campaign, credits and cards, and survives reload.
- [x] axe-core reports 0 WCAG 2 AA violations in Frappé and Latte, including SC-900 screens and the 3D models.
- [x] Mistake review lists missed questions and pairs, orders the most-missed first, and clears an item after two right answers in a row (tests/t43.py).
- [x] Offline: after one online visit the hosted app reloads with the network off.
- [x] SC-500: every stop has at least 8 cards and 8 questions, each domain fills its full-mock share, and the pack passes axe in both themes.
- [x] AZ-104: every stop has at least 8 cards and 8 questions, each domain fills its full-mock share, and the pack passes axe in both themes.
- [x] SC-900: every stop has at least 7 cards and 7 questions, and each domain has enough questions for a full mock (asserted when the pack is built).

## Success metrics

- Next practice assessment at 80%+ with at least 25 minutes used.
- All of World 1 at 2+ stars.
- Fewer misses on look-alike pairs (tracked in Practice Assessment notes).

## Risks

- **Small topic pools.** Shared responsibility and cost model have only 4 questions each, so repeats come fast. Mitigation: card mastery reduces checks, and more questions get added per world.
- **Balance** was tuned by a scripted perfect player. Real play may feel harder or easier. Retune enemy HP in data after real sessions.
