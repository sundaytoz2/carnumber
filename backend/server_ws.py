from fastapi import FastAPI, WebSocket, File, UploadFile
import subprocess
import os

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # 파일을 웹소켓을 통해 받음
        data = await websocket.receive_bytes()

        # 파일 저장
        with open("image.jpg", "wb") as f:
            f.write(data)

        # PaddleOCR 실행
        subprocess.run(["conda", "run", "-n", "carnumber_paddleocr", "paddleocr", "--image_dir", "image.jpg", "--lang", "korean"])

        # OCR 결과 읽기
        with open("ocr_result.txt", "r") as file:
            result = file.read()

        # 결과 전송
        await websocket.send_text(result)
