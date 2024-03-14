from typing import Any
from langchain.agents import tool
#from langchain.chains.llm import LLMChain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
#from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate
#from langchain.schema.runnable import RunnablePassthrough
from langchain_anthropic import ChatAnthropic
from langchain.chains.combine_documents import create_stuff_documents_chain
#from langchain import hub
import os


@tool
def get_product_info(description:str) -> Any:
    """ Get relevant information about a financial product. Returns information, 
     but also a list with documents in which this information is based """

    # Documents are stored as embeddings here
    vectorstore_path = "/Users/egi/tmp/FinGuruDocs/docs.index"
    embeddings = OpenAIEmbeddings()

    if os.path.exists(vectorstore_path):
         vectorstore = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
    
    # Create prompt to replace the hub.pull("langchain-ai/retrieval-qa-chat") prompt.
    # Must contain {input} and {context} variables
    template = """You are a financial assistant that provides information about financial products. 
                Use the following pieces of retrieved context to answer the question. 
                The answer should be always in Spanish.
                Try to provide three recommendations adapted to the request
                If you found a product, explain its features a bit and say which bank/entity issues it.
                If you don't know the answer, just say that you don't know. 
                Use six sentences maximum and keep the answer concise.
                Question: {input} 
                Context: {context} 
                Answer:
                """
    prompt = ChatPromptTemplate.from_messages([("system", template)])


    llm = ChatOpenAI(model_name = "gpt-3.5-turbo")
    #llm = ChatAnthropic(model='claude-3-opus-20240229')

    # Chain to prepare documents to be passed to the model. Documents will be
    # inserted in the {context} variable of the prompt
    combine_docs_chain = create_stuff_documents_chain(llm,prompt)

    # It's possible to adjust the number of results of the retriever (default is 4)
    # vectorstore.as_retriever(search_kwargs={"k": 1}))
    rag_chain = create_retrieval_chain(vectorstore.as_retriever(),combine_docs_chain=combine_docs_chain)
    
    res = rag_chain.invoke({"input":description})
    return res['answer'] # To return also the documents: ,res['context']
    

