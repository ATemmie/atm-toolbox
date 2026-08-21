"""用Playwright将HTML地图截图为PNG"""
import os, asyncio

MAP_DIR = os.path.join(os.path.dirname(__file__), "maps")

async def screenshot_html(html_path, png_path):
    """截取HTML地图为PNG"""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        os.system("pip install playwright -q")
        os.system("playwright install chromium")
        from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1200, "height": 800})
        file_url = "file:///" + os.path.abspath(html_path).replace("\\", "/")
        await page.goto(file_url, wait_until="networkidle")
        await page.wait_for_timeout(2000)  # 等待地图瓦片加载
        await page.screenshot(path=png_path, full_page=False)
        await browser.close()
        print(f"  [ok] {os.path.basename(png_path)} ({os.path.getsize(png_path)//1024}KB)")

async def main():
    from gen_leaflet_map import generate_maps
    html1, html2 = generate_maps()
    png1 = html1.replace(".html", ".png")
    png2 = html2.replace(".html", ".png")
    print("\n截图中...")
    await screenshot_html(html1, png1)
    await screenshot_html(html2, png2)

if __name__ == "__main__":
    asyncio.run(main())
