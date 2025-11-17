from fastapi import FastAPI
from fastapi.responses import HTMLResponse, ORJSONResponse
from fastapi.responses import RedirectResponse
from fastapi.responses import StreamingResponse
app = FastAPI()
async def fake_video_streamer():
    for i in range(10):
        yield b"My name is Ayan Ahmed and I'm an AI/ML Engineer making real world projects with LangGraph"


@app.get("/")
async def main():
    return StreamingResponse(fake_video_streamer())
@app.get('/students/',response_class=ORJSONResponse)
async def read_students():
    return [{'Student Name ':'Ayan Ahmed'}]


@app.get("/items/", response_class=HTMLResponse)
async def read_items():
    return """
    <html>
        <head>
            <title>Welcome to Ayan Ahmed Channel</title>
        </head>
        <body>
            <h1>Learn FastAPI</h1>
        </body>
    </html>
    """





@app.get("/typer")
async def redirect_typer():
    return RedirectResponse("https://www.youtube.com/playlist?list=PLKnIA16_RmvYsvB8qkUQuJmJNuiCUJFPL")