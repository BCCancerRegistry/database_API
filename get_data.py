"""from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import json
import pyodbc
import os
app = FastAPI()

# Load configuration from a JSON file
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

# Sample config.json
# {
#     "tables": {
#         "table1": {
#             "columns": ["column1", "column2"],
#             "filters": {"column1": "value1", "column2": "value2"}
#         },
#         "table2": {
#             "columns": ["column3", "column4"],
#             "filters": {"column3": "value3"}
#         }
#     }
# }

class TableData(BaseModel):
    table_name: str
    data: list


server = os.getenv("SERVER")
database = os.getenv("DATABASE")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
# Database connection settings
conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password}"
)

# Define an asset endpoint to retrieve data based on the configuration and filters
@app.get('/messages/{table_name}', response_model=TableData)
def get_table_data(table_name: str, filters: dict = Query({}, alias="filter_")):
    if table_name in config_data['tables']:
        # Assume you have a function to fetch data from the database
        # Replace this with your actual database retrieval logic
        table_columns = config_data['tables'][table_name]['columns']
        table_filters = config_data['tables'][table_name]['filters']

        # Apply filters provided in the request, overriding default filters from config
        table_filters.update(filters)

        table_data = retrieve_data_from_database(table_name, table_columns, table_filters)

        return {"table_name": table_name, "data": table_data}
    else:
        raise HTTPException(status_code=404, detail="Table not found")

def retrieve_data_from_database(table_name, table_columns, table_filters):
    try:
        # Establish a connection to the SQL Server database
        with pyodbc.connect(conn_str) as conn:
            # Create a cursor
            cursor = conn.cursor()

            # Construct the SQL query based on table name, columns, and filters
            query = (
                f"SELECT {', '.join(table_columns)} FROM {table_name} "
                f"WHERE {' AND '.join(f'{column} = ?' for column in table_filters)}"
            )

            # Execute the query with filter values
            cursor.execute(query, list(table_filters.values()))

            # Fetch all rows
            rows = cursor.fetchall()

            # Convert rows to a list of dictionaries
            data = [dict(zip(table_columns, row)) for row in rows]

            return data
    except pyodbc.Error as e:
        print(f"Error connecting to the database: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
"""