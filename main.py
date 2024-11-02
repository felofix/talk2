from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from qdrant_client import QdrantClient
from typing import List, Optional
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
import openai
from openai import OpenAI
import os

# Initialize FastAPI
app = FastAPI()

# Load environment variables
load_dotenv()

# API keys
openAI_key = os.getenv("OPENAI_KEY")
qdrant_key = os.getenv("QDRANT_KEY")
qdrant_url = "https://25c776da-e46f-4017-a9ae-57be7489d68e.us-east4-0.gcp.cloud.qdrant.io"

# Initialize Qdrant client and embeddings
qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_key)
embeddings = OpenAIEmbeddings(openai_api_key=openAI_key)
openai.api_key = openAI_key

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Data models
class UserMessage(BaseModel):
    message: str
    person: str  # e.g., 'Friedrich Nietzsche'
    previous_message: Optional[str] = None  # Optional field for the last message

class ChatResponse(BaseModel):
    reply: str

# Map each person to their respective Qdrant collection name
person_collection_map = {
    "Friedrich Nietzsche": "nietzsche",
    "Marcus Aurelius": "aurelius",
    "Ted Kaczynski": "kaczynski"
}

async def generate_reply(person: str, message: str, previous_message: Optional[str] = None) -> str:
    # Retrieve the appropriate collection name based on the person
    collection_name = person_collection_map.get(person)
    
    if not collection_name:
        return "This person is not available in the system."
    
    # Retrieve relevant chunks from Qdrant
    query_vector = embeddings.embed_query(message)
    search_results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=5  # Adjust based on your preference
    )
    
    # Concatenate retrieved texts
    context = "\n\n".join([hit.payload['text'] for hit in search_results])
    
    # Include the previous message in the context, if available
    if previous_message:
        context = f"Previous message: {previous_message}\n\n" + context
    
    # Generate response using OpenAI GPT
    prompt = f"""As {person}, answer the following question based on the context below. If you can't answer based on the context,
                try to answer like the person would. 

                Context:
                {context}

                Question:
                {message}

                Answer as {person} would:"""

    llm = OpenAI(api_key=openAI_key)

    response = llm.chat.completions.create(model="gpt-4o-2024-08-06", messages=[
        {"role": "system", "content": f"You are {person}, answer accordingly."},
        {"role": "user", "content": prompt}
    ])

    reply = response.choices[0].message.content
    return reply

# Endpoint to get available people
@app.get("/people")
def get_people():
    return list(person_collection_map.keys())

# Endpoint to serve the index.html
@app.get("/")
def read_index():
    return FileResponse('static/index.html')

# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(user_message: UserMessage):
    reply = await generate_reply(user_message.person, user_message.message, user_message.previous_message)
    return ChatResponse(reply=reply)
