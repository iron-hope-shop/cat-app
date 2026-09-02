# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2026-08-31

### Added
- Standalone iPad native project (`Quarry.xcodeproj`) built with SwiftUI and custom `CatGameViewController`.
- Cat-proofing iOS features:
  - System edge gesture deferral (`preferredScreenEdgesDeferringSystemGestures = .all`) to prevent accidental paw-swipe exits.
  - Auto-hidden home indicator (`prefersHomeIndicatorAutoHidden = true`).
  - Full-screen kiosk layout (`UIRequiresFullScreen = YES`, `prefersStatusBarHidden = true`).
  - Disabled WKWebView bounce, zoom, text selection, and gesture popups.
  - Ambient audio session configuration for seamless sound effects.
- Standalone PWA manifest and service worker for offline / Home Screen WebClip capability.
- App icons and asset catalog for iPad Pro and iOS displays.
- Local bundled web app in `Quarry/www/` with touch-hardened event listeners and offline font fallbacks.
- Instant local server launcher `serve.py` with automatic LAN IP resolution and error logging.

### Fixed
- Restored vertical touch scrolling on Home and Setup screens while preserving 100% swipe locking during active hunting sessions (`body.in-play`).

## [1.1.0] - 2026-08-31

### Changed
- Rebranded app to **cat-app** across titles, manifest, icons, metadata, Info.plist, and export filenames.
- Optimized iPad home screen layout:
  - Responsive side-by-side dashboard layout (`.home-layout`) for tablet displays in landscape & portrait.
  - Sticky primary column with live preview window and prominent "Start the hunt" CTA button.
  - Enlarged tactile specimen chips and settings controls with \(\ge 48\text{px}\) touch targets.
  - Dynamic canvas re-rendering on iPad orientation changes.

## [1.2.0] - 2026-08-31

### Changed
- Rebuilt the setup screen as a two-column panel sized to the iPad display: brand, live specimen window and Start button on the left; quarry picker and session settings on the right.
- The specimen window is now sized by the layout instead of a fixed pixel height, so it absorbs whatever vertical space is left over.
- In landscape the panel is pinned to the viewport height; in portrait it takes its natural height so the reading material meets the fold instead of leaving a dead gap.
- Settings rows stack their label above the segmented control when the column is too narrow to hold both on one line (iPad portrait).
- "Before you start" and the disclosures moved below the panel into a two-column reading section.

### Fixed
- Specimen and preview canvases are re-cut via `ResizeObserver` and `document.fonts.ready`, so they stay sharp after webfont load, rotation and Split View resizes.

## [1.3.0] - 2026-08-31

### Added
- Four new quarry: **Ant**, **Butterfly**, **Shrimp**, and **Jellyfish**, each with its own draw routine and movement temperament, in the same `SPECIES` table as the originals.
- **Backdrop** setting (Den / Underwater / Meadow / Nightfall) that retints the ground, the hiding tufts, and the drifting debris. Underwater rises as bubbles, Meadow drifts as petals, and Nightfall spins slowly as embers — Den keeps the original static leaves, undisturbed until a paw lands nearby.
- **Visual filter** setting (Underwater / Thermal / Dream), layered over the live field via new SVG filters (`#underwater`, `#thermal`, `#dream`) — separate from the existing Cat vision toggle, which stays a dedicated simulation of feline colour perception.
- Debris now drifts continuously on its own for every backdrop but Den, rather than only reacting to a paw.

## [1.7.1] - 2026-09-01

### Fixed
- Removed untracked runtime `error.log` requirement from unit test assertions so GitHub Actions CI tests pass cleanly in fresh checkout environments.
- Added graceful `swiftc` presence check in test suite for cross-platform CI runner compatibility.

## [1.7.0] - 2026-09-01

### Added
- Production Docker containerization (`Dockerfile` & `nginx.conf`) with HTTP/2, gzip compression, and PWA cache control headers.
- GitHub Actions CI/CD workflow (`.github/workflows/deploy.yml`) to automatically test, build, and deploy container images to Google Cloud Artifact Registry and Cloud Run.
- One-click GCP provisioning script (`scripts/setup_gcp_cicd.sh`) to enable services, create Artifact Registry repositories, and configure IAM service accounts.

## [1.6.0] - 2026-09-01

### Added
- Automated PWA force-update lifecycle:
  - Client automatically calls `registration.update()` upon app start, `visibilitychange` (bringing iPad app to foreground), and `pageshow`.
  - Service worker `skipWaiting` / `controllerchange` auto-reload automatically activates updated game builds without requiring manual browser cache clearing.
  - HTTP `Cache-Control: no-cache, no-store, must-revalidate` headers in `serve.py` for `sw.js` and manifests prevent stale proxy/browser caching.

### Changed
- Replaced unaccelerated CPU-bottlenecked SVG `<filter>` implementations with GPU-accelerated Metal/WebKit CSS filter pipelines (`hue-rotate`, `saturate`, `contrast`, `invert`, `drop-shadow`).
- Restored full Retina native resolution and smooth 60/120 FPS performance across Underwater, Thermal, and Dream visual modes with zero frame drops or pixelation.

## [1.5.0] - 2026-09-01

### Added
- Four new stimulating quarry types:
  - **Snake**: Sinusoidal S-curve slither, tapered scale spine, viper head, and an animated flicking forked tongue with explosive lunges.
  - **Lizard**: Fast scampering gecko with 4 splayed paddling feet and whipping tail that darts and freezes flat.
  - **Laser**: High-speed radiant bouncing dot leaving luminous light ribbons.
  - **Frog**: Crouch-and-launch springy leaps with webbed feet and throat sac pulses.
- Anti-boredom engine & attention recovery:
  - Fast idle recovery trigger at 7 seconds of inactivity.
  - **Wand Teaser**: A glowing decoy/feather streak swoops across the screen to snap attention back to the hunt.
  - **Curiosity Audio Lures**: Feline-calibrated high-frequency chirps (5.8–6.4 kHz) and scamper clicks that call the cat back to the screen.
  - **Frenzy Swarm**: Toggleable companion mini critters that scatter across the field and pop points when caught.

## [1.4.0] - 2026-09-01

### Fixed
- Setup screen no longer shoves **Start the hunt** below the fold on iPad: the dashboard is pinned to the viewport and the quarry/settings column scrolls on its own.
- Starting a hunt no longer waits on the fullscreen permission prompt, so the field can appear as a black empty screen.
- Native WKWebView scrolling is enabled on Home/Setup so the panel and reading material stay reachable.

### Changed
- Dropped the Google Fonts network dependency so the game can load with no internet.
- Service worker precaches each local asset individually (a single 404 no longer blocks install) and only falls back to `index.html` for navigations.
- Local server is threaded, ignores dropped iPad connections, serves HTTPS on port 8443 so iPad Safari can register the PWA, and accepts `POST /log` for client exceptions.
