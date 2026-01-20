# SQLite Manager Tool

A lightweight SQLite database management & automation project for macOS/Linux.
It provides JSON outputs, table management, sample seeding, and a self-test script.

## Features
- Create SQLite DB and tables (`init`)
- Seed sample data (`seed`)
- List tables (`list`)
- JSON report with row counts (`report`)
- Self-Test (Auto Test Ability)

## Requirements
- Python 3 (stdlib only)
- SQLite (bundled with macOS)

## Quick Start
```bash
python3 src/cli.py init
python3 src/cli.py seed
python3 src/cli.py report
python3 src/self_test.py

## Demo Video

A short screen recording that demonstrates:
- Database initialization
- Seeding sample data
- JSON report output
- Self-test execution

📁 Location: `docs/demo.mp4`
