from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from typing_extensions import ParamSpec
    from typing_extensions import TypeVar

    P = ParamSpec("P")
    R = TypeVar("R")


def to_sync() -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator to convert async methods to sync methods.
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        import functools

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                import asyncio

                from rich import print_json

                print_json(data=asyncio.run(func(*args, **kwargs)))  # type: ignore[arg-type]
            except:  # noqa: E722
                raise SystemExit(1) from None

            raise SystemExit(0)

        return wrapper

    return decorator


def main() -> None:
    """
    Main entry point for the CLI.
    """
    import logging

    logging.basicConfig(
        level=logging.ERROR,
        format="[%(asctime)s] [%(levelname)-7s] [%(name)s] %(message)s",
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logger = logging.getLogger("depsdev")

    try:
        import typer
    except ImportError:
        msg = (
            "The 'cli' optional dependency is not installed. "
            "Please install it with 'pip install depsdev[cli]'."
        )
        logger.error(msg)  # noqa: TRY400
        raise SystemExit(1) from None

    from depsdev.v3alpha import DepsDevClientV3Alpha

    client = DepsDevClientV3Alpha()

    app = typer.Typer(
        name="depsdev",
        help="A CLI tool to interact with the https://docs.deps.dev/api/",
        no_args_is_help=True,
    )
    app.command(rich_help_panel="v3")(to_sync()(client.get_package))
    app.command(rich_help_panel="v3")(to_sync()(client.get_version))
    app.command(rich_help_panel="v3")(to_sync()(client.get_requirements))
    app.command(rich_help_panel="v3")(to_sync()(client.get_dependencies))
    app.command(rich_help_panel="v3")(to_sync()(client.get_project))
    app.command(rich_help_panel="v3")(to_sync()(client.get_project_package_versions))
    app.command(rich_help_panel="v3")(to_sync()(client.get_advisory))
    app.command(rich_help_panel="v3")(to_sync()(client.query))

    # app.command(rich_help_panel="v3alpha")(to_sync()(client.get_version_batch))
    app.command(rich_help_panel="v3alpha")(to_sync()(client.get_dependents))
    app.command(rich_help_panel="v3alpha")(to_sync()(client.get_capabilities))
    app.command(rich_help_panel="v3alpha")(to_sync()(client.get_project_batch))
    app.command(rich_help_panel="v3alpha")(to_sync()(client.get_similarly_named_packages))
    app.command(rich_help_panel="v3alpha")(to_sync()(client.purl_lookup))
    app.command(rich_help_panel="v3alpha")(to_sync()(client.purl_lookup_batch))
    app.command(rich_help_panel="v3alpha")(to_sync()(client.query_container_images))

    return app()


if __name__ == "__main__":
    main()
