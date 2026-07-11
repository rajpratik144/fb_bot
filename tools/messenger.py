import re

class MessengerTool:
    def __init__(self, browser_engine):
        self.engine = browser_engine

    def get_latest_message(self):
        try:
            # Just find all text bubbles and take the last one
            bubbles = self.engine.page.locator('div[dir="auto"]').all()
            if not bubbles: return None
            
            last_text = bubbles[-1].inner_text().strip()
            
            # Basic check: if it's too short or a timestamp, ignore
            if len(last_text) < 2 or ":" in last_text: return None
            
            return last_text
        except:
            return None

    def send_reply(self, text):
        try:
            selector = 'div[role="textbox"]'
            self.engine.page.locator(selector).first.click()
            self.engine.page.keyboard.type(text)
            self.engine.page.keyboard.press("Enter")
            return True
        except:
            return False