from fastapi import FastAPI, UploadFile, HTTPException
import os
from dotenv import load_dotenv
import groq

from models import Question


app = FastAPI()

@app.get("/")
def root():
    return {"message": "FASTAPI is running!"}


load_dotenv()  # Load environment variables
API_KEY = os.getenv("API_KEY")


# Set up the Groq client
client = groq.Groq(api_key=API_KEY)

# Chat context setup
chat_context = [
    {
        "role": "system",
        "content": 'You are a friendly and helpful educational chatbot named "Nemo." Your purpose is to assist users and mention Nemo in your responses.',
    }
]

@app.post("/ask/")
async def ask_question(question: Question):
    if API_KEY is None:
        raise HTTPException(status_code=500, detail="API key is not set.")
    
    # Append user message to chat context
    chat_context.append({"role": "user", "content": question.question})
    
    try:
        # Call Groq's model completion API
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=chat_context,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        
        # Gather the response
        response = ""
        for chunk in completion:
            response += chunk.choices[0].delta.content or ""
        
        # Add assistant's response to chat history (chat context)
        chat_context.append({"role": "assistant", "content": response})
        
        # Return the response
        return {"response": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
