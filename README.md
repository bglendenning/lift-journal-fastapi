# Lift Journal FastAPI

## Installing the requirements

```bash
user@host:./lift-journal-fastapi$ python -m venv <venv_dir>
user@host:./lift-journal-fastapi$ source <venv_dir>/bin/systemd-socket-activate
user@host:./lift-journal-fastapi$ pip install -r requirements.txt
```

## Configuring the environment

```bash
# Secret key (for generating JWT)
user@host:./lift-journal-data$ export LIFT_JOURNAL_FASTAPI_SECRET_KEY=<secret_key>

# Granular database configuration
user@host:./lift-journal-data$ export LIFT_JOURNAL_DATA_DB_ENGINE=<database engine>
user@host:./lift-journal-data$ export LIFT_JOURNAL_DATA_DB_USERNAME=<database username>
user@host:./lift-journal-data$ export LIFT_JOURNAL_DATA_DB_PASSWORD=<database password>
user@host:./lift-journal-data$ export LIFT_JOUNRAL_DATA_DB_SERVER=<database server>
user@host:./lift-journal-data$ export LIFT_JOURNAL_DATA_DB_NAME=<database name>

# URL database configuration
user@host:./lift-journal-data$ export LIFT_JOURNAL_DATA_DB_URL=<database url>
```

## Managing the database

_[Lift Journal Data](https://github.com/bglendenning/lift-journal-data)_ provides database management functions. The script provides three command line arguments:

* `--create-tables` creates all non-existent tables defined in the ORM models
* `--drop-tables` drops all existent tables defined in the ORM models
* `--load-lifts` populates the `lift` table with fixture data

```bash
user@host:./lift-journal-data$ ljd_manage <arguments>
```

## Running the development server

```bash
user@host:./lift-journal-data/lift_journal_fastapi$ fastapi dev main.py
```
