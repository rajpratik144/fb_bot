import csv, random, os

class TopicManager:
    def __init__(self, filename="topics.csv"):
        self.filename = filename

    def get_random_topic(self):
        if not os.path.exists(self.filename):
            return "Life in 2025"
        
        topics = []
        with open(self.filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row: topics.append(row[0])
        
        # Avoid the header if it exists
        if topics[0].lower() == "topic": topics.pop(0)
        return random.choice(topics)