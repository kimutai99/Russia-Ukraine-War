import pandas as pd
import requests
import io
import psycopg2
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Kobo credentials
KOBO_USERNAME = os.getenv("KOBO_USERNAME")
KOBO_PASSWORD = os.getenv("KOBO_PASSWORD")
KOBO_CSV_URL = "https://kf.kobotoolbox.org/api/v2/assets/aZXWsZGZhqLn3xMaXUDff7/export-settings/esLzUHFGpDxBvpUMp7hofRS/data.csv"

# PostgreSQL credentials
PG_HOST = os.getenv("PG_HOST")
PG_DATABASE = os.getenv("PG_DATABASE")
PG_USER = os.getenv("PG_USERNAME")  # ✅ Fixed: using correct variable
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_PORT = int(os.getenv("PG_PORT", "5432"))

# Schema and table details
schema_name = "war"
table_name = "russia_ukraine_conflict"

# Step 1: Fetch data from Kobo Toolbox
print("📥 Fetching data from Kobo Toolbox...")
response = requests.get(KOBO_CSV_URL, auth=HTTPBasicAuth(KOBO_USERNAME, KOBO_PASSWORD))

if response.status_code == 200:
    print("✅ Data fetched successfully.")

    # Load data into DataFrame
    df = pd.read_csv(io.StringIO(response.text), sep=';', on_bad_lines='skip')

    # Step 2: Clean and transform
    print("🧹 Processing data...")
    df.columns = [col.strip().replace(" ", "_").replace("&", "and").replace("-", "_") for col in df.columns]

    # Parse only the "Date" column
    df["Date"] = pd.to_datetime(df.get("Date"), errors="coerce")

    # Calculate total soldier casualties
    df["Total_Soldier_Casualties"] = df[["Casualties", "Injured", "Captured"]].sum(axis=1, skipna=True)

    # Step 3: Upload to PostgreSQL
    print("🚀 Uploading to PostgreSQL...")

    conn = psycopg2.connect(
        host=PG_HOST,
        database=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
        port=PG_PORT
    )
    cur = conn.cursor()

    # Create schema if not exists
    cur.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")

    # Drop and recreate table
    cur.execute(f"DROP TABLE IF EXISTS {schema_name}.{table_name};")
    cur.execute(f"""
        CREATE TABLE {schema_name}.{table_name} (
            id SERIAL PRIMARY KEY,
            "start" TEXT,
            "end" TEXT,
            "date" DATE,
            country TEXT,
            event TEXT,
            oblast TEXT,
            casualties INT,
            injured INT,
            captured INT,
            civilian_casualties INT,
            new_recruits INT,
            combat_intensity FLOAT,
            territory_status TEXT,
            percentage_occupied FLOAT,
            area_occupied FLOAT,
            Total_Soldier_Casualties INT
        );
    """)

    # Insert rows
    insert_query = f"""
        INSERT INTO {schema_name}.{table_name} (
            "start", "end", "date", country, event, oblast,
            casualties, injured, captured, civilian_casualties,
            new_recruits, combat_intensity, territory_status,
            percentage_occupied, area_occupied, Total_Soldier_Casualties
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        cur.execute(insert_query, (
            row.get("start"),
            row.get("end"),
            row.get("Date"),
            row.get("Country"),
            row.get("Event"),
            row.get("Oblast"),
            int(row.get("Casualties", 0)) if pd.notna(row.get("Casualties")) else 0,
            int(row.get("Injured", 0)) if pd.notna(row.get("Injured")) else 0,
            int(row.get("Captured", 0)) if pd.notna(row.get("Captured")) else 0,
            int(row.get("Civilian_Casualties", 0)) if pd.notna(row.get("Civilian_Casualties")) else 0,
            int(row.get("New_Recruits", 0)) if pd.notna(row.get("New_Recruits")) else 0,
            float(row.get("Combat_Intensity", 0)) if pd.notna(row.get("Combat_Intensity")) else 0,
            row.get("Territory_Status"),
            float(row.get("Percentage_Occupied", 0)) if pd.notna(row.get("Percentage_Occupied")) else 0,
            float(row.get("Area_Occupied", 0)) if pd.notna(row.get("Area_Occupied")) else 0,
            int(row.get("Total_Soldier_Casualties", 0)) if pd.notna(row.get("Total_Soldier_Casualties")) else 0,
        ))

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Data successfully loaded into PostgreSQL!")

else:
    print(f"❌ Failed to fetch data. Status code: {response.status_code}")
