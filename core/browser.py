# core/browser.py
import random, time, os, requests
from playwright.sync_api import sync_playwright

class BrowserEngine:
    def __init__(self, headless=False):
        self.session_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fb_session'))
        self.headless = headless

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
        self.pw.stop()

    def random_wait(self, min_s=3, max_s=6): time.sleep(random.uniform(min_s, max_s))

    def lexical_type(self, text):
        """Standard Lexical Injection with Triple-Lock Focus"""
        print("💉 Attempting Triple-Lock Injection...")
        try:
            # We use the selector for the editor
            selector = 'div[data-lexical-editor="true"]'
            
            # 1. Physical Focus & Click via Playwright
            target = self.page.locator(selector).last
            target.focus()
            target.click(force=True)
            self.random_wait(1, 2)

            # 2. Internal JS Injection
            self.page.evaluate("""(txt) => {
                const editor = document.querySelector('div[data-lexical-editor="true"]');
                if (editor) {
                    editor.focus();
                    // Clear any existing selection and put cursor at start
                    const selection = window.getSelection();
                    const range = document.createRange();
                    range.selectNodeContents(editor);
                    range.collapse(false); // Put cursor at the end
                    selection.removeAllRanges();
                    selection.addRange(range);
                    
                    // Inject the text
                    document.execCommand('insertText', false, txt);
                    
                    // Dispatch events so React/Lexical 'sees' the change
                    editor.dispatchEvent(new Event('input', { bubbles: true }));
                    editor.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }""", text)
            print("✅ Injection command sent.")
        except Exception as e:
            print(f"❌ Injection Error: {e}")

    def bulldozer_click(self, selector):
        try:
            self.page.locator(selector).first.click(force=True, timeout=5000)
        except:
            self.page.evaluate(f"document.querySelector('{selector}').click()")

    def kill_blockers(self):
        for sel in ['div[role="button"]:has-text("Delete draft")', 'div[role="dialog"] [aria-label="Close"]', 'div[role="button"]:has-text("Not now")']:
            try:
                el = self.page.locator(sel).last
                if el.is_visible(timeout=500): el.click(force=True)
            except: continue

    def download_media(self, url, filename):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'temp_media', filename))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in r: f.write(chunk)
            return path
        return None
    
    def js_click(self, selector):
        try:
            self.page.evaluate(f"document.querySelector('{selector}').click()")
        except: pass


    def wait_for_button_ready(self, selector, timeout=20000):
        """Waits until a button is no longer technically disabled."""
        print("⏳ Waiting for 'Post' button to enable...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                btn = self.page.locator(selector).last
                # Facebook sets aria-disabled="true" while the image is processing
                state = btn.get_attribute("aria-disabled")
                if state == "false" or state is None:
                    print("✅ Post button is now READY.")
                    return True
                time.sleep(1)
            except:
                continue
        return False
    
    def clear_all_dialogs(self):
        """Force-closes any existing dialog boxes before starting a new task."""
        print("🧹 Cleaning up ghost dialogs...")
        try:
            # Facebook uses role="dialog" for post boxes and popups
            dialogs = self.page.locator('div[role="dialog"]').all()
            for dialog in dialogs:
                # Find the close button inside this specific dialog
                close_btn = dialog.locator('[aria-label="Close"], [aria-label="Exit"]').first
                if close_btn.is_visible(timeout=500):
                    close_btn.click(force=True)
                    self.random_wait(1, 2)
            
            # Additional safety: hit Escape twice
            self.page.keyboard.press("Escape")
            self.page.keyboard.press("Escape")
        except:
            pass

    def wait_for_attachment_lock(self, selector, timeout=30000):
        """Waits until the Post button officially recognizes the image attachment."""
        print("⏳ Waiting for Facebook to lock the image attachment...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                btn = self.page.locator(selector).last
                # Facebook sets aria-disabled="true" while processing the image.
                # It only turns to "false" (or disappears) when the image is READY to be sent.
                is_disabled = btn.get_attribute("aria-disabled")
                
                if is_disabled == "false" or is_disabled is None:
                    print("✅ Image locked and button ENABLED.")
                    return True
                
                time.sleep(1) # Check every second
            except:
                continue
        print("⚠️ Warning: Attachment lock timed out.")
        return False