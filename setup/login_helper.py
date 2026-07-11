import os
from playwright.sync_api import sync_playwright

def run_login():
    # We point to the session folder in the root
    session_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fb_session'))
    
    if not os.path.exists(session_path):
        os.makedirs(session_path)

    with sync_playwright() as p:
        # Launch headed so you can see and log in
        context = p.chromium.launch_persistent_context(
            user_data_dir=session_path,
            headless=False,
            viewport={'width': 1280, 'height': 720}
        )
        page = context.new_page()
        page.goto("https://www.facebook.com")
        
        print("\n" + "="*30)
        print("ACTION REQUIRED: Log into Facebook manually.")
        print("1. Enter your credentials.")
        print("2. Handle 2FA if needed.")
        print("3. Once you see your home feed, press ENTER here.")
        print("="*30 + "\n")
        
        input("Press Enter after you have logged in...")
        
        context.close()
        print(f"✅ Success! Session saved in {session_path}")

if __name__ == "__main__":
    run_login()