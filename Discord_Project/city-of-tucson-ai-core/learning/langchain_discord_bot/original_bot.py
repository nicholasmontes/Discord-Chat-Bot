
import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
import os
from langchain.prompts import SystemMessagePromptTemplate, PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.schema import HumanMessage

load_dotenv(find_dotenv())

# Define the folder path and file paths
folder_path = "./learning/langchain_discord_bot/documents"
file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.txt')]

# Initialize the chat model and embeddings
embeddings = OpenAIEmbeddings()
chat = ChatOpenAI(temperature=0)

# Define the prompt template
prompt_template = """I'm an AI-Core Discord chatbot. 

You are role-playing as the "AI-Core Discord chatbot", an AI designed to provide comprehensive and accurate information for AI-CORE. 
You will respond to users' queries about various aspects of AI-CORE's projects and members information.

## Refer to the .txt files for information. aicore_website.txt is information for the company. The other txt files include employee's id, name, username, and messages. 


## Introduction
When started, give this information to users.

"Welcome to AI-Core Discord chatbot. Feel free to ask any questions on AI-CORE!"

{context}

Please provide the most suitable response for the user's question.
Answer:"""

prompt = PromptTemplate(
    template=prompt_template, input_variables=["context"]
)
system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)

# Set up Discord bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def process_files(file_paths):
    """Process multiple .txt files"""
    all_documents = []
    for file_path in file_paths:
        try:
            print(f"Processing {file_path}...")
            loader = TextLoader(file_path)
            documents = loader.load()
            all_documents.extend(documents)
            print(f"Loaded {len(documents)} documents from {file_path}")
        except Exception as e:
            print(f"Error loading {file_path}: {e}")

    # Split the documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=100)
    texts = text_splitter.split_documents(all_documents)

    # Create embeddings and retriever
    retriever = Chroma.from_documents(texts, embeddings).as_retriever()
    return retriever

@bot.command()
async def question(ctx, *, question):
    try:
        retriever = await process_files(file_paths)
        
        if retriever:
            docs = retriever.get_relevant_documents(query=question)
            formatted_prompt = system_message_prompt.format(context=docs)

            messages = [formatted_prompt, HumanMessage(content=question)]
            result = chat(messages)
            await ctx.send(result.content)
        else:
            await ctx.send("Failed to process the documents.")
    except Exception as e:
        print(f"Error occurred: {e}")
        await ctx.send("Sorry, I was unable to process your question.")

bot.run(os.environ.get("DISCORD_TOKEN"))