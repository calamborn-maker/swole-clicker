# Swole Clicker — Publishing Guide

One self-contained `index.html` runs everywhere. `PLATFORM` is detected at runtime:

| Where it runs | PLATFORM | Saves | Ads |
|---|---|---|---|
| `localhost` / `file://` | `dev` | localStorage | simulated (1 s overlay) |
| GitHub Pages / Netlify / itch | `selfhost` | localStorage | none |
| GameDistribution domains | `gamedistribution` | localStorage | GD SDK (set `GD_GAME_ID`) |
| anything else (CrazyGames) | `crazygames` | CrazyGames Data module (cloud), falls back to localStorage | CrazyGames SDK v3 |

If the CrazyGames SDK reports `environment === 'disabled'` (not actually on CrazyGames), the game behaves like `selfhost`.

---

## CrazyGames (primary)

### Build
```
python3 tools/build-crazygames.py
```
Produces `dist/crazygames/` and `swole-clicker-crazygames.zip` (index.html + privacy-policy.html, ~80 KB),
with the GitHub-Pages-only SEO/social tags stripped. Upload the zip.

### What's integrated (SDK v3 — https://docs.crazygames.com/sdk/intro/)
- Loads `https://sdk.crazygames.com/crazygames-sdk-v3.js`, `await SDK.init()`, checks `SDK.environment`.
- `loadingStart()` after init → `loadingStop()` + first `gameplayStart()` when the game is ready.
- `gameplayStop()/gameplayStart()` around every modal, ad, rival minigame and the posing show (deduplicated so they always alternate).
- Rewarded ads (`requestAd('rewarded')`), user-initiated only: 2× offline earnings, 7× frenzy, protein windfall, 2× quest reward, 2× rival reward.
- Midgame ads (`requestAd('midgame')`) only at natural breaks — after hitting the stage and after the offline-earnings popup — with a 3-minute client cooldown.
- Every ad pauses the game loop and mutes all audio (music + SFX), resuming on `adFinished` **and** `adError`. The game works fully with an ad blocker.
- Cloud saves through the Data module (`SDK.data.getItem/setItem`).
- Logged-in player's username + avatar shown in the header (User module), updated on login.
- `happytime()` on first win against each rival and on hitting the stage.
- No external links in-game except the privacy policy; social share buttons are hidden on portals (copy-link uses `SDK.game.inviteLink`).
- Desktop/landscape layout fits the window from 800×450 to 1920×1080 with no page scrolling; portrait phones get a stacked layout.
- Content kept PEGI 12: no drugs or tobacco (the serum items and the chew straw replaced steroids/cigar), no real trademarks ("Swoleympia").

### Assets (`assets/crazygames/`)
| File | Spec |
|---|---|
| `cover-landscape-1920x1080.png` | 16:9 cover, title text only |
| `cover-portrait-800x1200.png` | 2:3 cover, title text only |
| `cover-square-800x800.png` | 1:1 cover, title text only |
| `video-landscape-1920x1080.mp4` | 19.9 s, silent, H.264, cover as the first second |
| `video-portrait-1080x1620.mp4` | 20 s, silent, H.264, cover as the first second |

Covers are drawn from the game itself by `tools/preview.html` (serve the repo over http and open it).
Store text (title, descriptions, controls, tags) is in `LISTING.md`.

### Submission checklist
1. Create a developer account at https://developer.crazygames.com and fill in payout/tax details.
2. New game → upload `swole-clicker-crazygames.zip` (HTML5, entry `index.html`).
3. Use the portal's preview/QA mode to check: ads show and pause/mute the game, the username badge appears when logged in, progress survives a reload.
4. Add covers, videos and the text from `LISTING.md`. Orientation: landscape (also works in portrait on mobile).
5. Submit for Basic Launch review.

---

## GameDistribution (secondary)
- Paste your game id into `const GD_GAME_ID='...'` in `index.html`, and enable "Rewarded Ads" for the game in the GD portal.
- GD domains are auto-detected (`PLATFORM='gamedistribution'`).
- Assets GD asks for: 512×512 icon (`assets/icon-512.png`), 1280×720 cover (`assets/cover-1280x720.png`), title, descriptions, category, controls.

## Self-hosting (GitHub Pages)
`main` is published at https://calamborn-maker.github.io/swole-clicker/ — no ads, localStorage saves, social share card `preview.png`.
