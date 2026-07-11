# import os
# from langchain_groq import ChatGroq
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.messages import HumanMessage, AIMessage

# class FacebookAgent:
#     def __init__(self):
#         self.llm = ChatGroq(model="openai/gpt-oss-20B", groq_api_key=os.getenv("GROQ_API_KEY"), temperature=0.7)

#     def decide_action(self, incoming_text, history_data, partner_name, is_owner, has_media=False):
#         history = [HumanMessage(content=h['content']) if h['role'] == 'user' else AIMessage(content=h['content']) for h in history_data]
        
#         media_status = "The Boss HAS attached a photo." if has_media else "No photo attached."
        
#         # STRICT INSTRUCTIONS TO AVOID 400 ERROR
#         system_msg = (
#             f"You are Pratik's Assistant. You are talking to {partner_name}. {media_status} "
#             "IMPORTANT: Output ONLY plain text. Never use JSON or tool-calling blocks. "
#         )
        
#         if is_owner:
#             system_msg += (
#                 "If Pratik asks to POST: Reply exactly 'COMMAND:POST | [Content]'. "
#                 "If an image is needed but missing, use 'COMMAND:POST | WITH_IMAGE | [Content]'. "
#                 "Keep the post under 50 words. Be direct."
#             )
#         else:
#             system_msg += "Be casual, use Hinglish, keep it under 10 words. Do not help with posts."

#         prompt = ChatPromptTemplate.from_messages([
#             ("system", system_msg),
#             MessagesPlaceholder(variable_name="history"),
#             ("human", "{input}")
#         ])

#         response = (prompt | self.llm).invoke({"history": history, "input": incoming_text})
#         return response.content

#     def generate_ai_image(self, prompt_text):
#         import urllib.parse
#         return f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt_text)}?width=1024&height=1024&nologo=true"



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
                       "IMPORTANT: Keep it under 40 words so it types quickly."),
            ("human", f"Topic: {topic}")
        ])
        chain = prompt | self.llm
        response = chain.invoke({})
        return response.content