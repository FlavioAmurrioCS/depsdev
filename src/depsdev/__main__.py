from __future__ import annotations

import asyncio
import functools
import logging
import shutil
from typing import TYPE_CHECKING

import typer

from depsdev import DepsDevClient

if TYPE_CHECKING:
    from collections.abc import Callable

    from typing_extensions import ParamSpec
    from typing_extensions import TypeVar

    P = ParamSpec("P")
    R = TypeVar("R")

main = typer.Typer(
    name="depsdev",
    help="A CLI tool to interact with the Deps.Dev API.",
    no_args_is_help=True,
    context_settings={
        "max_content_width": shutil.get_terminal_size().columns,
    },
)

client = DepsDevClient()


def to_sync() -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator to convert async methods to sync methods.
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                from rich import print_json

                print_json(data=asyncio.run(func(*args, **kwargs)))  # type: ignore[arg-type]
            except:  # noqa: E722
                raise SystemExit(1) from None

            raise SystemExit(0)

        return wrapper

    return decorator


main.command()(to_sync()(client.get_package))
main.command()(to_sync()(client.get_version))
main.command()(to_sync()(client.get_requirements))
main.command()(to_sync()(client.get_dependencies))
main.command()(to_sync()(client.get_project))
main.command()(to_sync()(client.get_project_package_versions))
main.command()(to_sync()(client.get_advisory))
main.command()(to_sync()(client.query))

logging.basicConfig(
    level=logging.ERROR,
    format="[%(asctime)s] [%(levelname)-7s] [%(name)s] %(message)s",
)
logging.getLogger("httpx").setLevel(logging.WARNING)

if __name__ == "__main__":
    main()
