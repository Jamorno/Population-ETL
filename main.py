from etl import PopulationETL

if __name__ == "__main__":
    api_url = "https://datausa.io/api/data?drilldowns=Nation&measures=Population"
    etl = PopulationETL(api_url)
    etl.run()