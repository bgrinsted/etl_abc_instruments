from src.database import Delivery, FactOrderItem, Payment, Product, Client

# TODO: move this to a config file

TABLE_MAPPING = {  # define mapping of columns between the dataframe and database tables
    "facts": {  # mapping for fact table
        "fact_order_item": {  # mapping for fact_order_item table
            "table": "fact_order_item",  # table name in the database
            "class": FactOrderItem,  # corresponding database model
            "mapping": {  # mapping of dataframe columns to database columns
                "OrderNumber": "OrderNumber",
                "Quantity": "ProductQuantity",
                "TotalPrice": "TotalPrice",
                "Currency": "Currency"
            }
        },
    },
    "dimensions": {
        "dim_product": {
            "table": "dim_product",
            "class": Product,
            "mapping": {"Name": "ProductName",
                        "Type": "ProductType",
                        "UnitPrice": "UnitPrice"}
        },
        "dim_client": {
            "table": "dim_client",
            "class": Client,
            "mapping": {"Name": "ClientName"}
        },
        "dim_payment": {
            "table": "dim_payment",
            "class": Payment,
            "mapping": {"Type": "PaymentType",
                        "Date": "PaymentDate"}
        },
        "dim_delivery": {
            "table": "dim_delivery",
            "class": Delivery,
            "mapping": {"Address": "DeliveryAddress",
                        "City": "DeliveryCity",
                        "Postcode": "DeliveryPostcode",
                        "Country": "DeliveryCountry",
                        "ContactNumber": "DeliveryContactNumber"}
        },

    }
}
