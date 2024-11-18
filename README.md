# Fast startup process:

- `git clone https://github.com/Meta-Champ/backend`
- `cd ./sim-backend`
- `python3.12 -m pip install poetry`
- `poetry install`
- `poetry run alembic init migration`

Move `alembic.ini.example` to `alembic.ini`, configure and create first migration:
- `poetry run alembic revision --autogenerate -m '000000_initial'`
(Example of migration result: 0c470d5da040_initial)
- `poetry run alembic upgrade head`

Move `.env.examle` to `.env`, configure settings and run project:
- `poetry run python3.12 main.py`

F.A.Q. for work with alembic:
- https://habr.com/ru/articles/585228/
- https://konstantinklepikov.github.io/myknowlegebase/notes/alembic.html
