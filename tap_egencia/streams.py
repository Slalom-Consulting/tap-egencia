"""Stream type classes for tap-egencia."""

from __future__ import annotations

from pathlib import Path
import json

from tap_egencia.client import egenciaStream

from singer_sdk.typing import PropertiesList, Property, StringType

from typing import Any, Dict, Iterable


from tap_egencia.schemas.post_transactions import linksObject
from tap_egencia.schemas.get_transactions import (
    metadataObject,
    paymentObject,
    policyObject,
    priceObject,
    transactionsObject,
    travelDatesObject,
    travelerObject,
    customDataFieldsObject,
    durationObject,
    identifierObject
)

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class TransactionsStream(egenciaStream):
    """Define reporting/transactions stream."""

    name = "transactions-api"
    schema = PropertiesList(
        Property("traveler", travelerObject),
        Property("advance_purchase_days", StringType),
        Property("advance_purchase_window", StringType),
        Property("ancillary_type", StringType),
        Property("booking_method", StringType),
        Property("custom_data_fields", customDataFieldsObject),
        Property("cabin_class_name", StringType),
        Property("class_of_service", StringType),
        Property("client_code", StringType),
        Property("company_name", StringType),
        Property("department", StringType),
        Property("duration", durationObject),
        Property("geography_type", StringType),
        Property("identifier", identifierObject),
        Property("invoice_date", StringType),
        Property("is_active", StringType),
        Property("is_agent_assisted", StringType),
        Property("is_special_request", StringType),
        Property("line_of_business", StringType),
        Property("location", StringType),
        Property("meeting_name", StringType),
        Property("parent_client_code", StringType),
        Property("payment_instrument_info", paymentObject),
        Property("point_of_sale", StringType),
        Property("point_of_sale_country", StringType),
        Property("policy", policyObject),
        Property("price", priceObject),
        Property("purchase_count", StringType),
        Property("rate_type", StringType),
        Property("segment_count", StringType),
        Property("ticket_code", StringType),
        Property("ticket_status", StringType),
        Property("transaction_date", StringType),
        Property("transaction_status", StringType),
        Property("transaction_type", StringType),
        Property("travel_dates", travelDatesObject),
        Property("vendor", StringType),
        Property("vendor_name", StringType)
    ).to_dict()

    def parse_response(self, response) -> Iterable[Dict[str, Any]]:
        return iter(json.loads(response.content.decode())["transactions"])


class TransactionsResponseStream(egenciaStream):
    """Define reporting/transactions stream."""

    name = "transactionsResponse-api"
    schema = PropertiesList(
        Property("failure-response", StringType),
        Property("report_id", StringType),
        Property("metadata", metadataObject),
        Property("transactions", transactionsObject),
        Property("_links", linksObject)
    ).to_dict()

    def parse_response(self, response) -> Iterable[Dict[str, Any]]:
        return super().parse_response(response)
