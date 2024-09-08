from dotenv import load_dotenv, find_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.llms import OpenAI  

load_dotenv(find_dotenv())

#  the prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world class technical documentation writer."),
    ("user", "{input}")
])

# Initialize the OpenAI LLM
llm = OpenAI()

# Combine the prompt and LLM
chain = prompt | llm

# Invoke the chain with the input
response = chain.invoke({"input": "how can langsmith help with testing?"})
print(response)
