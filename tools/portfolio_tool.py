from langchain.agents import tool


@tool
def get_portfolio_info(client_id:str) -> str:
    """ Returns relevant information about a client portfolio"""
    return "Solo hay transacciones relacionadas con depositos"