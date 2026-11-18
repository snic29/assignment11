# Module 11

This FastAPI calculator supports addition, subtraction, multiplication, and
division. It also validates and stores calculations with SQLAlchemy and
Pydantic.

## Run Locally

Start PostgreSQL with the provided Compose service. It creates the `fastapi_db`
database at `localhost:5432` with the `postgres` user and password. The
integration-test fixture creates and drops the application tables, so use a
disposable database that contains no data you need.

```bash
docker compose up -d db
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install --with-deps chromium
pytest
```

The test suite includes unit, PostgreSQL integration, and Playwright
end-to-end tests. To run only the new calculation tests:

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fastapi_db \
  pytest tests/unit/test_calculation_factory.py \
         tests/unit/test_calculation_schema.py \
         tests/integration/test_calculation.py
```

To use a separate test database, create it once and point `DATABASE_URL` to it:

```bash
docker compose exec db createdb -U postgres assignment11_test
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/assignment11_test pytest
```

To run the application directly, set the database URL and start the server:

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fastapi_db \
  python3 main.py
```

The calculator is available at [http://localhost:8000](http://localhost:8000).
The `POST /calculations` endpoint accepts `a`, `b`, and a type of `Add`, `Sub`,
`Multiply`, or `Divide`.

## Docker Hub

The published image is
[stelni/assignment11](https://hub.docker.com/r/stelni/assignment11). Pull and run it with:

```bash
docker pull stelni/assignment11:latest
docker run --rm -p 8000:8000 stelni/assignment11:latest
```