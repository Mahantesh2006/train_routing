import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List

from database import init_db, get_db_connection
from routing_engine import search_routes


app = FastAPI(
    title="Indirect Train & Connecting Route Planner",
    description="Engine for finding direct and 1-stop connecting trains with day-of-week & buffer time constraint validation.",
    version="1.0.0"
)

# Initialize DB on startup
@app.on_event("startup")
def startup_event():
    init_db()

class RouteSearchRequest(BaseModel):
    origin: str = Field(..., example="NDLS")
    destination: str = Field(..., example="SBC")
    departure_date: str = Field(..., example="2026-07-27")
    min_buffer_mins: int = Field(45, ge=15, le=300)
    max_buffer_mins: int = Field(360, ge=60, le=1440)
    sort_by: str = Field("duration", example="duration") # "duration", "layover", "fare", "earliest_arrival"

@app.get("/api/stations")
def get_stations():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT code, name, city, lat, lng, is_junction FROM stations ORDER BY city, name")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/api/search")
def api_search_routes(req: RouteSearchRequest):
    if req.origin == req.destination:
        raise HTTPException(status_code=400, detail="Origin and Destination cannot be the same station.")
    
    try:
        results = search_routes(
            origin=req.origin,
            destination=req.destination,
            departure_date=req.departure_date,
            min_buffer_mins=req.min_buffer_mins,
            max_buffer_mins=req.max_buffer_mins,
            sort_by=req.sort_by
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/network")
def get_network_graph():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT code, name, city, lat, lng, is_junction FROM stations")
    stations = [dict(r) for r in cursor.fetchall()]

    cursor.execute("""
        SELECT DISTINCT s1.station_code as source, s2.station_code as target, t.name as train_name, t.train_no
        FROM schedules s1
        JOIN schedules s2 ON s1.train_no = s2.train_no AND s2.stop_seq = s1.stop_seq + 1
        JOIN trains t ON s1.train_no = t.train_no
    """)
    edges = [dict(r) for r in cursor.fetchall()]
    conn.close()

    return {"nodes": stations, "edges": edges}

# Real-Time Telemetry State
state = {
    "emergency_override": False,
    "junctions": {
        "J-101": {"name": "Kalaburagi Junction", "status": "OPEN", "code": "KLBG"},
        "J-102": {"name": "Yesvantpur Junction", "status": "CONFLICT", "code": "YPR"},
        "J-103": {"name": "SBC Interchange", "status": "DIVERGING", "code": "SBC"},
        "J-104": {"name": "Mysuru Line", "status": "OPEN", "code": "MYS"},
        "J-105": {"name": "Vijayapura Hub", "status": "CLOSED", "code": "BJP"},
        "J-106": {"name": "Belagavi Pass", "status": "OPEN", "code": "BGM"}
    },
    "conflicts": [
        {
            "id": "CONF-902",
            "junction": "J-102",
            "train1": "#TR-804",
            "train1_name": "Karnataka SF",
            "train2": "#TR-412",
            "train2_name": "SBC Rajdhani",
            "description": "Signal Overlap at Junction J-102 (Track Segment 2B). Both units scheduled to enter block simultaneously at 118 km/h.",
            "status": "ACTIVE",
            "severity": "CRITICAL"
        }
    ]
}

@app.get("/api/telemetry")
def get_telemetry():
    return state

@app.post("/api/signal/action")
def signal_action(action: str = Query(...), train_id: Optional[str] = Query(None)):
    if action == "reroute":
        state["conflicts"] = [c for c in state["conflicts"] if c["id"] != "CONF-902"]
        state["junctions"]["J-102"]["status"] = "DIVERGED"
        return {"status": "SUCCESS", "message": f"Train {train_id or '#TR-412'} successfully rerouted via Track 2B bypass."}
    elif action == "hold":
        state["conflicts"] = [c for c in state["conflicts"] if c["id"] != "CONF-902"]
        state["junctions"]["J-102"]["status"] = "HOLD"
        return {"status": "SUCCESS", "message": f"Signal S-402 HELD. Train {train_id or '#TR-804'} holding position at approach marker."}
    elif action == "emergency":
        state["emergency_override"] = not state["emergency_override"]
        return {"status": "SUCCESS", "emergency_override": state["emergency_override"]}
    raise HTTPException(status_code=400, detail="Invalid action")

@app.post("/api/junction/toggle")
def toggle_junction(junction_id: str = Query(...)):
    if junction_id in state["junctions"]:
        curr = state["junctions"][junction_id]["status"]
        next_status = "CLOSED" if curr in ["OPEN", "DIVERGING"] else "OPEN"
        state["junctions"][junction_id]["status"] = next_status
        return {"status": "SUCCESS", "junction_id": junction_id, "new_status": next_status}
    raise HTTPException(status_code=404, detail="Junction not found")

# Mount static folder for web UI
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Indirect Train / Connecting Route Planner API is running."}

