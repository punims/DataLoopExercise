from fastapi import FastAPI, HTTPException
import httpx
import asyncio
from pydantic import BaseModel

app = FastAPI()

class StartGame(BaseModel):
    self_url: str
    other_server_url: str
    pong_time_ms: int

game_state = {
    "self_url": "",
    "other_server_url": "",
    "pong_time_ms": 1000,
    "is_active": False,
    "paused": False
}

@app.post("/start")
async def start_game(game_details: StartGame):
    if game_state["is_active"]:
        raise HTTPException(status_code=400, detail="Game is already active.")
    game_state.update({
        "self_url": game_details.self_url,
        "other_server_url": game_details.other_server_url,
        "pong_time_ms": game_details.pong_time_ms,
        "is_active": True,
        "paused": False
    })
    asyncio.create_task(send_ping())
    return {"message": "Game started"}

async def send_ping():
    while game_state["is_active"] and not game_state["paused"]:
        await asyncio.sleep(game_state["pong_time_ms"] / 1000)
        target_url = game_state["other_server_url"]
        print(target_url)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(target_url + "/ping")
                print("Ping sent and pong received.")
        except Exception as e:
            print(f"Error sending ping: {e}")

@app.post("/ping")
async def receive_ping():
    print("RECEIVED PING")
    if game_state["paused"]:
        return {"message": "Game is paused"}
    game_state['self_url'], game_state['other_server_url'] = game_state['other_server_url'], game_state['self_url']
    asyncio.create_task(send_ping())
    return {"message": "pong"}

@app.post("/pause")
async def pause_game():
    if not game_state["is_active"]:
        raise HTTPException(status_code=400, detail="Game is not active.")
    game_state["paused"] = True
    return {"message": "Game paused"}

@app.post("/resume")
async def resume_game():
    if not game_state["is_active"]:
        raise HTTPException(status_code=400, detail="Game is not active.")
    if not game_state["paused"]:
        raise HTTPException(status_code=400, detail="Game is not paused.")
    game_state["paused"] = False
    asyncio.create_task(send_ping())
    return {"message": "Game resumed"}

@app.post("/stop")
async def stop_game():
    game_state["is_active"] = False
    return {"message": "Game stopped"}

@app.post("/startwait")
async def start_wait_game(game_details: StartGame):
    if game_state["is_active"]:
        raise HTTPException(status_code=400, detail="Game is already active.")
    game_state.update({
        "self_url": game_details.self_url,
        "other_server_url": game_details.other_server_url,
        "pong_time_ms": game_details.pong_time_ms,
        "is_active": True,
        "paused": False
    })
