# SC-900 pack + 3D models smoke test
from playwright.sync_api import sync_playwright
import os,sys
SP=sys.argv[1] if len(sys.argv)>1 else '.'
f='file://'+os.path.abspath('index.html');errs=[]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844})
    pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None);pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(f);pg.wait_for_timeout(400)
    assert pg.title()=='Nimbus Cloud Quest'
    # models in AZ-900 sections
    for sec,n in (('s4',2),('s8',3),('s1',1),('s6',1)):
        pg.evaluate("location.hash='learn/%s'"%sec);pg.wait_for_timeout(300)
        assert pg.locator('.m3w').count()==n,sec
        for i in range(n):
            w=pg.locator('.m3w').nth(i);w.scroll_into_view_if_needed()
            w.locator('.m3p .cbtn').nth(1).click();pg.wait_for_timeout(450)
            w=pg.locator('.m3w').nth(i);assert w.locator('.m3i b').count()==1 and w.locator('.bx.on').count()>=1
            w.screenshot(path='%s/m_%s_%d.png'%(SP,sec,i))
    # tap a box, spread, rotate, drag
    pg.evaluate("location.hash='learn/s8'");pg.wait_for_timeout(300)
    w=pg.locator('.m3w').first;w.locator('.bx').last.evaluate('e=>e.click()');pg.wait_for_timeout(200)
    assert pg.locator('.m3w').first.locator('.m3i b').inner_text()=='Data'
    pg.locator('[data-act=m3ex]').first.click();pg.wait_for_timeout(450);pg.locator('.m3w').first.screenshot(path=SP+'/m_spread.png')
    rz0=pg.evaluate("getComputedStyle(document.querySelector('.m3s')).getPropertyValue('--rz')")
    bb=pg.locator('.m3d').first.bounding_box();pg.mouse.move(bb['x']+60,bb['y']+150);pg.mouse.down();pg.mouse.move(bb['x']+200,bb['y']+150,steps=5);pg.mouse.up();pg.wait_for_timeout(200)
    rz1=pg.evaluate("document.querySelector('.m3s').style.getPropertyValue('--rz')");assert rz0.strip()!=rz1.strip(),(rz0,rz1)
    assert pg.evaluate("document.documentElement.scrollWidth")<=390
    # switch to SC-900
    pg.evaluate("location.hash='certs'");pg.wait_for_timeout(300);pg.click('[data-act="cert:sc900"]');pg.wait_for_timeout(400)
    assert pg.inner_text('#bq').upper()=='SC-900 QUEST'
    for t in ('home','learn','cards','play','me'):
        pg.click('nav [data-tab=%s]'%t);pg.wait_for_timeout(250);pg.screenshot(path='%s/sc_%s.png'%(SP,t),full_page=(t in('learn','play')))
        assert pg.evaluate("document.documentElement.scrollWidth")<=390,t
    assert pg.locator('.campcta').count()==0
    pg.evaluate("location.hash='learn/s1'");pg.wait_for_timeout(300);assert pg.locator('.m3w').count()==3
    assert pg.locator('.bossart .bx').count()==0
    pg.evaluate("location.hash='play'");pg.wait_for_timeout(300);assert pg.locator('.bossart .bx').count()>20 and pg.locator('.bossart svg').count()==0
    for s in range(1,15):
        pg.evaluate("location.hash='learn/s%d'"%s);pg.wait_for_timeout(120);assert pg.locator('h1').count()>=1
    # cards session, quiz, duel, boss, mock: just start each and answer one
    pg.click('nav [data-tab=cards]');pg.click('[data-act=cards-go]');pg.wait_for_timeout(300);pg.screenshot(path=SP+'/sc_card.png')
    def play():
        for sel in ('[data-act=quit]','[data-act=quit-yes]'):
            q=pg.locator(sel)
            if q.count() and q.first.is_visible():q.first.click();pg.wait_for_timeout(150)
        if not pg.locator('nav [data-tab=play]').is_visible():pg.reload();pg.wait_for_timeout(400)
        pg.click('nav [data-tab=play]');pg.wait_for_timeout(200)
    play()
    acts=pg.evaluate("[...document.querySelectorAll('#view [data-act]')].map(e=>e.dataset.act)");print(acts)
    for a in ('pscope:d4','quiz','duel','boss:4:1','mock:quick','mock:hard'):
        play()
        m=[x for x in acts if x==a or x.startswith(a+':') or x.startswith(a)]
        if not m:print('NO ACT',a);continue
        pg.locator('#view [data-act="%s"]'%m[0]).first.click();pg.wait_for_timeout(500)
        pg.screenshot(path='%s/sc_run_%s.png'%(SP,a.replace(':','_')))
        o=pg.locator('[data-act^="opt:"],[data-act^="duelpick:"]')
        if o.count():o.first.click();pg.wait_for_timeout(300)
    play()
    # switch back, AZ progress intact, reload keeps cert
    pg.evaluate("location.hash='certs'");pg.wait_for_timeout(300);pg.click('[data-act="cert:az900"]');pg.wait_for_timeout(300)
    assert pg.inner_text('#bq').upper()=='AZ-900 QUEST';pg.click('nav [data-tab=play]');pg.wait_for_timeout(300);assert pg.locator('.campcta').count()==1
    b.close()
print('ERRORS',errs)
