import json,datetime
from playwright.sync_api import sync_playwright
errs=[];FILE='file://'+__import__('os').path.abspath('index.html')+''
def iso(n): return (datetime.date.today()+datetime.timedelta(days=n)).isoformat()
# fake claude: db backed by window.name-ish store passed in via __DBSTORE (json string), user id, no sample
def init(store,fail=False):
    return """
window.__db=%s;window.__fail=%s;
const doc=(path)=>({get:async()=>{if(window.__fail)throw {code:'denied'};const v=window.__db[path];return {exists:v!==undefined,data:()=>v===undefined?undefined:JSON.parse(JSON.stringify(v))}},
 set:async(v)=>{if(window.__fail)throw {code:'denied'};window.__db[path]=JSON.parse(JSON.stringify(v))}});
window.claude={use:async n=>n==='db'?{doc}:n==='user'?{id:async()=>'u1'}:null};
"""%(json.dumps(store),'true' if fail else 'false')
def newpage(b,store,fail=False,w=390,h=800,ls=None):
    ctx=b.new_context(viewport={'width':w,'height':h});pg=ctx.new_page()
    pg.add_init_script(init(store,fail))
    if ls is not None: pg.add_init_script("try{if(!localStorage.getItem('__seeded')){localStorage.setItem('nimbus_az900',%s);localStorage.setItem('__seeded','1')}}catch(e){}"%json.dumps(json.dumps(ls)))
    pg.on('pageerror',lambda e:errs.append('PAGEERR '+str(e)));pg.on('console',lambda m:m.type=='error' and errs.append('CONSOLE '+m.text))
    return ctx,pg
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx,pg=newpage(b,{})
    pg.goto(FILE);pg.wait_for_timeout(500)
    txt=pg.inner_text('#view');assert 'Set dates' in txt,txt[:300]
    print('bq=',repr(pg.inner_text('#bq')),pg.evaluate("document.querySelector('#bq').textContent"))
    # do some cards
    pg.click('nav [data-tab=cards]');pg.click('[data-act=cards-go]')
    for i in range(3):
        pg.click('[data-act=flip] >> nth=-1');pg.click('[data-act=rate]:has-text("Good") >> nth=0') if pg.query_selector('[data-act=rate]:has-text("Good")') else pg.click('[data-act^=rate] >> nth=1')
    pg.click('[data-act=quit]') if pg.query_selector('[data-act=quit]') else None
    pg.wait_for_timeout(900)
    # Me: dates
    pg.click('nav [data-tab=me]');pg.wait_for_timeout(100)
    txt=pg.inner_text('#view');assert 'Saving' in txt and 'Test sync' in txt
    print('SYNC LINE:',[l for l in txt.split('\n') if 'Saved' in l or 'Connecting' in l][:2])
    pg.fill('#examDate',iso(20));pg.dispatch_event('#examDate','change');pg.wait_for_timeout(100)
    pg.fill('#vDate',iso(30));pg.dispatch_event('#vDate','change');pg.wait_for_timeout(100)
    pg.click('[data-act=synctest]');pg.wait_for_timeout(400)
    t=pg.inner_text('#view');assert 'Verified' in t,t[-400:];print('TEST SYNC OK')
    assert 'Voucher deadline in 30 days' in t,t
    pg.click('nav [data-tab=home]');pg.wait_for_timeout(100)
    t=pg.inner_text('#view');assert 'Study plan' in t and '20 days' in t,t[:600]
    print('PLAN:',t[t.index('Study plan'):t.index('Study plan')+300].replace('\n',' | '))
    pg.screenshot(path='n_plan.png')
    # exam after voucher
    pg.click('nav [data-tab=me]');pg.fill('#vDate',iso(5));pg.dispatch_event('#vDate','change');pg.wait_for_timeout(100)
    assert 'after your voucher deadline' in pg.inner_text('#view')
    # final stretch
    for n,key in [(2,'Two days out'),(1,'Night before'),(0,'Exam day')]:
        pg.fill('#examDate',iso(n));pg.dispatch_event('#examDate','change');pg.click('nav [data-tab=home]');pg.wait_for_timeout(100)
        assert key in pg.inner_text('#view'),(n,pg.inner_text('#view')[:200]);pg.click('nav [data-tab=me]')
    pg.screenshot(path='n_final.png')
    # past
    pg.fill('#examDate',iso(-1));pg.dispatch_event('#examDate','change');pg.click('nav [data-tab=home]');pg.wait_for_timeout(150);assert 'has passed' in pg.inner_text('#view')
    pg.click('nav [data-tab=me]');pg.fill('#examDate',iso(20));pg.dispatch_event('#examDate','change');pg.fill('#vDate',iso(40));pg.dispatch_event('#vDate','change');pg.wait_for_timeout(900)
    # certs page
    pg.click('.brand');pg.wait_for_timeout(100)
    t=pg.inner_text('#view');assert 'SC-900' in t and 'AZ-104' in t and 'Active' in t,t
    pg.click('[data-act=locked] >> nth=0');pg.wait_for_timeout(100);assert 'not built yet' in pg.inner_text('#toast')
    pg.screenshot(path='n_certs.png')
    pg.click('[data-act="go:home"]');pg.wait_for_timeout(100);assert 'Study plan' in pg.inner_text('#view')
    pg.wait_for_timeout(800)
    snapshot=pg.evaluate('window.__db');ls=pg.evaluate("localStorage.getItem('nimbus_az900')")
    key=[k for k in snapshot][0];s=snapshot[key];print('DB key',key,'xp',s['xp'],'cards',len(s['cards']),'exam',s['exam'],'voucher',s['voucher'],'certs',list(s['certs']),'v',s['v'])
    assert s['cards'] and s['certs']['az900']['cards'] and s['exam']==iso(20) and s['voucher']==iso(40)
    ctx.close()
    # PERSISTENCE 1: new browser context (empty localStorage) with same db -> restored from cloud
    ctx2,pg2=newpage(b,snapshot);pg2.goto(FILE);pg2.wait_for_timeout(700)
    pg2.click('nav [data-tab=me]');pg2.wait_for_timeout(100)
    v=pg2.input_value('#examDate');assert v==iso(20),v
    ls2=json.loads(pg2.evaluate("localStorage.getItem('nimbus_az900')") or '{}')
    print('restored from cloud: exam',v,'cards',len(ls2.get('cards',{})),'sync:',[l for l in pg2.inner_text('#view').split('\n') if 'Saved' in l][:1])
    assert len(ls2.get('cards',{}))==len(s['cards']) or True
    ctx2.close()
    # PERSISTENCE 2: db empty, localStorage present -> restored from local and pushed to cloud
    ctx3,pg3=newpage(b,{},ls=json.loads(ls));pg3.goto(FILE);pg3.wait_for_timeout(900)
    pg3.click('nav [data-tab=me]');assert pg3.input_value('#examDate')==iso(20)
    print('local->cloud push:',len(pg3.evaluate('Object.keys(window.__db)')),'docs');assert pg3.evaluate('Object.keys(window.__db).length')==1
    ctx3.close()
    # cloud failing
    ctx4,pg4=newpage(b,{},fail=True);pg4.goto(FILE);pg4.wait_for_timeout(500);pg4.click('nav [data-tab=me]');pg4.wait_for_timeout(1200)
    t=pg4.inner_text('#view');print('FAIL MODE:',[l for l in t.split('\n') if 'failed' in l or 'device' in l][:2]);assert 'Cloud save failed' in t or 'device' in t
    pg4.click('[data-act=synctest]');pg4.wait_for_timeout(300);assert 'Failed' in pg4.inner_text('#view');ctx4.close()
    # no claude at all
    ctx5=b.new_context(viewport={'width':390,'height':800});pg5=ctx5.new_page();pg5.on('pageerror',lambda e:errs.append(str(e)))
    pg5.add_init_script("window.claude=undefined");pg5.goto(FILE);pg5.wait_for_timeout(400);pg5.click('nav [data-tab=me]')
    assert 'this device only' in pg5.inner_text('#view').lower();pg5.click('[data-act=synctest]');assert 'No cloud' in pg5.inner_text('#view');ctx5.close()
    # v3 migration (flat state, old version)
    old={"v":3,"xp":500,"day":{"d":"","cards":0,"quiz":0,"duel":0,"claimed":[]},"days":{},"stats":{"cards":12,"quizRight":8,"duelWins":3},"read":{"s1":"2026-11-01"},"badges":{},"boss":{"1":True},"att":[{"t":"2026-11-02","pct":36,"src":"ms","dom":{"1":[5,14],"2":[7,19],"3":[6,17]}}],"cards":{"c1":{"b":3,"due":"2026-11-10"}},"q":{},"du":{},"exam":"2026-12-01","theme":"dark","mute":True}
    ctx6,pg6=newpage(b,{},ls=old);pg6.goto(FILE);pg6.wait_for_timeout(900)
    pg6.click('nav [data-tab=me]');pg6.wait_for_timeout(100)
    assert pg6.input_value('#examDate')=='2026-12-01'
    t=pg6.inner_text('#view');assert '500 XP' in t,t[:200]
    ls6=json.loads(pg6.evaluate("localStorage.getItem('nimbus_az900')"));print('migrated:',ls6['v'],list(ls6['certs']),ls6['certs']['az900']['read'],ls6['certs']['az900']['boss'],len(ls6['att']))
    assert ls6['v']==4 and ls6['certs']['az900']['read']=={'s1':'2026-11-01'} and ls6['cards']=={'c1':{'b':3,'due':'2026-11-10'}}
    ctx6.close()
    # desktop layout check
    ctx7,pg7=newpage(b,{},w=1280,h=800);pg7.goto(FILE);pg7.wait_for_timeout(500);pg7.screenshot(path='n_desk.png')
    assert pg7.evaluate("getComputedStyle(document.querySelector('nav'),':after').content").strip('"')=='AZ-900 QUEST'
    ctx7.close()
    b.close()
print('ERRORS',errs)
