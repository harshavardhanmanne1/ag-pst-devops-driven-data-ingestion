# ag-pst-devops-driven-data-ingestion
# Analog devices

## This project demonstrates DevOps-driven data ingestion and analysis using Docker, PostgreSQL, Python, and Pandas.
Demonstration of a data ingestion pipeline where movie datasets (CSV files) are loaded into a PostgreSQL database using Python (Pandas + SQLAlchemy).
The system is fully containerized using Docker & Docker Compose, making it portable and easy to run anywhere.

The pipeline automates:
1. Spinning up a PostgreSQL database inside Docker.
2. Ingesting multiple CSV datasets into structured database tables.
3. Running SQL queries for analysis inside the containerized environment.


## Technologies & Tools Used

1. Python 3.10 (data ingestion & queries)
2. Pandas (CSV -> PostgreSQL ingestion)
3. SQLAlchemy (Python DB connection)
4. PostgreSQL 15 (database)
5. Docker & Docker Compose (containerization)


## Structure of the project:
```bash
├── data/
│   ├── tmdb_5000_movies1.csv     # Movie metadata (budget, language, title, etc.)
│   ├── tmdb_5000_movies2.csv     # Movie details (revenue, runtime, ratings, etc.)
│   └── tmdb_5000_movies3.csv     # Movie cast & crew info
│
├── ingest/
│   ├── Dockerfile                # Python image setup for ingestion service
│   ├── main.py                   # Main ingestion & analysis logic
│   ├── requirements.txt          # Python dependencies
│
├── .env                          # Environment variables (DB credentials)
├── docker-compose.yml            # Defines database + ingestion services
└── README.md                     # Project documentation
```

## Installation and setup

1. Clone the repository:
```shell
git clone <your_repo_url>
cd ag-pst-devops-driven-data-ingestion
```
2.  Create .env File:

```env
DB_USER=admin
DB_PASS=admin123
DB_NAME=mydb
```
3. Build and run with Docker Compose
```bash
docker-compose down -v
docker-compose up --build
```
This will:
* Start a PostgreSQL container (``postgres_db``)
* Start the ingestion service (``ingest_service``) that:
   * Waits for DB readiness
   * Loads all CSV data into tables
   * Runs sample queries

## Workflow

1. ``docker-compose.yml``
   * Defines two services:
     * ``postgres_db`` (PostgreSQL database)
     * ``ingest_service`` (Python ingestion)
2. ``Dockerfile`` (ingest/)
   * Builds a lightweight Python image
   * Installs dependencies from ``requirements.txt``
   * Runs ``main.py``
3. ``main.py``
   * Waits for PostgreSQL to be ready
   * Loads CSV datasets into tables (``movie_metadata``, ``movie_details``, ``movie_castcrew``) using Pandas ``to_sql``
   * Executes sample queries and prints results
4. ``requirements.txt``
   * Contains Python libraries:
```php
pandas
sqlalchemy
psycopg2-binary
```
5. ``.env``
   * Stores DB credentials (kept outside code for security)
6. ``data/*.csv``
   * TMDB 5000 Movies datasets of 3 different CSV files.


## Running the Pipeline

When you run ``docker-compose up --build``, the following happens automatically:
1. PostgreSQL database starts inside Docker.
2. ``ingest_service`` waits until DB is ready.
3. CSVs (``tmdb_5000_movies*.csv``) are read with Pandas.
4. Pandas writes them into 3 PostgreSQL tables:
   * ``movie_metadata``
   * ``movie_details``
   * ``movie_castcrew``
5. Example SQL queries are executed and results are printed in logs.


## Output

* Data is ingested into PostgreSQL automatically.
* SQL queries produce logs (visible in Docker logs).
* Screenshots confirm successful ingestion & analysis.
  
### Screenshots (Project Execution Walkthrough)

1. **Docker Image Build:**
   * The Python ingestion service image was built successfully.  
   * This confirms that the `Dockerfile` inside `ingest/` was executed correctly.  

      <img width="720" height="1080" alt="Screenshot (57)" src="https://github.com/user-attachments/assets/d70e1e66-302f-4225-a2a0-a5245ab45992" />

2. **Docker Build Logs:** Showing the step-by-step installation of dependencies and preparation of the image.  
   * Build Info & Status
     
      <img width="720" height="1080" alt="Screenshot (59)" src="https://github.com/user-attachments/assets/a052edcb-5fcb-4047-a5a4-d97b08a28dc9" />

   * Build Stats (timing & layers)
     
      <img width="720" height="1080" alt="Screenshot (60)" src="https://github.com/user-attachments/assets/d0417234-8ad2-4950-a534-1a714c8f6f94" />

   * Detailed Logs
     
      <img width="720" height="1080" alt="Screenshot (61)" src="https://github.com/user-attachments/assets/9f3341b5-bf76-4886-add4-a07dd515cadb" />

3. **Running Containers**
   * Both containers (`postgres_db` and `ingest_service`) are running successfully.  
   * This validates that `docker-compose.yml` orchestrated the services correctly.  

      <img width="720" height="1080" alt="Screenshot (62)" src="https://github.com/user-attachments/assets/8c9a01b4-fd20-4c45-99c3-bd19b20ba789" />

4. **Docker Volumes**
   * PostgreSQL data is persisted in a Docker volume (`db_data`).  
   * This ensures that even if the container restarts, the data remains intact.
     
      <img width="720" height="1080" alt="Screenshot (58)" src="https://github.com/user-attachments/assets/5b8b4bab-f54a-485e-ac67-d29f982c1325" />

5. **PostgreSQL Logs**
   * Logs from the Postgres container confirming that the database initialized correctly and is ready to accept connections.  

      <img width="720" height="1080" alt="Screenshot (63)" src="https://github.com/user-attachments/assets/63a8fd36-d51f-4a26-8aff-78cd6cd60607" />

6. **Query Outputs:** the shows the ingestion pipeline loaded CSV data into PostgreSQL, and queries were executed successfully.
   * Top 5 Movies by Revenue
     
      <img width="720" height="560" alt="Screenshot (55)" src="https://github.com/user-attachments/assets/f10bd4eb-786b-4228-9662-5e62f406ade9" />
      
   * Top 5 Movies by Average Rating, Insert, and Join Query
     
      <img width="720" height="560" alt="Screenshot (56)" src="https://github.com/user-attachments/assets/2e885db3-9c3b-47c2-a7a1-034851508584" />

## Summary
* PostgreSQL database runs in a container
* CSV data is ingested automatically with Pandas
* SQL queries confirm ingestion & analysis
* Docker Desktop screenshots validate images, containers, logs, and volumes
