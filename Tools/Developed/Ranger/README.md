# RANGER

This tool allows you to scan a range of IPs or single IPs using the Shodan API. You can extract IPs from a given CIDR range or provide a file containing a list of IPs and ranges. The results will be organized by IP ranges or individual IPs in separate directories, making it easy to review Shodan information or note which IPs had no Shodan data available.

## Features

- **Extract IPs from a CIDR range**: Extract all IPs from a given CIDR range and save them to a `.txt` file.
- **Shodan Scan**: Perform a Shodan scan for each IP or range, saving the results in a structured way.
- **Organized Output**: For each unique range or individual IP, a separate directory is created to store the Shodan results.

## Requirements

- Python 3.x
- External dependencies (listed in `requirements.txt`):
  - `requests`: For making HTTP requests to the Shodan API.
  - `termcolor`: For adding colored output in the terminal.

## Installation

1. Clone or download this repository.
2. Navigate to the project directory.
3. Install the required dependencies using `pip`:
   ```bash
   pip install -r requirements.txt

## To Do

- **Add active reconnaissance features (rustscan/masscan integration)
- **Data analysis and categorization based on Shodan/Rustscan/Masscan ouptut
