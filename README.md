# CaboGest

CaboGest is a lightweight Python application for managing small business data and operations. It provides a simple modular structure for configuration, entities, UI, and utilities—designed for easy customization and local deployment.

**Key features**
- Clean, modular Python codebase for quick iteration
- Database schema included for easy local setup (`cabogest_db.sql`)
- Simple CLI/GUI entry via `main.py`

**Repository layout**

- `main.py` — application entry point
- `cabogest_db.sql` — database schema dump
- `modules/` — application modules
  - `db_config.py` — database connection/config
  - `entities.py` — domain entities and models
  - `ui.py` — user interface components
  - `utils.py` — helper utilities

Database
--------

This repository includes `cabogest_db.sql`, a SQL dump you can use to create a local MySQL database.

MySQL / MariaDB example:

```bash
# replace USER and DBNAME with your values
mysql -u USER -p DBNAME < cabogest_db.sql
```

Running the app
---------------

Run the main entry point from the project root:

```bash
python main.py
```

If the application expects environment variables or a config file, set them before running. See `modules/db_config.py` for database configuration and connection details.

Development notes
-----------------

- Code is organized under `modules/` — small, focused modules make it easy to extend.
- Tests: none included by default. Add tests under a `tests/` folder and run with `pytest`.

Contributing
------------

Contributions are welcome. Open an issue to discuss changes, then submit a pull request with a clear description and tests where applicable.

Contact
-------

For questions or help, open an issue in this repository.
