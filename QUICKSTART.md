# Quick Start Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/AdrianCurtin/mongodb_wt_browser.git
cd mongodb_wt_browser

# Install dependencies
pip install -r requirements.txt
```

## Quick Test

Run the included test demo to see all features:

```bash
python test_demo.py
```

This will:
1. Create a sample WiredTiger database
2. Demonstrate all CLI commands
3. Show example exports in JSON and CSV formats

## Basic Usage

### 1. List Tables in Your Database

```bash
python cli.py list-tables /path/to/your/mongodb/data
```

### 2. View Table Details

```bash
python cli.py info /path/to/your/mongodb/data table_name
```

### 3. Export a Table

**To JSON:**
```bash
python cli.py export /path/to/your/mongodb/data table_name output.json
```

**To CSV:**
```bash
python cli.py export /path/to/your/mongodb/data table_name output.csv --format csv
```

### 4. Export All Tables

```bash
python cli.py export-all /path/to/your/mongodb/data ./exports
```

## Common Scenarios

### Analyzing a MongoDB Backup

```bash
# First, find what tables are in the backup
python cli.py list-tables /backup/mongodb/dbPath

# Get details about a specific collection
python cli.py info /backup/mongodb/dbPath collection-0-12345

# Export the collection
python cli.py export /backup/mongodb/dbPath collection-0-12345 my_data.json
```

### Sampling Data

Export just the first 100 records:

```bash
python cli.py export /path/to/db table_name sample.json --limit 100
```

### Batch Processing

Export all tables with a limit:

```bash
python cli.py export-all /path/to/db ./exports --format csv --limit 1000
```

## Python API

```python
from wt_browser import WiredTigerBrowser

with WiredTigerBrowser('/path/to/db') as browser:
    # List tables
    tables = browser.list_tables()
    
    # Export
    browser.export_table_to_json(tables[0], 'output.json')
```

## Troubleshooting

**"Database path does not exist"**
- Verify the path points to the WiredTiger database directory
- Look for files like `WiredTiger`, `WiredTiger.wt`, `WiredTiger.turtle`

**"Failed to open WiredTiger database"**
- Ensure you have read permissions
- Check that the database is not currently locked by another process

**"Table not found"**
- Run `list-tables` first to see available tables
- MongoDB internal names differ from collection names

## Next Steps

- Read the [full README](README.md) for comprehensive documentation
- Check [examples.py](examples.py) for Python API examples
- Review [test_demo.py](test_demo.py) to understand all features

## Getting Help

For issues or questions:
1. Check the [README](README.md) troubleshooting section
2. Open an issue on GitHub
3. Review the example code in this repository
