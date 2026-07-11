# tools/feed.py
class FeedPoster:
    def __init__(self, engine):
        self.engine = engine

    def post_text(self, content):
        page = self.engine.page
        try:
            page.goto("https://www.facebook.com/")
            self.engine.random_wait(7, 10)
            self.engine.kill_blockers()

            # 1. Open Post Box
            trigger = 'div[role="main"] span:has-text("What\'s on your mind")'
            self.engine.bulldozer_click(trigger)
            self.engine.random_wait(4, 6)

            # 2. Human Typing
            # Target the Lexical Editor div specifically
            input_sel = 'div[data-lexical-editor="true"]'
            print("Commencing human typing sequence...")
            self.engine.human_type(input_sel, content)
            
            # 3. Post-typing pause (simulating a human reading the post)
            self.engine.random_wait(3, 5)

            # 4. Click Post
            post_btn = 'div[role="dialog"] div[aria-label="Post"]'
            self.engine.bulldozer_click(post_btn)
            
            # 5. Verify the dialog closes
            page.wait_for_selector('div[role="dialog"]', state="hidden", timeout=15000)
            return True
        except Exception as e:
            print(f"Post Failed: {e}")
            return False