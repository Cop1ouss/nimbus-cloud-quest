# Mistake review: misses collect in the Arena and clear after two right answers in a row
import json,os,sys
from playwright.sync_api import sync_playwright
SP=sys.argv[1] if len(sys.argv)>1 else '.'
F='file://'+os.path.abspath('index.html')
P=json.load(open('src/data_packs.json'))['packs']['az900']
ones=[q for q in P['questions'] if q['kind']=='one'][:3];ids=[q['id'] for q in ones]
byq={q['q']:q for q in ones}
def st():return json.loads(pg.evaluate("localStorage.getItem('nimbus_az900')"))
def answer_right():
    q=byq[pg.inner_text('.qpanel p[style*="font-size:18px"]').strip()]
    want=q['opts'][q['ans'][0]].strip()
    texts=[o.inner_text() for o in pg.query_selector_all('.opt')]
    pg.locator('.opt').nth([i for i,t in enumerate(texts) if want in t][0]).click();pg.wait_for_timeout(40)
    if pg.query_selector('[data-act=qcheck]'):pg.click('[data-act=qcheck]')
    pg.wait_for_timeout(120);return q['id']
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844})
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(F);pg.wait_for_timeout(400)
    pg.click('nav [data-tab=play]');pg.wait_for_timeout(300)
    assert 'Nothing to review yet' in pg.inner_text('#view') and pg.locator('[data-act=review-q]').count()==0
    # seed: q0 missed twice, q1 missed then right once, q2 already cleared, one missed duel pair
    seed={"v":4,"q":{ids[0]:{"c":0,"w":2,"st":0,"lw":2},ids[1]:{"c":1,"w":1,"st":1,"lw":1},ids[2]:{"c":3,"w":1,"st":2}},
          "du":{P['duels'][0]['id']:{"c":0,"w":1,"st":0}}}
    pg.evaluate("s=>localStorage.setItem('nimbus_az900',s)",json.dumps(seed));pg.reload();pg.wait_for_timeout(500)
    pg.click('nav [data-tab=play]');pg.wait_for_timeout(300)
    t=pg.inner_text('#view');assert '2 questions and 1 duel pair' in t,t[:500]
    pg.locator('.mode',has_text='Mistake review').screenshot(path=SP+'/review_arena.png')
    pg.click('[data-act=review-q]');pg.wait_for_timeout(300)
    first=answer_right();assert first==ids[0],(first,ids)   # most-missed first
    pg.click('[data-act=qnext]');pg.wait_for_timeout(150);answer_right()
    s=st()['q'];assert s[ids[0]]['st']==1 and s[ids[1]]['st']==2,s
    pg.reload();pg.wait_for_timeout(500);pg.click('nav [data-tab=play]');pg.wait_for_timeout(300)
    assert '1 question and 1 duel pair' in pg.inner_text('#view')
    pg.click('[data-act=review-d]');pg.wait_for_timeout(300)
    assert pg.locator('[data-act^="duelpick:"]').count()==2
    b.close()
print('ERRORS',errs)
