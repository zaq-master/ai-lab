from playwright.sync_api import sync_playwright
import pathlib
p=pathlib.Path(__file__).parent
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1080})
    pg.goto((p/'icon.src.html').resolve().as_uri()); pg.screenshot(path=str(p/'icon.png')); b.close()
