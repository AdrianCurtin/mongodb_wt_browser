#!/usr/bin/env python3
"""
Real-world usage example for MongoDB WiredTiger Browser.
This demonstrates common scenarios when working with MongoDB backups.
"""

from pathlib import Path
from wt_browser import WiredTigerBrowser


def analyze_mongodb_backup(backup_path: str):
    """
    Analyze a MongoDB backup to understand its contents.
    
    Args:
        backup_path: Path to MongoDB backup directory (containing WiredTiger files)
    """
    print("=" * 70)
    print("MongoDB Backup Analysis")
    print("=" * 70)
    print(f"\nBackup Location: {backup_path}\n")
    
    try:
        with WiredTigerBrowser(backup_path) as browser:
            # Step 1: List all tables
            tables = browser.list_tables()
            print(f"Found {len(tables)} table(s):\n")
            
            # Categorize tables
            collections = [t for t in tables if t.startswith('collection-')]
            indexes = [t for t in tables if t.startswith('index-')]
            system = [t for t in tables if not t.startswith(('collection-', 'index-'))]
            
            print(f"Collections: {len(collections)}")
            print(f"Indexes: {len(indexes)}")
            print(f"System tables: {len(system)}")
            print()
            
            # Step 2: Analyze each collection
            if collections:
                print("Collection Details:")
                print("-" * 70)
                for collection in collections[:5]:  # Show first 5
                    info = browser.get_table_info(collection)
                    print(f"  • {collection}: {info['record_count']} records")
                
                if len(collections) > 5:
                    print(f"  ... and {len(collections) - 5} more collections")
            
            # Step 3: Show system tables
            if system:
                print("\nSystem Tables:")
                print("-" * 70)
                for sys_table in system:
                    info = browser.get_table_info(sys_table)
                    print(f"  • {sys_table}: {info['record_count']} records")
    
    except FileNotFoundError:
        print(f"Error: Backup directory not found at {backup_path}")
        print("\nThis is an example script. To use it:")
        print("1. Replace the path with your actual MongoDB backup directory")
        print("2. The directory should contain WiredTiger files")
    except Exception as e:
        print(f"Error analyzing backup: {e}")


def export_specific_collection(backup_path: str, collection_table: str, output_dir: str):
    """
    Export a specific collection from a MongoDB backup.
    
    Args:
        backup_path: Path to MongoDB backup directory
        collection_table: Name of the collection table (e.g., 'collection-0-12345')
        output_dir: Directory to save exported data
    """
    print("=" * 70)
    print("Export Specific Collection")
    print("=" * 70)
    print(f"\nExporting: {collection_table}")
    print(f"From: {backup_path}")
    print(f"To: {output_dir}\n")
    
    try:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        with WiredTigerBrowser(backup_path) as browser:
            # Check if table exists
            tables = browser.list_tables()
            if collection_table not in tables:
                print(f"Error: Collection '{collection_table}' not found")
                print("\nAvailable collections:")
                for t in [x for x in tables if x.startswith('collection-')]:
                    print(f"  • {t}")
                return
            
            # Get collection info
            info = browser.get_table_info(collection_table)
            print(f"Collection has {info['record_count']} records")
            
            # Export to JSON
            json_file = output_path / f"{collection_table}.json"
            browser.export_table_to_json(collection_table, str(json_file))
            print(f"\n✓ Exported to: {json_file}")
    
    except Exception as e:
        print(f"Error exporting collection: {e}")


