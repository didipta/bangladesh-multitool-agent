from pathlib import Path
import sqlite3

import pandas as pd
from datasets import load_dataset


BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "databases"

DB_DIR.mkdir(parents=True, exist_ok=True)


DATASETS = {
    "institutions": {
        "repo": "Mahadih534/Institutional-Information-of-Bangladesh",
        "db": "institutions.db",
        "table": "institutions",
    },
    "hospitals": {
        "repo": "Mahadih534/all-bangladeshi-hospitals",
        "db": "hospitals.db",
        "table": "hospitals",
    },
    "restaurants": {
        "repo": "Mahadih534/Bangladeshi-Restaurant-Data",
        "db": "restaurants.db",
        "table": "restaurants",
    },
}


def clean_column_name(column: str) -> str:
    """Convert column names into SQLite-friendly names."""

    return (
        str(column)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        .replace("(", "")
        .replace(")", "")
    )


def convert_dataset(name: str, config: dict):
    print("\n" + "=" * 60)
    print(f"Processing: {name}")
    print("=" * 60)

    print(f"Dataset: {config['repo']}")

    # Download/load dataset from Hugging Face
    dataset = load_dataset(config["repo"])

    print(f"Available splits: {list(dataset.keys())}")

    # Usually the dataset has a train split.
    split_name = list(dataset.keys())[0]

    df = dataset[split_name].to_pandas()

    print(f"Rows: {len(df)}")
    print(f"Original columns: {list(df.columns)}")

    # Clean column names
    df.columns = [
        clean_column_name(column)
        for column in df.columns
    ]

    print(f"Cleaned columns: {list(df.columns)}")

    # SQLite path
    db_path = DB_DIR / config["db"]

    # Remove old database if it exists
    if db_path.exists():
        db_path.unlink()

    # Create SQLite database
    with sqlite3.connect(db_path) as connection:

        df.to_sql(
            config["table"],
            connection,
            if_exists="replace",
            index=False,
        )

    print(f"✓ Database created: {db_path}")
    print(f"✓ Table created: {config['table']}")
    print(f"✓ Rows inserted: {len(df)}")


def main():
    print("\n🇧🇩 Bangladesh Multi-Tool Agent")
    print("Creating SQLite databases...\n")

    for name, config in DATASETS.items():
        try:
            convert_dataset(name, config)

        except Exception as error:
            print(f"\n❌ Failed to process {name}")
            print(f"Error: {error}")

    print("\n" + "=" * 60)
    print("DATABASE CREATION COMPLETED")
    print("=" * 60)

    print("\nDatabases:")

    for database in DB_DIR.glob("*.db"):
        print(f"✓ {database.name}")


if __name__ == "__main__":
    main()