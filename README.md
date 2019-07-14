# Bitwarden JSON to 1Password CSV converter

This is a tool that converts a Bitwarden vault exported as JSON into CSV files that can be imported into 1Password.

The 1Password CSV file format is described here: https://support.1password.com/create-csv-files/.

The tool creates one CSV file per supported item type: Logins, secure notes and credit cards. The files will be saved to the current working directory under the names `1p_logins.csv`, `1p_notes.csv` and `1p_cards.csv`.

## Requirements

- Python 3.x (no third-party packages required).

## Usage

```bash
$ curl -O https://raw.githubusercontent.com/philwo/bw-to-1p/master/bw-to-1p.py
$ ./bw-to-1p.py bitwarden_export_20190714190322.json

Writing converted items to 1p_logins.csv, 1p_notes.csv and 1p_cards.csv...
Successfully converted 736 logins, 17 notes and 10 cards.
```
