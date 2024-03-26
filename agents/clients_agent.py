from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

examples = [
    {"input": "Listame todos los clientes.", "query": "SELECT * FROM clientes;"},
    {
        "input": "Encuentra todos los clientes que tienen un patrimonio de más de 20000",
        "query": "SELECT * FROM clientes WHERE Patrimonio_estimado > 20000;",
    },
    {
        "input": "Dime la media de patrimonio de los clientes solteros que residan fuera de España.",
        "query": "select avg(Patrimonio_estimado) from clientes where Situacion_familiar = 'soltero' and Tipo_de_cliente ='no residente';",
    },
    {
        "input": "Dime el porcentaje de clientes han manifestado interés por invertir en bienes raices",
        "query": "select (count(case when Preferencias_manifestadas like '%bienes raíces%' then 1 END) * 100.0 / count(*)) from clientes;",
    },
    {
        "input": "Dime los nombres de los clientes que cumplan años esta semana y tengan depositado más de 20000 euros",
        "query": "select Nombre,Apellido,Fecha_de_nacimiento from clientes where strftime('%W',Fecha_de_nacimiento) = strftime('%W','now') and Total_depositado > 20000;",
    },
    {
        "input": "Que clientes con alta tolerancia al riesgo y nivel de renta alto tienen depositado menos de 100000",
        "query": "select * from clientes where Total_depositado < 100000 and Nivel_de_renta = 'alto' and Nivel_tolerancia_riesgo > 7;",
    },
    {
        "input": "Que clientes llevan más de diez años con nosotros, de nivel adquisitivo medio y alto, y tengan menos de 40000€ con nosotros",
        "query": "select Nombre,Apellido,Fecha_de_creacion,Total_depositado,Nivel_de_renta from clientes WHERE Fecha_de_creacion <= strftime('%Y-%m-%d', 'now', '-5 years') and Total_depositado < 40000 and (Nivel_de_renta = 'alto' or Nivel_de_renta = 'medio');",
    },
    {
        "input": "Que cinco clientes son los que más tienen invertido con nosotros",
        "query": "SELECT Nombre, Apellido, Total_depositado from clientes ORDER BY Total_depositado DESC LIMIT 5;",
    },
    {
        "input": "Que tres clientes llevan más tiempo sin operar con nosotros",
        "query": "SELECT Nombre, Apellido, Ultima_actualizacion FROM clientes ORDER BY Ultima_actualizacion ASC LIMIT 3;",
    },
    {
        "input": "Cuantos clientes tenemos",
        "query": 'SELECT COUNT(*) FROM Clientes;',
    },
    {
        "input": "Que clientes con nivel adquisitivo alto son menores de 30 años y viven en España",
        "query": "SELECT Nombre, Apellido, Fecha_de_nacimiento, Nivel_de_renta FROM clientes WHERE Nivel_de_renta = 'alto' AND strftime('%Y', 'now') - strftime('%Y', Fecha_de_nacimiento) < 30 AND Tipo_de_cliente = 'residente';"
    },
]


def create_clients_agent():

    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        OpenAIEmbeddings(),
        FAISS,
        k=5,
        input_keys=["input"],
    )

    system_prefix = """You are an agent designed to interact with a SQL database that contains information about clients of a bank.
    Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
    Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
    You can order the results by a relevant column to return the most interesting examples in the database.
    Never query for all the columns from a specific table, only ask for the relevant columns given the question.
    You have access to tools for interacting with the database.
    Only use the given tools. Only use the information returned by the tools to construct your final answer.
    You MUST double check your query before executing it. If you get an error while executing a query, 
    rewrite the query and try again.

    The fields of the client tables are:
                Nombre TEXT,
                Apellido TEXT,
                Fecha_de_nacimiento DATE,
                Nivel_de_renta TEXT,
                Patrimonio_estimado NUMERIC,
                Total_depositado NUMERIC,
                Situacion_familiar TEXT,
                Tipo_de_cliente TEXT,
                Preferencias_manifestadas TEXT,
                Fecha_de_creacion DATE,
                Ultima_actualizacion DATE,
                Nivel_tolerancia_riesgo INTEGER

    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

    If the question does not seem related to the database, just return "I don't know" as the answer.

    Here are some examples of user inputs and their corresponding SQL queries:"""

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=PromptTemplate.from_template(
            "User input: {input}\nSQL query: {query}"
        ),
        input_variables=["input", "dialect", "top_k"],
        prefix=system_prefix,
        suffix="",
    )

    full_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate(prompt=few_shot_prompt),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    db = SQLDatabase.from_uri("sqlite:///dbclientes.db")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    agent = create_sql_agent(
        llm=llm,
        db=db,
        prompt=full_prompt,
        verbose=True,
        agent_type="openai-tools",
    )

    return agent

if __name__ == "__main__":
    
    client_agent = create_clients_agent()
    client_agent.invoke({"input": "Dame 20 clentes con nivel adquisitivo alto, que sean menores de 20 años y que sean residentes en España"})

