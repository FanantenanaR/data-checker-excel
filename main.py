import importlib
import os

from model.sheet import SheetTable, SheetConfig
import pandas as pd


def create_dataframe_from_excel(filepath: str, sheet_name):
    try:
        df = pd.read_excel(filepath, sheet_name=sheet_name, header=0)
        return df
    except Exception as e:
        print(f"Erreur lors de la lecture de la feuille '{sheet_name}': {str(e)}")
        raise e


def build_dictionary_from_excel(filepath: str, sheet_names: []):
    datas = {}
    for sheet_name in sheet_names:
        datas[sheet_name] = create_dataframe_from_excel(filepath, sheet_name)
    return datas


def validate(file_path: str, config: SheetConfig):
    if config.sheet_tables is None:
        config.build_sheet_info()

    datas = build_dictionary_from_excel(file_path, [val.sheet_name for key, val in config.sheet_tables.items()])
    return config.check_validity(datas)


def check_package(package_name):
    """Check if a Python package is installed"""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def find_excel_files(directory):
    """
    Finds all Excel files (.xlsx) in the specified directory. In case you want to check more than one file
    :param directory: The directory to search for Excel files.
    :return: A list of Excel file paths.
    """
    excel_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xlsx'):
                file_path = os.path.join(root, file)
                excel_files.append(os.path.abspath(file_path))
    return excel_files


if __name__ == '__main__':
    try:
        required_packages = ['pandas', 'json']

        # Vérification des packages requis avant de continuer
        for package in required_packages:
            has_it = check_package(package)
            if not has_it:
                raise ImportError(f"Package '{package}' is not installed.")

        # Utilisation de la classe SheetTable
        sheet_config = SheetConfig("config/data.json")

        excel_founds = find_excel_files("data/")
        for excel_file in excel_founds:
            print("Checking for", excel_file)
            print()
            resultat = validate(excel_file, sheet_config)
            print()
            for key, value in resultat.items():
                print(f"{key}: {'OK' if value else 'Invalid'}")
            print("---"*10)
    except ImportError as import_error:
        print(import_error)
    except Exception as e:
        print(e)
