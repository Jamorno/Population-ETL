# 🧬 Population ETL Project

This ETL (Extract, Transform, Load) pipeline fetches U.S. population data from a public API, processes it using Python, and loads it into a PostgreSQL database. The project also exports the final dataset into a CSV file for further analysis.

---

## Features

- Extracts real-time population data via API
- Transforms and cleans the data using pandas
- Loads data into PostgreSQL database
- Exports the results to `summary_population.csv`
- Uses `.env` for secure configuration
- Built with modular OOP design

---

## Tech Stack

- Python 3
- pandas
- requests
- psycopg2
- python-dotenv
- PostgreSQL

---

## Output
- population.log – Logs of the ETL process
- summary_population.csv – Exported dataset
- PostgreSQL table: population_stats

---

## Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/Jamorno/COVID-19-Tracker-ETL.git
cd COVID-19-Tracker-ETL

# 2. Set up a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
touch .env

# Paste into .env file
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password_here

# 5. Run the ETL pipeline
python main.py
```
