from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field, ValidationError
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from anthropic import BadRequestError
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool,wiki_tool,save_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str] 

# llm=ChatOpenAI(model="gpt-4o-mini")

llm2 = ChatOpenAI(
    # model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

# print("Loaded key:", os.getenv("ANTHROPIC_API_KEY"))  # check if it's loaded

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# response = llm2.invoke("What is the capital of France?")
# print(response.content)

# print("sofkokfor")


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert research assistant. 
        Your task is to gather comprehensive information on a given topic, including a detailed summary, key points, relevant sources, and tools used for research. 
        Wrap the outputs in this format and provide no other text.
        {format_instructions}
        """,
    ),
    ("placeholder", "{chat_history}"),
    ("human", "{Query}"),
    ("placeholder", "{agent_scratchpad}")
]).partial(format_instructions=parser.get_format_instructions())

tools=[search_tool , wiki_tool, save_tool]

agent = create_tool_calling_agent(
    llm=llm2,
    tools=tools,
    prompt=prompt

    # output_parser=parser
)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
)
while True:
    query = input("What can I help you? ")

    raw_response = agent_executor.invoke({"Query": query})
    # print("Raw response:", raw_response)
    try:
        structured_response = parser.parse(raw_response.get("output",raw_response))#["output"])
        print(structured_response)
        print("\n---------------------------------------------------------------------------\n")

    except Exception as e:
        print("Error parsing response:", e, "Raw response",raw_response)

# raw_response = agent_executor.invoke({"Query": "Provide a detailed search about Egyptian history."})
# print("Raw response:", raw_response)