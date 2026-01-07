# Bachelor progress ROADMAP

---

### Week 1 – Local MVP Setup

**Objectives**
 We first create a base project where we connect to the existing clean database and try to query via API
 The responses are in JSON format that later will cause some problems when we have Null values 

**Tasks**

- create basic endpoints that work [x]
- connect to the already cleaned database locally [x]
- expose the endpoints via notebook [x]

**Outcome and Bottlenecks**
- endpoints were accesable, but the code and logic is quite complicated. Maybe we can hide the request somewhere under a button or a feature
---


### Week 2 – Testing localy

**Objectives**
The local setup should work on Martins notebook
maybe we switch already to parquets 
Send Dataframes?

**Tasks**
- more endpoints [x]
- We can query large chunks of data thanks to parquets [x]
- creating a copy of Martin notebook that would represent the same reasearch but with different data source [x]
- creating a helper function in the notebook that loads the parquete and transforms the response into dataframe so that the client just asks for the data [x]
- setting semantic limit based on what Martin uses [-]

**Outcome & Bottlenecks**
- endpoints represent the state of Martin notebook.
- Trying to figure out what kind of limits should I set for the data, since its should be scalable.
---


### Week 3 – Change of structure 

**Objectives**
We came across some bottleneck. 
What if the client want to access the data and work on it offline ?
Overengineering the access via server
It can work also as a standalone notebook 
initial design goal: multi-user controlled access → server API
updated constraints: offline demo, conference setting → local DB
trade-off: portability vs central governance/version control
final solution: local-first with optional API wrapper (room to work with)

**Tasks**
- restructure the project and create a new repo in gitlab[]
- keep the old version in github[]
- in /src/ paste the existing code for server connection []
- in /src/ create a new version that connects to the database[]


**Outcome**

---


### Week 4 – Transform layer

**Objectives**
Right now, the API mask mirrors the existing Oxford workflow and only replaces the data source.
A transform layer on top of the API would be possible, but it would introduce methodological decisions (e.g. filtering, normalization).
I wanted to align first whether these steps should stay in the notebook or be standardized in the API.
- Existing notebooks continue to work
- 
- validate endpionts(for example if sth does not exist)

**Tasks**

- create a transform layer that resembles the one Martin uses, but this time working tight with the database []

**Outcome & Bottlenecks**
- 

---

### Week 5 – Change of structure 

**Objectives**


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
  GET /nuts
  ```
  ```
  GET /nuts?platte=14
  ```

  ```
  GET /data?platte=14&slot=10&data_origin=HF_Data&limit=20000
  ```

### Supported Filters

- `Platte` (required)
- `Nut` (required)
- `DataOrigin` (required)
- `Signal` (required)
- `limit` (should be scalable)

---



##  Success Criteria

The **Data Access** task is considered complete when:

- 



