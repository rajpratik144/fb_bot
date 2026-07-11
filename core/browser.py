# import asyncio
# from playwright.async_api import async_playwright

# class BrowserEngine:
#     def __init__(self, user_data_dir="./fb_session"):
#         self.user_data_dir = user_data_dir
#         self.browser = None
#         self.context = None

#     async def launch(self, headless=False):
#         playwright = await async_playwright().start()
#         # Optimized for 8GB RAM: No hardware acceleration needed for scraping
#         self.context = await playwright.chromium.launch_persistent_context(
#             user_data_dir=self.user_data_dir,
#             headless=headless,
#             args=[
#                 "--disable-blink-features=AutomationControlled",
#                 "--no-sandbox",
#                 "--disable-dev-shm-usage",
#                 "--disable-gpu" 
#             ]
#         )
#         return self.context

#     async def bulldozer_click(self, page, selector):
#         """Bypasses transparent layers via JS click"""
#         await page.evaluate(f'''(sel) => {{
#             const el = document.querySelector(sel);
#             if (el) {{
#                 el.dispatchEvent(new MouseEvent('click', {{view: window, bubbles: true, cancelable: true}}));
#             }}
#         }}''', selector)

#     async def lexical_type(self, page, selector, text):
#         """Bypasses Facebook's Lexical Editor by injecting text directly into the data model"""
#         await page.focus(selector)
#         await page.evaluate(f'''(text) => {{
#             const el = document.activeElement;
#             const dataTransfer = new DataTransfer();
#             dataTransfer.setData('text/plain', text);
#             el.dispatchEvent(new ClipboardEvent('paste', {{
#                 clipboardData: dataTransfer,
#                 bubbles: true,
#                 cancelable: true
#             }}));
#         }}''', text)

#     async def close(self):
#         if self.context:
#             await self.context.close()

# core/browser.py
# import random, time, os
# from playwright.sync_api import sync_playwright

# class BrowserEngine:
#     # ADDED 'headless=False' HERE
#     def __init__(self, headless=False):
#         self.session_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fb_session'))
#         self.headless = headless
#         self.pw = None
#         self.context = None

#     def start(self):
#         self.pw = sync_playwright().start()
#         self.context = self.pw.chromium.launch_persistent_context(
#             user_data_dir=self.session_path,
#             headless=self.headless,
#             user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
#         )
#         self.page = self.context.new_page()
#         return self.page

#     def stop(self):
#         if self.context:
#             self.context.close()
#         if self.pw:
#             self.pw.stop()

#     def random_wait(self, min_s=3, max_s=6):
#         time.sleep(random.uniform(min_s, max_s))

#     def human_type(self, selector, text):
#         try:
#             self.page.locator(selector).first.focus()
#             self.page.keyboard.type(text, delay=random.randint(50, 100))
#         except Exception as e:
#             print(f"Typing error: {e}")

# core/browser.py
import random, time, os
from playwright.sync_api import sync_playwright

class BrowserEngine:
    def __init__(self, headless=False):
        self.session_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fb_session'))
        self.headless = headless
        self.pw = None
        self.context = None

    def start(self):
        self.pw = sync_playwright().start()
        self.context = self.pw.chromium.launch_persistent_context(
            user_data_dir=self.session_path,
            headless=self.headless,
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        self.page = self.context.new_page()
        return self.page

    def stop(self):
        if self.context: self.context.close()
        if self.pw: self.pw.stop()

    def random_wait(self, min_s=3, max_s=7):
        time.sleep(random.uniform(min_s, max_s))

    def human_type(self, selector, text):
        """Simulates physical keyboard presses with randomized timing"""
        try:
            element = self.page.locator(selector).first
            element.wait_for(state="visible", timeout=5000)
            
            # Click to focus like a human
            element.click(force=True)
            self.random_wait(1, 2)
            
            # Type character by character with hardware-level events
            # Randomized delay between 50ms and 150ms per key
            self.page.keyboard.type(text, delay=random.randint(50, 150))
            print(f"Typed: {text[:20]}...")
        except Exception as e:
            print(f"Typing error: {e}")

    def bulldozer_click(self, selector):
        try:
            self.page.locator(selector).first.click(force=True, timeout=5000)
        except:
            self.page.evaluate(f"document.querySelector('{selector}').click()")

    def kill_blockers(self):
        blockers = ['div[role="dialog"] [aria-label="Close"]', 'div[role="button"]:has-text("Not now")', '[aria-label="Dismiss"]']
        for sel in blockers:
            try:
                el = self.page.locator(sel).first
                if el.is_visible(timeout=500): el.click(force=True)
            except: continue