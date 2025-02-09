import asyncio
from playwright.async_api import async_playwright

async def get_chapter_list(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await asyncio.sleep(5)
        await page.evaluate("smallToBig()")
        await asyncio.sleep(2)
        chapters = await page.query_selector_all("#catalog ul li a")
        await asyncio.sleep(2)
        chapter_list = {}
        for chapter in chapters:
            title = await chapter.inner_text()
            link = await chapter.get_attribute("href")
            chapter_list[title.strip()] = link
        await browser.close()
        return chapter_list


async def scrape_chapter(chapter_name, chapter_url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(chapter_url)
        await asyncio.sleep(1)
        filename = f"{chapter_name}.md"
        with open(filename, "a", encoding="utf-8") as f:
            content = await page.inner_text("div.txtnav")
            f.write(content + "\n\n")
        await browser.close()
        print(f"已儲存: {filename}")


async def main():
    urls_and_names = []

    while True:
        url = input("網址 (輸入 exit 退出): ")
        if url.lower() == "exit":
            break
        chapter_name = input("檔案名稱: ")
        urls_and_names.append((url, chapter_name))

    for url, chapter_name in urls_and_names:
        try:
            chapter_list = await get_chapter_list(url)
            index = 0
            for title in chapter_list:
                index += 1
                print(f"{title} - {chapter_list[title]}")  # 顯示所有章節名稱
                if index >= 0:
                    await scrape_chapter(chapter_name, chapter_list[title])
                    await asyncio.sleep(4)
        except:
            pass

asyncio.run(main())
