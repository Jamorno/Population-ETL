from config import db_config
import requests, logging, psycopg2
import pandas as pd

logging.basicConfig(
    filename="population.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class PopulationETL:
    def __init__(self, api_url):
        self.api_url = api_url
        self.conn = psycopg2.connect(**db_config)

    def extract_data(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()
            logging.info("Data extracted from API")
            return data
        except Exception as e:
            logging.error(f"Failed to fetch API: {e}")
            return None

    def transform_data(self, raw_data):
        try:
            records = []
            for data in raw_data["data"]:
                records.append({
                    "nation": data.get("Nation"),
                    "year": data.get("Year"),
                    "population": data.get("Population")
                })

            df = pd.DataFrame(records)
            logging.info(f"Transformed {len(df)} records.")
            return df

        except Exception as e:
            logging.error(f"Error transforming data: {e}")
            return pd.DataFrame()

    def load_data_to_database(self, df):
        try:
            cursor = self.conn.cursor()

            cursor.execute("DROP TABLE IF EXISTS population_stats")

            cursor.execute(
                """CREATE TABLE IF NOT EXISTS population_stats (nation TEXT, year TEXT, population INTEGER)"""
            )

            for _, row in df.iterrows():
                cursor.execute(
                    """INSERT INTO population_stats (nation, year, population) VALUES (%s, %s, %s)""", (
                        row["nation"], row["year"], row["population"]
                    )
                )

            self.conn.commit()
            logging.info("Loaded data to postgreSQL.")

        except Exception as e:
            logging.error("Error to load data to postgreSQL")

        finally:
            cursor.close()

    def export_summary(self, output_csv="summary_population.csv"):
        try:
            query ="SELECT * FROM population_stats"
            df = pd.read_sql(query, self.conn)
            df.to_csv(output_csv, index=False)
            logging.info(f"Exported summary to {output_csv}")

        except Exception as e:
            logging.error(f"Failed to export summary: {e}")

    def run(self):
        raw = self.extract_data()
        if raw is None:
            logging.error("No data to process.")
            return

        df = self.transform_data(raw)
        if df.empty:
            logging.warning("No data after transformation.")
            return

        self.load_data_to_database(df)
        self.export_summary()

        self.conn.close()

        logging.info("ETL process completed.")
        logging.info("..............................................................................")