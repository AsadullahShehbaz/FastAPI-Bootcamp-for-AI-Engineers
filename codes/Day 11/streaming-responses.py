from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

async def fake_video_streamer():
    for i in range(10):
        yield b"some fake video bytes "

# Streaming Fake bytes of Video Example
@app.get("/video")
async def main():
    return StreamingResponse(fake_video_streamer())

# Streaming Video File Example 
some_file_path = "large-video-file.mp4"

@app.get("/video-file")
async def video_file():
    def iterfile():
        with open(some_file_path,mode="rb") as f:
            yield from f
    return StreamingResponse(iterfile(),media_type="video/mp4")

# File Response Example
from fastapi.responses import FileResponse

@app.get("/video-file-response",response_class=FileResponse)
async def video_response():
    # return FileResponse(some_file_path,media_type="video/mp4")
    return some_file_path

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)