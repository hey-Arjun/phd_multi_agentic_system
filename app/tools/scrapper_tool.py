import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from typing import List

class ScraperTool:
    def __init__(self):
        self.browser_args = ["--disable-gpu", "--no-sandbox"]
    
    def _prepare_url(self, url: str) -> str:
        """Ensures the URL has a protocol prefix."""
        url = url.strip().lower()
        if not url.startswith(('http://', 'https://')):
            return f"https://{url}"
        return url
    
    async def scrape_url(self, url: str) -> str:
        """
        Navigates to a URL and returns cleaned text content.
        """
        full_url = self._prepare_url(url)
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=self.browser_args)
            page = await browser.new_page()

            await page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            })

            try: 
                # FIX: Use full_url here
                await page.goto(full_url, wait_until="networkidle", timeout=90000)
                content = await page.content()

                soup = BeautifulSoup(content, "lxml")
                # Remove non-content elements to save LLM tokens
                for element in soup(["script", "style", "header", "footer", "nav", "aside"]):
                    element.decompose()

                return soup.get_text(separator="\n", strip=True)
            
            except Exception as e:
                return f"Error scraping {full_url}: {str(e)}"
            finally: 
                await browser.close()

    async def extract_links(self, url: str) -> List[str]:
        """
        New: Extracts all unique absolute links from a page.
        Used by the Research Agent to find PhD listing sub-pages.
        """
        full_url = self._prepare_url(url)
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=self.browser_args)
            page = await browser.new_page()
            try:
                await page.goto(full_url, wait_until="networkidle", timeout=90000)
                # Client-side script to pull all absolute hrefs
                links = await page.evaluate("""
                    () => Array.from(document.querySelectorAll('a[href]'))
                               .map(a => a.href)
                """)
                return list(set(links)) # Returns unique links
            except Exception as e:
                print(f"Error extracting links from {full_url}: {e}")
                return []
            finally:
                await browser.close()

