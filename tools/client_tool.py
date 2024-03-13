from langchain.agents import tool

@tool
def get_client_info(client_id:str) -> str:
    """ Returns relevant information about a client"""
    return "El cliente solo ha invertido en letras del tesoro y es averso al riesgo"