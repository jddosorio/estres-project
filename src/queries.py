"""Validated ClickHouse queries used by the dashboard."""

from __future__ import annotations

import re

import pandas as pd
import streamlit as st

from src.clickhouse_client import configured_database, get_client


_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def quote_identifier(value: str) -> str:
    """Quote a ClickHouse identifier after strict validation."""
    if not _IDENTIFIER.fullmatch(value):
        raise ValueError(f"Unsupported ClickHouse identifier: {value!r}")
    return f"`{value}`"


def qualified_table(table: str) -> str:
    database = configured_database()
    return f"{quote_identifier(database)}.{quote_identifier(table)}"


@st.cache_data(ttl=30, show_spinner=False)
def connection_info() -> pd.DataFrame:
    return get_client().query_df(
        "SELECT now() AS server_time, currentUser() AS user, version() AS version"
    )


@st.cache_data(ttl=30, show_spinner=False)
def list_tables() -> list[str]:
    database = configured_database()
    result = get_client().query_df(
        "SELECT name FROM system.tables WHERE database = {database:String} ORDER BY name",
        parameters={"database": database},
    )
    return result["name"].astype(str).tolist()


@st.cache_data(ttl=30, show_spinner=False)
def describe_table(table: str) -> pd.DataFrame:
    return get_client().query_df(f"DESCRIBE TABLE {qualified_table(table)}")


@st.cache_data(ttl=60, show_spinner=False)
def preview_table(table: str, limit: int = 100) -> pd.DataFrame:
    limit = max(1, min(int(limit), 5000))
    return get_client().query_df(
        f"SELECT * FROM {qualified_table(table)} LIMIT {{limit:UInt32}}",
        parameters={"limit": limit},
    )


@st.cache_data(ttl=60, show_spinner=False)
def read_environment_data(
    table: str,
    x_column: str,
    temperature_column: str,
    humidity_column: str,
    hours: int,
    limit: int,
    use_time_filter: bool,
) -> pd.DataFrame:
    table_sql = qualified_table(table)
    x_sql = quote_identifier(x_column)
    temperature_sql = quote_identifier(temperature_column)
    humidity_sql = quote_identifier(humidity_column)
    limit = max(10, min(int(limit), 100000))

    where_sql = ""
    parameters: dict[str, int] = {"limit": limit}
    if use_time_filter:
        where_sql = f"WHERE {x_sql} >= now() - INTERVAL {{hours:UInt32}} HOUR"
        parameters["hours"] = max(1, min(int(hours), 24 * 365))

    query = f"""
        SELECT
            {x_sql} AS x_value,
            {temperature_sql} / 1000.0 AS temperature_c,
            {humidity_sql} / 1000.0 AS humidity_pct
        FROM {table_sql}
        {where_sql}
        ORDER BY {x_sql} DESC
        LIMIT {{limit:UInt32}}
    """
    result = get_client().query_df(query, parameters=parameters)
    return result.sort_values("x_value").reset_index(drop=True)

