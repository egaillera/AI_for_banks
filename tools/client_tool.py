from langchain.agents import tool

@tool
def get_client_info(client_id:str) -> str:
    """ Returns relevant information about a client"""
    return "El cliente tiene baja tolerancia al riesgo y le gustan los productos de BBVA"