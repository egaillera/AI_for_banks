from langchain.agents import tool
from pydantic.v1 import BaseModel, Field


class ClientInput(BaseModel):
    client_id: str = Field(description="ID of the client to look for")

@tool(args_schema=ClientInput)
def get_client_info(client_id:str) -> str:
    """ Returns relevant information about a client"""
    return "El cliente tiene productos de BBVA con baja tolerancia al riesgo"