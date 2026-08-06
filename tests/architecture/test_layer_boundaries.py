from pytest_archon import archrule

# All rules use only_direct_imports=True: app/dependencies.py is the composition
# root and intentionally imports from every layer to wire concrete
# implementations to interfaces, so presentation modules that import
# app.dependencies would otherwise look like they transitively import
# data_access/business internals. Direct imports are what actually matter for
# these boundaries.


def test_presentation_should_not_import_data_access():
    (
        archrule(
            "presentation_should_not_import_data_access",
            comment="Presentation must reach persistence only through business services (via app.dependencies), never data_access directly",
        )
        .match("app.presentation*")
        .should_not_import("app.data_access*")
        .check("app", only_direct_imports=True)
    )


def test_presentation_should_not_import_business_internals():
    (
        archrule(
            "presentation_should_not_import_business_internals",
            comment="Routers may only depend on business exceptions (to translate into HTTP responses) and the app.dependencies composition root, not services/entities/interfaces directly",
        )
        .match("app.presentation*")
        .should_not_import("app.business.services*", "app.business.entities*", "app.business.interfaces*")
        .check("app", only_direct_imports=True)
    )


def test_business_should_not_import_presentation():
    (
        archrule(
            "business_should_not_import_presentation",
            comment="Business logic must not depend on the HTTP layer",
        )
        .match("app.business*")
        .should_not_import("app.presentation*")
        .check("app", only_direct_imports=True)
    )


def test_business_should_not_import_data_access_internals():
    (
        archrule(
            "business_should_not_import_data_access_internals",
            comment="Business layer may depend on data_access.interfaces (abstractions) but never concrete ORM models, repositories, or mappers",
        )
        .match("app.business*")
        .should_not_import("app.data_access.database*", "app.data_access.repositories*", "app.data_access.mappers*")
        .check("app", only_direct_imports=True)
    )


def test_data_access_should_not_import_presentation():
    (
        archrule(
            "data_access_should_not_import_presentation",
            comment="Persistence code must not depend on the HTTP layer",
        )
        .match("app.data_access*")
        .should_not_import("app.presentation*")
        .check("app", only_direct_imports=True)
    )


def test_data_access_should_not_import_business_internals():
    (
        archrule(
            "data_access_should_not_import_business_internals",
            comment="data_access may depend on business.entities (for mapping) but never business services or interfaces",
        )
        .match("app.data_access*")
        .should_not_import("app.business.services*", "app.business.interfaces*")
        .check("app", only_direct_imports=True)
    )


def test_business_should_not_import_web_framework():
    (
        archrule(
            "business_should_not_import_web_framework",
            comment="Business logic must stay framework-agnostic — no direct dependency on FastAPI, Flask, Starlette, or Django",
        )
        .match("app.business*")
        .should_not_import("fastapi*", "flask*", "starlette*", "django*")
        .check("app", only_direct_imports=True)
    )
