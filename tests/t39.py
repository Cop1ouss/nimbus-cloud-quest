import json
from playwright.sync_api import sync_playwright
F='file://'+__import__('os').path.abspath('index.html')+''
seed={"v":4,"xp":777,"cards":{"c1":{"b":3,"due":"2026-12-01"}},"camp":{"lv":{str(i):3 for i in range(1,11)},"mast":{"vm":4},"cash":90,"loadout":["payg","scale","ha","shared","dr"]}}
errs=[]
def st(pg): return json.loads(pg.evaluate("localStorage.getItem('nimbus_az900')"))
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':900})
    pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
    pg.add_init_script("window.claude={use:async n=>n==='downloads'?{save:async o=>{window.__dl=o}}:null}")
    pg.goto(F);pg.wait_for_timeout(300);pg.evaluate("s=>localStorage.setItem('nimbus_az900',s)",json.dumps(seed));pg.reload();pg.wait_for_timeout(500)
    s=st(pg);print('badges on open:',sorted(k for k in s['badges'] if k in('w1','foil','daily')),'toast:',pg.inner_text('#toast')[:40])
    # loadout guard
    pg.click('nav [data-tab=play]');pg.click('[data-act=campmap]');pg.click('[data-act="cview:loadout"]');pg.wait_for_timeout(100)
    print('guard: start aria-disabled=',pg.get_attribute('[data-act=endless]','aria-disabled'),'| warning shown:', 'Add a damage or deploy card' in pg.inner_text('.camp'))
    pg.evaluate("document.querySelector('[data-act=endless]').click()");pg.wait_for_timeout(100);print('still on loadout:', 'Pick your loadout' in pg.inner_text('.camp'))
    pg.click('[data-act="ltog:vm"]');pg.wait_for_timeout(50);print('after adding VM, start enabled:',pg.get_attribute('[data-act=endless]','aria-disabled') is None)
    pg.click('[data-act=quit]')
    # backup
    pg.click('nav [data-tab=me]');pg.wait_for_timeout(150);pg.click('[data-act=dl-prog]');pg.wait_for_timeout(200)
    dl=pg.evaluate('window.__dl');bk=json.loads(dl['data']);print('backup file:',dl['filename'],'xp',bk['xp'],'camp lv',len(bk['camp']['lv']))
    open('backup_test.json','w').write(dl['data']);open('bad.json','w').write('{"hello":1}')
    # wipe
    pg.click('[data-act=reset]');pg.click('[data-act=reset-yes]');pg.wait_for_timeout(150);print('after wipe xp',st(pg)['xp'])
    # bad file rejected
    pg.set_input_files('#restoreIn','bad.json');pg.wait_for_timeout(200);print('bad file toast:',pg.inner_text('#toast')[:40],'| confirm shown:',bool(pg.query_selector('[data-act=restore-yes]')))
    # good file -> confirm -> restored
    pg.set_input_files('#restoreIn','backup_test.json');pg.wait_for_timeout(200);print('confirm text:',pg.inner_text('[role=alert]')[:110].replace('\n',' '))
    pg.click('[data-act=restore-yes]');pg.wait_for_timeout(200);s=st(pg);print('restored xp',s['xp'],'camp lv',len(s['camp']['lv']),'cash',s['camp']['cash'],'cards',list(s['cards']))
    pg.reload();pg.wait_for_timeout(400);print('after reload xp',st(pg)['xp'])
    pg.screenshot(path='v27_restore.png',full_page=True)
    b.close()
print('ERRORS',errs)
