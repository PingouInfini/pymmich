import logging
from enum import StrEnum, unique

_LOGGER = logging.getLogger(__name__)


@unique
class AssetJob(StrEnum):
    REGENERATE_THUMBNAIL = "regenerate-thumbnail"
    REFRESH_METADATA = "refresh-metadata"
    TRANSCODE_VIDEO = "transcode-video"
