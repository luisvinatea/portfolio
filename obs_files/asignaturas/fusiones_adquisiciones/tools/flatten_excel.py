import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import re
import json

# Paths to data files
base_path = (
    "/home/luisvinatea/Dev/portfolio/obs_files/asignaturas/fusiones_adquisiciones/data/"
)
workbook_path = base_path + "workbook.xml"
sheet1_path = base_path + "sheet1.xml"
shared_strings_path = base_path + "sharedStrings.xml"
calc_chain_path = base_path + "calcChain.xml"

# Parse workbook.xml to get sheet information
workbook_tree = ET.parse(workbook_path)
workbook_root = workbook_tree.getroot()

# Extract workbook metadata (sheet names and IDs)
sheets_info = [
    {
        "name": sheet.get("name"),
        "sheetId": sheet.get("sheetId"),
        "id": sheet.get(
            "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
        ),
    }
    for sheet in workbook_root.findall(
        ".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheet"
    )
]

# Parse sheet1.xml to extract cell data
sheet_tree = ET.parse(sheet1_path)
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
shared_strings_tree = ET.parse(shared_strings_path)
shared_strings_root = shared_strings_tree.getroot()
shared_strings = [
    si.text
    for si in shared_strings_root.findall(
        ".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"
    )
]

# Create a DataFrame from cell data
data = []
for cell in cells_data:
    value = cell["value"]
    # If cell type is 's', it's a shared string
    if cell["type"] == "s" and value and value.isdigit():
        value = shared_strings[int(value)]
    data.append([cell["ref"], value, cell["formula"]])

df = pd.DataFrame(data, columns=["Cell", "Value", "Formula"])

# Clean data: Replace empty strings with NaN for easier handling of missing values
df.replace("", np.nan, inplace=True)

# Convert the dataframe to make it more readable by adding calculated values where necessary
df["Calculated Value"] = np.nan

# Get calculation order from calcChain.xml
calc_chain_tree = ET.parse(calc_chain_path)
calc_chain_root = calc_chain_tree.getroot()
calc_order = [
    c.get("r")
    for c in calc_chain_root.findall(
        ".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c"
    )
]

# Define the calculations based on the formulas in the cell data
for cell_ref in calc_order:
    if cell_ref in df["Cell"].values:
        index = df[df["Cell"] == cell_ref].index[0]
        row = df.loc[index]
        if pd.notna(row["Formula"]):
            try:
                # Replace cell references with actual values
                formula = row["Formula"]
                # Use regex to find all cell references in the formula, including absolute references
                cell_refs = re.findall(r"\$?[A-Z]+\$?[0-9]+", formula)
                for ref in cell_refs:
                    # Remove dollar signs for easier matching
                    clean_ref = ref.replace("$", "")
                    if clean_ref in df["Cell"].values:
                        ref_value = df.loc[df["Cell"] == clean_ref, "Value"].values[0]
                        if pd.notna(ref_value):
                            try:
                                ref_value = float(ref_value)
                            except ValueError:
                                ref_value = 0  # Handle non-numeric values gracefully
                            formula = formula.replace(ref, str(ref_value))
                        else:
                            formula = formula.replace(
                                ref, "0"
                            )  # Replace missing values with 0 for calculations
                    else:
                        formula = formula.replace(
                            ref, "0"
                        )  # Replace undefined references with 0

                # Debugging output to track formula replacement
                print(f"Formula after replacement for cell {row['Cell']}: {formula}")

                # Remove leading zeros from numeric literals to avoid syntax errors
                formula = re.sub(r"\b0+(\d)", r"\1", formula)

                # Prevent division by zero by replacing any '/ 0' with a safe alternative
                if re.search(r"/\s*0(\.0*)?", formula):
                    print(
                        f"Potential division by zero detected in cell {row['Cell']}. Adjusting formula."
                    )
                    formula = re.sub(r"/\s*0(\.0*)?", "/ 1e-10", formula)

                # Additional check to prevent division by zero by validating each divisor
                tokens = re.split(r"([\+\-\*/\(\)])", formula)
                for i, token in enumerate(tokens):
                    if (
                        token.strip().isdigit()
                        and float(token) == 0
                        and i > 0
                        and tokens[i - 1] == "/"
                    ):
                        print(
                            f"Explicit division by zero detected in cell {row['Cell']}. Adjusting divisor to avoid error."
                        )
                        tokens[i] = "1e-10"
                formula = "".join(tokens)

                # Calculate the value using eval (for simplicity; eval can be risky if input is untrusted)
                calculated_value = eval(formula)
                df.at[index, "Calculated Value"] = calculated_value
            except ZeroDivisionError:
                print(f"Error calculating formula at {row['Cell']}: Division by zero")
                df.at[index, "Calculated Value"] = np.nan
            except Exception as e:
                print(f"Error calculating formula at {row['Cell']}: {e}")

# Fill in the final calculated values in the 'Value' column where needed
df["Value"] = df["Value"].combine_first(df["Calculated Value"])

# Save the final dataframe to a CSV file
df.to_csv("final_output.csv", index=False)

# Create a summary text file with specific answers
with open("summary.txt", "w") as summary_file:
    summary_file.write("Summary of Key Results:\n\n")

    # Write key findings (e.g., BPA calculations)
    for index, row in df.iterrows():
        if row["Cell"] in [
            "D34",
            "E34",
            "D53",
            "E53",
        ]:  # Example cells with key values (e.g., BPA Post, BPA Combined)
            summary_file.write(f"{row['Cell']}: {row['Value']}\n")

print("Final CSV and summary text file have been saved.")
