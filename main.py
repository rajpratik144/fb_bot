# # main.py
# import time, os, random
# from core.browser import BrowserEngine
# from core.agent import FacebookAgent
# from tools.messenger import MessengerTool
# from tools.feed import FeedTool
# from dotenv import load_dotenv

# load_dotenv()

# def run_simple_bot():
#     engine = BrowserEngine(headless=False)
#     ai_brain = FacebookAgent()
    
#     try:
#         engine.start()
#         messenger = MessengerTool(engine)
#         feed = FeedTool(engine)
        
#         print("Listening for messages...")
#         engine.page.goto("https://www.facebook.com/messages/t/1742551683409374") # Your self-chat
#         engine.random_wait(5, 8)
        
#         last_seen = ""
        
#         # Run for 10 minutes
#         end_time = time.time() + 600
#         while time.time() < end_time:
#             current_msg = messenger.get_latest_message()
            
#             if current_msg and current_msg != last_seen:
#                 print(f"New Message: {current_msg}")
#                 last_seen = current_msg
                
#                 # Ask AI what to do
#                 # (Using your existing decide_action method)
#                 response = ai_brain.decide_action(current_msg, [], "Boss", True)
                
#                 if "COMMAND:POST" in response:
#                     post_text = response.split("|")[-1].strip()
#                     feed.create_text_post(post_text)
#                     messenger.send_reply("Post created!")
#                 else:
#                     messenger.send_reply(response)
                    
#             time.sleep(5)

#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         engine.stop()

# if __name__ == "__main__":
#     run_simple_bot()

# main.py
import os, time, random, datetime
from dotenv import load_dotenv
from core.browser import BrowserEngine
from core.agent import FacebookBrain
from core.topics import TopicManager
from tools.lurker import Lurker
from tools.feed import FeedPoster

load_dotenv()

def run_autonomous_session():
    engine = BrowserEngine(headless=False)
    brain = FacebookBrain()
    topics = TopicManager()
    
    try:
        engine.start()
        lurker = Lurker(engine)
        poster = FeedPoster(engine)

        # 1. Human Simulation: Visit random pages first
        lurker.simulate_browsing()

        # 2. Select Topic & Generate Content
        topic = topics.get_random_topic()
        content = brain.generate_post(topic)
        print(f"Goal: Post about '{topic}'")

        # 3. Action: Post with Human Typing
        if poster.post_text(content):
            print(f"Success at {datetime.datetime.now().strftime('%H:%M:%S')}")
        else:
            print("Failure.")

    except Exception as e:
        print(f"Session Error: {e}")
    finally:
        engine.stop()

if __name__ == "__main__":
    print("🤖 UNIVERSAL AGENT v3.1 ACTIVE")
    while True:
        # Plan for 8 to 10 posts in a cycle
        daily_count = random.randint(8, 10)
        print(f"\nPlan: {daily_count} posts for this cycle.")

        for i in range(daily_count):
            run_autonomous_session()
            
            # Wait for 1.5 - 2.5 hours
            # wait_time = random.randint(5400, 9000) 
            wait_time = random.randint(60, 120) 

            
            # For testing, you can change this to random.randint(60, 120)
            
            wake_time = datetime.datetime.now() + datetime.timedelta(seconds=wait_time)
            print(f"Next task at: {wake_time.strftime('%H:%M:%S')}")
            time.sleep(wait_time)