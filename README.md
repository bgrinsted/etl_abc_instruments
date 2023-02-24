# etl_abc_instruments

## Overview

This is a simple ETL pipeline that takes a CSV file of ABC Instruments data and transforms it into an analytical model
hosted in a SQLite database.

## Behaviour

Any files in the `data/raw` directory will be processed and moved to the `data/raw/processed` directory. The processed
data will be loaded into the SQLite database `data/published/order_deliveries.db`.

## ETL Process

1. Read CSV file from `data/raw` directory.
2. Transform data into a pandas DataFrame.
3. Clean data.
4. Load data into SQLite database.
5. Move processed file to `data/raw/processed` directory.

## Getting Started (macOS, Linux, Windows)

1. Download and unpack the zip file
2. Open a terminal
3. Enter project directory: `cd etl-abc-instruments`
4. Follow the instructions below for your operating system.

## Option 1: Docker

- For Windows users; to view the SQLite database file in a GUI (e.g. DBeaver, JetBrains) the database needs to be copied
  to a native Windows mount.
- Further information can be found here [DBeaver](https://github.com/dbeaver/dbeaver/issues/17217) and here [JetBrains](https://youtrack.jetbrains.com/issue/DBE-11014)
- If unsure and running Windows, follow Option 3.

### Prerequisites

1. Docker installed.
    - **macOS**: [Install Docker Desktop](https://docs.docker.com/desktop/).
    - **Linux/Ubuntu**: [Install Docker Compose](https://docs.docker.com/compose/install/)
      and [Install Docker Engine](https://docs.docker.com/engine/install/).

2. Executing the following command will build the Docker image and run the app:
```bash
docker build -t etl_abc_instruments . && \
docker run \
-v $(pwd)/data/raw:/app/data/raw \
-v $(pwd)/data/raw/processed:/app/data/raw/processed \
-v $(pwd)/data/published:/app/data/published \
--rm --name etl_abc_instruments-container etl_abc_instruments
```

## Option 2: macOS, Linux:

1. Create virtual environment: `python -m venv venv`
2. Activate virtual env: `source venv/bin/activate`
3. Install requirements: `pip install -r requirements`
4.  Run app: `python main.py`

## Option 3: Windows:

1. Create virtual environment: `python -m venv venv`
2. Activate virtual env: `venv\Scripts\activate`
3. Install requirements: `pip install -r requirements`
4. Run app: `python main.py`

## Running the tests

1. Activate virtual env: `source venv/bin/activate` or `venv\Scripts\activate`
2. Run tests: `pytest`

## Project Layout

```
├── Dockerfile
├── README.md
├── assets
│   └── targert_erd.png
├── conftest.py
├── data
│   ├── published
│   │   └── order_delivery.db
│   ├── raw
│   │   ├── abc_insturments_orders_deliveries.csv
│   │   └── processed
│   └── schemas
│       └── raw_schema.yml
├── main.py
├── requirements.txt
├── src
│   ├── database.py
│   ├── filereader.py
│   ├── loader.py
│   ├── mappings.py
│   ├── transformer.py
│   └── utils
│       └── utils.py
└── tests
    └── test_utils.py
```

## Target Database Model

![targert_erd.png](assets%2Ftargert_erd.png)

## Querying the model

- The design maintains a current view of the orders (i.e. FACT_ORDER_ITEMS history isn't preserved)
- Dimension changes are captured, preserving previous version, though not bound to a timeperiod, nor flagged as such.
- Queries should use FACT_ORDER_ITEMS as the entry point to the model.