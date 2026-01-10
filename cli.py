#!/usr/bin/env python3
"""
Command-line interface for MongoDB WiredTiger Browser.
"""

import click
import sys
from pathlib import Path
from wt_browser import WiredTigerBrowser


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    MongoDB WiredTiger Browser - A tool to open and export MongoDB WiredTiger backups.
    """
    pass


@cli.command()
@click.argument('db_path', type=click.Path(exists=True))
def list_tables(db_path):
    """
    List all tables in a WiredTiger database.
    
    DB_PATH: Path to the WiredTiger database directory
    """
    try:
        with WiredTigerBrowser(db_path) as browser:
            tables = browser.list_tables()
            
            if tables:
                click.echo(f"\nFound {len(tables)} table(s) in {db_path}:")
                click.echo("-" * 50)
                for table in tables:
                    click.echo(f"  • {table}")
            else:
                click.echo(f"No tables found in {db_path}")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('db_path', type=click.Path(exists=True))
@click.argument('table_name')
def info(db_path, table_name):
    """
    Display information about a specific table.
    
    DB_PATH: Path to the WiredTiger database directory
    TABLE_NAME: Name of the table to inspect
    """
    try:
        with WiredTigerBrowser(db_path) as browser:
            table_info = browser.get_table_info(table_name)
            
            click.echo(f"\nTable Information: {table_name}")
            click.echo("-" * 50)
            click.echo(f"Exists: {table_info['exists']}")
            
            if table_info['exists']:
                click.echo(f"Record Count: {table_info['record_count']}")
                
                if table_info.get('config'):
                    click.echo(f"\nConfiguration:")
                    click.echo(f"  {table_info['config']}")
                
                if table_info.get('error'):
                    click.echo(f"\nWarning: {table_info['error']}", err=True)
            else:
                click.echo(f"Table '{table_name}' does not exist in the database.")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('db_path', type=click.Path(exists=True))
@click.argument('table_name')
@click.argument('output_file', type=click.Path())
@click.option('--format', '-f', type=click.Choice(['json', 'csv']), default='json',
              help='Output format (default: json)')
@click.option('--limit', '-l', type=int, default=None,
              help='Limit number of records to export')
def export(db_path, table_name, output_file, format, limit):
    """
    Export a table to JSON or CSV format.
    
    DB_PATH: Path to the WiredTiger database directory
    TABLE_NAME: Name of the table to export
    OUTPUT_FILE: Path to the output file
    """
    try:
        with WiredTigerBrowser(db_path) as browser:
            # Check if table exists
            tables = browser.list_tables()
            if table_name not in tables:
                click.echo(f"Error: Table '{table_name}' not found in database.", err=True)
                click.echo(f"\nAvailable tables:", err=True)
                for t in tables:
                    click.echo(f"  • {t}", err=True)
                sys.exit(1)
            
            # Export based on format
            if format == 'json':
                browser.export_table_to_json(table_name, output_file, limit)
            elif format == 'csv':
                browser.export_table_to_csv(table_name, output_file, limit)
            
            click.echo(f"✓ Export completed successfully!")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('db_path', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path())
@click.option('--format', '-f', type=click.Choice(['json', 'csv']), default='json',
              help='Output format (default: json)')
@click.option('--limit', '-l', type=int, default=None,
              help='Limit number of records per table')
def export_all(db_path, output_dir, format, limit):
    """
    Export all tables to the specified directory.
    
    DB_PATH: Path to the WiredTiger database directory
    OUTPUT_DIR: Directory where exported files will be saved
    """
    try:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        with WiredTigerBrowser(db_path) as browser:
            tables = browser.list_tables()
            
            if not tables:
                click.echo("No tables found to export.")
                return
            
            click.echo(f"\nExporting {len(tables)} table(s) to {output_dir}...")
            click.echo("-" * 50)
            
            for table in tables:
                ext = 'json' if format == 'json' else 'csv'
                output_file = output_path / f"{table}.{ext}"
                
                try:
                    if format == 'json':
                        browser.export_table_to_json(table, str(output_file), limit)
                    elif format == 'csv':
                        browser.export_table_to_csv(table, str(output_file), limit)
                except Exception as e:
                    click.echo(f"  ✗ Failed to export '{table}': {e}", err=True)
            
            click.echo(f"\n✓ All tables exported to {output_dir}")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
