import json
from datetime import datetime, date
from typing import Dict

import pandas as pd


class SheetColumn:
    """
        Class representing a column in a data sheet.
    """
    def __init__(self, column_data):
        self.name = column_data['name']
        self.column_name_sheet = column_data['columnNameSheet']
        self.column_name_db = column_data['columnNameDB']
        self.type_value = column_data['typeValue']
        self.value_format = column_data.get('valueFormat', '')
        self.min_value = column_data.get('minValue', None)
        self.max_value = column_data.get('maxValue', None)
        self.description = column_data['description']
        self.default_value = column_data.get('defaultValue', '')
        self.nullable = column_data.get('isNullable', False)

    def __str__(self):
        return f"""Name: {self.name}, 
                Column Name (Sheet): {self.column_name_sheet}, 
                Column Name (DB): {self.column_name_db}, 
                Type: {self.type_value}, 
                Value Format: {self.value_format}, 
                Min Value: {self.min_value}, 
                Max Value: {self.max_value}, 
                Description: {self.description}, 
                Is nullable: {self.nullable}"""

    def check_validity(self, value):
        """
            Checks the validity of a given value.
        """
        nullity_state = self.check_value_nullity(value)
        if nullity_state is False:
            return False
        if self.type_value in ['int', 'float', 'decimal']:
            return self.check_numeric_validity(float(value))
        if self.type_value in ['date', 'datetime']:
            return self.check_date_validity(value)
        if self.type_value == 'str':
            return self.check_str_validity(str(value))
        return False

    def check_value_nullity(self, value):
        """
            Checks the nullity of a value.
        """
        if self.nullable is True:
            return True
        return value is not None

    def check_str_validity(self, value: str):
        """
            Checks the validity of a string value.
        """
        if self.type_value != 'str':
            return False
        if self.min_value is not None and len(value) < self.min_value:
            return False
        if self.max_value is not None and len(value) > self.max_value:
            return False
        return True

    def check_numeric_validity(self, value: float):
        """
            Checks the validity of a numeric value.
        """
        if self.type_value not in ['int', 'float', 'decimal']:
            return False
        if self.min_value is not None and value < self.min_value:
            return False
        if self.max_value is not None and value > self.max_value:
            return False
        return True

    def check_date_validity(self, value):
        """
            Checks the validity of a date value.
        """
        if (isinstance(value, pd.Timestamp)
                or isinstance(value, datetime)
                or isinstance(value, date)):
            return True
        if isinstance(value, str):
            if self.type_value == 'date':
                date_formats = ['%Y-%m-%d', '%d-%m-%Y', '%d-%m-%y', '%y-%m-%d']
                for date_format in date_formats:
                    try:
                        datetime.strptime(str(value), date_format)
                        return True
                    except ValueError:
                        pass
                return False
        return False


class SheetTable:
    """
        Class representing a sheet in the Excel file
    """
    def __init__(self, json_file):
        with open(json_file) as f:
            table_data = json.load(f)
        self.name = table_data['name']
        self.sheet_name:str = table_data['sheet']
        self.columns = [SheetColumn(column_data) for column_data in table_data['columns']]
        self.dict_columns = None
        self.columns_to_dict()

    def __str__(self):
        column_info = "\n".join([str(column) for column in self.columns])
        return f"Name: {self.name}\nSheet: {self.sheet_name}\nColumns:\n{column_info}"

    def columns_to_dict(self):
        """
            transforming the columns to a dictionary { column Name in sheet : column object }
            :return: the dictionary
        """
        if self.dict_columns is None:
            self.dict_columns = {column.column_name_sheet: column for column in self.columns}
        return self.dict_columns

    def check_validity(self, data: pd.DataFrame):
        data_size = len(data)
        for index in range(data_size):
            for col in self.columns:
                try:
                    row = data[col.column_name_sheet][index]
                    # print("row", index, "col", col.column_name_sheet, "value", row)
                    if col.check_validity(row) is False and not col.nullable:
                        raise Exception(f"invalid data in col '{col.column_name_sheet}' at row: '{index}', value = '{row}'")
                except Exception as e:
                    error_message = "There is an error for the column '" + col.column_name_sheet + "', at row: '"+ str(index)+"', value = '"+str(data[col.column_name_sheet][index])+"'"
                    if not col.nullable:
                        print(e)
                        raise Exception(error_message)
        return True


class FileInfo:
    def __init__(self, filename, description):
        self.filename = filename
        self.description = description


class SheetConfig:
    """
        All information about each spreadsheet in the Excel file
    """
    def __init__(self, json_file):
        with open(json_file) as f:
            table_data = json.load(f)
        self.name = table_data['name']
        self.files = [FileInfo(file["filename"], file["description"]) for file in table_data['files']]
        self.sheet_tables: Dict[str, SheetTable] = None

    def build_sheet_info(self):
        """
            Initializes sheet information and then put it in the attribute **`sheet_tables`**.
        """
        sheet_tables = {}
        for file in self.files:
            sheet_table = SheetTable(file.filename)
            sheet_tables[sheet_table.sheet_name] = sheet_table
        self.sheet_tables = sheet_tables

    def check_validity(self, datas: Dict[str, pd.DataFrame]):
        """
            Checks the validity of data for each spreadsheet.
            :param datas: A dictionary of the form {sheet_name: DataFrame}
            :return: A dictionary of the form {sheet_name: Boolean_result}
        """
        # Initialize the result dictionary
        result = {}

        # Iterate over each sheet table
        for key, sheet_table in self.sheet_tables.items():
            # sheet, here we go (again)
            try:
                # Check the validity of data for the current sheet table
                result[sheet_table.sheet_name] = sheet_table.check_validity(datas[sheet_table.sheet_name])
            except Exception as e:
                print(f"Error in {sheet_table.name}: {e}")
                # Record the result as False due to the error. You got it wrong, hehe
                result[sheet_table.sheet_name] = False

        # return literally the result
        return result

