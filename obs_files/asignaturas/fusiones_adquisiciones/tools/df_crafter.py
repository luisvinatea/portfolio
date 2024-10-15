import pandas as pd
import numpy as np
import re

# Load cell data from CSV
df = pd.read_csv("cell_data.csv")

# Clean data: Replace empty strings with NaN for easier handling of missing values
df.replace("", np.nan, inplace=True)

# Convert the dataframe to make it more readable by adding calculated values where necessary
df["Calculated Value"] = np.nan

# Define the calculations based on the formulas in the cell data
for index, row in df.iterrows():
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
