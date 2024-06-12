import logging
from enum import StrEnum, unique

_LOGGER = logging.getLogger(__name__)


@unique
class JobName(StrEnum):
    THUMBNAIL_GENERATION = "thumbnailGeneration"
    METADATA_EXTRACTION = "metadataExtraction"
    VIDEO_CONVERSION = "videoConversion"
    FACE_DETECTION = "faceDetection"
    FACIAL_RECOGNITION = "facialRecognition"
    SMART_SEARCH = "smartSearch"
    BACKGROUND_TASK = "backgroundTask"
    STORAGE_TEMPLATE_MIGRATION = "storageTemplateMigration"
    MIGRATION = "migration"
    SEARCH = "search"
    SIDECAR = "sidecar"
    LIBRARY = "library"
    NOTIFICATIONS = "notifications"
