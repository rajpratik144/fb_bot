import random

class Lurker:
    def __init__(self, engine):
        self.engine = engine

    def simulate_browsing(self):
        destinations = ["https://www.facebook.com/watch", "https://www.facebook.com/groups/feed/","https://www.facebook.com/friends", "https://www.facebook.com/marketplace","https://www.facebook.com/"]
        urls = random.sample(destinations, random.randint(3, 4))
        
        for url in urls:
            print(f"Lurking on: {url}")
            self.engine.page.goto(url)
            self.engine.random_wait(5, 10)
            for _ in range(random.randint(4, 6)):
                self.engine.page.mouse.wheel(0, random.randint(500, 1800))
                self.engine.random_wait(2, 5)