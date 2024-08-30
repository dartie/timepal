# TimePal

**TimePal** is a command-line tool that allows you to view the current or specific time across multiple time zones. It provides two main functionalities:
1. Display the current time (or a specific time) for all people of interest.
2. Simulate being a specific person to view the times of other people relative to that person's local time.

## Features

- Display the local time for all configured time zones.
- Override the local timezone with a specific one using the `-t/--local-timezone` option.
- Search for a person and display the time relative to their time zone using the `-s/--search` option.
- Automatically parse and display the current time if no specific time is provided.

## Prerequisites

Ensure you have the following Python packages installed:
- `pyyaml`
- `pytz`
- `python-dateutil`
- `colorama`

You can install these packages using pip:

```bash
pip install -r requirements.txt
```

## Installation
1. Clone the repository or download the script file.
1. Place the script in a directory of your choice.
1. Ensure you have a settings.yml file in the same directory as the script.

## `settings.yml` Structure
The `settings.yml` file should contain the following structure:

```yaml
local: "Europe/Zurich"  # Your local timezone
targets:
  "America/New_York": ["John Doe"]
  "Asia/Tokyo": ["Jane Smith", "Yuki Tanaka"]
  "Australia/Sydney": ["Liam Brown"]
```

* `local`: Your default local timezone.
* `targets`: A dictionary where the keys are time zones and the values are lists of people in those time zones.


## Usage
Run the script using Python:

```bash
python timezone_checker.py
```

### Command-Line Options
* `-S`, `--settings`: Specify the settings file containing all the time zones and people (default: `settings.yml`).
* `-t`, `--local-timezone`: Override the default local timezone.
* `-s`, `--search`: Search for a person and use their timezone as the local timezone.
* `local_date_time`: Specify the local datetime in the format `YYYY-MM-DD HH:MM[:SS]`. If not provided, the current time will be used.


### Examples

1. Display the current time across all configured time zones:

    ```bash
    python timezone_checker.py
    ```

1. Display a specific time across all configured time zones:

    ```bash
    python timezone_checker.py "2024-08-30 14:00:00"
    ```

1. Display the time across all configured time zones, pretending you are in a different timezone:
 
    ```bash
    python timezone_checker.py -t "America/Los_Angeles"
    ```

1. Display the time across all configured time zones as if you were a specific person:

    ```bash
    python timezone_checker.py -s "John Doe"
    ```

# Author
This tool was developed by Dario Necco.