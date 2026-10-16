# Swole Clicker — Changes

## Overhaul (October 2026) — save version 8
Single-file `index.html`, vanilla JS. No players existed before this update, so older saves only get
sensible defaults rather than careful migration.

**Character.** 15 tappable muscles (front + back view, 🔄 turn button / `T`), tap zones that match the drawn
shapes, 35 exercise animations (2–3 per muscle, unlocked at muscle Lv 8 and 20), idle posing routine, per-muscle
levels and growth with definition, striations and veins, symmetry bonus and 🎯 weak-point ×2 reps.

**Progression.** Hidden shop items, item milestones (×1.5 at 25/50/100/150/200 owned), item info popups,
buy ×1/×10/×100/Max, 59 upgrades (two per muscle), 🎤 Stage tab with cube-root trophies, a judged posing show and
14 trophy perks. Economy rebalanced with a greedy-player simulation (late items pay back ~1.33× slower per tier).

**Moment-to-moment.** Pump meter → Beast Mode (reps ×5), five gym events (delivery, spotter, crush, photo shoot,
rep storm), 8 rivals with four minigames (arm-wrestle, perfect form, hold the weight, pose-off) that award titles,
cosmetics and +5% gains.

**Presentation.** Five gyms that change with rank (Dad's Garage → Swoleympia Stage) showing owned gear, a different
music style per gym (grunge, lo-fi, house, metal, arena anthem), synthesized SFX, 90 awards in 12 categories with
progress bars, a stats chart and income breakdown, ⚙️ settings, and 13 one-time tutorial tips.

**Publishing.** CrazyGames SDK v3 (init, loading/gameplay events, rewarded + midgame ads, Data-module saves,
username/avatar), fit-to-window landscape layout, PEGI 12 content pass, new share card, covers and preview videos.
See `PUBLISHING.md`.

## Earlier (June 2026)
- Publish-readiness: rewarded ads, daily login streak, Locker (body type, skin, hair, accessories), first-60s
  onboarding, pause-when-hidden, share card.
- Daily quests and portal adapters (CrazyGames + GameDistribution).

## Launch-results update (October 15, 2026)
Based on the CrazyGames Basic Launch stats (mobile gameplay conversion 41%, D1 retention ~4.8%, playtime 7–9 min).
- **First visit:** brand-new players skip the daily-bonus popup and go straight to the tap-a-muscle tutorial; the
  Day-1 bonus is paid as the tutorial's reward (first purchase). Gameplay starts immediately for CrazyGames.
- **Save safety:** if the CrazyGames SDK answers after the 4 s boot fallback, saving is held until the cloud save is
  checked; the run with more lifetime gains wins (fixes a blank run overwriting a real save on slow connections).
  Saves are also mirrored to localStorage as a backup.
- **Come-back hooks:** daily bonus shows tomorrow's reward; Quests show a reset countdown and "3 new quests tomorrow"
  when all are claimed; a one-time tip explains idle earnings while away.
- **Next goal:** a line under the rank bar always shows one thing to aim for (claimable quest → waiting rival →
  affordable upgrade → nearest award with progress); tapping it opens that tab.
- **Covers v2:** big before/after split covers in `assets/crazygames/v2/`.

## Full Launch compliance — part A (October 16, 2026)
CrazyGames Full Launch notes: readability across screen sizes, Muscles panel too small, too many Data-module writes.
- **Fixed 16:9 layout on CrazyGames (landscape):** designed at 960×540; `html` font-size = 16px × scale and the whole
  stylesheet is in rem, so the layout is identical at every iframe size (text ≥ 12px at 821×462, scales up in
  fullscreen). The canvas backing resolution follows its on-screen size. Muscles: a 2-column list with all 15 rows
  visible. Title hidden (CrazyGames shows it under the iframe). `?fixed` previews it locally. Website/iOS unchanged.
- **Saves:** cloud (Data module) writes at most every 5 s, flushed on tab hide/close; localStorage keeps every save.
- **Ads:** UI blocked from request until finish/error; audio mutes only once the ad starts; no ad after the
  welcome-back popup; a midgame break after a finished rival match; ad blocker → boosts disabled with an inline note.
  Rewarded boosts moved from under DO A REP to a "Free boosts" card at the top of the Shop.
- **Account:** a guest who logs in mid-game is saved and the page reloads to load the account's progress.
- **Space:** holding it no longer auto-repeats reps.

## Visual polish — part B (October 16, 2026)
- **Icon set:** 54 hand-drawn SVG icons (`tools/icons.py` → inline sprite in index.html; `ic('id')` in JS) replace the
  emojis for all 37 shop items, the 8 tabs, prices (gains), trophy badge, settings, turn, ad boosts, mystery items.
  Same art on every OS (emojis looked different/cheap on Windows).
- **Font:** Lilita One (SIL OFL, 10.7 KB woff2, embedded) for numbers, headings, buttons, tabs and item names.
- **Feel:** hover/press states on rows, tabs and buttons; panel fade-in on tab switch; purchase pop on the bought row;
  a "RANK UP!" banner with confetti on the stage when the run's rank climbs.
