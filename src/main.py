from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from tools import *
from dotenv import load_dotenv

load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

# Initialize LLM 
llm=init_chat_model("groq:openai/gpt-oss-120b")


# Tools 
tools = [addition, subtraction, multiply, division, power, human_assistance]

#Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
tool_node = ToolNode(tools=[addition, subtraction, multiply, division])
graph_builder.add_node("tools", tool_node)
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")

# memory for chatbot
memory = InMemorySaver()

# Compile graph
graph = graph_builder.compile(checkpointer=memory)


def stream_graph_updates(user_input: str, thread_id: str):
    events = graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        {"configurable": {"thread_id": thread_id}},
        stream_mode="values",
    )
    for event in events:
        event["messages"][-1].pretty_print()

while True:
    try:
        thread_id = "session-1"
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input, thread_id)
    except:
        # fallback if input() is not available
        user_input = "Hi, How can I help you?"
        print("User: " + user_input)    
        stream_graph_updates(user_input, thread_id)
        break

