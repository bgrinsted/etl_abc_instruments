from src.utils.utils import insert_or_update_fact, get_or_create_dimension
from sqlalchemy.orm import Session
from src.mappings import TABLE_MAPPING
from src.database import FactOrderItem


# TODO: multiple facts

class Loader:
    """
    given a pandas dataframe, this class is capable of loading the data into a SQL database
    """

    def __init__(self, df, engine):
        self._df = df
        self.engine = engine
        self.session = Session(self.engine)

    def load_target(self):
        with Session(self.engine) as session:  # use context manager to automatically close the session
            for _, row in self._df.iterrows():  # loop through each row in the dataframe
                # get the mapping for the fact table
                fact_mapping = TABLE_MAPPING["facts"]["fact_order_item"]["mapping"]

                # create a dictionary of keyword arguments for the fact
                fact_kwargs = {fact_key: row[fact_value] for fact_key, fact_value in fact_mapping.items()}

                # create a dictionary of keyword arguments for the dimensions
                dimensions_kwargs = {
                    # get or create the corresponding dimension record
                    dim_key: get_or_create_dimension(session, dim_value["class"],
                                                     **{fact_key: row[fact_value] for fact_key, fact_value in
                                                        dim_value["mapping"].items()})
                    for dim_key, dim_value in TABLE_MAPPING["dimensions"].items()
                }
                # insert or update the facts with their corresponding dimension records IDs
                order = insert_or_update_fact(session, FactOrderItem, **fact_kwargs, **dimensions_kwargs)
                session.add_all([order])  # add the record to the session
        try:
            session.commit()
        except:
            session.rollback()
        finally:
            session.close_all()

