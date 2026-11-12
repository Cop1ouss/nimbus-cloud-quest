from playwright.sync_api import sync_playwright
F='file://'+__import__('os').path.abspath('index.html')+''
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':800});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(F);pg.wait_for_timeout(300);pg.click('nav [data-tab=cards]');pg.click('[data-act=cards-go]')
    lab=lambda:pg.inner_text('.fc .lab')
    print('1',lab(), 'rate' , bool(pg.query_selector('[data-act^="rate:"]')))
    pg.click('.fc');print('2',lab(),bool(pg.query_selector('[data-act="rate:good"]')))
    pg.click('.fc');print('3 back',lab(),'rate still',bool(pg.query_selector('[data-act="rate:good"]')),'showbtn',bool(pg.query_selector('button.pri[data-act=flip]')))
    pg.click('button.pri[data-act=flip]');print('4',lab())
    pg.click('button:has-text("Flip back")');print('5',lab())
    pg.keyboard.press('Space');print('6 space',lab());pg.keyboard.press('3');pg.wait_for_timeout(100);print('7 next card', pg.inner_text('.row .small').split('\n')[0], 'seen reset', not pg.query_selector('[data-act="rate:good"]'))
    print('stats',pg.evaluate("JSON.parse(localStorage.getItem('nimbus_az900')).stats.cards"));pg.screenshot(path='n_flip.png')
print(errs)
