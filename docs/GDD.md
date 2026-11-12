# Nimbus: Cloud Clash — GDD v1

**Pitch:** A card battler where you build and defend a simulated Azure tenant. You play Azure services as cards to survive incidents, and every card works only if you know what it actually does.

**Player fantasy:** You are the cloud architect on call. Outages, bill shocks and attackers hit your tenant. You make the right architecture call, and you get faster and more certain every level.

**Core loop:** read the incident's next attack → play the Azure card that counters it (answer its recall check to cast at full power) → survive the wave and earn credits and new cards → build a stronger deck and tenant → face harder incidents.

The learning is the move itself. Picking the right counter (Availability Zones against a zone outage, a resource lock against an accidental delete) is applying an AZ-900 concept, not a quiz gate in front of the game.

**Session length:** 3–6 minutes per level (phone-first).

## Mechanics (3 for v1)

1. **Play a card (answer to cast).** You draw 5 cards, each an Azure service with a credit cost. Tap a card, answer its one-line recall check (1 question from the existing 154-question bank, or a this-or-that pair), and it deploys.
   - Right: full effect and a combo bonus.
   - Wrong: the card fizzles, you see the explanation, and the card goes into your review pile.
   - Feedback: card flip, a hit number and a sound within 100 ms.
2. **The tenant board (simulated Azure).** A living diagram of your environment:
   - Management group → Subscription → Resource group, inside a region with 3 Availability Zone lanes and a paired region off to the side.
   - Deployed cards appear as resources in a lane. Placement matters:
     - A VM in one zone dies to a zone outage; a zone-redundant one survives.
     - GRS storage survives a region disaster because the copy sits in the paired region.
     - A lock blocks an accidental delete.
   - The board is how you picture the concepts.
3. **Incidents with telegraphed intents.** Each enemy shows its next move one turn ahead. You choose the counter; uptime (your HP) drops if you are wrong or too slow. Examples:

| Incident | What it does | Counters |
|---|---|---|
| Zone Outage | Wipes one zone lane | Availability Zones, Scale Sets |
| Region Disaster | Wipes the whole region | GRS/GZRS, region pairs |
| Bill Shock | Drains your credits | Budgets, Reservations, Advisor |
| Brute-Force Sign-in | Damages identity | MFA, Conditional Access |
| Accidental Delete | Removes a resource | Resource lock (Delete/ReadOnly) |
| Rogue Deploy | Spawns a non-compliant resource | Azure Policy |
| Traffic Spike | Overloads compute | Scale Sets, App Service autoscale |
| Silent Failure | Hidden damage over time | Azure Monitor, Service Health |

## Progression

- **4 worlds, 40 levels.** Each level introduces one new card or one new incident, never both. The map follows the exam domains:
  - **World 1, Cloud Concepts:** 10 levels.
  - **World 2, Architecture and Services:** 16 levels.
  - **World 3, Management and Governance:** 10 levels.
  - **World 4, Exam Day:** a 4-level gauntlet mixing everything.
- **Bosses:** each world ends with its existing boss (CapEx Colossus, Zone Hydra, Policy Warden), now as a multi-phase card fight. The three duel rivals (Bill Shock Imp, Latency Gremlin, Misconfig Phantom) return as mini-bosses.
- **Stars (1–3) per level:** 1 for survive, 2 for 80%+ recall accuracy, 3 for no fizzles.
- **Rewards:**
  - Credits buy new cards from the Azure Marketplace shop.
  - Cleared worlds unlock Tenant upgrades: a second region, management groups.
- **Confidence track:** each of the official AZ-900 objectives gets a meter filled by correct casts in real play. It lights up which objectives you have proven under pressure. It is never sold as a pass prediction.

## Fail and win

- **Fail:** uptime hits 0 and the tenant goes down. You retry in under 5 seconds with a "what took you down" card naming the concept and linking the Learn page. Nothing is lost except the run.
- **Win:** stars, credits, a new card, the next level. Boss wins unlock the world's badge and a short "you just used X, Y, Z" recap.

## Content is data (JSON)

- **Cards:** service, cost, effect, counters, linked question IDs.
- **Incidents:** intent pattern, damage, counters.
- **Levels:** deck rules, waves, the new thing introduced, star targets.
- **Questions and duel pairs:** reused from Nimbus (154 questions, 77 pairs).

Adding levels or a new cert later is a data change, not new code.

## Art and audio

- **Look:** flat, clear, diagrammatic. Uncook Catppuccin **Frappé** (study/certs).
- **Text:** JetBrains Mono everywhere.
- **Colour meanings:** gem tokens keep their meanings: `red` = boss HP and damage, `green` = success, `yellow` = XP.
- **Graphics:** stroke SVG icons and no emoji. Card frames use 18px radius with an 8px top band.
- **Characters:** Nimbo and the three bosses, recoloured to Frappé.
- **Audio:** the existing synthesized sound effects.

## Platform and controls

- **iPhone first:** tap to select and tap to play, no drag required. Works one-handed in portrait.
- **Desktop:** keys 1–5 play cards, Space ends the turn.
- **Saving:** progress saves to your account.

## MVP (ship first)

- The full loop, the tenant board and the card/question system.
- **World 1 complete:** 10 levels, about 14 cards, 5 incident types and the CapEx Colossus boss.
- The level map, stars, credits and the shop.

## Later (listed so it is not built yet)

- **More worlds:** Worlds 2–4 and their cards and incidents.
- **Run types:** daily challenge, endless "on-call shift" mode.
- **Collection:** card foils for mastery.
- **Content:** SC-900 card set once AZ-900 is passed.
- **Shared progress:** share weak spots between Nimbus and the game.

## Open questions

1. Separate game, or a Campaign mode inside Nimbus?
2. Ship World 1 first, or all 4 worlds in one go?
3. Build Protocol: which format do you use?
