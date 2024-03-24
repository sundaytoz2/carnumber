# main.py
from typing import List
from fastapi import FastAPI, File, UploadFile, Form, Request
import subprocess
import os
import shutil
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/raw/")
async def create_upload_file2(request: Request):
    print(request)
    print(await request.body())
    return "hhh"

@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    print('upload called:', file)
    with open("temp.jpg", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    result = subprocess.run(
        ['conda', 'run', '-n', 'carnumber_paddleocr', 'paddleocr', '--image_dir', 'temp.jpg', '--lang', 'korean'],
        capture_output=True, text=True
    )
    os.remove("temp.jpg")  # Remove the temporary file after processing
    return {"result": result.stdout}


@app.post("/submit-form/")
async def submit_form(text_data: str = Form(...)):
    return {"received_data": text_data}
# run server
# uvicorn server:app --reload

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 허용할 출처 목록
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메소드
    allow_headers=["*"],  # 허용할 헤더
)