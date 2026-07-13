# core/agent.py
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

class FacebookBrain:
    def __init__(self):
        self.llm = ChatGroq(
            model="openai/gpt-oss-20B", 
            groq_api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.8
        )

    def generate_post(self, topic):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a creative social media manager. "
                       "Write a casual, one-paragraph Facebook post. "
                       "Include 1 relevant emoji. "
                       "IMPORTANT: Keep it under 40 words so it types quickly."
                       "IMPORTANT: After every hashtag you must have a whitespace."),
            ("human", f"Topic: {topic}")
        ])
        chain = prompt | self.llm
        response = chain.invoke({})
        return response.content
    
    def generate_ai_image(self, prompt_text):
        """Returns a URL for an AI generated image based on the topic"""
        import urllib.parse
        encoded_prompt = urllib.parse.quote(prompt_text)
        return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"