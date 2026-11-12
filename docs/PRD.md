# PRD — Nimbus: Cloud Clash (Campaign mode)

**Owner:** Dajoni Gomez · **Status:** Full game loop shipped (v29) · **Updated:** Nov 9, 2026

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

## Out of scope

Leaderboards and sharing, AZ-104 and SC-500 content, a Cloud Clash campaign for SC-900.

## Acceptance criteria

- [x] Level 1 opens; level N+1 opens only after level N is cleared.
- [x] An automated playthrough clears all 40 levels with correct answers.
- [x] Every threat in every level has a counter card in that level's deck (asserted when the data is built).
- [x] Purchases, upgrades, perks, best shift and daily clears survive reload.
- [x] On-Call Shift and Daily Incident playable end to end in automated runs.
- [x] Wrong answers fizzle cards, and losing shows the threat lesson. Retry takes one tap.
- [x] Stars and card mastery save and survive reload.
- [x] Works at 390px (iPhone) and 1280px; keys 1–5 play cards, Space ends the turn, A–D answer.
- [x] No console errors in automated runs.
- [x] Backup → wipe → restore brings back XP, campaign, credits and cards, and survives reload.
- [x] axe-core reports 0 WCAG 2 AA violations in Frappé and Latte, including SC-900 screens and the 3D models.
- [x] SC-900: every stop has at least 7 cards and 7 questions, and each domain has enough questions for a full mock (asserted when the pack is built).

## Success metrics

- Next practice assessment at 80%+ with at least 25 minutes used.
- All of World 1 at 2+ stars.
- Fewer misses on look-alike pairs (tracked in Practice Assessment notes).

## Risks

- **Small topic pools.** Shared responsibility and cost model have only 4 questions each, so repeats come fast. Mitigation: card mastery reduces checks, and more questions get added per world.
- **Balance** was tuned by a scripted perfect player. Real play may feel harder or easier. Retune enemy HP in data after real sessions.
