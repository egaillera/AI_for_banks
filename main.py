from sys import prefix
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent, initialize_agent, AgentType
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate

from dotenv import load_dotenv

from tools.client_tool import get_client_info
from tools.portfolio_tool import get_portfolio_info
from tools.product_tool import get_product_info, get_product_tool

from agents.clients_agent import create_clients_agent


if __name__ == "__main__":
    load_dotenv()

    tools = [get_client_info, get_portfolio_info, get_product_info]

    # Get the prompt to use - you can modify this!
    prompt = hub.pull("hwchase17/react")

    react_template = """You are a financial assistant. Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

    react_prompt = PromptTemplate.from_template(react_template)

    clients_agent = create_clients_agent()

    # Choose the LLM to use
    #llm = ChatOpenAI()
    #llm = ChatAnthropic(model='claude-3-opus-20240229')

    # Construct the ReAct agent
    #main_agent = create_react_agent(llm, tools, react_prompt)
    grand_agent = initialize_agent(
        tools = [
            Tool(
                name = "ClientsAgent",
                func = clients_agent.run,
                description = """ useful when you need to get information about clients. If needed, 
                You can send to this tool a complete query in natural language, 
                not just the name of the client"""
            ),
            Tool(
                name = "ProductTool",
                func = get_product_info,
                description = """ useful when you need to get information about financial product. If 
                needed, send to this tool a complete query in natural language, not just the name of the product"""
            ),
        ],
        #llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
        llm = ChatAnthropic(model='claude-3-opus-20240229'),
        agent_type = AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose = True
    )

    # Create an agent executor by passing in the agent and tools
    #agent_executor = AgentExecutor(agent=grand_agent, tools=tools, verbose=True, handle_parsing_errors=True)

    grand_agent.invoke({"input":"que productos hay parecidos al RENTA 4 GLOBAL"})

    