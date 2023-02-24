import os
import shutil
import pandas as pd
import pandera as pa
from pandera import io


class FileReader:
    # dictionary of supported file types and the function for reading the file
    FILE_READERS = {
        ".csv": pd.read_csv,
    }

    def __init__(self, filepath, validate=True):
        self._filepath = filepath
        self._filename = os.path.basename(filepath)
        self._filetype = os.path.basename(os.path.dirname(filepath))
        self._file_ext = os.path.splitext(filepath)[-1]
        self.df = self.read_file()
        if validate:  # if validate is True, validate the contents of the file
            self.validate_content()

    # function to read the file based on its file extension
    def read_file(self):
        if self._file_ext not in FileReader.FILE_READERS:  # check if the file extension is supported
            raise Exception(f"Unsupported filetype {self._file_ext}")
        return FileReader.FILE_READERS[self._file_ext](self._filepath, keep_default_na=False)

        # function to validate the contents of the file using a schema

    def validate_content(self):
        # construct the path to the schema file based on the file type
        schema_path = os.path.join("data", "schemas", f"{self._filetype}_schema.yml")
        with open(schema_path, "r") as file:  # open the schema file
            yaml_schema = file.read()  # read the schema file
        schema = pa.io.from_yaml(yaml_schema)  # parse the schema file using pandera
        self.df = schema.validate(self.df)  # validate the contents of the DataFrame using the schema

    # function to move the file to an archive directory
    def move_file_to_archive(self):
        archive_dir = os.path.join("data", "raw", "processed")  # construct the path to the archive directory
        # move the file to the archive directory
        shutil.move(self._filepath, os.path.join(archive_dir, self._filename))
