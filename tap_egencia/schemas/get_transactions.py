from singer_sdk.typing import (
    PropertiesList,
    Property,
    NumberType,
    StringType,
    BooleanType,
    ArrayType,
)
from tap_egencia.schemas.utils.custom_objects import CustomObject


class linksObject(CustomObject):
    properties = PropertiesList(Property("empty", BooleanType))


class metadataObject(CustomObject):
    properties = PropertiesList(
        Property("current_page", NumberType),
        Property("latest_reconciled_date", StringType),
        Property("page_limit", NumberType),
        Property("total_pages", NumberType),
        Property("total_records", NumberType),
    )


class durationObject(CustomObject):
    properties = PropertiesList(
        Property("end", StringType),
        Property("minutes", StringType),
        Property("start", StringType),
    )


class identifierObject(CustomObject):
    properties = PropertiesList(
        Property("confirmation_number", StringType),
        Property("invoice_number", StringType),
        Property("itinerary_number", StringType),
        Property("pnr", StringType),
        Property("record_locator", StringType),
        Property("ticket_number", StringType),
    )


class paymentObject(CustomObject):
    properties = PropertiesList(
        Property("credit_card_bin", StringType),
        Property("credit_card_last4_digits", StringType),
        Property("credit_card_type", StringType),
    )


class policyObject(CustomObject):
    properties = PropertiesList(
        Property("in_policy", StringType),
        Property("policy_reason_code", StringType),
        Property("policy_reason_description", StringType),
    )


class priceObject(CustomObject):
    properties = PropertiesList(
        Property("average_leg_amount", StringType),
        Property("average_leg_price", StringType),
        Property("average_segment_amount", StringType),
        Property("base", StringType),
        Property("base_amount", StringType),
        Property("best_fare_option", StringType),
        Property("change_fee", StringType),
        Property("change_fee_amount", StringType),
        Property("change_fees", StringType),
        Property("coupon_amount", StringType),
        Property("extra_guest_charges", StringType),
        Property("extra_person_amount", StringType),
        Property("fare_bases", StringType),
        Property("fee", StringType),
        Property("fees", StringType),
        Property("flight_amount", StringType),
        Property("goodwill_amount", StringType),
        Property("leg_amount", StringType),
        Property("lowest_logical_fare", StringType),
        Property("published_fare", StringType),
        Property("segment_amount", StringType),
        Property("tax", StringType),
        Property("tax_gst", StringType),
        Property("tax_hst", StringType),
        Property("tax_qst", StringType),
        Property("tax_vat", StringType),
        Property("taxes", StringType),
        Property("total", StringType),
        Property("transaction_amount", StringType),
        Property("transaction_amount_tax_gst", StringType),
        Property("transaction_amount_tax_hst", StringType),
        Property("transaction_amount_tax_qst", StringType),
        Property("transaction_amount_vat", StringType),
        Property("trip_amount", StringType),
        Property("true_ticket_amount", StringType),
    )


class travelDatesObject(CustomObject):
    properties = PropertiesList(
        Property("travel_end_date", StringType),
        Property("travel_start_date", StringType),
    )


class travelerObject(CustomObject):
    properties = PropertiesList(
        Property("email", StringType),
        Property("group", StringType),
        Property("is_guest", StringType),
        Property("meeting_attendee_group", StringType),
        Property("name", StringType),
    )


class transactionsObject(CustomObject):
    properties = ArrayType(
        PropertiesList(
            Property("advance_purchase_days", StringType),
            Property("advance_purchase_window", StringType),
            Property("ancillary_type", StringType),
            Property("booking_method", StringType),
            Property("cabin_class", StringType),
            Property("cabin_class_name", StringType),
            Property("class_of_service", StringType),
            Property("client_code", StringType),
            Property("company_name", StringType),
            # Property("custom_data_fields", ObjectType),
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
            Property("traveler", travelerObject),
            Property("vendor", StringType),
            Property("vendor_name", StringType),
        )
    )
