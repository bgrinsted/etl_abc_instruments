# Import necessary modules and functions
import logging
import os
from sqlalchemy import create_engine
from src.database import Base
from src.filereader import FileReader
from src.transformer import Transformer
from src.loader import Loader


# A function to process a directory of files
def process_data_dir(directory):
    # Create a logger object to log messages
    logger = logging.getLogger(__name__)

    # Create a database engine object to connect to the database
    engine = create_engine("sqlite:///data/published/order_delivery.db", echo=True)

    # Create the tables in the database
    Base.metadata.create_all(engine)

    # Get a list of all files in the directory
    with os.scandir(directory) as entries:
        files = [entry for entry in entries if entry.is_file()]

    # If there are no files to process, log an error and return
    if not files:
        logger.error("No files to process")
        return

    # Loop over all files in the directory and process
    for file in files:
        # Get the path to the file
        file_path = file.path

        logger.info(f"Processing file {file_path}")
        try:
            # Read the file and create a DataFrame
            file_obj = FileReader(file_path)
            raw_df = file_obj.df
            # Clean the DataFrame and create a new, cleaned DataFrame
            clean_df = Transformer(raw_df, date_columns=["PaymentDate"]).clean()
            # Load the cleaned DataFrame into the database
            Loader(clean_df, engine).load_target()
            # Move the processed file to an archive directory
            file_obj.move_file_to_archive()

            logger.info(f"File {file_path} processed successfully")
        except Exception as e:

            logger.exception(f"Error processing file {file_path}: {e}")


if __name__ == "__main__":
    # Configure the logging module INFO
    logging.basicConfig(level=logging.INFO)
    # Define the directory containing the files to process
    data_dir = os.path.join("data", "raw")
    # Call the function to process the files in the directory
    process_data_dir(data_dir)
