# FRIDAAY
## Format Representing Interdependent Data Actions As YAML

Who needs SQL, Python, JavaScript and CSV?
Get it all done by FRIDAAY

# Usage
FRIDAAY uses `poetry` to manage both dependencies and the virtual environment:
```
$ poetry install # or '$ poetry update'
$ poetry env use python3
$ poetry run pytest
$ poetry run ptw
```

# Overview

FRIDAAY defines a new "atomic unit" of abstraction for the modern data stack called Data Actions.  
Each Data Action defines a semantic mapping for creating a new "frame" from existing frames (or inline data).
This allows analysts and data scientists to declaratively specify their intent, empowering the underlying platform to efficiently satisfy those requirements. We call this production-ready alternative to traditional exploratory notebooks a [PipeBook](https://ihack.us/2022/06/30/pipebook-yml-reimagining-notebooks-as-resilient-data-pipelines/).

Right now, business logic and data dependencies are trapped inside complex (and often incompatible) programming languages such as SQL, Python, and Scala, and APIs like Spark vs Pandas, TensorFlow vs MLFlow, etc. FRIDAAY replaces these with a simple yet extensible "programming format" based on YAML that enables:
- fine-grained orchestration
- full-fidelity no-code visual programming of data pipelines
- platform and language independence
- reusable specification of dashboards and data apps  
- inline tests and alerting
- uniform specification of external integrations
- schema-aware autocompletion and templates
- ad-hoc materialization and incrementalism
- version-controlled user-facing semantic models and metric layers
- deterministic transformations between versions and vendors
- novel interaction paradigms beyond notebooks and REPLs
- turning legacy code into structured data, which we can manage using all our data superpowers

## Example
Available with the package in `folder = path_resource(PKG_ID, PIPE_FOLDER)`
```
fridaay:
  version: 0.1
  do: core.init
  imports:
   sql: dad_sql_pandas
  set: # global constants (COMMENT)
    NAME: demo_pets
    SAPIENT: Human

test_data:
  doc: Sample data for test purposes
  do: sql.load
  columns: ['Name','Age','Weight', 'Type', 'Timestamp']
  data:
  - ['Ernie', 54, 170.5, 'Human Tech Nerd', 2020-03-20]
  - ['Qhuinn', 7, 36.3, 'English Cocker Spaniel', 2022-06-27]
  - ['Frolic', 2, 76.2, 'Chocolate Labrador', 2022-06-27]

demo_pets:
  do: sql.select
  from: $$ # last frame
  cols:
    Name: .str Personal Name
    Age: .int.year Age
    Weight: .float.pound Current Weight
  where_all:
  - ["Name","!=",Ernie]
  #- ['Timestamp','>', 2022-01-01]
  save: [table]
```

# Releases
```
$ poetry version patch
$ poetry build && poetry publish
$ poetry version prepatch
```
