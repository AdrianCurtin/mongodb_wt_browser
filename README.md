# MongoDB WiredTiger Browser

A Python tool to open MongoDB WiredTiger backups and export tables to various formats.

## Overview

MongoDB WiredTiger Browser is a command-line application that allows you to:
- Open and browse MongoDB WiredTiger database backups
- List all tables in a WiredTiger database
- View detailed information about specific tables
- Export individual tables or all tables to JSON or CSV formats

## Features

- 🔍 **Browse WiredTiger Databases**: Open and inspect MongoDB WiredTiger backup directories
- 📋 **List Tables**: Discover all tables stored in the database
- ℹ️ **Table Information**: Get detailed metadata about specific tables including record counts
- 📤 **Export Data**: Export table data to JSON or CSV formats
- 🚀 **Batch Export**: Export all tables at once
- 🔒 **Read-Only Mode**: Safely browse backups without modifying data
- 🎯 **Record Limiting**: Export a subset of records for testing or sampling

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

The tool provides a command-line interface with several commands:

### List All Tables

Display all tables in a WiredTiger database:

```bash
python cli.py list-tables /path/to/wiredtiger/db
```

Example output:
```
Found 5 table(s) in /path/to/wiredtiger/db:
--------------------------------------------------
  • collection-0-123456789
  • collection-1-987654321
  • index-2-111222333
  • sizeStorer
  • _mdb_catalog
```

### View Table Information

Get detailed information about a specific table:

```bash
python cli.py info /path/to/wiredtiger/db table_name
```

Example output:
```
Table Information: collection-0-123456789
--------------------------------------------------
Exists: True
Record Count: 1500

Configuration:
  key_format=q,value_format=u,type=file
```

### Export a Single Table

Export a table to JSON format:

```bash
python cli.py export /path/to/wiredtiger/db table_name output.json
```

Export a table to CSV format:

```bash
python cli.py export /path/to/wiredtiger/db table_name output.csv --format csv
```

Export with a record limit:

```bash
python cli.py export /path/to/wiredtiger/db table_name output.json --limit 100
```

### Export All Tables

Export all tables to a directory:

```bash
python cli.py export-all /path/to/wiredtiger/db ./exports
```

Export all tables as CSV:

```bash
python cli.py export-all /path/to/wiredtiger/db ./exports --format csv
```

Export all tables with record limit per table:

```bash
python cli.py export-all /path/to/wiredtiger/db ./exports --limit 1000
```

## Command Reference

### `list-tables`

List all tables in a WiredTiger database.

**Syntax:**
```bash
python cli.py list-tables DB_PATH
```

**Arguments:**
- `DB_PATH`: Path to the WiredTiger database directory

### `info`

Display information about a specific table.

**Syntax:**
```bash
python cli.py info DB_PATH TABLE_NAME
```

**Arguments:**
- `DB_PATH`: Path to the WiredTiger database directory
- `TABLE_NAME`: Name of the table to inspect

### `export`

Export a table to JSON or CSV format.

**Syntax:**
```bash
python cli.py export [OPTIONS] DB_PATH TABLE_NAME OUTPUT_FILE
```

**Arguments:**
- `DB_PATH`: Path to the WiredTiger database directory
- `TABLE_NAME`: Name of the table to export
- `OUTPUT_FILE`: Path to the output file

**Options:**
- `-f, --format [json|csv]`: Output format (default: json)
- `-l, --limit INTEGER`: Limit number of records to export

### `export-all`

Export all tables to the specified directory.

**Syntax:**
```bash
python cli.py export-all [OPTIONS] DB_PATH OUTPUT_DIR
```

**Arguments:**
- `DB_PATH`: Path to the WiredTiger database directory
- `OUTPUT_DIR`: Directory where exported files will be saved

**Options:**
- `-f, --format [json|csv]`: Output format (default: json)
- `-l, --limit INTEGER`: Limit number of records per table

## Output Formats

### JSON Format

JSON exports include metadata and structured records:

```json
{
  "table": "collection-0-123456789",
  "record_count": 100,
  "records": [
    {
      "key": "1",
      "value": "..."
    },
    {
      "key": "2",
      "value": "..."
    }
  ]
}
```

### CSV Format

CSV exports use a simple key-value structure:

```csv
key,value
1,"..."
2,"..."
```

## Python API

You can also use the tool programmatically in your Python code:

```python
from wt_browser import WiredTigerBrowser

# Using context manager (recommended)
with WiredTigerBrowser('/path/to/db') as browser:
    # List tables
    tables = browser.list_tables()
    print(f"Found {len(tables)} tables")
    
    # Get table info
    info = browser.get_table_info('table_name')
    print(f"Record count: {info['record_count']}")
    
    # Export to JSON
    browser.export_table_to_json('table_name', 'output.json')
    
    # Export to CSV
    browser.export_table_to_csv('table_name', 'output.csv', limit=1000)

# Manual connection management
browser = WiredTigerBrowser('/path/to/db')
browser.open()
try:
    tables = browser.list_tables()
finally:
    browser.close()
```

## Requirements

- `pymongo>=4.6.0`: MongoDB Python driver
- `wiredtiger>=11.2.0`: WiredTiger storage engine Python bindings
- `click>=8.1.7`: Command-line interface creation kit

## How It Works

1. **WiredTiger Connection**: The tool opens a read-only connection to the WiredTiger database
2. **Metadata Discovery**: Uses WiredTiger's metadata cursor to discover available tables
3. **Data Reading**: Opens cursors on individual tables to read key-value pairs
4. **Serialization**: Converts WiredTiger data types to Python types and serializes to JSON/CSV
5. **Export**: Writes formatted data to output files

## Common Use Cases

### Backup Analysis

Analyze MongoDB backups without restoring them to a running server:

```bash
python cli.py list-tables /backup/mongodb/data
python cli.py info /backup/mongodb/data _mdb_catalog
```

### Data Migration

Export data for migration to another system:

```bash
python cli.py export-all /backup/mongodb/data ./migration_data --format json
```

### Debugging

Inspect specific collections during debugging:

```bash
python cli.py export /backup/mongodb/data collection-0-123 debug_output.json --limit 10
```

### Testing

Extract sample data for testing:

```bash
python cli.py export /backup/mongodb/data collection-users test_users.json --limit 100
```

## Troubleshooting

### "Failed to open WiredTiger database"

- Ensure the path points to a valid WiredTiger database directory
- Check that the directory contains WiredTiger files (WiredTiger, WiredTiger.wt, etc.)
- Verify you have read permissions for the directory and files

### "Table not found"

- Use `list-tables` command first to see available tables
- MongoDB internal table names may differ from collection names
- Check for typos in the table name

### Binary Data in Exports

- WiredTiger stores binary data which may not be human-readable
- The tool attempts to decode as UTF-8, falling back to hex representation
- Consider the original MongoDB data types when interpreting exported data

## Limitations

- **Read-Only**: The tool only reads data; it cannot modify WiredTiger databases
- **Binary Data**: Complex binary data may not export cleanly to JSON/CSV
- **Schema-Less**: WiredTiger stores raw key-value pairs without schema information
- **MongoDB Specific**: Designed for MongoDB's use of WiredTiger; may not work with other WiredTiger applications

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available under the MIT License.

## Author

Adrian Curtin

## Acknowledgments

- Built with [WiredTiger](https://source.wiredtiger.com/) - High-performance storage engine
- Uses [Click](https://click.palletsprojects.com/) for CLI
- Designed for [MongoDB](https://www.mongodb.com/) backup analysis