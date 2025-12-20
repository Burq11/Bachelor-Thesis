# Decision Week 1: Data Access & API Baseline

**Date:** 2025-20-12  

In Week 1, the goal was to establish a minimal but working data-access layer
that allows filtered access to CNC sensor measurements via a REST API.
The raw dataset contains heterogeneous sensor signals, missing values,
and mixed data types, which led to early serialization issues.

---

## Decisions

- The data-access service is implemented using **FastAPI** with **DuckDB** as the backend.
- The API returns **JSON** for small and exploratory data access.
- The `/data` endpoint filters measurements by **Platte (plate)** and **Nut (slot/run)**.
- Missing and invalid numeric values (`NaN`, `Inf`) are **sanitized at the API layer**
  to guarantee JSON-compatible responses.
- Timestamps are converted to **ISO-formatted strings** before serialization.
- No data aggregation or transformation is performed at this stage;
  the API exposes **raw, filtered measurements**.

---

## Non-Decisions (Explicitly Deferred)

- No Parquet or binary data export in Week 1.
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
