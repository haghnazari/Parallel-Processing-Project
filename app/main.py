from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from .registry import get_registry
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(
    title="Parallel Processing",
    description="پروژه پایانی درس پردازش موازی - سعید حق نظری",
    version="1.0.0",
)


class ScenarioRequest(BaseModel):
    scenario_id: int


@app.get("/")
async def ui():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "index.html not found"}


@app.post("/{method}/{tool}")
async def execute_scenario(method: str, tool: str, request: ScenarioRequest):
    registry = get_registry(method)

    try:
        result = registry[tool](request.scenario_id)

        return {
            "status": "success",
            "method": method,
            "tool": tool,
            "scenario_id": request.scenario_id,
            "output": result.get("output", "No output"),
            "explanation": result.get("explanation", "No explanation"),
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution error: {str(e)}")


static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")
