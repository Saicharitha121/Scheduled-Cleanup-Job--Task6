import logging
import os
import datetime
import json
import pyodbc
from azure.storage.blob import BlobServiceClient

import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(microsecond=0)
    logging.info(f"Timer trigger started at {utc_timestamp}")

    # SQL connection
    conn_str = os.environ["SQL_CONNECTION_STRING"]
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Calculate cutoff date (30 days ago)
    cutoff = (datetime.datetime.utcnow() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')

    # Select old rows
    cursor.execute("SELECT * FROM Orders WHERE OrderDate < ?", cutoff)

    rows = cursor.fetchall()
    if not rows:
        logging.info("No old orders to archive.")
        return

    # Prepare NDJSON content
    ndjson_lines = []
    columns = [column[0] for column in cursor.description]
    for row in rows:
        ndjson_lines.append(json.dumps(dict(zip(columns, row))))

    # Blob path: archive/orders/YYYY/MM/DD/orders_<timestamp>.ndjson
    blob_service_client = BlobServiceClient.from_connection_string(os.environ["AzureWebJobsStorage"])
    container_name = os.environ["BLOB_CONTAINER_NAME"]

    today = datetime.datetime.utcnow()
    blob_path = f"{today.year}/{today.month:02d}/{today.day:02d}/orders_{today.strftime('%H%M%S')}.ndjson"

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_path)

    # Upload NDJSON
    blob_client.upload_blob("\n".join(ndjson_lines))

    # Delete archived rows
    cursor.execute("DELETE FROM Orders WHERE OrderDate < ?", cutoff)
    conn.commit()

    logging.info(f"Archived {len(rows)} rows to blob {blob_path}")
    cursor.close()
    conn.close()
