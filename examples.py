#!/usr/bin/env python3
"""
Example usage of MongoDB WiredTiger Browser
"""

from wt_browser import WiredTigerBrowser
from pathlib import Path


def example_basic_usage():
    """Basic usage example."""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    db_path = "/path/to/wiredtiger/database"
    
    # Using context manager (recommended)
    try:
        with WiredTigerBrowser(db_path) as browser:
            # List all tables
            tables = browser.list_tables()
            print(f"\nFound {len(tables)} table(s):")
            for table in tables:
                print(f"  • {table}")
            
            # Get info about first table
            if tables:
                first_table = tables[0]
                info = browser.get_table_info(first_table)
                print(f"\nTable '{first_table}' has {info['record_count']} records")
            
            # Export to JSON
            if tables:
                output_dir = Path("./exports")
                output_dir.mkdir(exist_ok=True)
                output_file = output_dir / f"{tables[0]}.json"
                browser.export_table_to_json(tables[0], str(output_file), limit=10)
    
    except FileNotFoundError:
        print(f"\nNote: This is just an example. Database path does not exist.")
    except Exception as e:
        print(f"\nError: {e}")


def example_manual_connection():
    """Example with manual connection management."""
    print("\n" + "=" * 60)
    print("Example 2: Manual Connection Management")
    print("=" * 60)
    
    db_path = "/path/to/wiredtiger/database"
    
    browser = None
    try:
        browser = WiredTigerBrowser(db_path)
        browser.open()
        
        # List tables
        tables = browser.list_tables()
        print(f"\nTables: {', '.join(tables)}")
        
    except FileNotFoundError:
        print(f"\nNote: This is just an example. Database path does not exist.")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        if browser:
            browser.close()


def example_export_all():
    """Example of exporting all tables."""
    print("\n" + "=" * 60)
    print("Example 3: Export All Tables")
    print("=" * 60)
    
    db_path = "/path/to/wiredtiger/database"
    output_dir = Path("./exports")
    
    try:
        output_dir.mkdir(exist_ok=True)
        
        with WiredTigerBrowser(db_path) as browser:
            tables = browser.list_tables()
            
            print(f"\nExporting {len(tables)} tables to {output_dir}...")
            
            for table in tables:
                output_file = output_dir / f"{table}.json"
                try:
                    browser.export_table_to_json(table, str(output_file), limit=100)
                    print(f"  ✓ Exported {table}")
                except Exception as e:
                    print(f"  ✗ Failed to export {table}: {e}")
    
    except FileNotFoundError:
        print(f"\nNote: This is just an example. Database path does not exist.")
    except Exception as e:
        print(f"\nError: {e}")


def example_csv_export():
    """Example of CSV export."""
    print("\n" + "=" * 60)
    print("Example 4: CSV Export")
    print("=" * 60)
    
    db_path = "/path/to/wiredtiger/database"
    
    try:
        with WiredTigerBrowser(db_path) as browser:
            tables = browser.list_tables()
            
            if tables:
                first_table = tables[0]
                output_file = f"./exports/{first_table}.csv"
                browser.export_table_to_csv(first_table, output_file, limit=50)
                print(f"\n✓ Exported {first_table} to CSV format")
    
    except FileNotFoundError:
        print(f"\nNote: This is just an example. Database path does not exist.")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    print("MongoDB WiredTiger Browser - Usage Examples")
    print("=" * 60)
    print("\nThese examples demonstrate the Python API.")
    print("For the database path to work, replace '/path/to/wiredtiger/database'")
    print("with an actual WiredTiger database directory.\n")
    
    example_basic_usage()
    example_manual_connection()
    example_export_all()
    example_csv_export()
    
    print("\n" + "=" * 60)
    print("For CLI usage, see README.md or run: python cli.py --help")
    print("=" * 60)
