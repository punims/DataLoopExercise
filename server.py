from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import asyncio

app = FastAPI()

class StartGame(BaseModel):
    other_server_url: str
    pong_time_ms: int

game_state = {
    "other_server_url": "",
    "pong_time_ms": 1000,
    "is_active": False
}

@app.post("/start")
async def start_game(game_details: StartGame):
    game_state["other_server_vol"] = game_details.other_server_url
    game_state["pong_time_ms"] = game_details.pong_time_ms
    game_state["is_active"] = True
    asyncio.create_task(ping_pong_cycle())
    return {"message": "Game started"}

async def ping_pong_cycle():
    while game_state["is_active"]:
        await asyncio.sleep(game_state["pong_time_ms"] / 1000)  # Convert ms to seconds
        try:
            async with httpx.AsyncClient() as client:
                await client.post(game_state["other_server_url"] + "/ping")
        except Exception as e:
            print(f"Failed to send ping: {e}")

@app.post("/ping")
async def ping_pong():
    return {"message": "pong"}

@app.post("/stop")
async def stop_game():
    game_state["is_active"] = False
    return {"message": "Game stopped"}