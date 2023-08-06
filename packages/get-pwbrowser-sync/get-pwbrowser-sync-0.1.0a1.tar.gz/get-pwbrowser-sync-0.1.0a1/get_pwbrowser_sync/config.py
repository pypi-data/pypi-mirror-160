"""Configure params DEBUG HEADFUL PROXY."""
from pathlib import Path
from typing import Optional

from logzero import logger

# import dotenv
from pydantic import AnyUrl, BaseSettings  # pylint: disable=no-name-in-module


class Settings(BaseSettings):  # pylint: disable=too-few-public-methods
    """Configure params DEBUG HEADFUL PROXY."""

    debug: bool = False
    headful: bool = False
    proxy: Optional[AnyUrl] = None

    class Config:  # pylint: disable=too-few-public-methods
        """Config."""

        env_prefix = "PWBROWSER_"
        # extra = "allow"
        env_file = ".env"
        env_file_encoding = "utf-8"  # pydantic doc

        logger.info(
            "env_prefix: %s, env_file: %s", env_prefix, Path(env_file).resolve()
        )
