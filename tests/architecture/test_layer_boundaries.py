from pytest_archon import archrule

# All rules use only_direct_imports=True: app/dependencies.py is the composition
# root and intentionally imports from every feature and every layer to wire
# concrete implementations to interfaces, so a router that imports
# app.dependencies would otherwise look like it transitively imports
# data_access internals. Direct imports are what actually matter for these
# boundaries.
#
# The layout is feature-based: app/auth/ and app/todos/ are self-contained
# slices, each with its own business/, data_access/ and presentation/ layers,
# and app/shared/ holds the pieces both features build on, organised by
# technical concern rather than by layer: shared/database/ (Base, session,
# ISqlAlchemyRepository) and shared/errors/ (AppError/BusinessError, the
# ErrorResponse schema and the one feature-neutral OpenAPI response).
#
# Feature-specific OpenAPI response dicts now live in the slice that owns
# them (<feature>/presentation/responses.py), so no pattern here refers to
# app.shared.presentation* or app.shared.data_access* any more.

FEATURES = ("auth", "todos")


def _internals(feature: str) -> tuple[str, ...]:
    """Modules of `feature` that no other feature may reach into.

    A feature's public surface is its business entity and its business/data
    access interfaces; its services, repositories, mappers, ORM models,
    routers, schemas and crypto helpers are private to it.
    """
    return (
        f"app.{feature}.business.service*",
        f"app.{feature}.data_access*",
        f"app.{feature}.presentation*",
        f"app.{feature}.security*",
    )


def test_auth_should_not_import_todos():
    (
        archrule(
            "auth_should_not_import_todos",
            comment="auth is the lower-level feature — it must not know todos exists at all",
        )
        .match("app.auth*")
        .should_not_import("app.todos*")
        .check("app", only_direct_imports=True)
    )


def test_todos_should_not_import_auth_internals():
    (
        archrule(
            "todos_should_not_import_auth_internals",
            comment="todos owns a user_id, so it may depend on the auth business entity — but never on auth's service, repository, mapper, ORM model, router or schemas",
        )
        .match("app.todos*")
        .should_not_import(*_internals("auth"))
        .check("app", only_direct_imports=True)
    )


def test_shared_should_not_import_features():
    (
        archrule(
            "shared_should_not_import_features",
            comment="app.shared is what features are built on — the dependency only ever points feature -> shared",
        )
        .match("app.shared*")
        .should_not_import("app.auth*", "app.todos*")
        .check("app", only_direct_imports=True)
    )


def test_presentation_should_not_import_data_access():
    (
        archrule(
            "presentation_should_not_import_data_access",
            comment="Inside a feature, presentation must reach persistence only through the business service (via app.dependencies), never data_access directly",
        )
        .match("app.*.presentation*")
        .should_not_import(
            "app.auth.data_access*", "app.todos.data_access*", "app.shared.database*"
        )
        .check("app", only_direct_imports=True)
    )


def test_presentation_should_not_import_business_internals():
    (
        archrule(
            "presentation_should_not_import_business_internals",
            comment="Routers may only depend on business exceptions (to translate into HTTP responses) and the app.dependencies composition root, not services/entities/interfaces directly",
        )
        .match("app.*.presentation*")
        .should_not_import(
            *(
                f"app.{f}.business.{m}*"
                for f in FEATURES
                for m in ("service", "entity", "interface")
            )
        )
        .check("app", only_direct_imports=True)
    )


def test_business_should_not_import_presentation():
    (
        archrule(
            "business_should_not_import_presentation",
            comment="Business logic must not depend on the HTTP layer",
        )
        .match("app.*.business*")
        .should_not_import(
            "app.auth.presentation*",
            "app.todos.presentation*",
        )
        .check("app", only_direct_imports=True)
    )


def test_business_should_not_import_data_access_internals():
    (
        archrule(
            "business_should_not_import_data_access_internals",
            comment="The business layer may depend on its feature's data_access interface (an abstraction) but never on concrete ORM models, repositories or mappers",
        )
        .match("app.*.business*")
        .should_not_import(
            *(
                f"app.{f}.data_access.{m}*"
                for f in FEATURES
                for m in ("model", "repository", "mapper")
            ),
            "app.shared.database*",
        )
        .check("app", only_direct_imports=True)
    )


def test_data_access_should_not_import_presentation():
    (
        archrule(
            "data_access_should_not_import_presentation",
            comment="Persistence code must not depend on the HTTP layer",
        )
        .match("app.*.data_access*")
        .should_not_import(
            "app.auth.presentation*",
            "app.todos.presentation*",
        )
        .check("app", only_direct_imports=True)
    )


def test_data_access_should_not_import_business_internals():
    (
        archrule(
            "data_access_should_not_import_business_internals",
            comment="data_access may depend on business entities (for mapping) but never on business services or interfaces",
        )
        .match("app.*.data_access*")
        .should_not_import(
            *(
                f"app.{f}.business.{m}*"
                for f in FEATURES
                for m in ("service", "interface")
            )
        )
        .check("app", only_direct_imports=True)
    )


def test_business_should_not_import_web_framework():
    (
        archrule(
            "business_should_not_import_web_framework",
            comment="Business logic must stay framework-agnostic — no direct dependency on FastAPI, Flask, Starlette, or Django",
        )
        .match("app.*.business*")
        .should_not_import("fastapi*", "flask*", "starlette*", "django*")
        .check("app", only_direct_imports=True)
    )
