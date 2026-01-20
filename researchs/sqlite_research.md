# SQLite Research

SQLite is a lightweight, serverless, embedded database engine.
It stores the entire database in a single file and does not require a running service.

## Key properties
- Serverless (no daemon)
- Zero-configuration
- ACID transactions
- Small footprint

## Why it fits OS/Automation projects
- Works well with scripts and system utilities
- Great for local storage (logs, inventories, small tools)
- Easy to automate and test

## Basic security notes
- Database file permissions matter
- Use parameterized queries when inserting user input
