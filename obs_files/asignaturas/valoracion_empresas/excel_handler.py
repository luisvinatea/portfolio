import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)


def read_excel_sheets_to_csv(file_path: str) -> None:
    """
    Reads xlsx and exports each sheet to a separate csv.
    Args:
        file_path (str): The path to the Excel file.
    """
    try:
        # Load the Excel file and extract sheet names
        excel_data = pd.ExcelFile(file_path, engine='openpyxl')
        sheet_names = excel_data.sheet_names

        # Loop through each sheet and export it to a CSV file
        for sheet_name in sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
            csv_file_name = f"{sheet_name.replace(' ', '_')}.csv"  # Create CSV file name
            df.to_csv(csv_file_name, index=False)
            logging.info(f"Exported sheet '{sheet_name}' to {csv_file_name}")
    except Exception as e:
        logging.error(f"Error processing Excel file: {e}")


def main():

    excel_file_path = 'obs_files/asignaturas/valoracion_empresas/Pista Evaluación final.xlsx'  # Replace with your Excel file path
    read_excel_sheets_to_csv(excel_file_path)


if __name__ == "__main__":
    main()