from singer_sdk.typing import (
    PropertiesList,
    Property,
)
from tap_egencia.schemas.utils.custom_objects import CustomObject

from singer_sdk.typing import (
    PropertiesList,
    Property,
    NumberType,
    StringType,
)

class firstObject(CustomObject):
    properties = PropertiesList(
        Property("href", StringType),
    )

class lastObject(CustomObject):
    properties = PropertiesList(
        Property("href", StringType),
    )

class linksObject(CustomObject):
    properties = PropertiesList(
        Property("first", firstObject),
        Property("last", lastObject)
    )

class metadataObject(CustomObject):
    properties = PropertiesList(
        Property("page_limit", NumberType),
        Property("total_records", NumberType),
        Property("total_pages", NumberType),
        Property("latest_reconciled_date", StringType),
    )
