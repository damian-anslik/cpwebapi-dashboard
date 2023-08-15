# Create a CSV file from a given .log file
# Here is the structure of a log line: 2023-08-15 11:47:13,587; INFO; endpoint: https://api.ibkr.com/v1/api/tickle; status_code: 200; response_time: 406.306ms; request_time: 2023-08-15 10:47:13.057120
# Here is another log line: 2023-08-15 13:51:43,600; INFO; endpoint: https://api.ibkr.com/v1/api/iserver/auth/status; status_code: 200; response_time: 406.512ms; request_time: 2023-08-15 12:51:43.083182

import csv
import re

# Open the log file
with open(".\logs\cpwebapi_20230815.log", "r") as log_file:
    # Open the CSV file
    with open("cpwebapi_20230815.csv", "w", newline="") as csv_file:
        # Create the CSV writer
        csv_writer = csv.writer(csv_file, delimiter=";")
        # Write the header
        csv_writer.writerow(
            [
                "date",
                "time",
                "level",
                "endpoint",
                "status_code",
                "response_time",
                "request_time",
            ]
        )
        # Read the log file line by line
        for line in log_file:
            # Extract the data from the log line
            match = re.match(
                r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}),\d{3}; (\w+); endpoint: (.*); status_code: (\d+); response_time: (\d+\.\d+)ms; request_time: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)",
                line,
            )
            if match:
                # Write the data to the CSV file
                csv_writer.writerow(
                    [
                        match.group(1),
                        match.group(2),
                        match.group(3),
                        match.group(4),
                        match.group(5),
                        match.group(6),
                        match.group(7),
                    ]
                )
