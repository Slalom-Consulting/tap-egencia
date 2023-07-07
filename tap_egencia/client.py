"""REST client handling, including egenciaStream base class."""

from __future__ import annotations
import json
from typing import Any, Dict, Iterable

import requests
import datetime

from pathlib import Path
from singer_sdk.streams import RESTStream

from tap_egencia.auth import Auth0Authenticator

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class egenciaStream(RESTStream):
    """egencia stream class."""

    @property
    def url_base(self) -> str:
        domain = self.config["egencia_base_url"]
        return domain

    @property
    def authenticator(self) -> Auth0Authenticator:
        """Return a new authenticator object."""
        return Auth0Authenticator.create_for_stream(self)

    @property
    def start_date(self) -> str | None:
        if self.config['start_date'] != '':
            date = self.config['start_date']
        else: 
            date = None

        return date
    
    @property
    def end_date(self) -> str | None:
        if self.config['end_date'] != '':
            date = self.config['end_date']
        else: 
            date = None
        return date
    
    def get_records(self, *args, **kwargs) -> Iterable[Dict[str, Any]]:
        # authenticator = super().authenticator
        # url_base = super().url_base
        # start_date = super().start_date
        # end_date = super().end_date
        
        self.path = "/bi/api/v1/transactions"

        session = requests.Session()
        session.headers = self.authenticator.auth_headers
        session.headers["Accept"] = "application/hal+json"
        session.headers["Content-Type"] = "application/json"

        if self.start_date == None:
            n_days_ago = datetime.datetime.now() - datetime.timedelta(7)
            self.start_date = n_days_ago.strftime("%Y-%m-%d %H:%M:%S")
   
        if self.end_date == None:
            today = datetime.datetime.now()
            self.end_date = today.strftime("%Y-%m-%d %H:%M:%S")

        self.body = {"start_date": f"{self.start_date}", "end_date": f"{self.end_date}"}

        post_transaction_request = session.prepare_request(
            requests.Request(method="POST", url=self.url_base + self.path, json=self.body)
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
                    self.url_base + self.path,
                ),
            )

            get_transaction_response = self._request(get_transaction_request, None)

            match get_transaction_response.status_code:
                case 200:
                    return self.parse_response(get_transaction_response)
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