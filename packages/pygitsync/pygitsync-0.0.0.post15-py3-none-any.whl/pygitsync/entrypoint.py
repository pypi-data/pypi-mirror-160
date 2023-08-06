"""Entry to the main execution path."""

import asyncio
import logging
import pathlib
import tempfile
import typing

import click
import daemon  # type: ignore

from ._configuration import DEFAULT_CONFIGURATION_FILE, _load_configuration
from ._repo import _fetch_repo

log = logging.getLogger(__name__)


T = typing.TypeVar("T", bound="WhileContext")


class WhileContext:
    """Define exit status of the consuming while loop.

    If ``is_daemon`` is true, then the ``keep_running`` method always returns
    true. If not, then ``keep_running`` return true the first call, and then
    false after that.
    """

    def __init__(self: T, is_daemon: bool) -> None:
        """Construct ``WhileContext`` object.

        Args:
            is_daemon: Flag if the system is supposed to operate as a daemon.
        """
        self._continue = True
        self.is_daemon = is_daemon

    def keep_running(self: T) -> bool:
        """Define the run state of the caller.

        Returns:
            True for the consumer to continue running, False for the consumer
            to stop running.
        """
        if self.is_daemon:
            # always keep running
            return True
        if (not self.is_daemon) and self._continue:
            # let the loop run this time, but subsequent calls indicate exit
            self._continue = False
            return True
        else:
            # stop running
            return False


async def main(
    configuration_file: pathlib.Path,
    is_daemon: bool,
    sleep_interval_seconds: typing.Optional[float],
) -> None:
    """
    Primary execution path of the utility.

    ``is_daemon`` true means the loop will never exit, otherwise the loop only
    runs once and then exits.

    Args:
        configuration_file: Path to ``pygitsync`` configuration file.
        is_daemon: Flag to prevent execution from exiting.
        sleep_interval_seconds: Duration of period between git fetches.
    """
    with tempfile.TemporaryDirectory() as d:
        working_directory = pathlib.Path(d)

        this_configuration = await _load_configuration(
            configuration_file,
            is_daemon,
            sleep_interval_seconds,
        )

        loop = WhileContext(this_configuration.application.is_daemon)
        while loop.keep_running():
            try:
                log.debug("git sync execution placeholder")
                await _fetch_repo(this_configuration.repo, working_directory)

                log.debug(
                    "sleeping for, "
                    f"{this_configuration.application.sleep_interval_seconds} "
                    "seconds"
                )
                await asyncio.sleep(
                    this_configuration.application.sleep_interval_seconds
                )
            except Exception as e:
                log.critical(f"unhandled exception detected, {str(e)}")
                # sleep after logging this exception to avoid consuming CPU
                # if exception occurs very early in the loop (before the loop
                # hits its own sleep delay).
                await asyncio.sleep(
                    this_configuration.application.exception_sleep_seconds
                )


@click.command()
@click.option(
    "--configuration",
    "-c",
    "configuration_file",
    default=DEFAULT_CONFIGURATION_FILE,
    help="Path to pygitsync configuration file.",
    show_default=True,
    type=click.Path(path_type=pathlib.Path),
)
@click.option(
    "--daemon",
    "-d",
    "is_daemon",
    default=False,
    help="Run utility indefinitely in the background. "
    "Default: run utility indefinitely in foreground.",
    is_flag=True,
)
@click.option(
    "--interval",
    "-i",
    "sleep_interval_seconds",
    default=None,
    help="Duration in seconds between git fetches.",
    show_default=True,
    type=float,
)
def process_cli_arguments(
    configuration_file: pathlib.Path,
    is_daemon: bool,
    sleep_interval_seconds: typing.Optional[float],
) -> None:
    """Process CLI options."""
    if is_daemon:
        with daemon.DaemonContext():
            asyncio.run(
                main(configuration_file, is_daemon, sleep_interval_seconds)
            )
    else:
        # run with the daemon context.
        asyncio.run(main(configuration_file, is_daemon, sleep_interval_seconds))


def flit_entry() -> None:
    """Flit script entry point."""
    process_cli_arguments()
