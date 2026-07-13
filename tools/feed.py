# # tools/feed.py
# import re
# import os

# class FeedPoster:
#     def __init__(self, engine):
#         self.engine = engine

#     def post_with_media(self, content, media_path=None):
#         page = self.engine.page
#         try:
#             # --- STEP 1: INITIALIZATION ---
#             print("🏠 Navigating to Home...")
#             page.goto("https://www.facebook.com/")
#             self.engine.random_wait(8, 10)
#             self.engine.clear_all_dialogs()

#             # --- STEP 2: OPEN BOX ---
#             # Using the exact placeholder text from your HTML
#             trigger = 'div[role="main"] span:has-text("What\'s on your mind")'
#             self.engine.bulldozer_click(trigger)
#             self.engine.random_wait(5, 7)

#             # --- STEP 3: UPLOAD MEDIA ---
#             if media_path and os.path.exists(media_path):
#                 print(f"📤 Injecting media...")
#                 # Target the file input inside the dialog
#                 page.locator('div[role="dialog"] input[type="file"]').set_input_files(media_path)
                
#                 # Wait for the 'Edit' button (visible in your HTML) to confirm upload
#                 self.engine.wait_for_upload()
#                 self.engine.random_wait(3, 5)

#             # --- STEP 4: THE "JOLT" (Focus/Blur Reset) ---
#             print("⚡ Resetting editor state...")
#             # We use JS to force the editor to 'Blur' (lose focus) and 'Focus' (regain)
#             # This mimics you clicking outside and back in.
#             page.evaluate("""() => {
#                 const editor = document.querySelector('div[data-lexical-editor="true"]');
#                 if (editor) {
#                     editor.blur(); 
#                     setTimeout(() => { editor.focus(); }, 100);
#                 }
#             }""")
#             self.engine.random_wait(2, 3)

#             # --- STEP 5: TEXT INJECTION ---
#             print("⌨️ Injecting text...")
#             # We use the specific Lexical selector from your HTML
#             input_sel = 'div[data-lexical-editor="true"]'
            
#             # Final text cleanup
#             safe_content = re.sub(r'(#\w+)', r'\1 ', content) + "  "
            
#             # Focus and Inject
#             page.locator(input_sel).last.focus()
#             self.engine.lexical_type(safe_content)
#             self.engine.random_wait(3, 5)

#             # --- STEP 6: DISPATCH ---
#             # Using the exact Post label from your HTML
#             post_btn = 'div[role="dialog"] div[aria-label="Post"]'
#             print("🚀 Executing Post...")
            
#             # The JS bulldozer is necessary because of the transparent layers in your HTML
#             self.engine.js_click(post_btn)
            
#             # --- STEP 7: VERIFY ---
#             try:
#                 page.wait_for_selector('div[role="dialog"]', state="hidden", timeout=12000)
#                 print("✅ POST SUCCESSFUL.")
#                 if media_path: os.remove(media_path)
#                 return True
#             except:
#                 print("⚠️ Dialog still visible, but post may have been sent.")
#                 return True

#         except Exception as e:
#             print(f"❌ Failure: {e}")
#             return False

# THE ABOVE IS THE MOST STABLE VERSION

# tools/feed.py
import re, os

class FeedPoster:
    def __init__(self, engine):
        self.engine = engine

    def post_with_media(self, content, media_path=None):
        page = self.engine.page
        try:
            page.goto("https://www.facebook.com/")
            self.engine.random_wait(8, 10)
            self.engine.clear_all_dialogs()

            # 1. Open the box
            trigger = 'div[role="main"] span:has-text("What\'s on your mind")'
            self.engine.bulldozer_click(trigger)
            self.engine.random_wait(5, 7)

            # 2. UPLOAD MEDIA FIRST
            if media_path and os.path.exists(media_path):
                print(f"📤 Injecting media...")
                page.locator('div[role="dialog"] input[type="file"]').set_input_files(media_path)
                
                # Wait for the visual Edit button
                page.wait_for_selector('text="Edit"', timeout=30000)
                print("📸 Image visible in UI.")
                
                # IMPORTANT: Wait for the 'Technical Lock'
                post_btn_sel = 'div[role="dialog"] div[aria-label="Post"]'
                self.engine.wait_for_attachment_lock(post_btn_sel)
                
                # Extra 5s buffer for your 2015 Mac to sync the data
                self.engine.random_wait(4, 6)

            # 3. INJECT TEXT SECOND (This forces the editor to refresh)
            input_sel = 'div[data-lexical-editor="true"]'
            print("⌨️ Injecting text...")
            page.locator(input_sel).last.click(force=True)
            self.engine.random_wait(2, 3)
            self.engine.lexical_type(content)
            self.engine.random_wait(4, 6)

            # 4. FINAL DISPATCH (Native Click Sequence)
            # Instead of a fast JS click, we simulate a human hovering and clicking
            print("🚀 Dispatching...")
            post_btn = page.locator('div[role="dialog"] div[aria-label="Post"]').last
            
            # Hover forces the browser to verify the button state
            post_btn.hover()
            self.engine.random_wait(1, 2)
            
            # Use native click with force=True (much more 'human' than JS Bulldozer)
            post_btn.click(force=True)
            
            # 5. VERIFY
            try:
                page.wait_for_selector('div[role="dialog"]', state="hidden", timeout=15000)
                print("✅ SUCCESS: Post with Media is LIVE.")
                if media_path: os.remove(media_path)
                return True
            except:
                print("❌ UI stuck. Image might have failed to attach.")
                return False

        except Exception as e:
            print(f"❌ Error: {e}")
            return False