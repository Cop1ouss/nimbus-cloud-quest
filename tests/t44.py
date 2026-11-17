# Cloud Clash for SC-900, AZ-104 and SC-500: a bot plays every level with right answers.
# Checks: every level winnable, saves are per cert, AZ-900 campaign save untouched, modes unlock.
# Run from the repo root: python3 tests/t44.py [cert ...]
import json, re, sys, os
from playwright.sync_api import sync_playwright
F = 'file://' + os.path.abspath('index.html')
PACKS = json.load(open('src/data_packs.json'))['packs']
CERTS = sys.argv[1:] or ['sc900', 'az104', 'sc500']
errs = []

def answer(pg, byq):
    head = re.split(r' choose', pg.inner_text('.cq'), flags=re.I)[0].strip()
    q = byq.get(head) or [v for k, v in byq.items() if k.startswith(head)][0]
    opts = [o.inner_text().strip() for o in pg.query_selector_all('.copt')]
    want = [q['opts'][i].strip() for i in q['ans']]
    for i, t in enumerate(opts):
        if t in want: pg.click('[data-act="canswer:%d"]' % i); pg.wait_for_timeout(15)
    pg.click('[data-act=ccont]'); pg.wait_for_timeout(25)

def turn(pg, C, T, byq):
    for _ in range(8):
        if not pg.query_selector('.hand'): return
        intent = pg.inner_text('.intent'); cr = int(pg.inner_text('.me').split('Credits')[1].split()[0]); best = None
        for i, c in enumerate(pg.query_selector_all('.ccard')):
            txt = c.inner_text(); k = [k for k, v in C.items() if v['n'] in txt][0]; cd = C[k]
            if cd['cost'] > cr: continue
            sc = (5 if any(T[t]['n'] in intent for t in cd.get('counters', [])) else 0) + (2 if cd['kind'] == 'deploy' else 0) + 1
            if best is None or sc > best[0]: best = (sc, i)
        if best is None: break
        pg.click('[data-act="cplay:%d"]' % best[1]); pg.wait_for_timeout(30)
        if pg.query_selector('.cmodal'): answer(pg, byq)
    if pg.query_selector('[data-act=cend]'): pg.click('[data-act=cend]'); pg.wait_for_timeout(40)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 390, 'height': 850})
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
    pg.goto(F); pg.wait_for_timeout(300)
    # AZ-900 player one level short of the CapEx Colossus: that save must survive other campaigns
    pg.evaluate("localStorage.setItem('nimbus_az900',JSON.stringify({camp:{lv:{1:3,2:3,3:3,4:3,5:3,6:3,7:3,8:3,9:2},mast:{}},onboarded:true}))")
    pg.reload(); pg.wait_for_timeout(300)
    for cert in CERTS:
        pk = PACKS[cert]; C = pk['campaign']['cards']; T = pk['campaign']['threats']
        byq = {q['q']: q for q in pk['questions'] if 'opts' in q}
        pg.evaluate("location.hash='certs'"); pg.wait_for_timeout(250); pg.click('[data-act="cert:%s"]' % cert); pg.wait_for_timeout(300)
        pg.click('nav [data-tab=play]'); pg.wait_for_timeout(150); pg.click('[data-act=campmap]'); pg.wait_for_timeout(100)
        assert pg.locator('[data-act=daily][disabled]').count() == 1, 'modes should start locked'
        w1 = max(l['id'] for l in pk['campaign']['levels'] if l['world'] == 1)
        assert 'level %d' % w1 in pg.inner_text('.camp'), 'unlock hint names world 1 boss'
        for L in pk['campaign']['levels']:
            if pg.query_selector('[data-act=campmap]'): pg.click('[data-act=campmap]'); pg.wait_for_timeout(30)
            pg.click('[data-act="cworld:%d"]' % L['world']); pg.wait_for_timeout(25)
            pg.click('[data-act="camp:%d"]' % L['id']); pg.wait_for_timeout(80); t = 0
            assert pg.locator('.lane').count() == 0 and pg.locator('.lay').count() == 0
            while pg.query_selector('[data-act=cend]') and t < 40: turn(pg, C, T, byq); t += 1
            txt = pg.inner_text('.camp'); up = [r for r in txt.split('\n') if 'Uptime left' in r][:1]
            print(cert, L['id'], L['n'][:26].ljust(26), 'WIN' if 'secured' in txt else 'LOSS', up, 'turns', t, flush=True)
            assert 'secured' in txt, (cert, L['id'])
            if L['id'] == w1:
                pg.click('[data-act=campmap]'); pg.wait_for_timeout(40)
                assert pg.locator('[data-act=daily][disabled]').count() == 0, 'modes open after world 1'
    st = pg.evaluate("JSON.parse(localStorage.getItem('nimbus_az900'))")
    assert st['camp']['lv'] == {str(i): (2 if i == 9 else 3) for i in range(1, 10)}, st['camp']['lv']
    for cert in CERTS:
        assert len(st['campx'][cert]['lv']) == len(PACKS[cert]['campaign']['levels']), cert
    b.close()
print('ERRORS', errs); assert not errs
print('t44 ok')
