#!/usr/bin/env python3
"""Build the CrazyGames upload: dist/crazygames/ + swole-clicker-crazygames.zip

The game file is the same everywhere — PLATFORM auto-detects CrazyGames at runtime. This build only
drops the website-only SEO/social tags (canonical, Open Graph, Twitter, JSON-LD) that point at the
GitHub Pages copy, and bundles the privacy policy (linked from Settings).
Run from anywhere:  python3 tools/build-crazygames.py
"""
import os, re, shutil, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, 'dist', 'crazygames')
ZIP = os.path.join(ROOT, 'swole-clicker-crazygames.zip')

html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
html = re.sub(r'\s*<link rel="canonical"[^>]*>', '', html)
html = re.sub(r'\s*<meta (?:property="og:|name="twitter:)[^>]*>', '', html)
html = re.sub(r'\s*<!-- Open Graph / social preview -->', '', html)
html = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', '', html, flags=re.S)
assert 'crazygames-sdk-v3.js' in html, 'expected the CrazyGames v3 SDK loader in index.html'
# CrazyGames takes a single HTML file, so inline the privacy policy (opened from Settings) as a template
pol = open(os.path.join(ROOT, 'privacy-policy.html'), encoding='utf-8').read()
body = re.search(r'<body>(.*)</body>', pol, re.S).group(1)
html = html.replace('</body>', '<template id="privacytpl">' + body + '</template>\n</body>', 1)
assert 'https://calamborn-maker.github.io' not in html, 'portal build should not link to the GitHub Pages site'

shutil.rmtree(DIST, ignore_errors=True)
os.makedirs(DIST)
open(os.path.join(DIST, 'index.html'), 'w', encoding='utf-8').write(html)
shutil.copy(os.path.join(ROOT, 'privacy-policy.html'), DIST)

with zipfile.ZipFile(ZIP, 'w', zipfile.ZIP_DEFLATED) as z:
    for name in sorted(os.listdir(DIST)):
        z.write(os.path.join(DIST, name), name)   # files at the zip root, index.html as the entry point
size = os.path.getsize(ZIP)
print(f'built {os.path.relpath(DIST, ROOT)}/ ({", ".join(sorted(os.listdir(DIST)))}) and {os.path.basename(ZIP)} ({size/1024:.0f} KB)')
