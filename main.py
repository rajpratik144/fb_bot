# main.py
import os
import time
import random
import datetime
import traceback
from dotenv import load_dotenv

# Core Module Imports
from core.browser import BrowserEngine
from core.agent import FacebookBrain
from core.topics import TopicManager
from core.db import init_db, log_successful_post, get_today_post_count

# Tool Module Imports
from tools.lurker import Lurker
from tools.feed import FeedPoster

load_dotenv()

def execute_autonomous_session():
    """
    A complete autonomous cycle: 
    1. Start Browser -> 2. Lurk -> 3. Think -> 4. Download -> 5. Post -> 6. Log
    """
    # init_db ensures app_memory.db exists
    init_db()
    
    # Set headless=True for background server deployment
    engine = BrowserEngine(headless=False) 
    brain = FacebookBrain()
    topics = TopicManager()
    
    media_path = None
    
    try:
        print(f"\n🚀 STARTING AUTONOMOUS SESSION: {datetime.datetime.now().strftime('%H:%M:%S')}")
        engine.start()
        
        # lurker = Lurker(engine)
        poster = FeedPoster(engine)

        # --- PHASE 1: HUMAN SIMULATION (LURKING) ---
        # Mimics a real user scrolling through random parts of Facebook
        # lurker.simulate_browsing()

        # --- PHASE 2: BRAIN & CONTENT GENERATION ---
        topic = topics.get_random_topic()
        print(f"🎯 Selected Topic from CSV: {topic}")
        
        # Generate the caption using LLM
        content = brain.generate_post(topic)
        
        # Generate the AI Image (Synthesize -> URL -> Download)
        print("🎨 Brain is synthesizing AI visuals...")
        image_url = brain.generate_ai_image(topic)
        media_path = engine.download_media(image_url, "autonomous_upload.jpg")

        # --- PHASE 3: EXECUTION (THE DISPATCH) ---
        print("🚀 Navigating to Feed for dispatch...")
        # Uses the improved 'Media-First' and 'Technical Lock' logic
        success = poster.post_with_media(content, media_path)

        if success:
            # --- PHASE 4: RECORDING SUCCESS ---
            log_successful_post(topic)
            total_today = get_today_post_count()
            print(f"✅ SUCCESS: Post is live. Daily Total: {total_today}")
        else:
            print("❌ FAILURE: Post sequence did not complete.")

    except Exception as e:
        print(f"🚨 CRITICAL SESSION ERROR: {e}")
        traceback.print_exc()
    finally:
        # Crucial for 2015 MacBook Air: Completely kill browser to free RAM
        print("🧹 Cleaning up session resources...")
        engine.stop()

def daily_heartbeat():
    """Calculates a random daily plan of 8-10 posts and executes it."""
    print("\n" + "="*50)
    print("🤖 UNIVERSAL AI AGENT v3.4: 24/7 MODE ACTIVE")
    print("="*50 + "\n")

    cycle_num = 0
    while True:
        cycle_num += 1
        # Manager Requirement: 8-10 posts per cycle
        posts_to_make = random.randint(8, 10)
        print(f"📅 NEW CYCLE #{cycle_num}: Plan is to post {posts_to_make} times.")

        for i in range(posts_to_make):
            execute_autonomous_session()
            
            # --- STOCHASTIC WAIT TIMER ---
            # Random wait between tasks (90 to 180 minutes for production)
            # For your demo/testing, use (60, 120) seconds
            wait_time = random.randint(60, 120) 
            
            wake_up = datetime.datetime.now() + datetime.timedelta(seconds=wait_time)
            print(f"\n💤 Task {i+1}/{posts_to_make} complete. Sleeping until {wake_up.strftime('%H:%M:%S')}")

            # Visual Countdown
            for remaining in range(wait_time, 0, -1):
                print(f"⏳ Heartbeat resumes in: {remaining}s   ", end="\r")
                time.sleep(1)
            
            print("\n🚀 Waking up for next task...")

if __name__ == "__main__":
    try:
        daily_heartbeat()
    except KeyboardInterrupt:
        print("\n👋 Agent shutdown by user.")