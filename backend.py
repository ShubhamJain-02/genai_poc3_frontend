from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from hugchat import hugchat
from hugchat.login import Login
import whisper

app = FastAPI()

EMAIL = "ngoyal7019@gmail.com"
PASSWD = "Naku@@1970"
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

@app.post("/process/")
def chat(request: ChatRequest):
    print('hji')
    try:
        print("file path",request.path)
        model = whisper.load_model("base")
        result = model.transcribe(request.path, language="en")
        print('got transcription', result)
        prompt = "I have converted the audio from a meeting to the following text, please give me minutes of the meeting plus summary: " + result["text"]
        query_result = str(chatbot.query(prompt, web_search=True))
        print("done",query_result)
        return {"response": query_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying chatbot: {e}")
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)