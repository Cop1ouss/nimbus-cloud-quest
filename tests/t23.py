import json
from playwright.sync_api import sync_playwright
F='file://'+__import__('os').path.abspath('index.html')+''
QS=json.load(open('src/data_packs.json'))['packs']['az900']['questions']
byq={q['q']:q for q in QS if 'opts' in q}
def find(pg):
    if pg.query_selector('.cells'):
        first=pg.inner_text('.cell .ctext').strip()
        for q in QS:
            if q.get('type')=='yn' and q['stmts'][0]==first: return q
            if q.get('type')=='match' and q['rows'][0]==first: return q
    return byq[pg.inner_text('.qpanel p[style*="font-size:18px"]').strip()]
def answer(pg,right=True,check=True):
    q=find(pg)
    if q.get('type')=='yn':
        for i,a in enumerate(q['ans']):
            v=a if right else 1-a
            pg.click('[data-act="cell:%d:%d"]'%(i,v));pg.wait_for_timeout(30)
    elif q.get('type')=='match':
        for i,a in enumerate(q['ans']):
            v=a if right else (a+1)%len(q['choices'])
            pg.select_option('select[data-cell="%d"]'%i,str(v));pg.wait_for_timeout(30)
    else:
        texts=[o.inner_text() for o in pg.query_selector_all('.opt')];want=[q['opts'][i].strip() for i in q['ans']]
        picks=[i for i,t in enumerate(texts) if any(w in t for w in want)] if right else [i for i,t in enumerate(texts) if not any(w in t for w in want)][:len(q['ans'])]
        for i in picks: pg.locator('.opt').nth(i).click();pg.wait_for_timeout(30)
    if check and pg.query_selector('[data-act=qcheck]'): pg.click('[data-act=qcheck]')
    return q
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':390,'height':850});pg=ctx.new_page();pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
    pg.goto(F);pg.wait_for_timeout(300)
    # --- hard mock
    pg.click('nav [data-tab=play]');pg.wait_for_timeout(100);pg.screenshot(path='v21_play.png',full_page=True)
    pg.click('[data-act="mock:hard"]');pg.wait_for_timeout(150)
    print('hard clock',pg.inner_text('#clock'))
    kinds=[];shots=set()
    for i in range(6):
        q=answer(pg,True,False);kinds.append(q.get('type','mc'))
        t=q.get('type','mc')
        if t in('yn','match') and t not in shots: pg.screenshot(path='v21_%s.png'%t);shots.add(t)
        pg.click('[data-act=mnext]');pg.wait_for_timeout(60)
    print('first 6 kinds',kinds)
    # count compound in whole exam via grid jump
    pg.click('[data-act=quit]');pg.wait_for_timeout(150)
    print('home banner:', 'Practice exam paused' in pg.inner_text('#view'))
    st=json.loads(pg.evaluate("localStorage.getItem('nimbus_az900')"));ms=st['mockSave'];print('saved: i',ms['i'],'answered',sum(1 for k,v in ms['ans'].items() if v and any(x is not None for x in v)),'hard',ms['hard'])
    types=[next(q for q in QS if q['id']==i).get('type','mc') for i in ms['ids']];import collections;print('hard exam mix',collections.Counter(types),'two',sum(1 for i in ms['ids'] if len(next(q for q in QS if q['id']==i)['ans'])>1 and next(q for q in QS if q['id']==i).get('type') is None))
    pg.reload();pg.wait_for_timeout(400);pg.screenshot(path='v21_banner.png')
    pg.click('[data-act=mock-resume]');pg.wait_for_timeout(150)
    print('resumed at',pg.inner_text('.qpanel')[:0], pg.inner_text('#view')[:12].replace('\n',' '))
    # jump back to q1 to see answer kept
    pg.click('[data-act="mjump:0"]');pg.wait_for_timeout(80);print('q1 kept selected:',bool(pg.query_selector('.opt.sel,[aria-pressed="true"],select[data-cell] option[selected]')))
    pg.click('[data-act=mfinish]');pg.click('[data-act=mfinish]');pg.wait_for_timeout(300)
    t=pg.inner_text('#view');print('result:',t[:120].replace('\n',' '))
    pg.click('[data-act=review-all]');pg.wait_for_timeout(100);rv=pg.inner_text('#view');print('review shows arrows:', '→' in rv)
    pg.click('[data-act=review-back]');pg.click('[data-act=quit]');pg.wait_for_timeout(100)
    st=json.loads(pg.evaluate("localStorage.getItem('nimbus_az900')"));print('mockSave after finish',st['mockSave'],'last att',st['att'][-1]['pct'],st['att'][-1].get('hard'))
    # --- recall-first quiz
    pg.click('nav [data-tab=play]');pg.click('[data-act="tog:recallQ"]');pg.wait_for_timeout(80)
    pg.click('[data-act=quiz-go]');pg.wait_for_timeout(100)
    hidden=not pg.query_selector('.opt') and bool(pg.query_selector('[data-act=reveal]'));cells=bool(pg.query_selector('.cells'))
    print('recall hides options:',hidden,'(compound first:',cells,')');pg.screenshot(path='v21_recallq.png')
    if hidden: pg.click('[data-act=reveal]');pg.wait_for_timeout(80);print('options after reveal',len(pg.query_selector_all('.opt')))
    # answer a few including any compound right then wrong
    for i in range(10):
        q=answer(pg,i%2==0);pg.wait_for_timeout(60)
        if q.get('type') and i%2: pg.screenshot(path='v21_compound_wrong.png')
        if pg.query_selector('[data-act=qnext]'): pg.click('[data-act=qnext]');pg.wait_for_timeout(60)
        if pg.query_selector('[data-act=reveal]'): pg.click('[data-act=reveal]');pg.wait_for_timeout(40)
        if not pg.query_selector('.qpanel'): break
    print('quiz end:',pg.inner_text('#view')[:60].replace('\n',' '))
    pg.click('[data-act=quit]')
    # --- cards typed recall + 3D flip
    pg.click('nav [data-tab=cards]');pg.click('[data-act=cards-go]');pg.wait_for_timeout(100)
    pg.fill('#recallIn','pay for what you use no upfront hardware');pg.screenshot(path='v21_card_q.png')
    pg.press('#recallIn','Enter');pg.wait_for_timeout(250);pg.screenshot(path='v21_card_mid.png');pg.wait_for_timeout(600)
    print('flipped class',pg.evaluate("document.querySelector('.fc3').className"),'| score:', pg.inner_text('.why')[:120].replace('\n',' ') if pg.query_selector('.why') else None)
    pg.screenshot(path='v21_card_a.png')
    pg.click('.fc3');pg.wait_for_timeout(700);print('back to front, input value kept:',pg.input_value('#recallIn') if pg.query_selector('#recallIn') else None)
    pg.click('.fc3');pg.wait_for_timeout(100);pg.click('[data-act="rate:good"]');pg.wait_for_timeout(100);print('next card input empty:',pg.input_value('#recallIn')=='')
    ctx.close()
    # --- boss hard with timer still ok
    ctx=b.new_context(viewport={'width':390,'height':850});pg=ctx.new_page();pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(F);pg.wait_for_timeout(300);pg.click('nav [data-tab=play]');pg.click('[data-act="boss:2:3"]');pg.wait_for_timeout(300);pg.screenshot(path='v21_boss_enter.png')
    for i in range(12):
        if not pg.query_selector('.qpanel'):break
        answer(pg,True);pg.wait_for_timeout(60)
        if pg.query_selector('[data-act=qnext]'):pg.click('[data-act=qnext]');pg.wait_for_timeout(60)
    pg.wait_for_timeout(1000);print('hard boss:',pg.inner_text('#view')[:80].replace('\n',' '));pg.screenshot(path='v21_boss_win.png')
    # desktop look
    pg.set_viewport_size({'width':1280,'height':800});pg.click('[data-act=quit]');pg.click('nav [data-tab=cards]');pg.click('[data-act=cards-go]');pg.wait_for_timeout(200);pg.screenshot(path='v21_desk_card.png')
    b.close()
print('ERRORS',errs)
