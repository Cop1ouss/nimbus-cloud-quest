import json,sys
from playwright.sync_api import sync_playwright
F='file://'+__import__('os').path.abspath('index.html')+''
pk=json.load(open('src/data_packs.json'))['packs']['az900'];C=pk['campaign']['cards'];byq={q['q']:q for q in pk['questions'] if 'opts' in q}
errs=[]
def answer_check(pg,right=True):
    import re
    head=re.split(r' choose',pg.inner_text('.cq'),flags=re.I)[0].strip()
    q=byq.get(head) or [v for k,v in byq.items() if k.startswith(head)][0]
    opts=[o.inner_text().strip() for o in pg.query_selector_all('.copt')];want=[q['opts'][i].strip() for i in q['ans']]
    idx=[i for i,t in enumerate(opts) if t in want] if right else [i for i,t in enumerate(opts) if t not in want][:len(q['ans'])]
    for i in idx: pg.click('[data-act="canswer:%d"]'%i);pg.wait_for_timeout(20)
    pg.click('[data-act=ccont]');pg.wait_for_timeout(30)
def turn(pg,right=True,shots=None):
    for _ in range(8):
        if not pg.query_selector('.hand'): return
        intent=pg.inner_text('.intent');cards=pg.query_selector_all('.ccard');names=[c.inner_text().split('\n') for c in cards]
        cr=int(pg.inner_text('.me').split('Credits')[1].split()[0])
        best=None
        for i,c in enumerate(pg.query_selector_all('.ccard')):
            nm=[k for k,v in C.items() if v['n'] in c.inner_text()][0];cd=C[nm]
            if cd['cost']>cr: continue
            score=(5 if any(pk['campaign']['threats'][t]['n'] in intent for t in cd.get('counters',[])+cd.get('guard',[])) else 0)+(2 if cd['kind']=='deploy' else 0)+1
            if best is None or score>best[0]: best=(score,i)
        if best is None: break
        hot=pg.query_selector_all('.lane')
        if hot:
            for zi,ln in enumerate(hot):
                if 'hot' not in (ln.get_attribute('class') or ''): pg.click('[data-act="clane:%d"]'%zi);pg.wait_for_timeout(15);break
        pg.click('[data-act="cplay:%d"]'%best[1]);pg.wait_for_timeout(40)
        if pg.query_selector('.cmodal'):
            if shots is not None and 'check' not in shots: pg.screenshot(path='v24_check.png');shots.add('check')
            answer_check(pg,right)
    if shots is not None and 'battle' not in shots: pg.screenshot(path='v24_battle.png',full_page=True);shots.add('battle')
    if pg.query_selector('[data-act=cend]'): pg.click('[data-act=cend]');pg.wait_for_timeout(50)
def play_level(pg,n,right=True,shots=None):
    pg.click('[data-act="camp:%d"]'%n);pg.wait_for_timeout(100);t=0
    while pg.query_selector('[data-act=cend]') and t<40: turn(pg,right,shots);t+=1
    return pg.inner_text('.camp'),t

with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':390,'height':850});pg=ctx.new_page();pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
    pg.goto(F);pg.wait_for_timeout(300);pg.click('nav [data-tab=play]');pg.click('[data-act=campmap]');pg.wait_for_timeout(100)
    for n in range(1,41):
        pg.click('[data-act=campmap]') if pg.query_selector('[data-act=campmap]') else None;pg.wait_for_timeout(40)
        L=[l for l in pk['campaign']['levels'] if l['id']==n][0]
        pg.click('[data-act="cworld:%d"]'%L['world']);pg.wait_for_timeout(30)
        shots=set() if n in (11,26,31,40) else None
        txt,t=play_level(pg,n,True,shots)
        if shots is not None:
            import shutil
            for k in ('battle','check'):
                try: shutil.move('v24_%s.png'%k,'w%d_%s.png'%(n,k))
                except Exception: pass
        res=txt.split('\n');print(n,L['n'][:22].ljust(22),'WIN' if 'secured' in txt else 'LOSS',[r for r in res if 'Uptime left' in r][:1],'turns',t,flush=True)
        if 'secured' not in txt:
            pg.click('[data-act="camp:%d"]'%n) if False else None
            break
    pg.click('[data-act=campmap]');pg.wait_for_timeout(50);pg.click('[data-act="cworld:2"]');pg.wait_for_timeout(50);pg.screenshot(path='w_map.png',full_page=True)
    b.close()
print('ERRORS',errs)
