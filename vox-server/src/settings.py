import os
from functools import lru_cache
from pathlib import Path
from typing import ClassVar

voicevox_core_path = Path(os.environ.get("VOICEVOX_CORE_PATH", "./voicevox_core"))
output_dir_path = Path(os.environ.get("OUTPUT_DIR_PATH", "./output"))


class Settings:
    allowed_origins: ClassVar[list[str]] = []
    voicevox_core_path: Path = voicevox_core_path
    output_dir_path: Path = output_dir_path


@lru_cache
def get_settings() -> Settings:
    return Settings()
