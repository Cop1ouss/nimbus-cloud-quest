import json,re
exec(open('t30.py').read().split('with sync_playwright() as p:')[0])
seed={"v":4,"camp":{"lv":{str(i):3 for i in range(1,11)},"mast":{"vm":12,"payg":4},"cash":300}}
def st(pg): return json.loads(pg.evaluate("localStorage.getItem('nimbus_az900')"))
with sync_playwright() as p:
    b=p.chromium.launch();ctx=b.new_context(viewport={'width':390,'height':900});pg=ctx.new_page()
    pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
    pg.goto(F);pg.wait_for_timeout(300);pg.evaluate("s=>localStorage.setItem('nimbus_az900',s)",json.dumps(seed));pg.reload();pg.wait_for_timeout(400);pg.screenshot(path='v26_hub.png',full_page=True)
    print('hub tiles:',[t.inner_text().split('\n')[0] for t in pg.query_selector_all('.tile')],'daily enabled:',not pg.is_disabled('.tile[data-act=daily]'))
    print('header icons svg:',pg.evaluate("!!document.querySelector('#pSound svg')&&!!document.querySelector('#pStreak svg')"))
    pg.click('nav [data-tab=play]');pg.click('[data-act=campmap]');pg.wait_for_timeout(100);pg.screenshot(path='v26_map.png')
    pg.click('[data-act="cview:shop"]');pg.wait_for_timeout(100);pg.screenshot(path='v26_shop.png',full_page=True)
    pg.click('[data-act="buy:perk:sla"]');pg.wait_for_timeout(80);pg.click('[data-act="buy:up:vm"]');pg.wait_for_timeout(80)
    s=st(pg)['camp'];print('after buys cash',s['cash'],'perks',s['perks'],'up',s['up'])
    pg.click('[data-act=campmap]');pg.click('[data-act="cview:coll"]');pg.wait_for_timeout(100);pg.screenshot(path='v26_coll.png',full_page=True)
    print('collection: foil',len(pg.query_selector_all('.coll .foil')),'locked',len(pg.query_selector_all('.coll .lockd')),'cards',len(pg.query_selector_all('.coll .ccard')))
    pg.reload();pg.wait_for_timeout(400);s=st(pg)['camp'];print('RAW',s);print('after reload cash',s['cash'],'perks',s['perks'],'up',s['up'])
    # loadout + endless
    pg.click('nav [data-tab=play]');pg.click('[data-act=campmap]');pg.click('[data-act="cview:loadout"]');pg.wait_for_timeout(100)
    print('start disabled w/0 picks:',pg.get_attribute('[data-act=endless]','aria-disabled'))
    for cid in ['vm','payg','scale','ha','patch','shared','dr','mon']: pg.click('[data-act="ltog:%s"]'%cid);pg.wait_for_timeout(30)
    pg.screenshot(path='v26_loadout.png',full_page=True)
    pg.click('[data-act=endless]');pg.wait_for_timeout(150)
    print('endless start:',pg.inner_text('.camp')[:80].replace('\n',' '),'| uptime',pg.inner_text('.me')[:30].replace('\n',' '))
    print('upgraded name shown:', 'Virtual Machine+' in pg.inner_text('.camp') or 'not in hand')
    waves=0
    for k in range(60):
        if pg.query_selector('[data-act=cend]'): turn(pg,True)
        elif pg.query_selector('[data-act^=edraft]'):
            waves+=1
            if waves==1: pg.screenshot(path='v26_draft.png')
            if waves>=3: break
            pg.click('[data-act^=edraft] >> nth=2');pg.wait_for_timeout(80)
        else: break
    print('endless after',waves,'wave wins:',pg.inner_text('.camp')[:90].replace('\n',' '),'best',st(pg)['camp']['endless'])
    # daily
    pg.click('[data-act=campmap]');pg.wait_for_timeout(80);c0=st(pg)['camp']['cash'];pg.click('[data-act=daily]');pg.wait_for_timeout(120)
    print('daily:',pg.inner_text('.camp')[:60].replace('\n',' '))
    t=0
    while pg.query_selector('[data-act=cend]') and t<40: turn(pg,True);t+=1
    s=st(pg)['camp'];print('daily end:',pg.inner_text('.camp')[:90].replace('\n',' '),'cash',c0,'->',s['cash'],'daily',s['daily'])
    pg.screenshot(path='v26_daily_end.png')
    pg.click('[data-act=daily]');t=0
    while pg.query_selector('[data-act=cend]') and t<40: turn(pg,True);t+=1
    print('daily replay cash',st(pg)['camp']['cash'])
    pg.click('nav [data-tab=me]') if pg.query_selector('nav [data-tab=me]') else (pg.click('[data-act=quit]'),pg.click('nav [data-tab=me]'))
    pg.wait_for_timeout(150);txt=pg.inner_text('#view');print('profile objectives:', 'Exam objectives' in txt,'| badges hex:',len(pg.query_selector_all('.bdg svg')),'| earned:',[x for x in ['World 1 Cleared','Daily Defender','Foil Card'] if x in txt])
    pg.screenshot(path='v26_profile.png',full_page=True)
    b.close()
print('ERRORS',errs)
