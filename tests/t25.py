import json
from playwright.sync_api import sync_playwright
F='file://'+__import__('os').path.abspath('index.html')+''
D={x['clue']:x for x in json.load(open('src/data_packs.json'))['packs']['az900']['duels']}
def duel(pg,right=True):
    x=D[pg.inner_text('.clue').strip()];want=x['a'] if x['ans']==0 else x['b']
    btns=pg.query_selector_all('.duel .opt');texts=[b.inner_text().strip() for b in btns]
    i=texts.index(want) if right else 1-texts.index(want)
    pg.click('[data-act="duelpick:%d"]'%i)
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':390,'height':850});pg=ctx.new_page();pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
    pg.clock.install();pg.goto(F);pg.wait_for_timeout(300)
    pg.click('nav [data-tab=play]');pg.click('[data-act=duel-go]');pg.wait_for_timeout(150);pg.screenshot(path='v22_rivals.png',full_page=True)
    # win vs imp
    pg.click('[data-act="rival:1"]');pg.wait_for_timeout(150);pg.screenshot(path='v22_duel.png')
    r=0
    while pg.query_selector('.clue') and r<20:
        duel(pg,True);pg.wait_for_timeout(80)
        if r==0: pg.screenshot(path='v22_duel_hit.png')
        pg.click('[data-act=duelnext]');pg.wait_for_timeout(80);r+=1
    pg.wait_for_timeout(900);print('imp:',pg.inner_text('#view')[:90].replace('\n',' '),'rounds',r);pg.screenshot(path='v22_duel_win.png')
    print('next rival btn',bool(pg.query_selector('[data-act="rival:2"]')))
    # lose to phantom via timeouts + wrong
    pg.click('[data-act="rival:2"]');pg.wait_for_timeout(100);pg.click('[data-act=duel-rivals]') if False else None
    pg.click('[data-act=quit]');pg.click('nav [data-tab=play]');pg.click('[data-act=duel-go]');pg.click('[data-act="rival:3"]');pg.wait_for_timeout(100)
    pg.clock.run_for(4500);pg.wait_for_timeout(100);print('timeout msg:', 'was faster' in pg.inner_text('#view'));pg.screenshot(path='v22_duel_slow.png')
    n=0
    while pg.query_selector('[data-act=duelnext]') and n<10:
        pg.click('[data-act=duelnext]');pg.wait_for_timeout(60)
        if pg.query_selector('.clue'): duel(pg,False);pg.wait_for_timeout(60)
        n+=1
    pg.wait_for_timeout(600);print('phantom:',pg.inner_text('#view')[:80].replace('\n',' '))
    st=json.loads(pg.evaluate("localStorage.getItem('nimbus_az900')"));print('rivals state',st.get('rivals'))
    # practice
    pg.click('[data-act=duel-rivals]');pg.click('[data-act="rival:0"]');pg.wait_for_timeout(100);print('practice has timer:',bool(pg.query_selector('#dtbar')),pg.inner_text('#view')[:30].replace('\n',' '))
    for i in range(10):
        duel(pg,True);pg.click('[data-act=duelnext]');pg.wait_for_timeout(40)
    print('practice end:',pg.inner_text('#view')[:60].replace('\n',' '))
    ctx.close()
    # boss art gallery
    ctx=b.new_context(viewport={'width':390,'height':850});pg=ctx.new_page();pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(F);pg.wait_for_timeout(300);pg.click('nav [data-tab=play]');pg.wait_for_timeout(200)
    el=pg.query_selector('.tiers');pg.evaluate("document.querySelectorAll('.tiers')[0].scrollIntoView()");pg.wait_for_timeout(200);pg.screenshot(path='v22_bosses.png')
    pg.click('[data-act="boss:2:2"]');pg.wait_for_timeout(1000);pg.screenshot(path='v22_hydra.png')
    pg.click('[data-act=quit]');pg.click('nav [data-tab=play]');pg.click('[data-act="boss:3:3"]');pg.wait_for_timeout(1000);pg.screenshot(path='v22_warden.png')
    b.close()
print('ERRORS',errs)
