import pandas as pd
import json

# Load the filtered metadata JSON
with open("filtered_metadata.json", "r") as f:
    metadata = json.load(f)

# Extract required components
cells_data = metadata["sheet1"]["cells"]
shared_strings = metadata["sharedStrings"]

# Create a DataFrame from cell data
data = []
for cell in cells_data:
    data.append([cell["ref"], cell["value"], cell["formula"]])

df = pd.DataFrame(data, columns=["Cell", "Value", "Formula"])

# Replace shared string indices with actual values
for index, row in df.iterrows():
    if (
        row["Value"]
        and row["Value"].isdigit()
        and int(row["Value"]) < len(shared_strings)
    ):
        df.at[index, "Value"] = shared_strings[int(row["Value"])]

# Save the DataFrame to a CSV file for quick inspection
df.to_csv("cell_data.csv", index=False)
print("DataFrame has been saved to cell_data.csv")