def sample_large_collection(backup_path: str, collection_table: str, sample_size: int = 100):
    """
    Export a sample of records from a large collection.
    Useful for testing or preview without exporting everything.
    
    Args:
        backup_path: Path to MongoDB backup directory
        collection_table: Name of the collection table
        sample_size: Number of records to export
    """
    print("=" * 70)
    print("Sample Large Collection")
    print("=" * 70)
    print(f"\nSampling {sample_size} records from: {collection_table}\n")
    
    try:
        output_path = Path("./samples")
        output_path.mkdir(exist_ok=True)
        
        with WiredTigerBrowser(backup_path) as browser:
            # Export sample
            sample_file = output_path / f"{collection_table}_sample.json"
            browser.export_table_to_json(
                collection_table, 
                str(sample_file), 
                limit=sample_size
            )
            
            print(f"✓ Sample exported to: {sample_file}")
            print(f"\nYou can now review the sample before exporting the full collection.")
    
    except Exception as e:
        print(f"Error sampling collection: {e}")


def migrate_backup_to_json(backup_path: str, output_dir: str):
    """
    Migrate an entire MongoDB backup to JSON files.
    Exports all collections (not indexes) to JSON format.
    
    Args:
        backup_path: Path to MongoDB backup directory
        output_dir: Directory to save all exported collections
    """
    print("=" * 70)
    print("Migrate Backup to JSON")
    print("=" * 70)
    print(f"\nMigrating from: {backup_path}")
    print(f"To: {output_dir}\n")
    
    try:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        with WiredTigerBrowser(backup_path) as browser:
            tables = browser.list_tables()
            
            # Only export collections (not indexes or system tables)
            collections = [t for t in tables if t.startswith('collection-')]
            
            print(f"Found {len(collections)} collection(s) to export\n")
            
            exported = 0
            failed = 0
            
            for collection in collections:
                try:
                    output_file = output_path / f"{collection}.json"
                    info = browser.get_table_info(collection)
                    
                    print(f"Exporting {collection} ({info['record_count']} records)...", end=" ")
                    browser.export_table_to_json(collection, str(output_file))
                    print("✓")
                    exported += 1
                    
                except Exception as e:
                    print(f"✗ Failed: {e}")
                    failed += 1
            
            print("\n" + "-" * 70)
            print(f"Migration complete: {exported} succeeded, {failed} failed")
    
    except Exception as e:
        print(f"Error during migration: {e}")


def main():
    """Main example runner."""
    print("\n" + "=" * 70)
    print("MongoDB WiredTiger Browser - Real-world Examples")
    print("=" * 70)
    print("\nThese examples demonstrate common MongoDB backup scenarios.")
    print("To use them, replace the example paths with your actual backup paths.\n")
    
    # Example paths (replace with your actual paths)
    example_backup_path = "/path/to/mongodb/backup"
    example_collection = "collection-0-1234567890123456789"
    
    # Example 1: Analyze a backup
    print("\nExample 1: Analyze MongoDB Backup")
    print("-" * 70)
    print("This shows what's inside a MongoDB backup without exporting anything.")
    analyze_mongodb_backup(example_backup_path)
    
    # Example 2: Export a specific collection
    print("\n\nExample 2: Export Specific Collection")
    print("-" * 70)
    print("This exports a single collection to JSON format.")
    # Uncomment to run:
    # export_specific_collection(example_backup_path, example_collection, "./exports")
    print("(Commented out - uncomment in code to run)")
    
    # Example 3: Sample a large collection
    print("\n\nExample 3: Sample Large Collection")
    print("-" * 70)
    print("This exports just the first N records for testing/preview.")
    # Uncomment to run:
    # sample_large_collection(example_backup_path, example_collection, sample_size=50)
    print("(Commented out - uncomment in code to run)")
    
    # Example 4: Migrate entire backup
    print("\n\nExample 4: Migrate Entire Backup to JSON")
    print("-" * 70)
    print("This exports all collections from a backup to JSON files.")
    # Uncomment to run:
    # migrate_backup_to_json(example_backup_path, "./migration_output")
    print("(Commented out - uncomment in code to run)")
    
    print("\n" + "=" * 70)
    print("To run these examples with your own data:")
    print("1. Edit this file and replace example_backup_path")
    print("2. Uncomment the example you want to run")
    print("3. Run: python mongodb_examples.py")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
