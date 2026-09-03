import os
import json
import re
import subprocess
import unittest

class TestQuarryStandaloneApp(unittest.TestCase):
    def test_inline_script_parses(self):
        """The whole app is one inline IIFE, so a single syntax error silently
        kills every listener on the page while the static HTML still renders."""
        import shutil
        import tempfile
        if not shutil.which('node'):
            self.skipTest("node not available in environment")
        pattern = re.compile(r'<script>\s*\n\(function\(\)\{.*?\n\}\)\(\);\s*\n</script>', re.S)
        for path in ['quarry.html', 'Quarry/www/index.html']:
            with open(path, 'r', encoding='utf-8') as f:
                src = f.read()
            match = pattern.search(src)
            self.assertIsNotNone(match, f"{path}: could not locate the main inline script")
            body = match.group(0)[len('<script>'):-len('</script>')]
            with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False,
                                             encoding='utf-8') as tmp:
                tmp.write(body)
                tmp_path = tmp.name
            try:
                res = subprocess.run(['node', '--check', tmp_path],
                                     capture_output=True, text=True)
                self.assertEqual(res.returncode, 0,
                                 f"{path}: inline script syntax error:\n{res.stderr}")
            finally:
                os.unlink(tmp_path)

    def test_no_listeners_on_missing_elements(self):
        """An unguarded getElementById(...).addEventListener on a removed element
        throws at load and kills every statement after it in the IIFE, which is
        what silently broke the login gate. Every id wired this way must exist."""
        pattern = re.compile(r'document\.getElementById\("([^"]+)"\)\s*\.\s*addEventListener')
        for path in ['quarry.html', 'Quarry/www/index.html']:
            with open(path, 'r', encoding='utf-8') as f:
                src = f.read()
            wired = set(pattern.findall(src))
            self.assertTrue(wired, f"No wired element ids found in {path}")
            for el_id in sorted(wired):
                self.assertIn(f'id="{el_id}"', src,
                              f'{path}: addEventListener on missing element id "{el_id}"')

    def test_prelogin_gate_is_login_only(self):
        """Pre-login shows the living critter canvas plus sign-in only. Mascot name
        cards and the PWA/science entry points belong to the post-login help flow."""
        for path in ['quarry.html', 'Quarry/www/index.html']:
            with open(path, 'r', encoding='utf-8') as f:
                src = f.read()
            for gone in ('splashScreen', 'splash-critter-card', 'splashEnterBtn',
                         'splashInstallBtn', 'Learn Science & Install PWA'):
                self.assertNotIn(gone, src, f'{path}: pre-login splash remnant "{gone}"')
            self.assertIn('authBgCanvas', src)
            self.assertIn('settingsInstallPwaBtn', src)
            self.assertIn('settingsReplayCourseBtn', src)

    def test_files_exist(self):
        required_files = [
            'quarry.html',
            'CHANGELOG.md',
            'Quarry.xcodeproj/project.pbxproj',
            'Quarry/QuarryApp.swift',
            'Quarry/ContentView.swift',
            'Quarry/CatGameViewController.swift',
            'Quarry/Info.plist',
            'Quarry/Assets.xcassets/Contents.json',
            'Quarry/Assets.xcassets/AppIcon.appiconset/Contents.json',
            'Quarry/Assets.xcassets/AccentColor.colorset/Contents.json',
            'Quarry/www/index.html',
            'Quarry/www/manifest.webmanifest',
            'Quarry/www/sw.js',
            'Quarry/www/icon-192.png',
            'Quarry/www/icon-512.png',
            'Quarry/www/apple-touch-icon.png',
            'Quarry/www/favicon.ico',
            'serve.py',
            'Dockerfile',
            'nginx.conf',
            '.github/workflows/deploy.yml',
            'scripts/setup_gcp_cicd.sh'
        ]
        for path in required_files:
            self.assertTrue(os.path.exists(path), f"Missing file: {path}")

    def test_swift_syntax(self):
        import shutil
        if not shutil.which('swiftc'):
            self.skipTest("swiftc not available in environment")
        res = subprocess.run([
            'swiftc', '-parse',
            'Quarry/QuarryApp.swift',
            'Quarry/ContentView.swift',
            'Quarry/CatGameViewController.swift'
        ], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Swift parse failed: {res.stderr}")

    def test_manifest_json(self):
        with open('Quarry/www/manifest.webmanifest', 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(data.get('display'), 'standalone')
        self.assertEqual(data.get('short_name'), 'cat-app')
        self.assertEqual(data.get('start_url'), './')
        self.assertIn('fullscreen', data.get('display_override', []))
        self.assertTrue(len(data.get('icons', [])) >= 2)

    def test_html_cat_proofing_and_ipad_layout(self):
        for path in ['quarry.html', 'Quarry/www/index.html']:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.assertIn('viewport-fit=cover', content)
            self.assertIn('apple-mobile-web-app-capable', content)
            self.assertIn('cat-app', content)
            for hook in ('home-app', 'home-primary', 'home-controls', 'home-extra'):
                self.assertIn(hook, content, f"{hook} missing from {path}")
            self.assertIn('grid-template-areas', content)
            self.assertIn('100dvh', content)
            self.assertIn('-webkit-touch-callout:none', content.replace(' ', ''))
            self.assertIn('gesturestart', content)
            self.assertIn('user-scalable=no', content)
            self.assertNotIn('fonts.googleapis.com', content)
            self.assertIn('overflow-y:auto', content.replace(' ', ''))
            self.assertIn('max-height:calc(100dvh', content.replace(' ', ''))
            self.assertIn('requestFullscreen().catch', content.replace(' ', ''))
            self.assertNotIn('async function startGame', content)
            self.assertIn('build-tag', content)
            self.assertIn('gateGoogleBtn', content)
            self.assertIn('authGate', content)
            self.assertIn('authBgCanvas', content)
            self.assertIn('FIREBASE_CONFIG', content)
            self.assertIn('data-min="0"', content)
            self.assertIn('settingsScreen', content)
            self.assertIn('openHelpBtn', content)
            self.assertIn('openSettingsBtn', content)
            self.assertIn('tabMobile', content)
            self.assertIn('tabTablet', content)
            self.assertIn('tabWorkstation', content)

    def test_service_worker_offline(self):
        with open('Quarry/www/sw.js', 'r', encoding='utf-8') as f:
            sw = f.read()
        self.assertIn("CACHE_NAME = 'cat-app-v23'", sw)
        self.assertIn('cache.add(url)', sw)
        self.assertNotIn('cache.addAll', sw)
        self.assertIn("request.mode === 'navigate'", sw)
        self.assertIn('self.skipWaiting()', sw)
        self.assertIn('clients.claim()', sw)
        self.assertIn('skipWaiting', sw)

    def test_species_and_anti_boredom_features(self):
        for path in ['quarry.html', 'Quarry/www/index.html']:
            with open(path, 'r', encoding='utf-8') as f:
                src = f.read()
            for sp in ('snake', 'lizard', 'laser', 'frog', 'beetle', 'mouse', 'spider'):
                self.assertIn(f'{sp}:', src, f"{sp} species missing from {path}")
            self.assertIn('drawSnake', src)
            self.assertIn('drawSnakeTrail', src)
            self.assertIn('drawLizard', src)
            self.assertIn('drawLaser', src)
            self.assertIn('drawFrog', src)
            self.assertIn('wandTeaser', src)
            self.assertIn('frenzy', src)
            self.assertIn('curiosityChirp', src)

    def test_server_pwa_https_and_logging(self):
        with open('serve.py', 'r', encoding='utf-8') as f:
            src = f.read()
        self.assertIn('ThreadingMixIn', src)
        self.assertIn('TLS_PORT', src)
        self.assertIn("'/log'", src)
        self.assertIn('ensure_tls_cert', src)

    def test_native_home_scrolls(self):
        with open('Quarry/CatGameViewController.swift', 'r', encoding='utf-8') as f:
            src = f.read()
        self.assertIn('isScrollEnabled = true', src)
        self.assertNotIn('isScrollEnabled = false', src)

    def test_icons_integrity(self):
        # Verify all PNG files start with standard PNG header
        png_files = [
            'Quarry/www/icon-192.png',
            'Quarry/www/icon-512.png',
            'Quarry/www/apple-touch-icon.png',
            'Quarry/Assets.xcassets/AppIcon.appiconset/AppIcon-1024.png',
            'Quarry/Assets.xcassets/AppIcon.appiconset/AppIcon-167.png',
            'Quarry/Assets.xcassets/AppIcon.appiconset/AppIcon-152.png',
            'Quarry/Assets.xcassets/AppIcon.appiconset/AppIcon-120.png'
        ]
        png_header = b'\x89PNG\r\n\x1a\n'
        for p in png_files:
            self.assertTrue(os.path.exists(p), f"Icon not found: {p}")
            with open(p, 'rb') as f:
                header = f.read(8)
                self.assertEqual(header, png_header, f"Invalid PNG header for {p}")

    def test_pbxproj_references(self):
        with open('Quarry.xcodeproj/project.pbxproj', 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('QuarryApp.swift', content)
        self.assertIn('ContentView.swift', content)
        self.assertIn('CatGameViewController.swift', content)
        self.assertIn('Assets.xcassets', content)
        self.assertIn('www', content)
        self.assertIn('PRODUCT_BUNDLE_IDENTIFIER = com.quarry.catgame', content)

    def test_idm_design_system_tokens(self):
        """Verify semantic IDM tokens for surfaces, borders, text, and shadows."""
        idm_tokens = [
            '--idm-bg-base',
            '--idm-bg-surface',
            '--idm-bg-subtle',
            '--idm-bg-hover',
            '--idm-border',
            '--idm-border-subtle',
            '--idm-border-focus',
            '--idm-border-accent',
            '--idm-text-primary',
            '--idm-text-secondary',
            '--idm-text-accent',
            '--idm-text-inverse',
            '--idm-shadow-sm',
            '--idm-shadow-md',
            '--idm-shadow-lg',
            '--idm-shadow-modal'
        ]
        for path in ['quarry.html', 'Quarry/www/index.html']:
            with open(path, 'r', encoding='utf-8') as f:
                src = f.read()
            for token in idm_tokens:
                self.assertIn(token, src, f"Missing IDM token {token} in {path}")

    def test_scorm_onboarding_enforcement(self):
        """Verify mandatory 5-module SCORM curriculum, modal styling, localStorage key, and settings replay."""
        for path in ['quarry.html', 'Quarry/www/index.html']:
            with open(path, 'r', encoding='utf-8') as f:
                src = f.read()
            # Modal hidden by default until .open is applied
            self.assertIn('.onboarding-modal{', src)
            self.assertIn('display:none;', src.replace(' ', ''))
            self.assertIn('.onboarding-modal.open{display:flex', src.replace(' ', '').replace('\n', ''))
            # 5 modules
            for i in range(1, 6):
                self.assertIn(f'id="onboardStep{i}"', src, f"Missing onboardStep{i} in {path}")
            # SCORM tracking key
            self.assertIn('cat_app_onboarded_scorm_v1', src, f"Missing SCORM v1 key in {path}")
            # Start Course button in App Settings
            self.assertIn('settingsReplayCourseBtn', src, f"Missing replay button in {path}")
            self.assertIn('>Start Course</button>', src, f"Missing 'Start Course' label in {path}")

    def test_html_files_identical(self):
        """quarry.html and Quarry/www/index.html must be identical."""
        with open('quarry.html', 'r', encoding='utf-8') as f:
            quarry_src = f.read()
        with open('Quarry/www/index.html', 'r', encoding='utf-8') as f:
            www_src = f.read()
        self.assertEqual(quarry_src, www_src, "quarry.html and Quarry/www/index.html differ")

if __name__ == '__main__':
    unittest.main()
