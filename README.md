# SyncAgent

SyncAgent is a Python-based synchronization tool designed to facilitate the seamless synchronization of data between two SQL databases. It leverages Python's powerful libraries and SQL's robustness to ensure data consistency and integrity across different database instances.

## Overview

This project is divided into several key components:

- **Agent_Surveillance**: Monitors changes in the source database to trigger synchronization processes.
- **MagasinAPI**: An API layer that could be interfacing with one of the databases, potentially for managing inventory or store data.
- **app.py**: The main application script that orchestrates the synchronization logic.
- **database.sql**: Contains the SQL schema for setting up the databases involved in the synchronization process.

## Features

- Real-time data synchronization between two SQL databases.
- Monitoring of database changes to initiate sync processes.
- API functionality for data management and operations.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/zakariabouachra/SyncAgent.git
   ```
2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```
3. Set up your SQL databases and import the `database.sql` schema into both databases.
4. Configure `app.py` with your database connection details and any specific synchronization rules or logic.
5. Run `app.py` to start the synchronization agent:
   ```
   python app.py
   ```

## Configuration

Make sure to adjust the database connection settings in `app.py` to match your environment. You may also need to customize the synchronization logic based on your specific use case and database schema.

## Contributing

Contributions to SyncAgent are welcome! If you have suggestions for improvements or new features, feel free to fork the repo, make your changes, and submit a pull request.
