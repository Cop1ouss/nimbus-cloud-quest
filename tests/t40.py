from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':900});msgs=[]
    pg.goto('file://'+__import__('os').path.abspath('index.html')+'');pg.wait_for_timeout(300);pg.click('nav [data-tab=me]');pg.wait_for_timeout(100)
    pg.evaluate("new MutationObserver(()=>window.__t=(window.__t||[]).concat(document.querySelector('#toast').textContent)).observe(document.querySelector('#toast'),{childList:true,subtree:true,characterData:true})")
    pg.set_input_files('#restoreIn','bad.json');pg.wait_for_timeout(400)
    print('toasts:',pg.evaluate('window.__t'))
    b.close()
