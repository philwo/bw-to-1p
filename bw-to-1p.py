#!/usr/bin/env python3
"""
Copyright 2019 Philipp Wollermann. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import argparse
import csv
import json
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Converts a Bitwarden vault exported as JSON into CSV files that can be imported into 1Password."
    )
    parser.add_argument(
        "input_file",
        nargs=1,
        help="A Bitwarden vault exported as JSON.",
        type=argparse.FileType("r"),
    )
    args = parser.parse_args()

    if not args.input_file:
        parser.print_help()
        return 1

    bw = json.load(args.input_file[0])

    print("Writing converted items to 1p_logins.csv, 1p_notes.csv and 1p_cards.csv...")
    logins = csv.writer(open("1p_logins.csv", "w", newline=""))
    notes = csv.writer(open("1p_notes.csv", "w", newline=""))
    cards = csv.writer(open("1p_cards.csv", "w", newline=""))

    logins_count, notes_count, cards_count = 0, 0, 0
    for item in bw["items"]:
        if item["type"] == 1:
            # Login:
            # title,website,username,password,notes,custom field 1,custom field 2, custom field …
            logins.writerow(
                [
                    item["name"],
                    item["login"].get("uris", [{}])[0].get("uri", ""),
                    item["login"]["username"],
                    item["login"]["password"],
                    item["notes"],
                    item["login"]["totp"],
                ]
            )
            logins_count += 1
        elif item["type"] == 2:
            # Note:
            # title,text of note
            notes.writerow([item["name"], item["notes"]])
            notes_count += 1
        elif item["type"] == 3:
            # Card:
            # title,card number,expiry date (MM/YYYY),cardholder name,PIN,bank name,CVV,notes
            cards.writerow(
                [
                    item["name"],
                    item["card"]["number"],
                    "{}/{}".format(item["card"]["expMonth"], item["card"]["expYear"]),
                    item["card"]["cardholderName"],
                    "1234",
                    "Bank name",
                    item["card"]["code"],
                    item["notes"],
                ]
            )
            cards_count += 1

    print(
        "Successfully converted {} logins, {} notes and {} cards.".format(
            logins_count, notes_count, cards_count
        )
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
