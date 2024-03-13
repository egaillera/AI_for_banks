from langchain.agents import tool
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain_anthropic import ChatAnthropic
import os


@tool
def get_product_info(description:str) -> str:
    """ Get relevant information about a financial product """

    vectorstore_path = "/Users/egi/tmp/FinGuruDocs/docs.index"
    embeddings = OpenAIEmbeddings()

    if os.path.exists(vectorstore_path):
         vectorstore = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
    
    
    template = """You are a financial assistant for question-answering tasks related to investment funds. 
                Use the following pieces of retrieved context to answer the question. 
                The answer should be always in Spanish.
                Try to provide three recommendations adapted to the request
                If you found a fund, explain its features a bit and say which bank/entity issues it.
                If you don't know the answer, just say that you don't know. 
                Use six sentences maximum and keep the answer concise.
                Question: {question} 
                Context: {context} 
                Answer:
                """
    prompt = ChatPromptTemplate.from_template(template)
    #llm = ChatOpenAI(model_name = "gpt-3.5-turbo")
    llm = ChatAnthropic(model='claude-3-opus-20240229')

    # It's possible to adjust the number of results of the retriever (default is 4)
    # vectorstore.as_retriever(search_kwargs={"k": 1}))
    rag_chain = (
        {"context": vectorstore.as_retriever(),  "question": RunnablePassthrough()} 
        | prompt 
        | llm
        | StrOutputParser() 
    )

    return rag_chain.invoke(description)

    

