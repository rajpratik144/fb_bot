import os
import facebook
import json
from typing import TypedDict, List
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END

load_dotenv()

# --- INITIALIZE ---
llm = ChatGroq(model="openai/gpt-oss-20B", groq_api_key=os.getenv("GROQ_API_KEY"))
graph_api = facebook.GraphAPI(access_token=os.getenv("FB_PAGE_TOKEN"))
PAGE_ID = graph_api.get_object('me')['id']
MEMORY_FILE = "replied_ids.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f: return json.load(f)
    return []

def save_memory(replied_ids):
    with open(MEMORY_FILE, 'w') as f: json.dump(replied_ids, f)

class AgentState(TypedDict):
    comments: List[dict]
    replies: List[dict]
    processed_ids: List[str]

# NODE 1: Deep Scan (Posts -> Comments -> Replies)
def fetch_comments_node(state: AgentState):
    print("--- DEEP SCANNING FOR NEW COMMENTS & REPLIES ---")
    replied_ids = load_memory()
    posts = graph_api.get_connections(id='me', connection_name='feed')
    all_new_interactions = []
    
    for post in posts['data']:
        # Fetch Top-Level Comments
        comments = graph_api.get_connections(id=post['id'], connection_name='comments')
        
        for c in comments['data']:
            # 1. Check the Top-Level Comment
            if c['from']['id'] != PAGE_ID and c['id'] not in replied_ids:
                all_new_interactions.append(c)
            
            # 2. CHECK FOR REPLIES TO THIS COMMENT (The "Follow-ups")
            replies = graph_api.get_connections(id=c['id'], connection_name='comments')
            for r in replies['data']:
                if r['from']['id'] != PAGE_ID and r['id'] not in replied_ids:
                    print(f"Found a follow-up reply: '{r['message']}'")
                    all_new_interactions.append(r)
    
    print(f"Found {len(all_new_interactions)} new interactions to handle.")
    return {"comments": all_new_interactions, "processed_ids": replied_ids}

# NODE 2: AI Brain (Remains the same)
def analyze_and_respond_node(state: AgentState):
    if not state['comments']: return {"replies": []}
    print("--- AI IS THINKING ---")
    replies = []
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a friendly AI Agent. Reply briefly (under 15 words). "
                   "If someone asks for money or help, be polite but firm that you are just a demo bot."),
        ("human", "{comment_text}")
    ])
    chain = prompt | llm

    for comment in state['comments']:
        response = chain.invoke({"comment_text": comment['message']})
        replies.append({"comment_id": comment['id'], "text": response.content})
    return {"replies": replies}

# NODE 3: Execute (Remains the same)
def post_replies_node(state: AgentState):
    replied_ids = state['processed_ids']
    for reply in state['replies']:
        graph_api.put_object(parent_object=reply['comment_id'], connection_name='comments', message=reply['text'])
        graph_api.put_object(parent_object=reply['comment_id'], connection_name='likes')
        replied_ids.append(reply['comment_id'])
    save_memory(replied_ids)
    return {"processed_ids": replied_ids}

# --- GRAPH SETUP ---
workflow = StateGraph(AgentState)
workflow.add_node("fetch_comments", fetch_comments_node)
workflow.add_node("analyze_comments", analyze_and_respond_node)
workflow.add_node("post_replies", post_replies_node)
workflow.set_entry_point("fetch_comments")
workflow.add_edge("fetch_comments", "analyze_comments")
workflow.add_edge("analyze_comments", "post_replies")
workflow.add_edge("post_replies", END)
app = workflow.compile()

if __name__ == "__main__":
    app.invoke({"comments": [], "replies": [], "processed_ids": []})