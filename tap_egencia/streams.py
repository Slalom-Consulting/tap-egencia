"""Stream type classes for tap-egencia."""

from __future__ import annotations

import requests
import datetime 

from pathlib import Path
import json

from tap_egencia.client import egenciaStream

from singer_sdk.typing import PropertiesList, Property, StringType

from typing import Any, Dict, Iterable


from tap_egencia.schemas.get_transactions import (
    paymentObject,
    policyObject,
    priceObject,
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
    authenticator = None

    def get_records(self, *args, **kwargs) -> Iterable[Dict[str, Any]]:
        authenticator = super().authenticator
        url_base = super().url_base
        start_date = super().start_date
        end_date = super().end_date
        
        self.path = "/bi/api/v1/transactions"

        session = requests.Session()
        session.headers = authenticator.auth_headers
        session.headers["Accept"] = "application/hal+json"
        session.headers["Content-Type"] = "application/json"

        if start_date == None:
            n_days_ago = datetime.datetime.now() - datetime.timedelta(7)
            start_date = n_days_ago.strftime("%Y-%m-%d %H:%M:%S")
   
        if end_date == None:
            today = datetime.datetime.now()
            end_date = today.strftime("%Y-%m-%d %H:%M:%S")

        self.body = {"start_date": f"{start_date}", "end_date": f"{end_date}"}

        post_transaction_request = session.prepare_request(
            requests.Request(method="POST", url=url_base + self.path, json=self.body)
        )


        post_transaction_response = self._request(post_transaction_request, None)

        if post_transaction_response.status_code != 201:
            replacementContent = { "failure-response": f"{post_transaction_response.status_code} - {post_transaction_response.reason}", "report_id": "", "metadata": {}, "transactions": [], "_links": {}}
            
            json_response = json.dumps(replacementContent)
            byte_response = json_response.encode()
            post_transaction_response._content = byte_response

            return super().parse_response(post_transaction_response)

        else:

            report_id = post_transaction_response.json()["report_id"]
            total_pages = post_transaction_response.json()["metadata"]["total_pages"]

            self.path = f"/bi/api/v1/transactions/{report_id}?page={total_pages}"

            get_transaction_request = session.prepare_request(
                requests.Request(
                    "GET",
                    url_base + self.path,
                ),
            )

            get_transaction_response = self._request(get_transaction_request, None)

            match get_transaction_response.status_code:
                case 200:
                    return iter(json.loads(get_transaction_response.content.decode())["transactions"])
                case 400:
                    raise Exception('Bad Request: Invalid input or request')
                case 401:
                    raise Exception("Unauthorized: authentication token empty, invalid or expired")
                case 403:
                    raise Exception("Forbidden: User not Validated for operation")
                case 405:
                    raise Exception("Client Error: Method Not Allowed for path")
                case 422:
                    raise Exception("Invalid input: invalid or missing required input")
                case 500:
                    raise Exception("Internal Server Error: unable to process request.")
                case _:
                # Return Status Code, Textual Reason for error and response body of error if occurance not listed above
                    raise Exception(get_transaction_response.status_code, get_transaction_response.reason, get_transaction_response.content)

