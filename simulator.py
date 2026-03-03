from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import os

app = FastAPI(title="Spice-as-a-Service API")

# NEW: This allows your web browser to communicate with this API safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SimulationRequest(BaseModel):
    netlist: str

@app.post("/simulate")
async def run_simulation(request: SimulationRequest):
    filename = "temp_circuit.cir"
    
    with open(filename, "w") as file:
        file.write(request.netlist)
    
    ngspice_path = "ngspice" 
    
    try:
        result = subprocess.run(
            [ngspice_path, "-b", filename],
            capture_output=True,
            text=True,
            check=True
        )
        return {
            "status": "success", 
            "output": result.stdout
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=400, detail=f"Ngspice error: {e.stderr}")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Ngspice executable not found.")
    finally:
        if os.path.exists(filename):
            os.remove(filename)