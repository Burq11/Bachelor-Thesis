# Decision Week 1: Data Access & API Baseline

**Date:** 2025-25-12  

In Week 2, the goal is to test the backend API with the existing Notebook from the supervisor.

---

## Decisions
 - switched to parquets since the data will scale up
 - copied Oxford notebook and changed the data source from processed folder to API backend mask
 - preamble so that we can set a flag that would determinate if we use the API of data in the file 
USE_API_BACKEND = os.getenv("USE_API_BACKEND", "0") == "1"
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
 - adding a client mask src/api_backend.py 
 import io
import requests
import pandas as pd

def list_plates(api_base_url: str) -> list[int]:
    r = requests.get(f"{api_base_url}/plates", timeout=30)
    r.raise_for_status()
    return [int(x["platte"]) for x in r.json()]

def list_nuts_for_plate(api_base_url: str, platte: int) -> list[float]:
    r = requests.get(f"{api_base_url}/plates/{platte}/nuts", timeout=30)
    r.raise_for_status()
    return r.json()

def load_df(api_base_url: str, platte: int, nut: float, *, limit: int = 20000,
            wcs_min: float | None = None, wcs_max: float | None = None) -> pd.DataFrame:
    params = {"platte": platte, "nut": nut, "limit": limit}
    if wcs_min is not None:
        params["wcs_min"] = wcs_min
    if wcs_max is not None:
        params["wcs_max"] = wcs_max

    r = requests.get(f"{api_base_url}/data.parquet", params=params, timeout=180)
    r.raise_for_status()
    return pd.read_parquet(io.BytesIO(r.content))

 - Patch viz/widgets_digital_twin.py
    if USE_API_BACKEND:
        from src.api_backend import list_plates
        platten_ids = list_plates(API_BASE_URL)
    else:
        parquet_files = list(processed_path.glob("Platte_*_Nut_*.parquet"))
        platten_ids = sorted({int(f.name.split("_")[1]) for f in parquet_files})


---

## Non-Decisions (Explicitly Deferred)

- 
- No aggregation, resampling, or feature engineering in the API.
- No schema refactoring of the underlying database.
- No authentication or authorization.
- No optimization for large-scale data retrieval.

---

## Rationale

The main bottleneck encountered in Week 1 was JSON serialization of raw sensor data.
By sanitizing values at the API boundary, the service remains robust against
imperfect data while keeping the implementation simple.
Further restructuring and performance improvements are deferred
until basic access and visualization workflows are validated.

---

## Consequences

- The API is stable and usable for notebooks and exploratory analysis.
- Data quality issues are handled defensively but not resolved at the source.
- Future iterations can introduce Parquet exports and cleaned views
  without breaking existing clients.
