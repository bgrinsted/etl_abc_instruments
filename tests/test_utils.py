from src.database import Client
from src.utils.utils import get_or_create_dimension


class TestGetOrCreate:
    def test_get(self, dbsession):
        client = Client(Name="client_123")
        dbsession.add(client)
        dbsession.commit()

        assert get_or_create_dimension(dbsession, Client, Name="client_123") == client

    def test_create(self, dbsession):
        client = Client(Name="client_123")
        dbsession.add(client)
        dbsession.commit()
        assert get_or_create_dimension(dbsession, Client, Name="client_1234") != client

# TODO: add tests for insert_or_update
# TODO: add tests for load_target
