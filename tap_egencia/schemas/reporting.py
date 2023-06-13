from singer_sdk.typing import (
    PropertiesList,
    Property,
    NumberType,
    StringType,
    BooleonType,
    ArrayType,
    ObjectType

)
from tap_egencia.schemas.utils.custom_objects import CustomObject

class linksObject(CustomObject):
    properties = PropertiesList(
        property("empty", BooleonType)
    )

class metadataObject(CustomObject):
    properties = PropertiesList(
        property("current_page", NumberType),
        property("latest_reconciled_date", StringType),
        property("page_limit", NumberType),
        property("total_pages", NumberType),
        property("total_records", NumberType),

    )

class durationObject(CustomObject):
    properties = PropertiesList(
        property("end", StringType),
        property("minutes", StringType),
        property("start", StringType),
    )

class identifierObject(CustomObject):
    properties = PropertiesList(
        property("confirmation_number", StringType),
        property("invoice_number", StringType),
        property("itinerary_number", StringType),
        property("pnr", StringType),
        property("record_locator", StringType),
        property("ticket_number", StringType),
    )

class paymentObject(CustomObject):
    properties = PropertiesList(
        property("credit_card_bin", StringType),
        property("credit_card_last4_digits", StringType),
        property("credit_card_type", StringType),
    )

class policyObject(CustomObject):
    properties = PropertiesList(
        property("in_policy", StringType),
        property("policy_reason_code", StringType),
        property("policy_reason_description", StringType),
    )

class priceObject(CustomObject):
    properties = PropertiesList(
        property("average_leg_amount", StringType),
        property("average_leg_price", StringType),
        property("average_segment_amount", StringType),
        property("base", StringType),
        property("base_amount", StringType),
        property("best_fare_option", StringType),
        property("change_fee", StringType),
        property("change_fee_amount", StringType),
        property("change_fees", StringType),
        property("coupon_amount", StringType),
        property("extra_guest_charges", StringType),
        property("extra_person_amount", StringType),
        property("fare_bases", StringType),
        property("fee", StringType),
        property("fees", StringType),
        property("flight_amount", StringType),
        property("goodwill_amount", StringType),
        property("leg_amount", StringType),
        property("lowest_logical_fare", StringType),
        property("published_fare", StringType),
        property("segment_amount", StringType),
        property("tax", StringType),
        property("tax_gst", StringType),
        property("tax_hst", StringType),
        property("tax_qst", StringType),
        property("tax_vat", StringType),
        property("taxes", StringType),
        property("total", StringType),
        property("transaction_amount", StringType),
        property("transaction_amount_tax_gst", StringType),
        property("transaction_amount_tax_hst", StringType),
        property("transaction_amount_tax_qst", StringType),
        property("transaction_amount_vat", StringType),
        property("trip_amount", StringType),
        property("true_ticket_amount", StringType),
    )

class travelDatesObject(CustomObject):
    properties = PropertiesList(
        property("travel_end_date", StringType),
        property("travel_start_date", StringType),
    )

class travelerObject(CustomObject):
    properties = PropertiesList(
        property("email", StringType),
        property("group", StringType),
        property("is_guest", StringType),
        property("meeting_attendee_group", StringType),
        property("name", StringType),

    )

class transactionsObject(CustomObject):
    properties = ArrayType(PropertiesList(
        property("advance_purchase_days", StringType),
        property("advance_purchase_window", StringType),
        property("ancillary_type", StringType),
        property("booking_method", StringType),
        property("cabin_class", StringType),
        property("cabin_class_name", StringType),
        property("class_of_service", StringType),
        property("client_code", StringType),
        property("company_name", StringType),
        property("custom_data_fields", ObjectType),
        property("department", StringType),
        property("duration", durationObject),
        property("geography_type", StringType),
        property("identifier", identifierObject),
        property("invoice_date", StringType),
        property("is_active", StringType),
        property("is_agent_assisted", StringType),
        property("is_special_request", StringType),
        property("line_of_business", StringType),
        property("location", StringType),
        property("meeting_name", StringType),
        property("parent_client_code", StringType),
        property("payment_instrument_info", paymentObject),
        property("point_of_sale", StringType),
        property("point_of_sale_country", StringType),
        property("policy", policyObject),
        property("price", priceObject),
        property("purchase_count", StringType),
        property("rate_type", StringType),
        property("segment_count", StringType),
        property("ticket_code", StringType),
        property("ticket_status", StringType),
        property("transaction_date", StringType),
        property("transaction_status", StringType),
        property("transaction_type", StringType),
        property("travel_dates", travelDatesObject),
        property("traveler", travelerObject),
        property("vendor", StringType),
        property("vendor_name", StringType),
    )
   )
    