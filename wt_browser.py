#!/usr/bin/env python3
"""
MongoDB WiredTiger Browser
A tool to open MongoDB WiredTiger backups and export tables.
"""

import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
import wiredtiger


class WiredTigerBrowser:
    """Browser for MongoDB WiredTiger database files."""
    
    def __init__(self, db_path: str):
        """
        Initialize the WiredTiger browser.
        
        Args:
            db_path: Path to the WiredTiger database directory
        """
        self.db_path = Path(db_path)
        self.conn = None
        
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database path does not exist: {db_path}")
        
        if not self.db_path.is_dir():
            raise ValueError(f"Database path must be a directory: {db_path}")
    
    def open(self):
        """Open connection to the WiredTiger database."""
        try:
            # Open WiredTiger connection in read-only mode
            config = "readonly=true"
            self.conn = wiredtiger.wiredtiger_open(str(self.db_path), config)
            print(f"Successfully opened WiredTiger database at: {self.db_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to open WiredTiger database: {e}")
    
    def close(self):
        """Close the WiredTiger connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            print("Database connection closed.")
    
    def list_tables(self) -> List[str]:
        """
        List all tables in the WiredTiger database.
        
        Returns:
            List of table names
        """
        if not self.conn:
            raise RuntimeError("Database connection not open. Call open() first.")
        
        tables = []
        session = self.conn.open_session()
        
        try:
            cursor = session.open_cursor("metadata:", None, None)
            
            for key, value in cursor:
                if key.startswith("table:"):
                    table_name = key.split(":", 1)[1]
                    tables.append(table_name)
            
            cursor.close()
        finally:
            session.close()
        
        return sorted(tables)
    
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """
        Get information about a specific table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Dictionary containing table information
        """
        if not self.conn:
            raise RuntimeError("Database connection not open. Call open() first.")
        
        session = self.conn.open_session()
        info = {
            "name": table_name,
            "exists": False,
            "config": None,
            "record_count": 0
        }
        
        try:
            # Check if table exists and get config
            metadata_cursor = session.open_cursor("metadata:", None, None)
            metadata_key = f"table:{table_name}"
            
            for key, value in metadata_cursor:
                if key == metadata_key:
                    info["exists"] = True
                    info["config"] = value
                    break
            
            metadata_cursor.close()
            
            if info["exists"]:
                # Count records by iterating through cursor
                # Note: This can be slow for large tables as it must scan all records.
                # Consider using --limit flag in export commands for large tables.
                try:
                    cursor = session.open_cursor(f"table:{table_name}", None, None)
                    count = 0
                    for _ in cursor:
                        count += 1
                    info["record_count"] = count
                    cursor.close()
                except Exception as e:
                    info["error"] = f"Could not count records: {e}"
        
        finally:
            session.close()
        
        return info
    
    def export_table_to_json(self, table_name: str, output_path: str, limit: Optional[int] = None):
        """
        Export table data to JSON format.
        
        Args:
            table_name: Name of the table to export
            output_path: Path to output JSON file
            limit: Maximum number of records to export (None for all)
        """
        if not self.conn:
            raise RuntimeError("Database connection not open. Call open() first.")
        
        session = self.conn.open_session()
        
        try:
            cursor = session.open_cursor(f"table:{table_name}", None, None)
            records = []
            count = 0
            
            for key, value in cursor:
                record = {
                    "key": self._serialize_value(key),
                    "value": self._serialize_value(value)
                }
                records.append(record)
                count += 1
                
                if limit and count >= limit:
                    break
            
            cursor.close()
            
            # Write to JSON file
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "table": table_name,
                    "record_count": count,
                    "records": records
                }, f, indent=2, ensure_ascii=False)
            
            print(f"Exported {count} records from '{table_name}' to {output_path}")
        
        finally:
            session.close()
    
    def export_table_to_csv(self, table_name: str, output_path: str, limit: Optional[int] = None):
        """
        Export table data to CSV format.
        
        Args:
            table_name: Name of the table to export
            output_path: Path to output CSV file
            limit: Maximum number of records to export (None for all)
        """
        if not self.conn:
            raise RuntimeError("Database connection not open. Call open() first.")
        
        session = self.conn.open_session()
        
        try:
            cursor = session.open_cursor(f"table:{table_name}", None, None)
            
            # Prepare output file
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['key', 'value'])
                
                count = 0
                for key, value in cursor:
                    writer.writerow([
                        self._serialize_value(key),
                        self._serialize_value(value)
                    ])
                    count += 1
                    
                    if limit and count >= limit:
                        break
            
            cursor.close()
            print(f"Exported {count} records from '{table_name}' to {output_path}")
        
        finally:
            session.close()
    
    def _serialize_value(self, value: Any) -> str:
        """
        Serialize a value to string format.
        
        Args:
            value: Value to serialize
            
        Returns:
            String representation of the value
        """
        if isinstance(value, (bytes, bytearray)):
            try:
                # Try to decode as UTF-8
                return value.decode('utf-8')
            except UnicodeDecodeError:
                # If that fails, return hex representation
                return value.hex()
        elif isinstance(value, tuple):
            # For composite values, join with separator
            return str(value)
        else:
            return str(value)
    
    def __enter__(self):
        """Context manager entry."""
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
