
import duckdb
import os
import numpy as np
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, HTTPException, Query
from pathlib import Path
import pandas as pd


app = FastAPI(title="Test API Connections")

#config
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR.parent / "data"/ "database.duckdb"
TABLE_NAME = os.getenv("TABLE_NAME", "my_data")
LIMIT = int(os.getenv("LIMIT", "1000"))

#database connection 
con = duckdb.connect(str(DB_PATH), read_only=True)


#endpoints
@app.get("/plates")
def list_plates():
    query = f"""
        SELECT DISTINCT Platte
        FROM {TABLE_NAME}
        WHERE Platte IS NOT NULL
        ORDER BY Platte
    """
    result = con.execute(query).fetchall()
    return [{"platte":  row[0]} for row in result]

@app.get("/slots")
def list_slots():
    query = f"""
        SELECT DISTINCT Nut
        FROM {TABLE_NAME}
        WHERE Nut IS NOT NULL
        ORDER BY Nut
    """
    result = con.execute(query).fetchall()
    return [{"nut":  row[0]} for row in result]

@app.get("/plate-slots")
def list_plate_slots_flat():
    sql = f"""
        SELECT DISTINCT Platte, Nut
        FROM {TABLE_NAME}
        WHERE Platte IS NOT NULL
          AND Nut IS NOT NULL
        ORDER BY Platte, Nut
    """
    rows = con.execute(sql).fetchall()
    return [{"platte": p, "slot": n} for (p, n) in rows]


@app.get("/plates/{platte}/slots")
def list_nuts_for_plate(platte: str):
    sql = f"""
        SELECT DISTINCT Nut
        FROM {TABLE_NAME}
        WHERE Platte = ?
          AND Nut IS NOT NULL
        ORDER BY Nut
    """
    rows = con.execute(sql, [platte]).fetchall()
    return [r[0] for r in rows]

@app.get("/schema")
def schema():
    rows = con.execute(f"DESCRIBE {TABLE_NAME}").fetchall()
    return [{"column": r[0], "type": r[1]} for r in rows]

#filters out the sepcific plate-nut combination
@app.get("/data")
def get_data(
    platte: str = Query(...),
    nut: float = Query(...),
    limit: int = Query(LIMIT, ge=1),
):
    limit = min(limit, LIMIT)

    # *return full rows for the selected Platte+Nut.
    # Later: switching to selecting only required columns, and/or return Parquet for large results.
    sql = f"""
        SELECT *
        FROM {TABLE_NAME}
        WHERE Platte = ?
          AND Nut = ?
        ORDER BY Time
        LIMIT ?
    """

    try:
        df = con.execute(sql, [platte, nut, limit]).df()
    except Exception as e:
        raise HTTPException(500, f"Query failed: {e}")
    
    if df.empty:
        raise HTTPException(404, "No data found for the given platte/nut.")
    
     # Make Time JSON-safe
    if "Time" in df.columns:
        df["Time"] = pd.to_datetime(df["Time"], errors="coerce")
        df["Time"] = df["Time"].dt.strftime("%Y-%m-%dT%H:%M:%S.%f")

    # Replace inf/-inf
    df = df.replace([np.inf, -np.inf], np.nan)

    # Force all columns to allow None
    df = df.astype(object).where(df.notna(), None)

    return jsonable_encoder(df.to_dict(orient="records"))