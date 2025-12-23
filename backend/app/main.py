
import duckdb
import io
import os
import numpy as np
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from fastapi import FastAPI, HTTPException, Query
from pathlib import Path
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


app = FastAPI(title="Test API Connections")

#config & helpers
############################################################
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR.parent / "data"/ "database.duckdb"
TABLE_NAME = os.getenv("TABLE_NAME", "my_data")
DEFAULT_LIMIT = int(os.getenv("DEFAULT_LIMIT", "20000"))
MAX_LIMIT = int(os.getenv("MAX_LIMIT", "200000"))
DEFAULT_FIELDS = ["Time", "Signal", "DataOrigin", "Value", "WCS_Y_mm", "Nut", "Platte", "Axis", "SensorType"]

def parse_csv_param(value: str | None) ->list[str] | None:
    if not value:
        return None
    items = [v.strip() for v in value.split(",")]
    items = [v for v in items if v]
    return items or None
############################################################

#database connection 
############################################################
con = duckdb.connect(str(DB_PATH), read_only=True)
############################################################

#endpoints
############################################################
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


@app.get("/nuts")
def list_nuts():
    query = f"""
        SELECT DISTINCT Nut
        FROM {TABLE_NAME}
        WHERE Nut IS NOT NULL
        ORDER BY Nut
    """
    result = con.execute(query).fetchall()
    return [{"nut":  row[0]} for row in result]


@app.get("/plate-nuts")
def list_plate_nuts_flat():
    sql = f"""
        SELECT DISTINCT Platte, Nut
        FROM {TABLE_NAME}
        WHERE Platte IS NOT NULL
          AND Nut IS NOT NULL
        ORDER BY Platte, Nut
    """
    rows = con.execute(sql).fetchall()
    return [{"platte": p, "slot": n} for (p, n) in rows]


@app.get("/plates/{platte}/nuts")
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


@app.get("/signals")
def list_signals(
    platte: str = Query(...),
    nut: float = Query(...),
    data_origin: str | None = Query(None),
):
    sql = f"""
        SELECT DISTINCT Signal
        FROM {TABLE_NAME}
        WHERE Platte = ?
          AND Nut = ?
          AND Signal IS NOT NULL
    """
    params = [platte, nut]

    if data_origin:
        sql += " AND DataOrigin = ?"
        params.append(data_origin)

    sql += " ORDER BY Signal"

    rows = con.execute(sql, params).fetchall()
    return [r[0] for r in rows]


#for debugging for now 
@app.get("/data")
def get_data(
    platte: str = Query(...),
    nut: float = Query(...),
    limit: int = Query(..., ge=1),
):
    limit = min(limit, MAX_LIMIT)

    # *return full rows for the selected Platte+Nut.
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


@app.get("/data.parquet")
def get_data_parquet(
    platte: str = Query(...),
    nut: float = Query(...),
    data_origin: str | None = Query(None),
    signals: str | None = Query(None),
    fields: str | None = Query(None),
    wcs_min: float | None = Query(None),
    wcs_max: float | None = Query(None),
    limit: int = Query(..., ge=1),
):
    limit = min(limit, MAX_LIMIT)

    # Validate fields against schema (avoid bad column names)
    schema_rows = con.execute(f"DESCRIBE {TABLE_NAME}").fetchall()
    valid_cols = {r[0] for r in schema_rows}

    requested_fields = parse_csv_param(fields) or DEFAULT_FIELDS
    selected_fields = [c for c in requested_fields if c in valid_cols]
    if not selected_fields:
        selected_fields = [c for c in DEFAULT_FIELDS if c in valid_cols]

    select_clause = ", ".join(selected_fields)

    sql = f"""
        SELECT {select_clause}
        FROM {TABLE_NAME}
        WHERE Platte = ?
          AND Nut = ?
    """
    params: list = [platte, nut]

    if data_origin:
        sql += " AND DataOrigin = ?"
        params.append(data_origin)

    signal_list = parse_csv_param(signals)
    if signal_list:
        placeholders = ", ".join(["?"] * len(signal_list))
        sql += f" AND Signal IN ({placeholders})"
        params.extend(signal_list)
        
    # Optional WCS range filter
    if wcs_min is not None:
        sql += " AND WCS_Y_mm >= ?"
        params.append(wcs_min)

    if wcs_max is not None:
        sql += " AND WCS_Y_mm <= ?"
        params.append(wcs_max)

    # Keep deterministic order if Time is available and selected
    if "Time" in valid_cols and "Time" in selected_fields:
        sql += " ORDER BY Time"

    sql += " LIMIT ?"
    params.append(limit)

    df = con.execute(sql, params).df()

    # Convert to parquet in-memory
    table = pa.Table.from_pandas(df, preserve_index=False)
    buf = io.BytesIO()
    pq.write_table(table, buf, compression="zstd")

    return Response(buf.getvalue(), media_type="application/octet-stream")

@app.get("/data-origins")
def list_data_origins(
    platte: str = Query(...),
    nut: float = Query(...),
):
    sql = f"""
        SELECT DISTINCT DataOrigin
        FROM {TABLE_NAME}
        WHERE Platte = ?
          AND Nut = ?
          AND DataOrigin IS NOT NULL
        ORDER BY DataOrigin
    """
    rows = con.execute(sql, [platte, nut]).fetchall()
    return [r[0] for r in rows]

