# Cricbuzz CLI Tool

## Overview
This CLI tool provides functionalities to retrieve live cricket match details and commentary from Cricbuzz. It allows users to list current matches, fetch match commentaries, and optionally monitor live updates.

## Features
- **List Matches**: Retrieve a list of current matches with match IDs, titles, and timestamps.
- **Fetch Commentary**: Get the last 10 match commentaries or as many as available for a given match ID.
- **Monitor Live Commentary**: With the `--commentary` and `--watch` flags together, continuously fetch and display new commentaries every 10 seconds.

## Usage
Ensure you have Python installed along with the necessary packages (`selenium`, `argparse`, `webdriver_manager`):
```bash
pip install selenium argparse webdriver_manager
```

## Commands

### List Current Matches
```bash
python cricbuzz_cli.py --list
```
### Fetch Match Commentary
```bash
python cricbuzz_cli.py --commentary <MATCH_ID>
```

Replace <MATCH_ID> with the actual match ID from Cricbuzz.

### Monitor Live Commentary

```bash
python cricbuzz_cli.py --commentary <MATCH_ID> --watch
```

Continuously fetches and displays new commentaries every 10 seconds for the specified match ID.

## Disclaimer

This project is developed for educational purposes only. Use at your own risk. There is no guarantee of legality or reliability for production use.
