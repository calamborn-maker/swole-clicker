# Swole Clicker — App Store submission

Everything you need to submit the iPhone app. The Xcode project is `ios/SwoleClicker.xcodeproj`.

## 1. Build & upload (Xcode)
1. Open `ios/SwoleClicker.xcodeproj` in Xcode (team **AD8HRS5Z7D**, bundle ID **com.calamborn.swoleclicker**, signing is Automatic).
2. *(Optional but recommended)* plug in your iPhone, pick it as the run destination, press ▶ and play for a minute.
3. Set the run destination to **Any iOS Device (arm64)** → **Product ▸ Archive**.
   Automatic signing registers the bundle ID with Apple the first time.
4. In the Organizer window: **Distribute App ▸ App Store Connect ▸ Upload** (defaults are fine).

If Xcode says there's no app record yet, do step 2 below first, then upload again.

## 2. Create the app in App Store Connect
appstoreconnect.apple.com → **Apps ▸ + ▸ New App**
- Platform: **iOS** · Name: **Swole Clicker** (if taken: *Swole Clicker: Gym Idle*)
- Primary language: **English (U.S.)** · Bundle ID: **com.calamborn.swoleclicker** · SKU: `swoleclicker`
- User access: Full access

## 3. Listing text
**Subtitle** (≤30): `Tap muscles. Get massive.`

**Promotional text** (≤170):
> Train 15 muscles, beat gym rivals and pose your way to Mr. Swoleympia. No ads. Plays offline.

**Description:**
> Swole Clicker is an idle gym game where every muscle counts. Tap any of 15 muscles on your lifter — chest, biceps, lats,
> glutes and more — and watch him do a real exercise for it: curls, bench press, pull-ups, deadlifts, hip thrusts and 30
> more moves. Each muscle grows on its own, so train evenly for a symmetry bonus… or go full Chicken Legs.
>
> Buy gym gear that keeps training while you're away, tap fast to fill the pump bar and go Beast Mode, and catch gym events
> like protein deliveries, rep storms and your gym crush watching you lift. Rank up from Dad's Garage to Mom's Basement, a
> real gym, a hardcore dungeon and finally the Swoleympia stage — each with its own soundtrack.
>
> Challenge 8 gym rivals in arm-wrestling, perfect-form, hold-the-weight and pose-off minigames to win titles and
> cosmetics. When you're huge, hit the stage: pose for three judges, earn trophies and spend them on permanent perks.
>
> • 15 tappable muscles, front and back, with 35 animated exercises
> • 37 pieces of gear, 59 upgrades and item milestones
> • Beast Mode, gym events and golden shakes
> • 8 rivals and 4 minigames
> • Prestige with a judged posing show and 14 trophy perks
> • 90 awards, daily quests and login streaks
> • 5 gyms with their own music, plus a locker full of silly cosmetics
> • No ads, no account, plays offline

**Keywords** (99/100 chars):
`idle,clicker,gym,muscle,bodybuilding,workout,tap,incremental,lifting,gains,fitness,flex,tapper,pump`

**Support URL:** https://calamborn-maker.github.io/swole-clicker/support.html
**Marketing URL** (optional): https://calamborn-maker.github.io/swole-clicker/
**Privacy Policy URL:** https://calamborn-maker.github.io/swole-clicker/privacy-policy.html
**Copyright:** `2026 Dumped`

## 4. Screenshots
iPhone **6.9" Display** — upload all six from `assets/appstore/iphone-6.9/` (1320×2868), in order:
`01-train-any-muscle`, `02-beast-mode`, `03-back-day`, `04-rivals`, `05-swoleympia-stage`, `06-gear-and-milestones`.
(App Store Connect scales these down for the smaller iPhone sizes. No iPad screenshots needed — the app is iPhone-only.)

## 5. Other App Store Connect sections
- **Category:** Games → primary **Casual**, secondary **Simulation**
- **Age rating questionnaire:** answer **None / No** to everything → **4+**
- **App Privacy:** "Do you or your third-party partners collect data from this app?" → **No** (*Data Not Collected*)
- **Pricing & Availability:** Free, all countries
- **Encryption:** already declared in the app (`ITSAppUsesNonExemptEncryption = NO`) — no questions to answer
- **Version 1.0 → Build:** pick the build you uploaded (appears ~10–30 min after upload)
- **App Review notes:**
  > Single-player idle game. No login, no ads, no in-app purchases, no network required. Tap any muscle on the character to
  > train it; tabs on the lower half of the screen open the shop, upgrades, rivals and more.

Then **Add for Review ▸ Submit**.

## Updating later
1. Change the game in `index.html` (it's the same game as the website/CrazyGames).
2. `python3 tools/build.py ios` — copies it into `ios/SwoleClicker/Web/index.html`.
3. Bump **Version**/**Build** (in `ios/project.yml`: `MARKETING_VERSION`, `CURRENT_PROJECT_VERSION`, then run `xcodegen` in `ios/`,
   or change them in Xcode's target settings) → Archive → Upload.

## What's in the app (for reference)
- `ios/SwoleClicker/GameView.swift` — full-screen WKWebView serving the bundled game from `swole://game/` (so saves persist),
  native haptics, iOS share sheet, external links open in Safari, crash recovery.
- `ios/SwoleClicker/SwoleClickerApp.swift` — SwiftUI app; ambient audio (respects the silent switch, mixes with music),
  hidden status bar / home indicator.
- `ios/SwoleClicker/PrivacyInfo.xcprivacy` — no tracking, no data collected.
- The game detects the app (`window.__SWOLE_APP__`) → no ads, local saves, safe-area padding.
