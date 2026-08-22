import pandas as pd
from sqlalchemy import create_engine, text

# Database Credentials
DB_USER = "root"
DB_PASSWORD = "anas4915??"  # MY SQL PASSWORD
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "ev_fleet_telemetry_db"

# Create Database if not exists
base_engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}")

with base_engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};"))
    conn.commit()
    print(f"Database '{DB_NAME}' created or verified.")

# Target Database Engine
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Read CSV Files
print("Reading CSV files from data/ folder...")
df_vehicles = pd.read_csv('data/dim_vehicles.csv')
df_telemetry = pd.read_csv('data/fact_telemetry.csv')

# Load to MySQL
print("Uploading dim_vehicles table...")
df_vehicles.to_sql('dim_vehicles', con=engine, if_exists='replace', index=False)

print("Uploading fact_telemetry table (50,000 records, please wait)...")
df_telemetry.to_sql('fact_telemetry', con=engine, if_exists='replace', index=False, chunksize=5000)

print("Data successfully loaded into MySQL database.")