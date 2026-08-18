"""Command-line ClickHouse connection check using Streamlit secrets."""

from pathlib import Path

import clickhouse_connect
import tomllib


project_dir = Path(__file__).resolve().parents[1]
secrets_path = project_dir / ".streamlit" / "secrets.toml"

if not secrets_path.exists():
    raise SystemExit(
        "Missing .streamlit/secrets.toml. Copy secrets.toml.example and add the password."
    )

with secrets_path.open("rb") as file:
    config = tomllib.load(file)["clickhouse"]

client = clickhouse_connect.get_client(
    host=config["host"],
    port=int(config.get("port", 8443)),
    username=config["username"],
    password=config["password"],
    database=config.get("database", "default"),
    secure=True,
)

row = client.query("SELECT currentUser(), version(), now()").first_row
print(f"Connected user: {row[0]}")
print(f"ClickHouse version: {row[1]}")
print(f"Server time: {row[2]}")

