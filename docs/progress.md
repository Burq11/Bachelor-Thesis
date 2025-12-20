# Bachelor progress

---
## ROADMAP

### Week 1 – Local MVP Setup

**Objectives**
 We first create a base project where we connect to the existing clean database and try to query via API
 The responses are in JSON format that later will cause some problems when we have Null values 

**Tasks**

- create basic endpoints that work [x]
- connect to the already cleaned database locally [x]
- expose the endpoints via notebook [x]

**Outcome and Bottelnecks**
*endpionts were accesable, but the code and logic is quite complicated. Maybe we can hide the request somewhere under a button or a feature
*
---

### Week 2 – Testing localy

**Objectives**
The local setup  should work on Martins notebook
maybe we switch already to parquets 
Send Dataframes?

**Tasks**
- more endpoints []
- We can query large chunks of data thanks to parquets []
- testing the endpoints with copy of Martins Notebook []
- setting semantic limit based on what Martin uses []

**Outcome**

-

---

### Week 3 – Transform layer

**Objectives**

- Existing notebooks continue to work
- if Martin replyes that he needs soemthing like this 

**Tasks**

-

**Outcome**

-

---

### Week 4 – Pushing the concept to the IWF

**Objectives**

- do we use Docker so that it runs on the server all the time?
- Preparation for server deployment

**Tasks**

-

**Outcome**

---

## Context & Scope

### Project Context

- A **large DuckDB database** (\~650k+ rows) exists.
- The database is hosted on an **institute server**.

### Team Responsibilities

- **Julia (Data Access):**
  - Design and implementation of the data access layer
  - Provide a server-side “mask” (API) to query DuckDB
  - Deliver queried data to notebooks as pandas DataFrames
- **Dennis (Data cleaning)**
  - refactoring and modernising existing cleanup process

### Explicit Out of Scope for now 

- UI / dashboards
- Export functionality
- Changes to notebook structure
---

## API Interface (Conceptual)

### Minimal Endpoints (MVP)

  ```
  GET /plates
  ```

  ```
  GET /slots
  ```
  ```
  GET /slots?platte=14
  ```

  ```
  GET /data?platte=14&slot=10&data_origin=HF_Data&limit=20000
  ```

### Supported Filters

- `Platte` (required)
- `Nut` (required)
- `DataOrigin` (optional)
- `Signal` (optional)
- `limit` (default small, hard cap enforced)
- `someting more?`

---



##  Success Criteria

The **Data Access** task is considered complete when:

- 



