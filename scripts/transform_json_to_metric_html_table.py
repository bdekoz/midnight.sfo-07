#!/usr/bin/env python

# run like:
# /transform_json_to_md_table.py ./input.json ./output.html

import pandas as pd
import json
import sys
import os

# setup
infile = sys.argv[1];
outfile = sys.argv[2];

def replace_between(original_str, start_marker, end_marker, replacement_str):
    start_index = original_str.find(start_marker)
    if start_index == -1:
        return original_str

    end_index = original_str.find(end_marker, start_index)
    if end_index == -1:
        return original_str

    part_before = original_str[:start_index]
    part_after = original_str[end_index + len(end_marker):]
    return part_before + replacement_str + part_after


def convert_json_to_html_table(inputf, outputf):
    """
    Reads data from a JSON file, converts it into a Pandas DataFrame,
    and then generates an HTML file containing a styled table of that data.

    Args:
        inputf (str): The path to the input JSON file.
        outputf (str): The path to the output HTML file.
    """

    # check inputs
    if os.path.exists(inputf):
        print(f"input data file '{inputf}' found")
    else:
        print(f"Error: input json file '{inputf}' not found")
        sys.exit(1)

    if os.path.exists(outputf):
        print(f"Error: output html file '{outputf}' already exists")
        sys.exit(1)
    else:
        print(f"output html file '{outputf}' created")

    # parse data info df and export.
    try:
        # 1. Read the JSON data from the input file
        with open(inputf, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Ensure the JSON data is a list of dictionaries or a dictionary
        # that can be directly converted to a DataFrame
        if not isinstance(data, (list, dict)):
            print(f"Error: JSON data in '{inputf}' is not in a recognized format for DataFrame creation (list or dictionary).", file=sys.stderr)
            sys.exit(1)

        # 2. Convert the JSON data into a Pandas DataFrame
        df = pd.DataFrame(data)

        # NB escape=False required if html is embedded
        html_table_string = df.to_html(escape=False, index=False, na_rep='nan', float_format='%.1f')

        # 4. Create a complete HTML document with the table
        # We'll use a simple HTML template with basic styling for a clean look
        html_content_base = f"""
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Metics Table</title>
</head>
<body>
    <div class="table-container">
        {html_table_string}
    </div>
</body>
</html>
        """

        # tables
        startt = "<table border"
        endt = ">"
        customtable = f"""<table>"""
        html_content = replace_between(html_content_base, startt, endt, customtable)

        # 5. Write the complete HTML content to the specified output file
        with open(outputf, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Successfully converted '{inputf}' to '{outputf}'.")

    except FileNotFoundError:
        print(f"Error: One of the files was not found. Please check paths.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{inputf}'. Ensure it's a valid JSON file.", file=sys.stderr)
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: No data to parse from '{inputf}'. The JSON file might be empty.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


convert_json_to_html_table(infile, outfile)
