import json,collections
from playwright.sync_api import sync_playwright
AXE=open(__import__('os').environ.get('AXE','node_modules/axe-core/axe.min.js')).read()  # npm i axe-core@4.10.2
seed={"v":4,"camp":{"lv":{str(i):3 for i in range(1,12)},"mast":{"vm":12},"cash":300,"loadout":["vm","payg","scale","ha","shared"]},"exam":"2026-12-10"}
out=collections.defaultdict(set)
def run(pg,label):
    pg.add_script_tag(content=AXE) if not pg.evaluate('!!window.axe') else None
    r=pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa','best-practice'],rules:{'region':{enabled:false}}}).then(r=>r.violations.map(v=>({id:v.id,impact:v.impact,n:v.nodes.length,ex:v.nodes.slice(0,2).map(x=>x.target.join(' ')+' :: '+(x.failureSummary||'').split('\\n').slice(1,2).join('')) })))")
    for v in r: out[(v['id'],v['impact'])].add(label+' x'+str(v['n'])+' '+' | '.join(v['ex'])[:220])
with sync_playwright() as p:
    b=p.chromium.launch()
    for theme in (None,'light'):
        pg=b.new_page(viewport={'width':390,'height':900})
        pg.goto('file://'+__import__('os').path.abspath('index.html')+'');pg.wait_for_timeout(300)
        sd=dict(seed);
        if theme: sd['theme']=theme
        pg.evaluate("s=>localStorage.setItem('nimbus_az900',s)",json.dumps(sd));pg.reload();pg.wait_for_timeout(500)
        th=theme or 'frappe'
        for t in ('home','learn','cards','play','me'):
            pg.click('nav [data-tab=%s]'%t);pg.wait_for_timeout(250);run(pg,th+':'+t)
        pg.click('nav [data-tab=play]');pg.click('[data-act=campmap]');pg.wait_for_timeout(150);run(pg,th+':map')
        for v in ('shop','coll','loadout'):
            pg.click('[data-act="cview:%s"]'%v);pg.wait_for_timeout(150);run(pg,th+':'+v);pg.click('[data-act=campmap]')
        pg.click('[data-act="camp:11"]');pg.wait_for_timeout(200);run(pg,th+':battle')
        pg.click('[data-act="cplay:0"]');pg.wait_for_timeout(600)
        if pg.query_selector('.cmodal'): run(pg,th+':castcheck')
        # SC-900 pack and 3D models
        pg.evaluate("location.hash='learn/s8'");pg.wait_for_timeout(300);pg.locator('.m3p .cbtn').first.click();pg.wait_for_timeout(200);run(pg,th+':model')
        pg.evaluate("location.hash='certs'");pg.wait_for_timeout(300);run(pg,th+':certs');pg.click('[data-act="cert:sc900"]');pg.wait_for_timeout(400)
        for t in ('home','learn','cards','play','me'):
            pg.click('nav [data-tab=%s]'%t);pg.wait_for_timeout(250);run(pg,th+':sc-'+t)
        pg.evaluate("location.hash='learn/s1'");pg.wait_for_timeout(300);run(pg,th+':sc-sec')
        pg.close()
    b.close()
for k,v in sorted(out.items(),key=lambda x:str(x[0][1])):
    print(k,len(v));[print('   ',x[:300]) for x in sorted(v)[:6]]
print('TOTAL rules',len(out))
