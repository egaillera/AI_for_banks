from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_openai import OpenAI, ChatOpenAI
from langchain_anthropic import ChatAnthropic

from dotenv import load_dotenv

from tools.client_tool import get_client_info
from tools.portfolio_tool import get_portfolio_info
from tools.product_tool import get_product_info


if __name__ == "__main__":
    load_dotenv()

    tools = [get_client_info, get_portfolio_info, get_product_info]

    # Get the prompt to use - you can modify this!
    prompt = hub.pull("hwchase17/react")

    # Choose the LLM to use
    #llm = ChatOpenAI()
    llm = ChatAnthropic(model='claude-3-opus-20240229')

    # Construct the ReAct agent
    main_agent = create_react_agent(llm, tools, prompt)

    # Create an agent executor by passing in the agent and tools
    agent_executor = AgentExecutor(agent=main_agent, tools=tools, verbose=True)

    agent_executor.invoke({"input":"dime productos que ofrezca BBVA apropiados para Angel Fernandez"})

    