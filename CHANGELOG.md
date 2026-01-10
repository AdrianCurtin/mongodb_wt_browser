# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-10

### Added
- Initial release of MongoDB WiredTiger Browser
- Core WiredTiger browser functionality (`wt_browser.py`)
- Command-line interface with Click (`cli.py`)
- Support for listing tables in WiredTiger databases
- Table information display with metadata and record counts
- Export functionality to JSON format with metadata
- Export functionality to CSV format
- Batch export all tables at once
- Record limiting for exports (sampling)
- Read-only database access for safe inspection
- Context manager support for resource management
- Comprehensive error handling and validation
- Python API for programmatic access
- Complete documentation (README.md)
- Quick start guide (QUICKSTART.md)
- Contributing guidelines (CONTRIBUTING.md)
- Usage examples (examples.py)
- Comprehensive test suite (test_demo.py)
- MIT License
- Setup.py for package installation
- Makefile for common development tasks
- Development requirements
- .gitignore for Python projects
- MANIFEST.in for package distribution

### Features
- **CLI Commands:**
  - `list-tables` - List all tables in a database
  - `info` - Display detailed table information
  - `export` - Export single table to JSON/CSV
  - `export-all` - Export all tables to a directory
  
- **Export Options:**
  - JSON format with structured metadata
  - CSV format for spreadsheet compatibility
  - Record limiting for sampling
  - Batch export all tables
  
- **Safety Features:**
  - Read-only mode (no modifications)
  - Comprehensive error handling
  - Path validation
  - Permission checking

### Dependencies
- Python 3.8+
- wiredtiger >= 11.2.0
- click >= 8.1.7

### Documentation
- Complete README with usage examples
- Quick start guide for rapid onboarding
- Contributing guidelines for developers
- API documentation in docstrings
- Inline code comments
- Example scripts

### Testing
- Comprehensive test suite with multiple scenarios
- Test database creation
- All CLI commands tested
- Both export formats verified
- Record limiting tested
- Batch operations tested

## [Unreleased]

### Planned Features
- Support for additional export formats (XML, Parquet)
- Progress bars for large exports
- Parallel export for multiple tables
- Table filtering and search
- Data transformation options
- Schema inference from data
- Integration with MongoDB tools
- GUI interface
- Docker support
- Pre-built binaries

---

## Version History

- **1.0.0** (2026-01-10): Initial release with core functionality
