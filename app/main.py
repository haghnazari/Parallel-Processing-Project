from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lock import run_lock_scenario

app = FastAPI(
    title="Parallel Processing",
    description="پروژه پایانی درس پردازش موازی - سعید حق نظری",
    version="1.0.0"
)

class ScenarioRequest(BaseModel):
    scenario_id: int

static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")

if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/ui")
async def ui():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "index.html not found"}


# نخ(Thread)
@app.post("/thread/lock")
async def thread_lock(request: ScenarioRequest):
    try:
        result = run_lock_scenario(request.scenario_id)
        return {
            "status": "success",
            "tool": "Lock",
            "scenario_id": request.scenario_id,
            "output": result["output"],
            "explanation": result["explanation"]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

