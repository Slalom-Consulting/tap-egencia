from singer_sdk.typing import (
    PropertiesList,
    Property,
)
from tap_egencia.schemas.utils.custom_objects import CustomObject

from singer_sdk.typing import (
    PropertiesList,
    Property,
    StringType
)
from tap_egencia.schemas.post_transactions import (
    linksObject,
    metadataObject
)

class schema(CustomObject):
    properties = PropertiesList(
        Property("report_id", StringType),
        Property("metadata", metadataObject),
        Property("_links", linksObject),
        ).to_dict
