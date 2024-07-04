from fastapi import FastAPI, HTTPException,File,UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from hugchat import hugchat
from hugchat.login import Login
import whisper
import os

app = FastAPI()

EMAIL = "shubhsiddh@gmail.com"
PASSWD = "S02092003j@"
cookie_path_dir = "./cookies/"

# Login and get cookies
try:
    sign = Login(EMAIL, PASSWD)
    cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
except Exception as e:
    raise Exception(f"Failed to initialize chatbot: {e}")

class ChatRequest(BaseModel):
    path: str

# class ChatRegen(BaseModel):
#     error: str
#     code: str

# Add CORS middleware
origins = [
    "http://localhost:3000",  # React app running on localhost
    "http://localhost:8000",  # Backend API running on localhost
    # Add more origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow these origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
temp_dir = "./temp"
os.makedirs(temp_dir, exist_ok=True)

@app.post("/process/")
async def process_audio(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(temp_dir, file.filename)
        print("Saving file to:", file_path)  # Debug log

        # Save the uploaded file to the temp directory
        with open(file_path, "wb") as f:
            f.write(await file.read())

        print("File saved:", file_path)  # Debug log

        # Load the Whisper model and transcribe the audio file
        model = whisper.load_model("base")
        result = model.transcribe(file_path, language="en")

        print("Transcription result:", result["text"])  # Debug log

        # Generate the prompt for Hugging Face chatbot
        prompt = "I have converted the audio from a meeting to the following text, please give me minutes of the meeting plus summary: " + result["text"]
        query_result = str(chatbot.query(prompt, web_search=True))

        print("Query result:", query_result)  # Debug log

        # Clean up the temporary file
        os.remove(file_path)
        
        return {"response": query_result}
    except Exception as e:
        print("Error processing audio:", e)  # Debug log
        raise HTTPException(status_code=500, detail=f"Error processing audio: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)