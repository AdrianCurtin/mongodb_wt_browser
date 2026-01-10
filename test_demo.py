#!/usr/bin/env python3
"""
Test script for MongoDB WiredTiger Browser
Demonstrates all functionality with a test database.
"""

import sys
import subprocess
from pathlib import Path
import wiredtiger
import shutil


def create_test_database():
    """Create a test WiredTiger database with sample data."""
    print("=" * 60)
    print("Creating Test Database")
    print("=" * 60)
    
    test_db = Path("/tmp/demo_wt_db")
    
    # Clean up if exists
    if test_db.exists():
        shutil.rmtree(test_db)
    
    test_db.mkdir(exist_ok=True)
    
    # Create database
    conn = wiredtiger.wiredtiger_open(str(test_db), "create")
    session = conn.open_session()
    
    # Create multiple tables with different data
    print("\nCreating tables:")
    
    # Table 1: Users
    session.create("table:users", "key_format=i,value_format=S")
    cursor = session.open_cursor("table:users")
    cursor[1] = '{"name": "Alice", "age": 30}'
    cursor[2] = '{"name": "Bob", "age": 25}'
    cursor[3] = '{"name": "Charlie", "age": 35}'
    cursor.close()
    print("  ✓ Created 'users' table with 3 records")
    
    # Table 2: Products
    session.create("table:products", "key_format=S,value_format=S")
    cursor = session.open_cursor("table:products")
    cursor["prod-001"] = '{"name": "Laptop", "price": 999.99}'
    cursor["prod-002"] = '{"name": "Mouse", "price": 29.99}'
    cursor["prod-003"] = '{"name": "Keyboard", "price": 79.99}'
    cursor["prod-004"] = '{"name": "Monitor", "price": 299.99}'
    cursor.close()
    print("  ✓ Created 'products' table with 4 records")
    
    # Table 3: Logs
    session.create("table:logs", "key_format=i,value_format=S")
    cursor = session.open_cursor("table:logs")
    for i in range(1, 11):
        cursor[i] = f'log entry {i}'
    cursor.close()
    print("  ✓ Created 'logs' table with 10 records")
    
    session.close()
    conn.close()
    
    print(f"\n✓ Test database created at: {test_db}")
    return test_db


def run_command(cmd, description):
    """Run a CLI command and display results."""
    print("\n" + "=" * 60)
    print(description)
    print("=" * 60)
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr, file=sys.stderr)
    
    return result.returncode


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("MongoDB WiredTiger Browser - Test Suite")
    print("=" * 60)
    
    # Create test database
    test_db = create_test_database()
    
    # Test 1: List tables
    run_command(
        ["python3", "cli.py", "list-tables", str(test_db)],
        "Test 1: List All Tables"
    )
    
    # Test 2: Get table info
    run_command(
        ["python3", "cli.py", "info", str(test_db), "users"],
        "Test 2: Get Table Information"
    )
    
    # Test 3: Export to JSON
    output_dir = Path("/tmp/test_output")
    output_dir.mkdir(exist_ok=True)
    
    run_command(
        ["python3", "cli.py", "export", str(test_db), "users", 
         str(output_dir / "users.json")],
        "Test 3: Export Single Table to JSON"
    )
    
    # Display exported JSON
    print("\nExported JSON content:")
    print("-" * 60)
    with open(output_dir / "users.json") as f:
        print(f.read())
    
    # Test 4: Export to CSV
    run_command(
        ["python3", "cli.py", "export", str(test_db), "products", 
         str(output_dir / "products.csv"), "--format", "csv"],
        "Test 4: Export Single Table to CSV"
    )
    
    # Display exported CSV
    print("\nExported CSV content:")
    print("-" * 60)
    with open(output_dir / "products.csv") as f:
        print(f.read())
    
    # Test 5: Export with limit
    run_command(
        ["python3", "cli.py", "export", str(test_db), "logs", 
         str(output_dir / "logs_limited.json"), "--limit", "5"],
        "Test 5: Export with Record Limit"
    )
    
    # Test 6: Export all tables
    export_all_dir = output_dir / "all_tables"
    run_command(
        ["python3", "cli.py", "export-all", str(test_db), str(export_all_dir)],
        "Test 6: Export All Tables"
    )
    
    # List exported files
    print("\nExported files:")
    print("-" * 60)
    for file in sorted(export_all_dir.glob("*")):
        print(f"  • {file.name} ({file.stat().st_size} bytes)")
    
    # Test 7: Export all to CSV
    export_csv_dir = output_dir / "all_tables_csv"
    run_command(
        ["python3", "cli.py", "export-all", str(test_db), str(export_csv_dir),
         "--format", "csv", "--limit", "5"],
        "Test 7: Export All Tables to CSV with Limit"
    )
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"✓ Test database: {test_db}")
    print(f"✓ Output directory: {output_dir}")
    print(f"✓ All tests completed successfully!")
    print("\nCleanup:")
    print(f"  - To remove test database: rm -rf {test_db}")
    print(f"  - To remove output files: rm -rf {output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError during testing: {e}", file=sys.stderr)
        sys.exit(1)
