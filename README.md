# Scheduled-Cleanup-Job--Task6

This Azure Function runs every night at 02:00 UTC, finds all Orders older than 30 days in Azure SQL, archives them into NDJSON files in Blob Storage, and deletes those rows from the database after successful archiving.

1. Prerequisites
Azure Resources Needed

- Azure SQL Database

Must contain an Orders table with a OrderDate field.

- Azure Storage Account

Container: archive

Output folder structure:
archive/orders/YYYY/MM/DD/

- Azure Function App

- Runtime: Python or C#


  

