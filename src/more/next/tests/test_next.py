import json

import pytest
from nextorm import (
    PK,
    Database,
    Entity,
    Opt,
    db_session,
    set_sql_debug,
)
from webtest import TestApp as Client

from more.next import NextApp


def test_query_document():
    db = Database()

    class Document(Entity):
        _table_ = "document"

        id: PK[int]
        title: Opt[str]
        content: Opt[str]

    db.bind("sqlite", ":memory:")
    db.generate_mapping(create_tables=True)
    set_sql_debug(True)

    with db_session:
        Document(title="My Title", content="My content")

    class App(NextApp):
        pass

    @App.path(model=Document, path="documents/{id}")
    def get_document(request, id=0):
        return Document[id]

    @App.json(model=Document)
    def document_default(self, request):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "link": request.link(self),
        }

    c = Client(App())

    response = c.get("/documents/1")

    assert response.json == {
        "id": 1,
        "title": "My Title",
        "content": "My content",
        "link": "http://localhost/documents/1",
    }


def test_update_document():
    db = Database()

    class Document(Entity):
        _table_ = "document"

        id: PK[int]
        title: Opt[str]
        content: Opt[str]

        def update(self, payload={}):
            self.set(**payload)

    db.bind("sqlite", ":memory:")
    db.generate_mapping(create_tables=True)
    set_sql_debug(True)

    with db_session:
        Document(title="My Title", content="My content")

    class App(NextApp):
        pass

    @App.path(model=Document, path="documents/{id}")
    def get_document(request, id=0):
        return Document[id]

    @App.json(model=Document)
    def document_default(self, request):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "link": request.link(self),
        }

    @App.json(model=Document, request_method="PUT")
    def document_update(self, request):
        self.update(request.json)

    c = Client(App())

    c.put("/documents/1", json.dumps({"title": "New Title"}))

    response = c.get("/documents/1")

    assert response.json == {
        "id": 1,
        "title": "New Title",
        "content": "My content",
        "link": "http://localhost/documents/1",
    }


def test_delete_document():
    db = Database()

    class Document(Entity):
        _table_ = "document"

        id: PK[int]
        title: Opt[str]
        content: Opt[str]

        def remove(self):
            self.delete()

    db.bind("sqlite", ":memory:")
    db.generate_mapping(create_tables=True)
    set_sql_debug(True)

    with db_session:
        Document(title="My Title", content="My content")

    class App(NextApp):
        pass

    @App.path(model=Document, path="documents/{id}")
    def get_document(request, id=0):
        return Document[id]

    @App.json(model=Document)
    def document_default(self, request):
        return {"id": self.id}

    @App.json(model=Document, request_method="DELETE")
    def document_remove(self, request):
        self.remove()

    c = Client(App())

    c.delete("/documents/1")

    with pytest.raises(KeyError):
        c.get("/documents/1")
