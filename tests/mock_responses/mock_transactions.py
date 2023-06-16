from tap_egencia.schemas.reporting import (
    linksObject,
    metadataObject
)

from singer_sdk.typing import (
    PropertiesList,
    Property,
)

def schema() -> dict:
    return PropertiesList(
        Property("links", linksObject),
        Property("metadata", metadataObject),
        ).to_dict()

# schema = PropertiesList(
#         Property("links", linksObject),
#         Property("metadata", metadataObject),
#         ).to_dict()
