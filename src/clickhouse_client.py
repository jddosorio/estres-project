"""ClickHouse Cloud connection shared by the Streamlit application."""

from __future__ import annotations

import clickhouse_connect
import streamlit as st


@st.cache_resource(show_spinner=False)
def get_client():
    """Create and cache one TLS connection pool for ClickHouse Cloud."""
    config = st.secrets["clickhouse"]
    return clickhouse_connect.get_client(
        host=config["host"],
        port=int(config.get("port", 8443)),
        username=config["username"],
        password=config["password"],
        database=config.get("database", "default"),
        secure=True,
        connect_timeout=15,
        send_receive_timeout=60,
    )


def configured_database() -> str:
    """Return the configured database name."""
    return str(st.secrets["clickhouse"].get("database", "default"))

