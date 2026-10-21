from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

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

if TYPE_CHECKING:
    from morepath import Request


def test_query_document() -> None:
    db: Database = Database()

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
    def get_document(request: Request[App], id: int = 0) -> Document:
        return Document[id]

    @App.json(model=Document)
    def document_default(self: Document, request: Request) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "link": request.link(self),
        }

    c: Client = Client(App())

    response = c.get("/documents/1")

    assert response.json == {
        "id": 1,
        "title": "My Title",
        "content": "My content",
        "link": "http://localhost/documents/1",
    }


def test_update_document() -> None:
    db: Database = Database()

    class Document(Entity):
        _table_ = "document"

        id: PK[int]
        title: Opt[str]
        content: Opt[str]

        def update(self: Document, payload: dict[str, Any] | None = None) -> None:
            if payload is not None:
                self.set(**payload)

    db.bind("sqlite", ":memory:")
    db.generate_mapping(create_tables=True)
    set_sql_debug(True)

    with db_session:
        Document(title="My Title", content="My content")

    class App(NextApp):
        pass

    @App.path(model=Document, path="documents/{id}")
    def get_document(request: Request, id: int = 0) -> Document:
        return Document[id]

    @App.json(model=Document)
    def document_default(self: Document, request: Request[App]) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "link": request.link(self),
        }

    @App.json(model=Document, request_method="PUT")
    def document_update(self: Document, request: Request[App]) -> None:
        self.update(request.json)

    c: Client = Client(App())

    c.put("/documents/1", json.dumps({"title": "New Title"}))

    response = c.get("/documents/1")

    assert response.json == {
        "id": 1,
        "title": "New Title",
        "content": "My content",
        "link": "http://localhost/documents/1",
    }


def test_delete_document() -> None:
    db: Database = Database()

    class Document(Entity):
        _table_ = "document"

        id: PK[int]
        title: Opt[str]
        content: Opt[str]

        def remove(self: Document) -> None:
            self.delete()

    db.bind("sqlite", ":memory:")
    db.generate_mapping(create_tables=True)
    set_sql_debug(True)

    with db_session:
        Document(title="My Title", content="My content")

    class App(NextApp):
        pass

    @App.path(model=Document, path="documents/{id}")
    def get_document(request: Request, id: int = 0) -> Document:
        return Document[id]

    @App.json(model=Document)
    def document_default(self: Document, request: Request) -> dict[str, Any]:
        return {"id": self.id}

    @App.json(model=Document, request_method="DELETE")
    def document_remove(self: Document, request: Request) -> None:
        self.remove()

    c: Client = Client(App())

    c.delete("/documents/1")

    with pytest.raises(KeyError):
        c.get("/documents/1")
