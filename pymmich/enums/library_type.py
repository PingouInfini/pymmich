import logging
from enum import StrEnum, unique

_LOGGER = logging.getLogger(__name__)


@unique
class LibraryType(StrEnum):
    UPLOAD = "UPLOAD"
    EXTERNAL = "EXTERNAL"
