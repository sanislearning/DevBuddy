import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

#Initially we need to create a StateGraph which represents the struture of what we are building. The node represents an llm
#and the functions our chatbot can call and edges specify how the bot should transition
#between these functions

#Below is copy pasted boilerplate from the official site
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]
#till here

graph_builder = StateGraph(State)

load_dotenv()
GOOGLE_API_KEY=os.getenv("GEMINI_API_KEY")

llm=init_chat_model("google_genai:gemini-2.0-flash")
