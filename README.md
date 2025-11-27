# Scheduled-Cleanup-Job--Task6

This Azure Function runs every night at 02:00 UTC, finds all Orders older than 30 days in Azure SQL, archives them into NDJSON files in Blob Storage, and deletes those rows from the database after successful archiving.

1. Prerequisites
Azure Resources Needed

- Azure SQL Database

- Must contain an Orders table with a OrderDate field.

- Server firewall must allow Azure services or Function App IP.

Azure Storage Account

- Container: archive

Output folder structure:
archive/orders/YYYY/MM/DD/

-Azure Function App

-Runtime: Python or C#

-Timer trigger enabled.


Local Development Requirements

- VS Code or Visual Studio

- Azure Functions Core Tools

- Python 3.9+ (if using Python)

 - Azure CLI


What the Function Does

- Connects to Azure SQL.

- Selects records older than 30 days using batching (e.g., 1000 rows).

- Generates an NDJSON file with one JSON object per line.

- Saves the file to Blob Storage:

- Deletes the same rows from SQL inside a transaction.

NDJSON Example Output
{"OrderID":1, "Customer":"Sai", "Amount":200, "OrderDate":"2024-09-20"}
{"OrderID":2, "Customer":"Charitha", "Amount":150, "OrderDate":"2024-09-10"}
