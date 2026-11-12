from playwright.sync_api import sync_playwright
errs=[];F='file://'+__import__('os').path.abspath('index.html')+''
with sync_playwright() as p:
    b=p.chromium.launch()
    for w,h in [(1057,811),(900,800),(1280,800),(700,800)]:
        pg=b.new_page(viewport={'width':w,'height':h});pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto(F);pg.wait_for_timeout(300);pg.click('nav [data-tab=cards]');pg.click('[data-act=cards-go]');pg.click('.fc');pg.wait_for_timeout(100)
        for r in ['hard','good','again','easy']:
            el=pg.query_selector('[data-act="rate:%s"]'%r)
            if not el: pg.click('.fc');el=pg.query_selector('[data-act="rate:%s"]'%r)
            bb=el.bounding_box();top=pg.evaluate("([x,y])=>{const e=document.elementFromPoint(x,y);return e?(e.closest('[data-act]')||e).outerHTML.slice(0,60):null}",[bb['x']+bb['width']/2,bb['y']+bb['height']/2])
            before=pg.evaluate("JSON.parse(localStorage.getItem('nimbus_az900')||'{}').stats?.cards||0")
            try: pg.mouse.click(bb['x']+bb['width']/2,bb['y']+bb['height']/2)
            except Exception as e: print('click err',e)
            pg.wait_for_timeout(120)
            after=pg.evaluate("JSON.parse(localStorage.getItem('nimbus_az900')||'{}').stats?.cards||0")
            print(w,r,'hit:',top[:50] if top else None,'saved',before,'->',after)
        pg.close()
    b.close()
print(errs)
