# This function gets or creates a model instance based on the provided query parameters.
# If an instance exists, it returns that instance. If not, it creates a new instance
# and returns that.
def get_or_create_dimension(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def insert_or_update_fact(session, model, **kwargs):
    # Query the database for an instance of the model
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    # If an instance is matched, no changes to record, return it
    if instance:
        return instance
    else:
        # Otherwise, try to find an instance with the same order number and delete it
        if old_instance := session.query(model).filter_by(OrderNumber=kwargs["OrderNumber"]).one_or_none():
            session.delete(old_instance)
            session.commit()
        # Create a new instance of the model with the specified keyword arguments
        instance = model(**kwargs)
        # Add the new instance to the session and commit the transaction
        session.add(instance)
        session.commit()
        return instance
