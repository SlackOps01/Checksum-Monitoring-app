# File Integrity Monitoring App

This is a Python-based File Integrity Monitoring application that calculates and monitors the checksums of files in a specified directory, notifying the user if any file modifications are detected. This helps in tracking unauthorized changes and maintaining file security.

## Features

- **Directory Monitoring**: Tracks all files within a specified directory.
- **File Hashing**: Calculates SHA-256 hash for each file to verify integrity.
- **Database Storage**: Stores file paths, hashes, and last modified timestamps in a local SQLite database.
- **File Integrity Check**: Compares current file hashes with stored hashes to detect unauthorized modifications.
- **User Notifications**: Sends a desktop notification when a file modification is detected.
- **Logging**: Logs file modification events in a log file for further analysis.

## Getting Started

### Prerequisites

- **Python** (>=3.6)
- Required Libraries:
  - `sqlalchemy`: For ORM and SQLite database management.
  - `plyer`: For sending desktop notifications.
  - `logging`: For logging warning messages to a file.
  - `hashlib`: For generating SHA-256 hash values.

You can install the required libraries via pip:

```bash
pip install sqlalchemy plyer
