"""Functions to communicate with the text to SQL app database."""

from typing import Any, List, Tuple

import sqlalchemy as sa
from sqlalchemy import schema
from sqlalchemy import sql


# SQL Database type (Used to prompt LLM)
sql_database_type = "SQLite"
# Create SQLAlchemy engine
_dbname = "sample.db"
_engine = sa.create_engine(f"sqlite:///{_dbname}")


def get_sql_schema() -> str:
    """Returns the schema for all SQL tables in the DB as a string."""
    metadata = sa.MetaData()
    metadata.reflect(bind=_engine)
    schema_string = ""
    for table in metadata.tables.values():
        schema_string += str(schema.CreateTable(table))
    return schema_string


def is_valid_sql(raw_sql: str) -> bool:
    """Returns True if the raw_sql input is a valid SQL statment.

    Args:
        raw_sql: Raw SQL statement to test validity.
    """
    explain_sql = f"Explain {raw_sql}"
    with _engine.connect() as con:
        try:
            con.execute(sql.text(explain_sql))
            return True
        except sa.exc.OperationalError:
            return False


def _execute_sql(raw_sql: str) -> sa.CursorResult[Any]:
    """Executes raw SQL statement.

    Args:
        raw_sql: Raw SQL statement to query the database.

    Returns:
        A sqlalchemy cursor result object from executing the raw SQL.
    """
    with _engine.connect() as con:
        result = con.execute(sql.text(raw_sql))
        return result


def get_sql_results_headers_and_values(
    raw_sql: str
) -> Tuple[List[str], List[List[Any]]]:
    """Returns a list of headers and results from executing raw SQL statement.

    Args:
        raw_sql: Raw SQL statement to query the database.

    Returns:
        column_headers_list: A list of the column names for the
            results of executing the raw_sql query.
        results_list: A list of the result rows from executing the raw_sql
            query on the database.
    """
    sql_result = _execute_sql(raw_sql)
    column_headers_list = list(sql_result.keys())
    results_list = [list(row) for row in sql_result]
    return column_headers_list, results_list
