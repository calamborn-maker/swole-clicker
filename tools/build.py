#!/usr/bin/env python3
"""Build the single-file game for a store.

  python3 tools/build.py crazygames   → dist/crazygames/ + swole-clicker-crazygames.zip
  python3 tools/build.py ios          → ios/SwoleClicker/Web/index.html (bundled into the iOS app)

Both builds drop the website-only SEO/social tags (canonical, Open Graph, Twitter, JSON-LD) and inline the
privacy policy as a <template> so Settings → Privacy Policy opens in-game (CrazyGames accepts one HTML file;
the iOS app should not navigate away). PLATFORM is detected at runtime, so the game code is identical.
"""
import os, re, shutil, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def single_file_html():
    html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    html = re.sub(r'\s*<link rel="canonical"[^>]*>', '', html)
    html = re.sub(r'\s*<meta (?:property="og:|name="twitter:)[^>]*>', '', html)
    html = re.sub(r'\s*<!-- Open Graph / social preview -->', '', html)
    html = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', '', html, flags=re.S)
    pol = open(os.path.join(ROOT, 'privacy-policy.html'), encoding='utf-8').read()
    body = re.search(r'<body>(.*)</body>', pol, re.S).group(1)
    html = html.replace('</body>', '<template id="privacytpl">' + body + '</template>\n</body>', 1)
    assert 'https://calamborn-maker.github.io/swole-clicker/"' not in html.split('<script>', 1)[0], 'SEO tags should be gone'
    return html


def build_crazygames():
    html = single_file_html()
    assert 'crazygames-sdk-v3.js' in html, 'expected the CrazyGames v3 SDK loader in index.html'
    dist = os.path.join(ROOT, 'dist', 'crazygames')
    zpath = os.path.join(ROOT, 'swole-clicker-crazygames.zip')
    shutil.rmtree(dist, ignore_errors=True)
    os.makedirs(dist)
    open(os.path.join(dist, 'index.html'), 'w', encoding='utf-8').write(html)
    shutil.copy(os.path.join(ROOT, 'privacy-policy.html'), dist)
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for name in sorted(os.listdir(dist)):
            z.write(os.path.join(dist, name), name)   # files at the zip root, index.html as the entry point
    print(f'built dist/crazygames/ and {os.path.basename(zpath)} ({os.path.getsize(zpath)/1024:.0f} KB) — upload dist/crazygames/index.html')


def build_ios():
    web = os.path.join(ROOT, 'ios', 'SwoleClicker', 'Web')
    os.makedirs(web, exist_ok=True)
    open(os.path.join(web, 'index.html'), 'w', encoding='utf-8').write(single_file_html())
    print('built ios/SwoleClicker/Web/index.html — now open ios/SwoleClicker.xcodeproj (run `xcodegen` in ios/ first if project.yml changed)')


if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else ''
    {'crazygames': build_crazygames, 'ios': build_ios}.get(target, lambda: sys.exit(__doc__))()
