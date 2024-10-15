import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import json

# Parse workbook.xml to get sheet information
workbook_tree = ET.parse(
    "/home/luisvinatea/Dev/portfolio/obs_files/asignaturas/fusiones_adquisiciones/data/workbook.xml"
)
workbook_root = workbook_tree.getroot()

# Extract workbook metadata (sheet names and IDs)
sheets_info = []
for sheet in workbook_root.findall(
    ".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheet"
):
    sheets_info.append(
        {
            "name": sheet.get("name"),
            "sheetId": sheet.get("sheetId"),
            "id": sheet.get(
                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
            ),
        }
    )

# Parse sheet1.xml to extract cell data
sheet_tree = ET.parse(
    "/home/luisvinatea/Dev/portfolio/obs_files/asignaturas/fusiones_adquisiciones/data/sheet1.xml"
)
sheet_root = sheet_tree.getroot()

# Extract cell values, references, and formulas
cells_data = []
for cell in sheet_root.findall(
    ".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c"
):
    cell_data = {
        "ref": cell.get("r"),
        "type": cell.get("t"),
        "value": None,
        "formula": None,
    }
    value_element = cell.find(
        "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v"
    )
    if value_element is not None:
        cell_data["value"] = value_element.text
    formula_element = cell.find(
        "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}f"
    )
    if formula_element is not None:
        cell_data["formula"] = formula_element.text
    cells_data.append(cell_data)

# Parse sharedStrings.xml to map shared strings
shared_strings_tree = ET.parse(
    "/home/luisvinatea/Dev/portfolio/obs_files/asignaturas/fusiones_adquisiciones/data/sharedStrings.xml"
)
shared_strings_root = shared_strings_tree.getroot()
shared_strings = [
    si.text
    for si in shared_strings_root.findall(
        ".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"
    )
]

# Parse calcChain.xml to understand calculation order
calc_chain_tree = ET.parse(
    "/home/luisvinatea/Dev/portfolio/obs_files/asignaturas/fusiones_adquisiciones/data/calcChain.xml"
)
calc_chain_root = calc_chain_tree.getroot()
calc_chain = []
for c in calc_chain_root.findall(
    ".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c"
):
    calc_chain.append(c.get("r"))

# Export filtered metadata to JSON file for easier inspection
metadata = {
    "workbook": {"sheets": sheets_info},
    "sheet1": {"cells": cells_data},
    "sharedStrings": shared_strings,
    "calcChain": calc_chain,
}

with open("filtered_metadata.json", "w") as json_file:
    json.dump(metadata, json_file, indent=4)

print("Filtered metadata has been saved to filtered_metadata.json")
