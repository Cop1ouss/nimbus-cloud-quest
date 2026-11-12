# Builds index.html from src/ (head.html + data_packs.json + app.js).
#   python3 build.py           rebuild index.html
#   python3 build.py --check   fail if index.html is out of date (CI)
#   python3 build.py --icons   also redraw icon.svg and the PNG icons (needs Playwright)
import json, re, sys

HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#303446">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Nimbus">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="icon" href="icon-192.png" sizes="192x192">
<link rel="manifest" href="manifest.webmanifest">
'''

head = open('src/head.html', encoding='utf-8').read()
data = json.dumps(json.load(open('src/data_packs.json', encoding='utf-8')), ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
app = open('src/app.js', encoding='utf-8').read()
assert head.startswith('<meta charset="utf-8">') and '__DATA__' in head
out = HEAD + head.replace('__DATA__', data) + '\n<script>\n' + app + '</script>\n'

if '--check' in sys.argv:
    if open('index.html', encoding='utf-8').read() != out:
        sys.exit('index.html is out of date: run python3 build.py and commit it')
    print('index.html is up to date')
else:
    open('index.html', 'w', encoding='utf-8').write(out)
    print('built index.html', len(out), 'bytes')

if '--icons' in sys.argv:
    mark = re.search(r'<svg class="bmark".*?</svg>', head).group(0).replace(' class="bmark"', '').replace(' aria-hidden="true"', '')
    icon = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><rect width="200" height="200" fill="#303446"/><g transform="translate(18 18) scale(.82)">' + mark + '</g></svg>'
    open('icon.svg', 'w', encoding='utf-8').write(icon)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        for n in (180, 192, 512):
            pg.set_viewport_size({'width': n, 'height': n})
            pg.set_content('<style>body{margin:0}body>svg{display:block;width:%dpx;height:%dpx}</style>' % (n, n) + icon)
            pg.wait_for_timeout(300); pg.screenshot(path='icon-%d.png' % n)
        b.close()
    print('drew icons')
