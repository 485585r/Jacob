import uvicorn
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse, FileResponse
from starlette.routing import Route, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket
import os

# Set environment variables
os.environ['TAVILY_API_KEY'] = "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"
os.environ['OPENAI_API_KEY'] = "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"

from langchain_openai_voice import OpenAIVoiceReactAgent
from server.utils import websocket_stream
from server.prompt import INSTRUCTIONS
from server.tools import TOOLS


async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    browser_receive_stream = websocket_stream(websocket)

    print(browser_receive_stream)

    agent = OpenAIVoiceReactAgent(
        model="gpt-4o-realtime-preview",
        tools=TOOLS,
        instructions=INSTRUCTIONS,
    )

    await agent.aconnect(browser_receive_stream, websocket.send_text)


async def homepage(request):
    with open("src/server/static/index.html") as f:
        html = f.read()
        return HTMLResponse(html)


# catchall route to load files from src/server/static


routes = [Route("/", homepage), WebSocketRoute("/ws", websocket_endpoint)]

app = Starlette(debug=True, routes=routes)

app.mount("/", StaticFiles(directory="src/server/static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)