"""{{cookiecutter.project_name.title()}} logger."""

import logging
import sys
from typing import Any, Callable


class {{cookiecutter.project_slug.replace('_', ' ').title().replace(' ', '')}}Logger:
    """{{cookiecutter.project_name.title()}} custom logger."""

    LEVELS = {
        "ERROR": 1,
        "WARNING": 2,
        "INFO": 3,
        "{{cookiecutter.project_name.upper()}}": 4,
    }

    def __init__(self, name: str) -> None:
        """Init magic method."""
        self.logger = logging.getLogger(name)
        self._configure()

        for level_name, level_value in self.LEVELS.items():
            setattr(
                self.logger,
                level_name.lower().replace('-', '_').replace(' ', '_'),
                self._create_log_method(level_value),
            )

    def _configure(self) -> None:
        """Logger configuration."""
        logging.basicConfig(
            stream=sys.stdout,
            format="  %(levelname)-3s: %(message)s",
        )

        for level_name, level_value in self.LEVELS.items():
            logging.addLevelName(level_value, f"[{level_name}]")

    def _create_log_method(self, level: int) -> Callable:
        """Create log method."""
        return lambda msg, *args: self.logger._log(level, msg, args)

    def get_logger(self) -> Any:
        """Get logger."""
        return self.logger
