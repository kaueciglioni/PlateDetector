from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Serve arquivos estáticos corretamente
app.mount("/static", StaticFiles(directory="/home/kaue/voxProjects/QRCodeVisualizer"), name="static")

@app.get("/")
def root():
    return {"message": "API de Vídeo - Acesse /video para ver o vídeo"}

@app.get("/video")
def get_video():
    video_path = "/home/kaue/voxProjects/QRCodeVisualizer/20250701_192617000_iOS.mp4"
    if os.path.exists(video_path):
        return FileResponse(
            path=video_path,
            media_type="video/mp4",
            filename="20250701_192617000_iOS.mp4"  # apenas o nome, não o caminho absoluto
        )
    return {"error": "Vídeo não encontrado"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)